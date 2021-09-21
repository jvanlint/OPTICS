#!/usr/bin/env python
"""
Download the given htmx version and the extensions we're using.
"""
import argparse
from typing import List, Optional
import requests
import os
import pathlib


def main(argv: Optional[List[str]] = None) -> int:
    default_directory = "static/js"
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="e.g. 1.5.0")
    parser.add_argument("-p", "--js_path",
                        help="root of js folder for project (default: static/js)",
                        default=default_directory,
                        )
    args = parser.parse_args(argv)
    version: str = args.version
    js_path: str = args.js_path
    js_path = os.path.normpath(os.path.join(js_path, "htmx"))
    ext_path = os.path.normpath(os.path.join(js_path, "ext"))

    if not directory_exists(js_path):
        create_directory(js_path)
    if not directory_exists(ext_path):
        create_directory(ext_path)

    download_file(version, "htmx.min.js", js_path)
    download_file(version, "ext/debug.js", js_path)
    download_file(version, "ext/event-header.js", js_path)

    print("✅")
    return 0


def directory_exists(directory):
    print(f"checking {directory} exists")
    return pathlib.Path(directory).exists()


def create_directory(path):
    try:
        print(f"creating folder: {path}")
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        # os.mkdir(path)
    except Exception as error:
        print(f"Error creating directory: {error}")


def download_file(version: str, name: str, path) -> None:
    print(f"{name}...")
    url = f"https://unpkg.com/htmx.org@{version}/dist/{name}"
    filename_and_path = os.path.join(path, name)
    r = requests.get(url)
    with open(filename_and_path, 'wb') as f:
        f.write(r.content)
    print(r.status_code)

    # Fix lack of trailing newline in minified files as otherwise pre-commit
    # has to fix it.
    if name.endswith(".min.js"):
        with open(filename_and_path, "a") as fp:
            fp.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())