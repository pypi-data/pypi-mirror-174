import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from ruamel.yaml import CommentedMap

from ktdg.utils import done_print, load_print

from . import answers as answers_
from . import questions as questions_
from . import skills as skills_
from . import students as students_

#########
# types #
#########


class Data(BaseModel):
    skills: list[skills_.Skill]
    students: list[students_.Student]
    questions: list[questions_.Question]
    answers: list[answers_.Answer]


class Config(BaseModel):
    skills: skills_.Config | list[skills_.Config] = skills_.Config()
    questions: questions_.Config | list[
        questions_.Config
    ] = questions_.Config()
    students: students_.Config | list[students_.Config] = students_.Config()
    answers: answers_.Config = answers_.Config()


############
# external #
############


def add_comments(config: Config) -> CommentedMap:
    config_ = CommentedMap(config.dict())
    config_["skills"] = skills_.add_comments(config.skills)
    config_["questions"] = questions_.add_comments(config.questions)
    config_["students"] = students_.add_comments(config.students)
    config_["answers"] = answers_.add_comments(config.answers)
    return config_


def generate(
    config: Config, as_dict: bool = False, echo: bool = True
) -> Data | dict[str, Any]:
    skills = skills_.generate(config.skills, echo=echo)
    students = students_.generate(config.students, skills, echo=echo)
    questions = questions_.generate(config.questions, skills, echo=echo)
    student_answers = answers_.generate(
        config.answers, students, questions, skills, echo=echo
    )
    answers = [aa for a in student_answers for aa in a]
    data = Data(
        skills=skills, students=students, questions=questions, answers=answers
    )
    done_print("Generated data.", echo=echo)
    if as_dict:
        return data.dict()
    else:
        return data


def save_data(
    data: Data | dict[str, Any], output_file: Path, echo: bool = True
) -> None:
    load_print("Saving data...", echo=echo)
    if isinstance(data, Data):
        data = data.dict()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    done_print("Saved data.", echo=echo)
