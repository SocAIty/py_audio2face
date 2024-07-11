from __future__ import annotations  # avoid circular import with import py_audio2face
import py_audio2face.audio2face as a2f

import os
from py_audio2face.settings import DEFAULT_PLAYER_INSTANCE



class _A2FPlayer:
    def set_root_path(self: a2f.Audio2Face, sounds_folder):

        # if is a file, get the folder
        if os.path.isfile(sounds_folder):
            sounds_folder = os.path.dirname(sounds_folder)

        # fix relative paths
        if not os.path.isabs(sounds_folder):
            sounds_folder = os.path.join(os.getcwd(), sounds_folder)

        payload = {
            "a2f_player": DEFAULT_PLAYER_INSTANCE,
            "dir_path": sounds_folder
        }

        self.post("A2F/Player/SetRootPath", payload=payload)

    def set_track(self: a2f.Audio2Face, input_sound_path: str):
        if not os.path.isfile(input_sound_path):
            raise FileNotFoundError(f"File {input_sound_path} doesn't exist")

        payload = {
            "a2f_player": DEFAULT_PLAYER_INSTANCE,
            "file_name": os.path.basename(input_sound_path),
            "time_range": [0, -1]
        }

        self.post("A2F/Player/SetTrack", payload=payload)

