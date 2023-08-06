from typing import Callable

from cleo.application import Application
from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from poetry.console.commands.command import Command

from poetry_aliases_plugin import config


class PluginException(RuntimeError):
    def __str__(self) -> str:
        return f'{config.PLUGIN_NAME}: {self.args[0]}'


class PluginCommandException(PluginException):

    command: str
    exception: BaseException

    def __init__(self, command: str, exception: BaseException, *args: object) -> None:
        self.command = command
        self.exception = exception
        super().__init__(*args, *exception.args)

    def __str__(self) -> str:
        return f'{config.PLUGIN_NAME}: [{self.command}] {self.exception.__class__.__name__}: {self.args[0]}'


def plugin_exception_wrapper(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except PluginException as ex:
            raise ex

        except BaseException as ex:
            raise PluginException(ex) from ex

    return wrapper


def normalize_command(command: str) -> str:
    command = command.removeprefix('poetry').strip()
    command = command if command.startswith('run') else f'run {command}'
    return command.strip()
