import json
from . import errors

CONFIG_FILE_PATH = 'sysmon.config.json'


class InvalidConfigError(errors.SysmonError):
    """Invalid system configuration error.
    """
    pass


class Config(dict):
    """Application configuration dict with helpers.
    """

    def get_flask_config(self):
        """Extract Flask config from Config and capitalise correctly for Flask.
        """
        if 'flask' not in self:
            raise InvalidConfigError("Config missing required 'flask' directive.")
        cfg = {}
        for key in self['flask']:
            cfg[key.upper()] = self['flask'][key]
        return cfg

    @classmethod
    def from_file(cls, filename):
        """Create Config instance from JSON config file.
        """
        with open(filename) as f:
            data = ''.join(f.readlines())
        try:
            config = cls()
            config.update(json.loads(data))
            return config
        except json.decoder.JSONDecodeError:
            raise InvalidConfigError('Unable to parse config file, is it valid JSON?') from None
