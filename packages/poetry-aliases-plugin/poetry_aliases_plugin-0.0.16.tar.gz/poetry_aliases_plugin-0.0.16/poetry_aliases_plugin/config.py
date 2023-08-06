from poetry.core.pyproject.toml import PyProjectTOML

PLUGIN_NAME = 'poetry-version-plugin'

# SPLIT_COMMAND = False

# RUN_WITH_POETRY = False
# RUN_WITH_SUBPROCESS = True


class AliasesConfig(object):
    """Обертка над конфигурацией pyproject"""

    pyproject: PyProjectTOML

    def __init__(self, pyproject: PyProjectTOML) -> None:
        self.pyproject = pyproject

    def validate(self):
        assert (
            self.settings['run_with_subprocess'] != self.settings['run_with_poetry']
        ), 'Нужно выбрать один из способов запуска программы: run_with_subprocess or run_with_poetry'

    @property
    def _default_aliases(self):
        return {'this': 'poetry run python -m this'}

    @property
    def aliases(self) -> dict:
        aliases = self.pyproject.data.get('tool', {}).get('aliases', {})
        return self._default_aliases | aliases

    @property
    def _default_setting(self):
        return {
            'find_poetry_command': False,
            'run_with_poetry': False,
            'run_with_subprocess': True,
        }

    @property
    def settings(self):
        settings = self.pyproject.data.get('tool', {}).get('aliases', {}).get('settings', {})
        return self._default_setting | settings
