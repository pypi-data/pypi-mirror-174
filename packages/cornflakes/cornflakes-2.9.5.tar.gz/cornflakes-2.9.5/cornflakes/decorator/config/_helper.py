
def is_config(cls):
    """Methoad to return falg that class is a config class."""
    return hasattr(cls, "__config_sections__")


def is_group(cls):
    """Methoad to return falg that class is a config group class."""
    return not hasattr(cls, "__config_sections__") and hasattr(cls, "__config_files__")


def is_config_list(cls):
    return getattr(cls, "__config_list__", False) or (hasattr(cls, "__args__") and
                                                      getattr(cls.__args__[0], "__config_list__", False))


def pass_section_name(cls):
    return "section_name" in cls.__dataclass_fields__.keys()

