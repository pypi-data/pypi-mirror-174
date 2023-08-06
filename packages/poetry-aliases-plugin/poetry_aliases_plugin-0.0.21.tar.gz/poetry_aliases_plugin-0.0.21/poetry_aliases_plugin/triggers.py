from __future__ import annotations


class TriggerCommand(object):
    """Объект команды, которая инициализировала использование псевдонима"""

    alias: str

    def __str__(self) -> str:
        return f'TriggerCommand: {self.alias}'

    def __init__(self, alias: str) -> None:
        self.alias = alias

    @classmethod
    def from_raw(cls, raw_command: str) -> TriggerCommand:
        if isinstance(raw_command, str):
            return cls(raw_command)

        raise TypeError(f'Alias command must be str, not {type(raw_command)}')
