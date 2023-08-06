from __future__ import annotations

import subprocess

from cleo.exceptions import CommandNotFoundException
from cleo.helpers import argument
from cleo.io.outputs.output import Verbosity
from poetry.console.commands.command import Command

from poetry_aliases_plugin import utils
from poetry_aliases_plugin.aliases import Alias, AliasesSet
from poetry_aliases_plugin.config import AliasesConfig
from poetry_aliases_plugin.triggers import TriggerCommand


class BaseAliasCommand(Command):
    @property
    def aliases_config(self):
        return AliasesConfig(self.poetry.pyproject)

    @property
    def trigger_command(self) -> TriggerCommand:
        raise NotImplementedError()

    def log(self, message, verbose: int | None = None):
        if verbose is None:
            verbose = Verbosity.QUIET

        self.io.write(message, True, verbose)

    def find_poetry_command(self, command: str) -> tuple[str, str]:
        if not self.aliases_config.settings['find_poetry_command']:
            return 'run', command.removeprefix('run').strip()

        args = command.split()

        poetry_command = args[0]

        try:
            self.application.get(poetry_command)

        except CommandNotFoundException:
            poetry_command = 'run'

        else:
            args = args[1:]

        return poetry_command.strip(), ' '.join(args).strip()

    def __poetry_call(self, poetry_command: str, args: str):
        self.log(f'Run with poetry: use poetry command "{poetry_command}" and args {args}')

        self.call(poetry_command, args)

    def __subprocess_call(self, poetry_command: str, args: str):
        self.log(f'Run with poetry with subprocess: use poetry command "{poetry_command}" and args {args}')

        subprocess_args = ['poetry', poetry_command] + args.split()

        command = subprocess.run(
            subprocess_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        command.check_returncode()

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
        self.log(f'Alias "{alias.alias}" -> command "{command}"')

        poetry_command, args = self.find_poetry_command(command)

        try:
            result = self.__exec_command(alias, poetry_command, args)

        except PermissionError as ex:
            if ex.errno == 13:
                raise utils.PluginCommandException(args, ex, f'У процесса poetry недостаточно прав для запуска программы: {ex.filename}')

            raise utils.PluginCommandException(args, ex) from ex

        except BaseException as ex:
            self.log(f'exec_command error: {ex.__class__.__name__}: {ex.args}')
            raise ex

        if result:
            self.log(f'complete: {result}', Verbosity.NORMAL)

        else:
            self.log(f'complete', Verbosity.NORMAL)

    @utils.plugin_exception_wrapper
    def handle(self) -> None:
        self.log(str(self.trigger_command))

        self.aliases_config.validate()

        aliases_set = AliasesSet.from_raw(self.aliases_config.aliases)
        triggered_aliases = aliases_set.get_triggered_aliases(self.trigger_command)

        for alias in triggered_aliases:
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
