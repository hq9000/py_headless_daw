from typing import List

from py_headless_daw.schema.unit import Unit
from py_headless_daw.schema.wiring import StreamNode, EventNode


class Chain(Unit):
    """
    represents a linear chain of units which is a unit on its own

    """

    # we dont need to call parent constructor in this case
    # noinspection PyMissingConstructor
    def __init__(self, first_unit: Unit, last_unit: Unit):
        """
        Units in the chain are expected to be properly interconnected prior to be passed here

        :param first_unit:
        :param last_unit:
        """

        if isinstance(first_unit, Unit) is not True:
            raise Exception

        if isinstance(last_unit, Unit) is not True:
            raise Exception

        self._fist_unit: Unit = first_unit
        self._last_unit: Unit = last_unit

    @Unit.input_stream_nodes.getter  # type: ignore
    def input_stream_nodes(self) -> List[StreamNode]:
        return self._fist_unit.input_stream_nodes

    @Unit.input_event_nodes.getter  # type: ignore
    def input_event_nodes(self) -> List[EventNode]:
        return self._fist_unit.input_event_nodes

    @Unit.output_stream_nodes.getter  # type: ignore
    def output_stream_nodes(self) -> List[StreamNode]:
        return self._last_unit.output_stream_nodes

    @Unit.output_event_nodes.getter  # type: ignore
    def output_event_nodes(self) -> List[EventNode]:
        return self._last_unit.output_event_nodes
