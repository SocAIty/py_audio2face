import os
import glob
import importlib_resources

def get_files_in_dir(path: str, extensions: list = None) -> list:
    """ returns all files in a directory filtered by extension list"""
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a directory")

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
    # the default dir is usually in C:\\Users\\USERNAME\\AppData\\Local\\ov\\pkg\\audio2face-2023.1.1\\
    # get users appdata dir

    appdata_dir =os.getenv('LOCALAPPDATA')
    audio2face_install_dir = os.path.join(appdata_dir, "ov/pkg/audio2face-2023.1.1/")
    if os.path.isdir(audio2face_install_dir):
        return audio2face_install_dir
    
    print("Could not find audio2face install dir in default location. Please specify manually.")
    return None


def get_mark_usd_file_path() -> str:
    usd_file_path= importlib_resources.files('py_audio2face') / 'assets' / 'mark_arkit_solved_default.usd'
    return str(usd_file_path)
