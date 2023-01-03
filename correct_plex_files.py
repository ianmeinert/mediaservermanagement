#!/usr/bin/python3

import argparse
import sys

from pathlib import Path, PurePath, PurePosixPath


def generate_new_file_name(file_path: Path) -> list[set]:
    """This method recursively collects the alphanumeric filenames and generates
    a new filename based on the parent path.

    Args:
        file_path (Path): the directory containing paths of files to be renamed

    Returns:
        list[set]: Each set contains [0] the original filename, and [1] the new file name
    """
    file_name_set = []

    # using list comprehension, recursively collect only the Paths for each alphanumeric file name
    files_to_fix = [f for f in file_path.rglob("*") if f.is_file() and f.stem.isalnum()]

    # loop over each Path in the list to generate the new path name
    for orig_file in files_to_fix:
        # the parent path
        path = PurePath(orig_file).parent.name
        # the name of the file
        name = orig_file.stem
        # the generated new file name, maintaining the Path
        new_file = str(orig_file).replace(name, path)
        # store the set for later use
        file_name_set.append((orig_file, Path(new_file)))

    return file_name_set


def inplace_rename_files_in_path(file_path: Path):
    """The method will rename the files in a given path

    Args:
        file_path (Path): the directory containing paths of files to be renamed
    """
    file_set = generate_new_file_name(file_path)

    if file_set:
        for file_name_set in file_set:
            file_name_set[0].rename(file_name_set[1])
            print(
                f"Renamed {PurePosixPath(file_name_set[0]).name} to {PurePosixPath(file_name_set[1]).name}"
            )
    else:
        print("No eligible files were found.")


def main(file_path):
    """The main method which passes the args to the filename generator

    Args:
        file_path (_type_): the directory containing paths of files to be renamed
    """
    inplace_rename_files_in_path(file_path)
    print("Process complete.")
    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename Plex files")
    parser.add_argument(
        "--path", metavar="path", required=True, help="the path to workspace"
    )

    args = parser.parse_args()
    main(file_path=Path(args.path))
