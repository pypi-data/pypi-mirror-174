from dataclasses import asdict
from typing import Dict, List, Callable

from cornflakes.decorator.config import Config, ConfigGroup
from cornflakes.decorator.config._load_config import create_file_loader
from cornflakes.decorator.config._load_config_group import create_group_loader
from cornflakes.decorator.config._protocols import Config, ConfigGroup


def to_dict(self) -> dict:
    """Method to convert Dataclass with slots to dict."""
    return asdict(self)


def create_dict_file_loader(
    cls=None,
) -> Callable[..., dict[str, Config | list[Config]]]:
    """Method to create file loader for ini files."""

    def from_dict(config_dict, *args, **kwargs) -> dict[str, Config | list[Config]]:
        kwargs.pop("config_dict", None)
        return create_file_loader(cls=cls)(config_dict=config_dict, *args, **kwargs)

    return from_dict


def create_dict_group_loader(
    cls=None,
) -> Callable[..., ConfigGroup]:
    """Method to create file loader for ini files."""

    def from_dict(config_dict, *args, **kwargs) -> ConfigGroup:
        kwargs.pop("config_dict", None)
        return create_group_loader(cls=cls)(config_dict=config_dict, *args, **kwargs)

    return from_dict
