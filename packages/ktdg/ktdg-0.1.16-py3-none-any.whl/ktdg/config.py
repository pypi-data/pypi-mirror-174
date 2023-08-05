from pathlib import Path

from ruamel.yaml import YAML

from .generation import Config, add_comments

############
# external #
############


def read_config(config: Path) -> Config:
    yaml = YAML()
    with open(config, "r") as f:
        config_ = Config(**yaml.load(f))
    return config_


def save_config(config: Config, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml = YAML()
    with open(path, "w") as f:
        yaml.dump(add_comments(config), f)
