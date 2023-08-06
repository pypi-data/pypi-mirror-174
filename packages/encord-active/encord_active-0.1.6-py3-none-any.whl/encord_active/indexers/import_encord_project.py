import re
import sys
from pathlib import Path
from typing import Optional, cast

import encord.exceptions
import yaml
from encord import EncordUserClient, Project
from termcolor import colored, cprint

project_root = Path(__file__).parents[1]
sys.path.append(project_root.as_posix())

from encord_active.indexers.run_all import run_indexers

PROJECT_HASH_REGEX = r"([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})"

_step = 1
text_color = "blue"
warning_color = "yellow"
error_color = "red"
file_color = "cyan"
header_color = "magenta"
note_color = "white"


def hr(char="-", length=64, color=header_color):
    cprint(char * length, color)


def step(status: str):
    global _step
    hr(char="=")
    cprint(f"| {_step}: {status:57s} |", header_color)
    hr()
    print()
    _step += 1


def box_text(text, title="Note", length=100, color=note_color):
    half_line_size = (length - len(title) - 2) // 2
    cprint("-" * half_line_size + f" {title} " + "-" * half_line_size, color)
    txt_len = length - 4
    rest = text
    i = 0
    while rest:
        substr_no_divide = rest[i * txt_len : (i + 1) * txt_len]
        if "\n" in substr_no_divide:
            idx = substr_no_divide.index("\n")
            line = substr_no_divide[:idx]
            remainder = [substr_no_divide[idx + 1 :]]
        elif len(substr_no_divide) == txt_len:
            line, *remainder = substr_no_divide.rsplit(" ", 1)
        else:
            line = substr_no_divide
            remainder = []

        if not remainder:
            rest = ""

        cprint(f"| {line:{length-4}s} |", color)
        if rest:
            rest = remainder[0] + rest[(i + 1) * txt_len :]
    hr(length=length, color=color)
    print()


def main():
    step("encord details".title())

    # == Get key file ==  #
    hr()
    cprint("First, we'll need the path to your public ssh key.", text_color)

    box_text(
        "If you haven't set up an ssh key with Encord, you can follow the tutorial in this link: "
        "https://docs.encord.com/admins/settings/public-keys/#set-up-public-key-authentication"
    )

    key_file = None
    while key_file is None or not key_file.is_file():
        key_file = Path(input(colored("Specify ssh private key path: ", text_color))).expanduser().absolute()

        if not key_file.is_file():
            print(
                colored("🔎 Key file", warning_color),
                colored(f"`{key_file}`", file_color),
                colored("doesn't exist", warning_color),
            )

    existing_key_file = cast(Path, key_file)
    with existing_key_file.open("r", encoding="utf-8") as f:
        key: str = f.read()
    client = EncordUserClient.create_with_ssh_private_key(key)

    # == Get project hash === #
    hr()
    cprint("Next, we need your encord project id.")
    box_text(
        "If you don't know your project id, follow these steps: \n"
        " 1. Log in to your account on https://app.encord.com/\n"
        " 2. Navigate to the Projects tab in the Navigation bar\n"
        " 3. Select a project\n"
        " 4. Navigate to the ‘Settings’ tab and select the ‘API access’ pane on the left\n"
        " 5. Find the `Project ID` in the center of the screen"
    )

    encord_project_hash = ""
    project: Optional[Project] = None
    while not encord_project_hash:
        _encord_project_hash = input(colored("Specify project id: ", text_color)).strip().lower()

        if not re.match(PROJECT_HASH_REGEX, _encord_project_hash):
            print(colored("🙈 Project id does not have the correct format.", warning_color))
            print("The format is a (hex) uuid: aaaaaaaa-bbbb-bbbb-bbbb-000000000000")
            continue

        # What I really had to do
        project = client.get_project(_encord_project_hash)
        try:  # some unnecessary test
            _ = project.title
        except encord.exceptions.AuthorisationError:
            print(colored("⚡️ You don't have access to the project, sorry 😫", error_color))
            continue

        encord_project_hash = _encord_project_hash

    if project is not None:
        existing_project = cast(Project, project)
    else:
        exit(1)

    # == Data storage location == #
    hr()
    cprint("Finally, we'll need to know where to store the data")

    accepted = False
    data_path = None
    while not accepted:
        data_path = Path(input(colored("Where should we store the data? ", text_color))).expanduser().absolute()

        print(colored("The absolute path of your data root will be", text_color), colored(f"`{data_path}`", "cyan"))
        ok_text = input(colored("Is this okay? [Y/n] ", text_color))
        accepted = not ok_text or "y" in ok_text.lower()

    if data_path is not None:
        existing_data_path = data_path
    else:
        exit(1)

    existing_data_path.mkdir(exist_ok=True, parents=True)

    meta_data = {
        "project_name": project.title,
        "project_description": project.description,
        "project_hash": project.project_hash,
        "ssh_key_path": existing_key_file.as_posix(),
    }
    meta_file_path = existing_data_path / "project_meta.yaml"
    yaml_str = yaml.dump(meta_data)
    with meta_file_path.open("w", encoding="utf-8") as f:
        f.write(yaml_str)

    cprint("Stored the following data: ", text_color)
    cprint(yaml_str, file_color)
    cprint("In file: ", text_color)
    cprint(f"`{meta_file_path}`", file_color)
    print()

    step("download data and run indexers".title())

    run_indexers(data_dir=existing_data_path)

    box_text(
        "The data is downloaded and the indexers are complete.\n"
        "\n"
        "Now run\n"
        + colored(f"> encord-active visualise {existing_data_path}", attrs=["reverse", "blink"])
        + " " * 12
        + "\n"
        + "to see your results.",
        title="🌟 Success 🌟",
        color="green",
    )
