import os
from ..audio2face import Audio2Face

DEFAULT_PLAYER_INSTANCE = "/World/audio2face/Player"


def set_root_path(a2f: Audio2Face, sounds_folder):
    payload = {
        "a2f_player": DEFAULT_PLAYER_INSTANCE,
        "dir_path": sounds_folder
    }

    a2f.post("A2F/Player/SetRootPath", payload=payload)


def set_track(a2f: Audio2Face, input_sound_path: str):
    if not os.path.isfile(input_sound_path):
        raise f"File {input_sound_path} doesn't exist"

    payload = {
        "a2f_player": DEFAULT_PLAYER_INSTANCE,
        "file_name": os.path.basename(input_sound_path),
        "time_range": [0, -1]
    }

    a2f.post("A2F/Player/SetTrack", payload=payload)
    