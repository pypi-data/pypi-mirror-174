import os
import subprocess
from itertools import chain
from os import PathLike

import ffmpy

INVALID_CHARS = " =+/,;'\"][}{)(@!#$%^&*"
VIDEO_EXTENSIONS = ["mp4"]


def find_files_with_extension(
    root: str | PathLike,
    extension: str,
    ignore_paths=None,
):
    print(f"{root = }")
    print(f"{ignore_paths = }")
    for root_dir, _, files in os.walk(root, topdown=True):
        print("processing", root_dir)
        if ignore_paths and any(p in root_dir for p in ignore_paths):
            continue

        for file in files:
            fname = os.path.join(root_dir, file)
            _, ext = os.path.splitext(fname)
            if extension == ext.lstrip("."):
                yield fname


def has_audio(video_path: str | PathLike) -> bool:
    p = subprocess.run(
        [
            "ffprobe",
            "-i",
            video_path,
            "-show_streams",
            "-select_streams",
            "a",
            "-loglevel",
            "error",
        ],
        capture_output=True,
    )
    p.check_returncode()
    lines = bytes(chain(p.stdout or b"", p.stderr or b""))
    return bool(lines)


def convert_to_gif(
    video_path: str | PathLike,
    dry_run: bool = False,
    no_delete: bool = False,
    delete_ask: bool = False,
):
    fname_noext, _ = os.path.splitext(video_path)
    gif_filename = f"{fname_noext}.gif"
    print("converting", video_path, "to", gif_filename)
    if not dry_run:
        filters = [
            "fps=30,scale=-1:-1:flags=lanczos,split[s0][s1]",
            "[s0]palettegen[p]",
            "[s1][p]paletteuse",
        ]
        filters_arg = ";".join(filters)
        ff = ffmpy.FFmpeg(
            inputs={video_path: None},
            outputs={gif_filename: f'-vf "{filters_arg}" -y'},
        )
        ff.run()

    if not no_delete and not delete_ask:
        print("deleting", video_path)
        if not dry_run:
            os.unlink(video_path)

    if delete_ask:
        print("converted", video_path, "to", gif_filename)
        while (reply := input("delete? [y]/n: ").strip().lower()) not in ("", "y", "n"):
            pass

        reply = reply or "y"
        if reply.strip().lower() == "y":
            print("deleting", video_path)
            os.unlink(video_path)


def remove_empty_files(
    root_path: str | PathLike,
    dry_run: bool = False,
    ignore_paths=None,
):
    ignore_paths = ignore_paths or []
    for root, _, files in os.walk(root_path):
        if ignore_paths and any(path in root for path in ignore_paths):
            continue

        for file in files:
            fname = os.path.join(root, file)
            if os.stat(fname).st_size == 0:
                print("deleting", fname)
                if not dry_run:
                    os.unlink(fname)


def change_invalid_names(
    root_path: str | PathLike,
    dry_run: bool = False,
    ignore_paths=None,
):
    ignore_paths = ignore_paths or []
    for root, _, files in os.walk(root_path):
        if ignore_paths and any(path in root for path in ignore_paths):
            continue

        for file in files:
            orig_filename = file
            new_filename = file
            for char in INVALID_CHARS:
                if char in orig_filename:
                    new_filename = new_filename.replace(char, "_")

            if orig_filename != new_filename:
                orig_path = os.path.join(root, orig_filename)
                new_path = os.path.join(root, new_filename)
                print("renaming", orig_path, "to", new_path)
                if not dry_run:
                    os.rename(orig_path, new_path)
