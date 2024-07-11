import os
import glob
import importlib_resources
from settings import APP_DATA_DIR


def get_files_in_dir(path: str, extensions: list = None) -> list:
    """ returns all files in a directory filtered by extension list"""
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    if not os.path.isdir(path):
        raise FileNotFoundError(f"{path} is not a directory")

    files = []
    # return all files
    if extensions is None:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        # return files filtered by extensions
        for ext in extensions:
            files.extend(glob.glob(os.path.join(path, "*" + ext)))

    return files


def get_audio2face_install_path():
    """
    Get the newest installed audio2face installation path from the default location (in AppData)
    """

    # the default dir is usually in C:\\Users\\USERNAME\\AppData\\Local\\ov\\pkg\\audio2face-2023.1.1\\
    # get users appdata dir
    # update to audio2face-2023.2.0

    # get installed versions:
    audio2face_install_dir = os.path.join(APP_DATA_DIR, "ov/pkg/")
    installed_versions = [
        os.path.basename(os.path.normpath(d))
        for d in glob.glob(audio2face_install_dir + "audio2face-*")
    ]
    if len(installed_versions) == 0:
        print("No audio2face versions found in default location. Please specify manually.")
        return None

    # take newest version
    installed_versions.sort(reverse=True)
    newest_version = installed_versions[0]
    print("Installed versions: ", installed_versions)
    print("Using version: ", newest_version)

    newest_year, newest_v = newest_version.split("-")[1].split(".", 1)
    newest_year, newest_v = int(newest_year), float(newest_v)
    if newest_year < 2023 or newest_v < 2.0:
        print(f"Your audio2face version {newest_year}.{newest_version} is old. "
              f"Please consider that a2emotion features won't work.")

    return os.path.join(audio2face_install_dir, newest_version)


def get_mark_usd_file_path(streaming = False) -> str:
    if not streaming:
        usd_file_path = importlib_resources.files('py_audio2face') / 'assets' / 'mark_arkit_solved_default.usd'
    else:
        usd_file_path = importlib_resources.files('py_audio2face') / 'assets' / 'mark_arkit_solved_streaming.usd'

    return str(usd_file_path)
