# logparse.py
""" log parser
    Accepts a filename on the command line. The file is a Linux-like log file
    from a system you are debugging. Mixed in among the various statements are
    messages indicating the state of the device. They look like this:
        Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON
    The device state message has many possible values, but this program cares
    about only three: ON, OFF, and ERR.

    Your program will parse the given log file and print out a report giving
    how long the device was ON and the timestamp of any ERR conditions.
"""
import re
from datetime import datetime
from typing import Optional, Dict, List


class Device:

    def __init__(self):
        self.state: Optional[str] = None
        self.state_since: Optional[datetime] = None
        self.state_timers: Dict[str, int] = {}
        self.error_timestamps: List[datetime] = []

    def move_to_state(self, new_state: str, date_time_str: str):

        date_time_obj = datetime.strptime(date_time_str, '%b %d %H:%M:%S:%f')
        timestamp = date_time_obj.timestamp()

        if new_state != self.state:
            if self.state_since is not None:
                timer_value = self.state_timers.get(self.state, 0)
                timer_value += timestamp - self.state_since
                self.state_timers[self.state] = timer_value
        if "ERR" == new_state:
            self.error_timestamps.append(date_time_obj)

        self.state = new_state
        self.state_since = timestamp


device = Device()

with open('test.log') as fp:
    pattern = re.compile(r'(.+) \[(\d+)].+Device State: ([^\s]+)')
    for line in fp:
        result = pattern.match(line)
        if result is not None:
            dt = result.groups()[0]
            state = result.groups()[2]
            device.move_to_state(state, dt)

print(f"ON: {device.state_timers['ON']}")

print('errors:')
for err in device.error_timestamps:
    print(str(err))
