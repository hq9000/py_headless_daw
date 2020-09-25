from typing import List, Union

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.exceptions import SchemaException


class Connector:
    _registry = []  # type: List[Connector]

    def __init__(self, in_node, out_node):
        # type: (Node, Node) -> None
        self.input_node: Node = in_node
        self.out_node: Node = out_node

        assert self.connected(in_node, out_node) is False, "these two nodes already have a connector between them"

        self.input_node.attach_to_connector_input(self)
        self.out_node.attach_to_connector_output(self)

        self._registry.append(self)

    @classmethod
    def connected(cls, node1, node2):
        # type: (Node, Node)->bool
        for connector in cls._registry:
            if connector.input_node is node1 and connector.out_node is node2:
                return True
            if connector.out_node is node1 and connector.input_node is node2:
                return True

        return False


class Node:
    def __init__(self, processing_unit=None):
        """
        :param processing_unit: # Unit we are not doing type checking here to avoid circular dependency
        """
        from py_headless_daw.schema.unit import Unit
        self.unit: Unit = processing_unit
        self._connectors: List[Connector] = []

    def attach_to_connector_output(self, connector: Connector):
        if self._is_unit_output():
            raise SchemaException(
                'this node is an output of a unit, but it has been attempted to connect to an output of a connector')

        self._connectors.append(connector)

    def attach_to_connector_input(self, connector: Connector):
        if self._is_unit_input():
            raise SchemaException(
                'this node is an input of a unit, but it has been attempted to connect to an input of a connector')

        self._connectors.append(connector)

    def is_stream(self) -> bool:
        return False

    def is_event(self) -> bool:
        return False

    def render(self, interval: TimeInterval, out_buffer: Union[np.ndarray, List[Event]]):
        """

        :param interval:
        :param out_buffer:
        :return:
        """
        # to postpone importing to avoid a cycle:
        from py_headless_daw.schema.unit import RENDERING_TYPE_REPLACE, RENDERING_TYPE_ADD

        nodes_to_render: List[Node]

        if not self._is_unit_output():
            # this node is not directly an output of a unit, so we
            # need to find its outputting units through the connectors
            nodes_to_render = []
            for connector in self._connectors:
                nodes_to_render.append(connector.input_node)
        else:
            # the node IS an output of a unit, so we render it directly`
            nodes_to_render = [self]

        for sequence_number, node_to_render in enumerate(nodes_to_render):

            if self.is_stream():
                if 0 == sequence_number:
                    node_to_render.unit.render(interval, out_buffer, None, node_to_render, RENDERING_TYPE_REPLACE)
                else:
                    node_to_render.unit.render(interval, out_buffer, None, node_to_render, RENDERING_TYPE_ADD)
            if self.is_event():
                if 0 == sequence_number:
                    node_to_render.unit.render(interval, None, out_buffer, node_to_render, RENDERING_TYPE_REPLACE)
                else:
                    node_to_render.unit.render(interval, None, out_buffer, node_to_render, RENDERING_TYPE_ADD)

    def _is_unit_output(self) -> bool:
        if self.unit is not None:
            return self.unit.is_output(self)
        else:
            return False

    def _is_unit_input(self) -> bool:
        return not self._is_unit_output()


class StreamNode(Node):

    def is_stream(self):
        return True


class EventNode(Node):

    def is_event(self):
        return True
