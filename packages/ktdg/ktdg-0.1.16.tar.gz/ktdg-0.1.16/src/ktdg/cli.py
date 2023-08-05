from pathlib import Path

import typer

from .config import Config, read_config, save_config
from .generation import generate, save_data
from .utils import done_print


def init_cli() -> typer.Typer:
    cli = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
    cli.command("create")(create_or_update_config)
    cli.command("c", hidden=True)(create_or_update_config)
    cli.command("generate")(generate_)
    cli.command("g", hidden=True)(generate_)
    return cli


def run_cli() -> None:
    cli = init_cli()
    cli()


def create_or_update_config(
    file: str = typer.Argument(
        ..., help="Path of the config to complete or create"
    ),
) -> None:
    """
    (c) Creates a config or completes it, saving it to the given file.
    """
    if not file.endswith(".yml"):
        file = f"{file}.yml"
    path = Path(file)
    try:
        config = read_config(path)
        save_config(config, path)
        done_print(f"Updated config {file}.")
    except FileNotFoundError:
        config = Config(name=path.stem)
        save_config(config, path)
        done_print(f"Created config {file}.")


def generate_(
    config: str = typer.Argument(..., help="Configuration file to use"),
    output_file: str = typer.Argument(
        "data.json", help="File in which to save the data."
    ),
) -> None:
    """
    (g) Generates the data for the given config, saving it as a json file.
    """
    config_ = read_config(Path(config))
    data = generate(config_)
    save_data(data, Path(output_file))
