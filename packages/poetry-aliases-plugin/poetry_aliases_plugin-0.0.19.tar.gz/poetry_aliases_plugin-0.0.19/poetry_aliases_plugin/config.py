from copy import deepcopy
import logging

from poetry.core.pyproject.toml import PyProjectTOML

PLUGIN_NAME = 'poetry-aliases-plugin'

logger = logging.getLogger('poetry_aliases_plugin')


class AliasesConfig(object):
    """Обертка над конфигурацией pyproject"""

    pyproject: PyProjectTOML

    def __init__(self, pyproject: PyProjectTOML) -> None:
        self.pyproject = pyproject

    def validate(self):
        assert self.settings['engine'] in ('poetry', 'subprocess'), (
            'Запуск через "%s" не предусмотрен. Доступны варианты: poetry, subprocess' % self.settings['engine']
        )

    @property
    def _default_aliases(self):
        return {'this': 'poetry run python -m this'}

    @property
    def aliases(self) -> dict:
        aliases = self.pyproject.data.get('tool', {}).get('aliases', {})
        aliases = self._default_aliases | aliases

        aliases = deepcopy(aliases)

        if 'settings' in aliases:
            del aliases['settings']

        return aliases

    @property
    def _default_setting(self):
        return {
            'find_poetry_command': False,
            'engine': 'poetry',
        }

    def validate_settings(self, settings: dict):
        pass

    @property
    def settings(self):
        settings = self.pyproject.data.get('tool', {}).get('aliases', {}).get('settings', {})
        return self._default_setting | settings
