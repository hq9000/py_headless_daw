from typing import List, Union, Optional

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.unit import Unit

class Connector:
    def __init__(self, in_node, out_node):
        self.input_node: Node = in_node
        self.out_node: Node = out_node

        self.input_node.connector = self
        self.out_node.connector = self


class Node:
    def __init__(self, processing_unit=None):
        """
        :param processing_unit: # Unit we are not doing type checking here to avoid circular dependency
        """
        self.unit: Unit = processing_unit
        self.connector: Optional[Connector] = None

    def set_connector(self, connector: Connector):
        self.connector = connector

    def set_unit(self, processing_unit: Unit):
        self.unit: Unit = processing_unit

    def is_stream(self) -> bool:
        return False

    def is_event(self) -> bool:
        return False

    def render(self, interval: TimeInterval, out_buffer: Union[np.ndarray, List[Event]]):

        if not self._is_unit_output():
            # this node is not directly an output of a unit, so we
            # need to find its outputting unit through the connector
            node_to_render: Node = self.connector.input_node
        else:
            # the node IS an output of a unit, so we render it directly`
            node_to_render = self

        if self.is_stream():
            node_to_render.unit.render(interval, out_buffer, None, node_to_render)
        if self.is_event():
            node_to_render.unit.render(interval, None, out_buffer, node_to_render)

    def _is_unit_output(self) -> bool:
        if self.unit is not None:
            return self.unit.is_output(self)
        else:
            return False


class StreamNode(Node):

    def is_stream(self):
        return True


class EventNode(Node):

    def is_event(self):
        return True
