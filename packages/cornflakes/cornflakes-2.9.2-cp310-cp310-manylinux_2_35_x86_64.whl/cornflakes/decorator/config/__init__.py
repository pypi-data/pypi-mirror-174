"""cornflakes config decorator module."""
from cornflakes.decorator.config._config import config, Config, is_config
from cornflakes.decorator.config._config_group import config_group, ConfigGroup, is_group
from cornflakes.decorator.config._loader import Loader


__all__ = [
    "config",
    "config_group",
    "is_config",
    "Config",
    "ConfigGroup",
    "Loader",
]
