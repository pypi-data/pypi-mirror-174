# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ktdg', 'ktdg.generation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.0,<2.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'tqdm>=4.64.0,<5.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ktdg = ktdg.cli:run_cli']}

setup_kwargs = {
    'name': 'ktdg',
    'version': '0.1.16',
    'description': 'Library to simulate knowledge tracing datasets',
    'long_description': '[![Pipeline](https://gitlab.com/antoinelb/ktdg/badges/main/pipeline.svg)](https://gitlab.com/antoinelb/ktdg/commits/main)\n[![coverage report](https://gitlab.com/antoinelb/ktdg/badges/main/coverage.svg)](https://gitlab.com/antoinelb/ktdg/commits/main)\n[![Pypi version](https://img.shields.io/pypi/v/ktdg)](https://pypi.org/project/ktdg/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n\n# ktdg (Knowledge tracing data generator)\n\nLibrary used to create synthetic knowledge tracing data.\nExample configs can be found in `config`.\n\n[__Usage__](#usage)\n| [__Setup__](#setup)\n| [__Documentation__](#documentation)\n\n## Usage\n\nTo create a new config or complete an existing one:\n\n```\n$ ktdg create --help\nUsage: ktdg create [OPTIONS] CONFIG\n\n  (c) Creates a config or completes it, saving it to the given file.\n\nArguments:\n  CONFIG  Path of the config to complete or create  [required]\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\nTo generate the synthetic data from the config:\n\n```\n$ ktdg generate --help\nUsage: ktdg generate [OPTIONS] CONFIG\n\n  (g) Generates the data for the given config, saving it as a json file named\n  "data.json".\n\nArguments:\n  CONFIG  Configuration file to use  [required]\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\n## Setup\n\n1. Install [`poetry`](https://github.com/python-poetry/poetry)\n\n2. `poetry config virtualenvs.in-project true`\n\n3. `poetry install`\n\n4. `source .venv/bin/activate`\n\n## Documentation\n\n### Generation\n\n#### Skills\n\nSkills are generated with the following parameters:\n\n$n^K$ / `n`: number of skills to generate\n\n`difficulty (float)`: by how much to scale question difficulties for questions needing this skill sampled from a distribution\n\n`seed (int)`: random seed to use when generating the skills\n\n#### Students\n\nStudents are generated with the following parameters:\n\n`n`: number of students to generate\n\n$n_i \\sim N^S, n_i \\in \\{0,...,n^K\\}$ / `n_skills (int)`: number of skills per student sampled from a distribution\n\n$m_{ik} \\sim M^Q, m_{ik} \\in [0,1]$ / `skill_mastery (float)`: mastery for a given student and skill sampled from a distribution\n\n$s_i^S \\sim S^S, s_i^S \\in [0,1]$ / `slip (float)`: slip rate for a given student sampled from a distribution\n\n$g_i^S \\sim G^S, g_i^S \\in [0,1]$ / `guess (float)`: guess rate for a given student sampled from a distribution\n\n$l_i^S \\sim L^S, l_i^S \\in [0,1]$ / `learning_rate (float)`: rate of learning for a given student sampled from a distribution\n\n$f_i^S \\sim F^S, f_i^S \\in [0,1]$ / `forget_rate (float)`: rate of forgetting for a given student sampled from a distribution\n\n`binary_learning (bool)`: if a skill should be considered known ($=1$) or not ($=0$) instead of being continuous between 0 and 1\n\n`seed (int)`: random seed to use when generating the students\n\n#### Questions\n\nQuestions are generated with the following parameters:\n\n`n`: number of questions to generate\n\n$n_j \\sim N^Q, n_j \\in \\{0,...,n^K\\}$ / `n_skills (int)`: number of skills per question sampled from a distribution\n\n$m_{ik} \\sim M^Q, m_{ik} \\in [0,1]$ / `skill_mastery (float)`: mastery for a given question and skill sampled from a distribution\n\n$d_j^Q \\sim D^Q, d_j^Q \\in [0,1]$ / `difficulty (float)`: difficulty for a given question sampled from a distribution\n\n$s_j^Q \\sim S^Q, s_j^Q \\in [0,1]$ / `slip (float)`: slip rate for a given question sampled from a distribution\n\n$g_j^Q \\sim G^Q, g_j^Q \\in [0,1]$ / `guess (float)`: guess rate for a given question sampled from a distribution\n\n`seed (int)`: random seed to use when generating the questions\n\n#### Answers\n\nAnswers are generated using the following formulas:\n\n$$\\boldsymbol{q}_j = \\left(q_{jk}\\right)_{k=1,...,n^K}$$\n\n$$s_{ij} = 1 - \\sqrt{(1 - s_i) \\cdot (1 - s_j)}$$\n\n$$g_{ij} = 1 - \\sqrt{(1 - g_i) \\cdot (1 - g_j)}$$\n\n$$\\boldsymbol{s}_i^0 = \\left(s_{ik}\\right)_{k=1,...,n^K}$$\n\n$$\\boldsymbol{s}_i^t = \\underbrace{f_i \\cdot \\boldsymbol{s}_i^{t-1}}_{\\text{skill forgetting}} + l_i \\cdot \\underbrace{(1 - g_a) \\cdot (1 - g_{ij})}_{\\text{adjustment for guessing}} \\cdot \\underbrace{(0.5 + d_j)}_{\\text{adjustment for difficulty}} \\cdot \\underbrace{(1 - w_a \\cdot (1 - a_i^t))}_{\\text{adjustment for correctness}} \\cdot \\boldsymbol{q}_j$$\n\n$$a_i^t = g_{ij} + (1 - s_{ij}) \\cdot \\frac{m_{ij}}{1 + m_{ij}}$$\n\n$$m_{ij} = \\exp\\left(m_a \\cdot (\\boldsymbol{q}_j^T\\boldsymbol{s}_i^t - d_j)\\right)$$\n\n\nfor question $j$ asked at time $t$ and with the following parameters:\n\n$n_i^A \\sim N^A, n_i^A \\in \\mathbb{N}$ / `n_per_student (int)`: number of questions asked per student sampled from a distribution\n\n$w_a \\in \\mathbb{R}^+$ / `wrong_answer_adjustment (float)`: by how much should the learning be scaled for a wrong answer\n\n$g_a \\in \\mathbb{R}^+$ / `guess_adjustment (float)`: by how much should the learning be scaled proportional to the guess parameter\n\n$m_a \\in \\mathbb{R}^+$ / `mastery_importance (float)`: by how much should the mastery importance part in the exponential be scaled by\n\n`max_repetitions (int)`: maximum number of repetition of a given question allowed per student\n\n`can_repeat_correct (bool)`: if a question answered correctly can be repeated\n\n`seed (int)`: random seed to use when generating the answers\n\n### Distributions\n\n__constant__: All samples have the same value `value`.\n\n__normal__: Samples are taken from a normal distribution with mean `mu` and standard deviation `sigma`.\n\n__binomial__: Samples are taken from a binomial distribution with number of possible successes `n` and probability of success `p`.\n',
    'author': 'Antoine Lefebvre-Brossard',
    'author_email': 'antoinelb@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/antoinelb/ktdg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
