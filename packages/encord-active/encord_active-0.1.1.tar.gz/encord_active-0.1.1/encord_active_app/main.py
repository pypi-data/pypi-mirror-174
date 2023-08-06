import sys
from pathlib import Path

import inquirer as i
import typer
from encord_active.indexers.fetch_prebuilt_indexers import (
    PREBUILT_PROJECTS,
    fetch_index,
)
from streamlit.web import cli as stcli

import encord_active_app.conf  # pylint: disable=unused-import

APP_NAME = "encord-active"

cli = typer.Typer(rich_markup_mode="markdown")

__PREBUILT_PROJECT_NAMES = list(PREBUILT_PROJECTS.keys())


@cli.command(rich_help_panel="Utils")
def download(
    project_dir: Path = typer.Option(
        None,
        help="Location of the project folder. Prebuilt indexes will be downloaded here.",
        prompt="Where should we store the data?",
        file_okay=False,
    ),
    project_name: str = typer.Option(
        None, help=f"Name of the project. Available projects: {__PREBUILT_PROJECT_NAMES}."
    ),
):
    """
    **Downloads** the prebuilt indexes 📁

    * If --project_name is not given as an argument, available prebuilt projects will be listed and the user can select it from the menu.
    """
    project_dir = Path(project_dir).expanduser().absolute()
    if not project_dir.exists():
        create = typer.confirm("Directory not existing, want to create it?")
        if not create:
            print("Not createing.")
            raise typer.Abort()
        project_dir.mkdir(parents=True)

    if project_name is not None and project_name not in PREBUILT_PROJECTS:
        print("No such project")
        raise typer.Abort()

    if not project_name:
        questions = [i.List("project_name", message="Choose a project", choices=__PREBUILT_PROJECT_NAMES)]
        answers = i.prompt(questions)
        if not answers or "project_name" not in answers:
            print("Project not selected.")
            raise typer.Abort()
        project_name = answers["project_name"]

    fetch_index(project_name, project_dir)


@cli.command(name="import", rich_help_panel="Utils")
def import_project():
    """
    **Imports** a project from Encord 📦
    """
    from encord_active.indexers.import_encord_project import main as import_script

    # TODO: move the setup into a config command.
    # currently the import setup will run every time.
    import_script()


@cli.command()
def visualise(
    project_path: Path = typer.Argument(
        ...,
        help="Path of the project you would like to visualise",
        file_okay=False,
    ),
):
    """
    Launches the application with the provided project ✨
    """
    streamlit_page = (Path(__file__).parent / "streamlit_entrypoint.py").expanduser().absolute()

    data_dir = Path(project_path).expanduser().absolute().as_posix()
    sys.argv = ["streamlit", "run", streamlit_page.as_posix(), data_dir]
    sys.exit(stcli.main())  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    cli(prog_name=APP_NAME)
