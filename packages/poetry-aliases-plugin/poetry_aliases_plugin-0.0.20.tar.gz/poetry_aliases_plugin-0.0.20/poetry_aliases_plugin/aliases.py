from __future__ import annotations


from poetry_aliases_plugin import utils
from poetry_aliases_plugin.triggers import TriggerCommand

RawAlias = str | dict[str, str | bool]


class Alias(object):

    alias: str
    commands: list[str]
    engine: str | None

    def __init__(self, alias: str, command_raw: str, engine: str | None = None) -> None:
        if command_raw is None:
            raise TypeError(f'Alias ({alias}) command data must have the key "command"')

        self.alias = alias
        self.commands = [utils.normalize_command(command) for command in command_raw.split('&&')]
        self.engine = engine

    @classmethod
    def from_raw(cls, alias: str, raw_alias: RawAlias) -> Alias:
        if isinstance(raw_alias, str):
            return cls(alias, raw_alias)

        if isinstance(raw_alias, dict):
            return cls(alias, raw_alias.get('command'), raw_alias.get('engine'))

        raise TypeError(f'Alias ({alias}) command must be str or dict, not {type(raw_alias)}')


class AliasesSet(object):
    """Множество списков"""

    aliases: dict[str, Alias]

    def __init__(self, aliases: dict[str, Alias]) -> None:
        self.aliases = aliases

    @classmethod
    def from_raw(cls, raw_aliases: dict[str, RawAlias]) -> AliasesSet:
        aliases = {alias_key: Alias.from_raw(alias_key, raw_alias) for alias_key, raw_alias in raw_aliases.items()}
        return cls(aliases)

    def get_triggered_aliases(self, trigger: TriggerCommand) -> list[Alias]:
        if trigger.alias not in self.aliases:
            raise utils.PluginException(f'alias "{trigger.alias}" not found')

        return [self.aliases[trigger.alias]]
