from argparse import ArgumentParser
from os import getcwd
from posixpath import expanduser, expandvars

from filecleaner.media_tools import (
    VIDEO_EXTENSIONS,
    change_invalid_names,
    convert_to_gif,
    find_files_with_extension,
    has_audio,
    remove_empty_files,
)


def get_args():
    parser = ArgumentParser(
        description="""
        Performs 3 things: removes empty files, removes weird characters
        from filenames and makes them underscores, converts videos
        without sound to gifs.
        """,
    )
    parser.add_argument(
        "-r",
        "--root",
        default=getcwd(),
        help="directory to work on, default is current working directory",
    )
    parser.add_argument(
        "--dry-run",
        default=False,
        action="store_true",
        help="no actions to take place",
    )
    parser.add_argument(
        "--one",
        default=False,
        action="store_true",
        help="only one conversion to take place",
    )
    parser.add_argument(
        "--no-delete",
        default=False,
        action="store_true",
        help="not to delete the video after the conversion",
    )
    parser.add_argument(
        "-d",
        "--delete-ask",
        default=False,
        action="store_true",
        help="ask to delete every time after conversion",
    )
    parser.add_argument(
        "--always-convert",
        default=False,
        action="store_true",
        help="to convert all videos to gifs",
    )
    parser.add_argument(
        "-i",
        "--ignore-paths",
        nargs="*",
        help="paths to ignore",
        default=[
            ".git",
        ],
    )
    return parser.parse_args()


def perform_clean(
    root: str,
    dry_run: bool,
    one: bool,
    no_delete: bool,
    always_convert: bool,
    ignore_paths: list,
    delete_ask: bool,
):
    remove_empty_files(root, dry_run=dry_run, ignore_paths=ignore_paths)
    change_invalid_names(root, dry_run=dry_run, ignore_paths=ignore_paths)
    one_action_performed = False
    for extension in VIDEO_EXTENSIONS:
        for file in find_files_with_extension(
            root,
            extension,
            ignore_paths=ignore_paths,
        ):
            if always_convert or not has_audio(file):
                convert_to_gif(
                    file,
                    dry_run=dry_run,
                    no_delete=no_delete,
                    delete_ask=delete_ask,
                )
                one_action_performed = True

            if one and one_action_performed:
                return


def main():
    args = get_args()
    perform_clean(
        expandvars(expanduser(args.root)),
        args.dry_run,
        args.one,
        args.no_delete,
        args.always_convert,
        args.ignore_paths,
        args.delete_ask,
    )


if __name__ == "__main__":
    main()
