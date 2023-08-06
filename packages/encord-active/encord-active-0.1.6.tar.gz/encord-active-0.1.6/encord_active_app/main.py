import sys
from pathlib import Path

import inquirer as i
import typer
from encord_active.indexers.fetch_prebuilt_indexers import (
    PREBUILT_PROJECT_TO_STORAGE,
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
        help="Location where to download the project. Prebuilt metrics will be downloaded as well.",
        prompt="Where should the prebuilt project be stored (absolute/relative path)?",
        file_okay=False,
    ),
    project_name: str = typer.Option(
        None, help=f"Name of the chosen project. Available prebuilt projects: {__PREBUILT_PROJECT_NAMES}."
    ),
):
    """
    **Downloads** a prebuilt project and metrics 📁

    * If --project_name is not given as an argument, available prebuilt projects will be listed
     and the user can select one from the menu.
    """
    project_parent_dir = Path(project_dir).resolve()
    if not project_parent_dir.exists():
        create = typer.confirm("Such directory does not exist, do you want to create it?")
        if not create:
            print("Canceling project download.")
            raise typer.Abort()
        project_parent_dir.mkdir(parents=True)

    if project_name is not None and project_name not in PREBUILT_PROJECTS:
        print("No such project in prebuilt projects.")
        raise typer.Abort()

    if not project_name:
        project_names_with_storage = [p + f" ({PREBUILT_PROJECT_TO_STORAGE[p]})" for p in __PREBUILT_PROJECT_NAMES]
        questions = [i.List("project_name", message="Choose a project", choices=project_names_with_storage)]
        answers = i.prompt(questions)
        if not answers or "project_name" not in answers:
            print("No project was selected.")
            raise typer.Abort()
        project_name = answers["project_name"].rsplit(" (", maxsplit=1)[0]

    # create project folder
    project_dir = project_parent_dir / project_name
    project_dir.mkdir(exist_ok=True)

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
