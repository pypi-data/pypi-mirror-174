import numpy as np
from pydantic import BaseModel
from ruamel.yaml import CommentedMap

from ktdg.utils import clip_0_1, load_print, parse_config, set_seed_if_missing

from .distributions import (
    Constant,
    Distribution,
    add_distribution_comments,
    generate_values,
    parse_distribution,
)

#########
# types #
#########


class Skill(BaseModel):
    id: int
    difficulty: float


class Config(BaseModel):
    n: int = 5
    difficulty: Distribution = Constant(value=1)
    seed: int = 0

    _parse_difficulty = parse_config("difficulty", parse_distribution)
    _set_seed = set_seed_if_missing("seed")

    class Config:
        validate_assignment = True


############
# external #
############


def generate(config: Config | list[Config], echo: bool = True) -> list[Skill]:
    load_print("Generating skills...", echo=echo)
    if isinstance(config, Config):
        difficulties = generate_params(config)
    else:
        difficulties = []
        for config_ in config:
            difficulties_ = generate_params(config_)
            difficulties = [*difficulties, *difficulties_]

    return [
        Skill(id=i, difficulty=difficulty)
        for i, difficulty in enumerate(difficulties)
    ]


def add_comments(
    config: Config | list[Config],
) -> CommentedMap | list[CommentedMap]:
    if isinstance(config, Config):
        config_ = CommentedMap(config.dict())
        config_.yaml_add_eol_comment(
            "Number of skils",
            "n",
        )
        config_.yaml_add_eol_comment(
            "Distribution of the skill difficulty",
            "difficulty",
        )
        config_["difficulty"] = add_distribution_comments(config.difficulty)
        config_.yaml_add_eol_comment(
            "random seed to use (set to 0 to have new seed)", "seed"
        )
        return config_
    else:
        return [add_comments(c) for c in config]  # type: ignore


############
# internal #
############


def generate_params(config: Config) -> list[float]:
    rng = np.random.default_rng(config.seed)
    difficulties = clip_0_1(generate_values(config.n, config.difficulty, rng))
    return difficulties
