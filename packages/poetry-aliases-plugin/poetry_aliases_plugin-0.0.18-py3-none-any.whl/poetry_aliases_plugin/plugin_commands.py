from __future__ import annotations

import subprocess

from cleo.exceptions import CommandNotFoundException
from cleo.helpers import argument
from cleo.io.outputs.output import Verbosity
from poetry.console.commands.command import Command

from poetry_aliases_plugin import config, utils
from poetry_aliases_plugin.aliases import Alias, AliasesSet
from poetry_aliases_plugin.config import AliasesConfig
from poetry_aliases_plugin.triggers import TriggerCommand


class BaseAliasCommand(Command):
    @property
    def aliases_config(self):
        return AliasesConfig(self.poetry.pyproject)

    def __find_poetry_command(self, command: str) -> tuple[str, str]:
        if not self.aliases_config.settings['find_poetry_command']:
            return 'run', command.removeprefix('run')

        args = command.split()

        poetry_command = args[0]

        try:
            self.application.get(poetry_command)

        except CommandNotFoundException:
            poetry_command = 'run'

        else:
            args = args[1:]

        return poetry_command, ' '.join(args)

    def __poetry_call(self, poetry_command: str, args: str):
        self.call(poetry_command, args)

    def __subprocess_call(self, poetry_command: str, string_args: str):
        args = string_args.split()

        # for arg in string_args.split():
        #     if not len(args):
        #         args.append(arg)
        #         continue

        #     if arg.startswith('--'):
        #         args[-1] = f'{args[-1]} {arg}'
        #         continue

        #     args.append(arg)

        args = ['poetry', poetry_command] + args

        return subprocess.run(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

    def __exec_command(self, alias: Alias, poetry_command: str, args: str):
        if alias.engine == 'poetry':
            self.__poetry_call(poetry_command, args)

        elif alias.engine == 'subprocess':
            self.__subprocess_call(poetry_command, args)

        elif self.aliases_config.settings['engine'] == 'poetry':
            self.__poetry_call(poetry_command, args)

        elif self.aliases_config.settings['engine'] == 'subprocess':
            self.__subprocess_call(poetry_command, args)

        else:
            raise RuntimeError('Не определен движок для запуска команды')

    def exec_command(self, alias: Alias, command: str):
        self.io.write(f'run command: {command}', True, Verbosity.QUIET)

        poetry_command, args = self.__find_poetry_command(command)

        try:
            result = self.__exec_command(alias, poetry_command, args)

        except PermissionError as ex:
            if ex.errno == 13:
                raise utils.PluginCommandException(args, ex, f'У процесса poetry недостаточно прав для запуска программы: {ex.filename}')

            raise utils.PluginCommandException(args, ex) from ex

        except Exception as ex:
            raise utils.PluginCommandException(args, ex) from ex


        if result:
            self.io.write(f'complete: {result}', True, Verbosity.NORMAL)

        else:
            self.io.write(f'complete', True, Verbosity.NORMAL)

    @property
    def trigger_command(self) -> TriggerCommand:
        raise NotImplementedError()

    @utils.plugin_exception_wrapper
    def handle(self) -> None:
        self.io.write(f'Trigger command: {self.trigger_command}', True, Verbosity.QUIET)

        self.aliases_config.validate()

        aliases_set = AliasesSet.from_raw(self.aliases_config.aliases)
        triggered_aliases = aliases_set.get_triggered_aliases(self.trigger_command)

        for alias in triggered_aliases:
            self.io.write(f'run alias: {alias.alias}', True, Verbosity.QUIET)

            for command in alias.commands:
                self.exec_command(alias, command)


class AliasCommand(BaseAliasCommand):
    name = 'l'

    arguments = [argument('alias', 'Registered alias')]

    @property
    def description(self):
        return 'Run aliases. Available: {0}'.format(', '.join(list(self.aliases_config.aliases)))

    @property
    def trigger_command(self) -> TriggerCommand:
        return TriggerCommand.from_raw(self.argument('alias'))
