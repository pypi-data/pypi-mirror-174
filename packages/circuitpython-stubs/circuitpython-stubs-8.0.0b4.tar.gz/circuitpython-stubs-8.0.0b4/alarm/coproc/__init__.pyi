from __future__ import annotations

import coproc

class CoprocAlarm:
    """Trigger an alarm when another core or co-processor requests wake-up."""

    def __init__(self, coproc: coproc.Coproc) -> None:
        """Create an alarm that will be triggered when the co-processor requests wake-up.

        The alarm is not active until it is passed to an `alarm`-enabling function, such as
        `alarm.light_sleep_until_alarms()` or `alarm.exit_and_deep_sleep_until_alarms()`.

        :param coproc.Coproc coproc: The coproc program to run.

        """
        ...
