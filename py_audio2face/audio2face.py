"""
Use the headless mode of audio2face to generate the lip and face animations for our characters.
The script includes methods to
- start, stop and monitor the audio2face headless server
- interact with the headless server via a requests api
- Export the generated animations to the unreal engine 5 scene
"""

import os
import tqdm

from py_audio2face.modules.clients._http_client import _A2F_HTTP_CLIENT
from py_audio2face.modules._general import _A2FGeneral
from py_audio2face.modules._player import _A2FPlayer
from py_audio2face.modules._audio2emotion import _A2F_Audio2Emotion
from py_audio2face.modules._export import _A2FExport
from py_audio2face.modules._streaming import _A2F_streaming

from py_audio2face import utils


class Audio2Face(
    _A2F_HTTP_CLIENT,
    _A2FGeneral,
    _A2FExport,
    _A2FPlayer,
    _A2F_Audio2Emotion,
    _A2F_streaming
):
    def __init__(
            self,
            api_url="http://localhost:8011",
            a2f_install_path: str = None,
            output_dir: str = None
    ):
        """
        api_url (str): The API endpoint for Audio2Face.
        a2f_install_path (str): Path to the Audio2Face installation directory. If its tried to get it from defualt dir
        output_dir (str): Optional output directory for generated animations.
        """
        self.api_url = api_url
        if a2f_install_path is None:
            a2f_install_path = utils.get_audio2face_install_path()
            if a2f_install_path is None:
                raise FileNotFoundError(
                    "Audio2Face installation path is not provided and not found in the registry. "
                    "Install Audio2Face and provide the installation path manually."
                )
        if a2f_install_path[-1] != "/":
            a2f_install_path += "/"

        self.a2f_install_path = a2f_install_path
        self.output_dir = output_dir
        self.process_audio2face = None  # process object for audio2face from subprocess

        self.loaded_scene = None  # the current loaded scene. Checked in init_a2f for not loading the same scene again

        # audio2emotion
        self.a2e_settings = self.get_default_a2e_settings()

    def init_a2f(self, streaming: bool = False):
        """
        Starts the audio2face headless server if a2f not running.
        Sends the arkit_resolved mark_usd_file / streaming file to the audio2face server to initialize the scene.
        """
        mark_usd_file = utils.get_mark_usd_file_path(streaming)
        if self.loaded_scene == mark_usd_file:
            return

        self.start_headless_server()
        self.load_scene(mark_usd_file)

    def audio2face_single(
            self,
            audio_file_path: str,
            output_path: str,
            fps: int = 60,
            emotion_auto_detect: bool = True
    ) -> str:
        """
        Generate the face animation from a single audio file.
        audio_file_path (str): Path to the audio file.
        output_path (str): Path to the output animation file.
        fps (int): Frames per second of the output animation.
        emotion_auto_detect (bool): Whether to detect emotions in audio and convert them to keyframes. To change the
            default settings, use the set_emotion method.
        return: the path of the output file
        """
        self.init_a2f()

        self.set_root_path(audio_file_path)
        self.set_track(audio_file_path)

        return self.export(output_path=output_path, fps=fps, emotion_auto_detect=emotion_auto_detect)

    def audio2face_folder(self, input_folder: str, output_folder: str, fps: int = 60, emotion: bool = False) -> list:
        """
        Generate the face animations from all audio files in a folder.
        input_folder (str): Path to the folder containing the audio files.
        output_folder (str): Path to the output folder for the animations.
        fps (int): Frames per second of the output animations.
        emotion_auto_detect (bool): Whether to generate emotion_auto_detect keys from the audio files.
        :return: a list of the paths of the output files
        """
        self.init_a2f()

        self.set_root_path(input_folder)

        audio_files = utils.get_files_in_dir(input_folder, [".wav", ".mp3"])

        # iterate and convert files
        audio_files_tqdm = tqdm.tqdm(audio_files)
        output_files = []
        for af in audio_files_tqdm:
            audio_files_tqdm.set_description(f"Processing {af}")
            self.set_track(af)

            # outfile name will be base file name of af_a2f_animation
            outfile_name, ext = os.path.basename(af).rsplit(".", 1)
            outfile_name = f"{output_folder}/{outfile_name}_a2f_animation"

            of = self.export(output_path=outfile_name, fps=fps, emotion_auto_detect=emotion)
            output_files.append(of)

        return output_files