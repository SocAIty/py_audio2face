from __future__ import annotations  # avoid circular import with import py_audio2face
import py_audio2face.audio2face as a2f
from settings import DEFAULT_A2E_INSTANCE

class _A2FGeneral:
    def get_scene(self: a2f.Audio2Face):
        return self.make_request("A2F/GetInstances")

    def load_scene(self: a2f.Audio2Face, usd_file_path: str = ""):
        # check if the scene is already loaded
        scene = self.get_scene()
        if usd_file_path in scene:
            return

        # load scene from file
        print(f"load scene {usd_file_path}")
        payload = {
            "file_name": usd_file_path
        }

        self.post("A2F/USD/Load", payload)

    def set_frame(self: a2f.Audio2Face, frame: int, as_timestamp: bool = False, a2f_instance: str = None):
        # get the default instance if not provided. Other instance needed for streaming.
        a2f_instance = a2f_instance or DEFAULT_A2E_INSTANCE

        payload = {
          "a2f_instance": a2f_instance,
          "frame": frame,
          "as_timestamp": as_timestamp
        }

        self.post("A2F/Player/SetFrame", payload)