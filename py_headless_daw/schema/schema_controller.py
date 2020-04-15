from typing import Dict, List

from em.platform.rendering.processing_strategies.event.event_buffer import EventBuffer
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.host import Host
from em.platform.rendering.schema.unit import Unit
from em.platform.rendering.schema.wiring import EventNode, StreamNode, Connector


class SchemaController:

    def __init__(self, host: Host):
        self._event_input_buffers: Dict[str] = {}
        self._stream_inputs_buffers: Dict[str] = {}
        self._stream_outputs: List[StreamNode] = []
        self.host: Host = host

    def add_event_input(self, name: str, schema_node: EventNode):
        buffer_unit = Unit(0, 0, 0, 1, self.host, EventBuffer())
        self._event_input_buffers[name] = buffer_unit
        Connector(buffer_unit.output_event_nodes[0], schema_node)

    def give_events(self, name: str, events: List[Event]):
        buffer: Unit = self._event_input_buffers[name]
        strategy: EventBuffer = buffer.get_processing_strategy()
        strategy.give_new_events(events)

    def add_stream_input(self, name: str, schema_node: StreamNode):
        raise NotImplementedError('not implemented yet')

    def assign_outputs(self, outputs: List[StreamNode]):
        self._stream_outputs = outputs

    def get_outputs(self) -> List[StreamNode]:
        return self._stream_outputs
