import logging
from typing import List, Union, Dict, cast

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
        self._processing_strategy = None  # no type hints to avoid an import cycle

        if processing_strategy is not None:
            self.set_processing_strategy(processing_strategy)

        self.name = 'unnamed'
        self._internal_buffers: Dict[Node] = {}

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

        for node in self.input_stream_nodes:
            node.render(interval, self._find_internal_buffer(node))

        for node in self.input_event_nodes:
            node.render(interval, self._find_internal_buffer(node))

        self.last_processed_interval_id = interval.id
        logging.debug('rendering processing strategy for unit ' + self.name)

        self._processing_strategy.render(interval, self._get_input_stream_buffers(), self._get_output_stream_buffers(),
                                         self._get_input_event_buffers(), self._get_output_event_buffers())

    def get_num_input_units(self) -> int:

        """

        finds a number of distinct units sending something into this one

        :return:
        """
        found_units: Dict[Unit] = {}
        all_input_nodes: List[Node] = self.input_stream_nodes + self.input_event_nodes

        for node in all_input_nodes:
            found_units[node.connector.input_node.unit] = 1

        return len(found_units.keys())

    def render_stream_through_sub_buffers(self, interval: TimeInterval, out_stream_buffers: List[np.ndarray],
                                          sub_buffers: List[np.ndarray]):

        num_total_samples = out_stream_buffers[0].shape[0]
        num_sub_buffer_samples = sub_buffers[0].shape[0]
        num_sub_buffers = round(num_total_samples / num_sub_buffer_samples)

        sub_buffer_length_in_bars = interval.get_length_in_bars() / num_sub_buffers

        for i in range(0, num_sub_buffers):
            sub_interval = TimeInterval()
            sub_interval.start_in_bars = interval.start_in_bars + i * sub_buffer_length_in_bars
            sub_interval.end_in_bars = interval.start_in_bars + (i + 1) * sub_buffer_length_in_bars
            sub_interval.num_samples = num_sub_buffer_samples

            self.render(sub_interval, sub_buffers[0], None, self.output_stream_nodes[0])
            self.render(sub_interval, sub_buffers[1], None, self.output_stream_nodes[1])

            out_stream_buffers[0][i * num_sub_buffer_samples:(i + 1) * num_sub_buffer_samples] = sub_buffers[0]
            out_stream_buffers[1][i * num_sub_buffer_samples:(i + 1) * num_sub_buffer_samples] = sub_buffers[1]

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

        if out_stream_buffer is not None:
            size_of_stream_buffer: int = len(out_stream_buffer)
            self._refresh_internal_buffers(interval, size_of_stream_buffer)
        else:
            self._refresh_internal_buffers(interval)

        if out_node.is_stream():
            out_node: StreamNode
            self._render_stream_buffer_to_output(out_node, out_stream_buffer, rendering_type)

        if out_node.is_event():
            out_node: EventNode
            self._render_event_buffer_to_output(out_node, out_event_buffer, rendering_type)

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

    def _convert_nodes_into_buffers(self, nodes: List[Node]) -> List:
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

    def get_all_output_nodes(self) -> List[Node]:
        # noinspection PyTypeChecker
        return self.output_stream_nodes + self.output_event_nodes

    def get_all_input_nodes(self) -> List[Node]:
        # noinspection PyTypeChecker
        return self.input_stream_nodes + self.input_event_nodes
