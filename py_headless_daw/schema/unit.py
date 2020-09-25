import logging
from typing import List, Union, Dict, cast, Optional, Sequence

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.exceptions import SchemaException
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.wiring import StreamNode, EventNode, Node

RENDERING_TYPE_REPLACE: str = 'replace'
RENDERING_TYPE_ADD: str = 'add'


class Unit:

    def __init__(self, number_of_stream_inputs: int, number_of_event_inputs: int, number_of_stream_outputs: int,
                 number_of_event_outputs: int, host: Host, processing_strategy=None):
        """

        :param number_of_stream_inputs:
        :param number_of_event_inputs:
        :param number_of_stream_outputs:
        :param number_of_event_outputs:
        :param processing_strategy:
        """
        self.host = host

        self._input_stream_nodes: List[StreamNode] = [StreamNode(self) for _ in range(number_of_stream_inputs)]
        self._output_stream_nodes: List[StreamNode] = [StreamNode(self) for _ in range(number_of_stream_outputs)]

        self._input_event_nodes: List[EventNode] = [EventNode(self) for _ in range(number_of_event_inputs)]
        self._output_event_nodes: List[EventNode] = [EventNode(self) for _ in range(number_of_event_outputs)]

        self.last_processed_interval_id: int = -1

        # inplace import to avoid cycle reference
        from py_headless_daw.schema.processing_strategy import ProcessingStrategy
        self._processing_strategy: Optional["ProcessingStrategy"] = None

        if processing_strategy is not None:
            self.set_processing_strategy(processing_strategy)

        self.name = 'unnamed'
        self._internal_buffers: Dict[Node, np.ndarray] = {}

    @property
    def output_stream_nodes(self) -> List[StreamNode]:
        return self._output_stream_nodes

    @property
    def input_stream_nodes(self) -> List[StreamNode]:
        return self._input_stream_nodes

    @property
    def output_nodes(self) -> List[Node]:
        return cast(List[Node], self._output_stream_nodes) + cast(List[Node], self._output_event_nodes)

    @property
    def input_nodes(self) -> List[Node]:
        return cast(List[Node], self._input_stream_nodes) + cast(List[Node], self._input_event_nodes)

    @property
    def output_event_nodes(self) -> List[EventNode]:
        return self._output_event_nodes

    @property
    def input_event_nodes(self) -> List[EventNode]:
        return self._input_event_nodes

    def set_processing_strategy(self, strategy):
        self._processing_strategy = strategy
        strategy.unit = self

    def get_processing_strategy(self):
        return self._processing_strategy

    def _refresh_internal_buffers(self, interval: TimeInterval, size_of_stream_buffer: Union[int, None] = None):
        """

        :param interval:
        :param size_of_stream_buffer:
        :return:
        """

        if interval.id == self.last_processed_interval_id:
            # already processed
            return

        if size_of_stream_buffer is not None:
            self._allocate_internal_stream_buffers(size_of_stream_buffer)

        self._allocate_internal_event_buffers()

        for stream_node in self.input_stream_nodes:
            stream_node.render(interval, self._find_internal_buffer(stream_node))

        for event_node in self.input_event_nodes:
            event_node.render(interval, self._find_internal_buffer(event_node))

        self.last_processed_interval_id = interval.id
        logging.debug('rendering processing strategy for unit "' + self.name + '" on %d:(%2.2f,%2.2f,%d)' % (
            interval.id, interval.start_in_seconds, interval.end_in_seconds, interval.num_samples))

        if self._processing_strategy is None:
            raise Exception('processing strategy not initialized in this unit')

        self._processing_strategy.render(interval, self._get_input_stream_buffers(), self._get_output_stream_buffers(),
                                         self._get_input_event_buffers(), self._get_output_event_buffers())

    def get_num_input_units(self) -> int:

        """

        finds a number of distinct units sending something into this one

        :return:
        """
        found_units: Dict[Unit, int] = {}
        all_input_nodes: List[Node] = []
        all_input_nodes.extend(self.input_stream_nodes)
        all_input_nodes.extend(self.input_event_nodes)

        return len(found_units.keys())

    def render(self, interval: TimeInterval, out_stream_buffer: Union[np.ndarray, None],
               out_event_buffer: Union[List[Event], None],
               out_node: Node, rendering_type: str):
        """

        :param rendering_type:
        :param interval:
        :param out_stream_buffer:
        :param out_event_buffer:
        :param out_node:
        :return:
        """

        self._validate_interval(interval)

        if out_stream_buffer is not None:
            size_of_stream_buffer: int = len(out_stream_buffer)
            self._refresh_internal_buffers(interval, size_of_stream_buffer)
        else:
            self._refresh_internal_buffers(interval)

        if out_node.is_stream():
            self._render_stream_buffer_to_output(
                cast(StreamNode, out_node),
                out_stream_buffer,
                rendering_type)

        if out_event_buffer is not None:
            if out_node.is_event():
                self._render_event_buffer_to_output(
                    cast(EventNode, out_node),
                    out_event_buffer,
                    rendering_type
                )

    def _render_stream_buffer_to_output(self, out_node: StreamNode, out_stream_buffer: np.ndarray, rendering_type: str):
        """

        :param out_node:
        :param out_stream_buffer:
        :return:
        """
        internal_buffer: np.ndarray = self._find_internal_buffer(out_node)
        if rendering_type == RENDERING_TYPE_REPLACE:
            np.copyto(out_stream_buffer, internal_buffer)
        elif rendering_type == RENDERING_TYPE_ADD:
            out_stream_buffer += internal_buffer
        else:
            raise SchemaException('unknown rendering type "' + rendering_type + '"')

    def _render_event_buffer_to_output(self, out_node: EventNode, out_event_buffer: List[Event], rendering_type: str):
        """

        :param out_node:
        :param out_event_buffer:
        :return:
        """
        internal_buffer: List[Event] = self._find_internal_buffer(out_node)
        for event in internal_buffer:
            out_event_buffer.append(event)

    def _find_internal_buffer(self, node: Node) -> Union[np.ndarray, List[Event]]:
        """

        :param node:
        :return:
        """
        return self._internal_buffers[node]

    def _allocate_internal_stream_buffers(self, size_of_stream_buffer: int):
        """

        :param size_of_stream_buffer:
        :return:
        """
        for node in self.input_stream_nodes + self.output_stream_nodes:

            if node in self._internal_buffers:
                # if size of the existing buffer does not match the requested size, we
                # forget this buffer
                existing_shape = self._internal_buffers[node].shape

                if existing_shape != (size_of_stream_buffer,):
                    self._internal_buffers[node] = None

            if node not in self._internal_buffers:
                self._internal_buffers[node] = np.ndarray([size_of_stream_buffer], np.float32)

    def _allocate_internal_event_buffers(self):
        """

        :return:
        """
        for node in self.input_event_nodes + self.output_event_nodes:
            self._internal_buffers[node] = []

    def _get_input_stream_buffers(self) -> List[np.ndarray]:
        return self._convert_nodes_into_buffers(self.input_stream_nodes)

    def _get_output_stream_buffers(self) -> List[np.ndarray]:
        return self._convert_nodes_into_buffers(self.output_stream_nodes)

    def _get_input_event_buffers(self) -> List[List[Event]]:
        return self._convert_nodes_into_buffers(self.input_event_nodes)

    def _get_output_event_buffers(self) -> List[List[Event]]:
        return self._convert_nodes_into_buffers(self.output_event_nodes)

    def _convert_nodes_into_buffers(self, nodes: Sequence[Node]) -> List:
        res = []
        for node in nodes:
            res.append(self._find_internal_buffer(node))
        return res

    def is_output(self, node_to_check: Node) -> bool:
        for node in self.get_all_output_nodes():
            if node_to_check is node:
                return True
        return False

    def is_input(self, node_to_check: Node) -> bool:
        for node in self.get_all_input_nodes():
            if node_to_check == node:
                return True
        return False

    def get_all_output_nodes(self) -> Sequence[Node]:
        # noinspection PyTypeChecker
        return self.output_stream_nodes + self.output_event_nodes  # type: ignore

    def get_all_input_nodes(self) -> Sequence[Node]:
        # noinspection PyTypeChecker
        return self.input_stream_nodes + self.input_event_nodes  # type: ignore

    def _validate_interval(self, interval: TimeInterval):
        inferred_sample_rate = round(interval.num_samples / (interval.end_in_seconds - interval.start_in_seconds))
        host_sample_rate = self.host.sample_rate

        if inferred_sample_rate != host_sample_rate:
            raise Exception(f"""sample rate inferred from the intrval: {inferred_sample_rate}, does not match
the host sample rate {host_sample_rate} (error: 3fd4b60f)""")
