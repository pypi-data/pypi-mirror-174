from __future__ import annotations

from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_aliases_plugin.plugin_commands import AliasCommand


class PoetryAliasesApplicationPlugin(ApplicationPlugin):
    @property
    def commands(self) -> list[type[Command]]:
        return [AliasCommand]
