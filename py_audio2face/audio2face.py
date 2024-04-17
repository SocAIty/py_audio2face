"""
Use the headless mode of audio2face to generate the lip and face animations for our characters.
The script includes methods to
- start, stop and monitor the audio2face headless server
- interact with the headless server via a requests api
- Export the generated animations to the unreal engine 5 scene
"""

import os
from json import JSONDecodeError
from subprocess import Popen, CREATE_NEW_CONSOLE
import time
import requests
import tqdm

from py_audio2face import utils  # Import utils from the package
from py_audio2face.settings import ROOT_DIR


class Audio2Face:
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
        self.mark_usd_file = utils.get_mark_usd_file_path()
        print(f"mark_usd_file {self.mark_usd_file}")
        if a2f_install_path is None:
            a2f_install_path = utils.get_audio2face_install_path()
            if a2f_install_path is None:
                raise ValueError("Audio2Face installation path is not provided and not found in the registry. "
                                 "Install Audio2Face and provide the installation path manually.")

        self.a2f_install_path = a2f_install_path
        self.output_dir = output_dir
        self.process_audio2face = None


    def start_headless_server(self):
        # check if already running
        status = self.make_request("status")
        if status == "OK":
            print("audio2face running")
            return status

        print("starting audio2face headless")
        batch_file = f"{self.a2f_install_path}audio2face_headless.bat"

        if not os.path.isfile(batch_file):
            raise ValueError(f"audio2face_headless.bat not found in {self.a2f_install_path}. Is audio2face installed?")


        self.process_audio2face = Popen(batch_file, universal_newlines=True, creationflags=CREATE_NEW_CONSOLE)
        print("wait until audio2face is ready")
        start_open = time.time()

        # not managed to print the console output in pipe don't know why it doesnt work.
        # TODO: make it with subprocess call..
        while True:
            status = self.make_request("status")
            if str(status).lower() == "ok":
                break
            elif int(time.time() - start_open) >= 60:
                status = "timeout"
                break
            else:
                time.sleep(0.5)

        print(f"status {status}")
        return status

    def shutdown_a2f(self):
        try:
            self.process_audio2face.kill()
        except:
            print("Can't kill a2f process. Was started seperately?")
    def make_request(self, api_route):
        url = f"{self.api_url}/{api_route}"
        try:
            response = requests.get(url)
            res = response.json()
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res

    def post(self, api_route: str, payload):
        url = f"{self.api_url}/{api_route}"

        try:
            response = requests.post(url, json=payload, headers="")
            res = response.json()
        except JSONDecodeError as e:
            print(f"Response of API {url} is not JSON format. Intended?")
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res

    def get_scene(self):
        return self.make_request("A2F/GetInstances")

    def load_scene(self, usd_file_path: str =""):
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

    def set_root_path(self, sounds_folder):
        payload = {
            "a2f_player": "/World/audio2face/Player",
            "dir_path": sounds_folder
        }

        self.post("A2F/Player/SetRootPath", payload=payload)

    def set_track(self, input_sound_path: str):
        if not os.path.isfile(input_sound_path):
            raise f"File {input_sound_path} doesn't exist"

        payload = {
            "a2f_player": "/World/audio2face/Player",
            "file_name": os.path.basename(input_sound_path),
            "time_range": [0, -1]
        }

        self.post("A2F/Player/SetTrack", payload=payload)

    def a2e_set_settings(self, settings: dict):
        """
        Sets the settings for the audio2emotion generation
        Available settings:
          "a2f_instance": "string",
          "a2e_window_size": 0,
          "a2e_stride": 0,
          "a2e_emotion_strength": 0,
          "a2e_smoothing_kernel_radius": 0,
          "a2e_smoothing_exp": 0,
          "a2e_max_emotions": 0,
          "a2e_contrast": 0,
          "preferred_emotion": [
            0
          ],
          "a2e_preferred_emotion_strength": 0,
          "a2e_streaming_smoothing": 0,
          "a2e_streaming_update_period": 0,
          "a2e_streaming_transition_time": 0
        """

        self.post("A2F/A2E/SetSettings", payload=settings)

    def set_emotions(self, emotions_strength: dict):
        """
        Sets the emotions on a global level for the whole track
        emotions_strength: dict with emotion names and strength between 0..1 like {"Amazement": 0.5, "Anger": 0.2, ...}
        available emotions: "Amazement", "Anger", "Cheekiness", "Disgust",
            "Fear", "Grief", "Joy", "Outofbreath", "Pain", "Sadness"
            check also get_emotion_names() to get the available emotions
        """

        payload = {
            "a2f_instance": "/World/audio2face/CoreFullface",
            "emotions": emotions_strength
        }

        self.post("A2F/A2E/SetEmotion", payload=payload)

    def generate_emotion_keys(self, settings: dict=None):
        """
        Sets the settings for the audio2emotion generation
        Available settings:
          "a2f_instance": "/World/audio2face/CoreFullface",  * Necessary, default to be /World/audio2face/CoreFullface
          "a2e_window_size": 1.4,               Emotion Detection Range     Sets the size, in seconds, of an audio chunk used to predict a single emotion per keyframe.
          "a2e_stride": 1,                      Keyframe Interval           Sets the number of seconds between adjacent automated keyframes.
          "a2e_emotion_strength": 0.5,          Emotion Strength            Sets the strength of the generated emotions relative to the neutral emotion.
          "a2e_smoothing_kernel_radius": 0,     * WTF?!
          "a2e_smoothing_exp": 0,               Smoothing(Exp)              Sets the number of neighboring keyframes used for emotion smoothing.
          "a2e_max_emotions": 5,                Max Emotions                Sets a hard limit on the quantity of emotions that Audio2Emotion will engage at one time. (Emotions are prioritized by their strength.)
          "a2e_contrast": 1,                    Emotion Contrast            Controls the emotion spread - pushing higher and lower values.
          "preferred_emotion": [                Preferred Emotion           Sets a single emotion as the base emotion for the character animation. The preferred emotion is taken from the current settings in the Emotion widget and is mixed with generated emotions throughout the animation. (is not set indicates whether or not you’ve set a preferred emotion.)
            0
          ],
          "a2e_preferred_emotion_strength": 0,  Strength                    Sets the strength of the preferred emotion. This determines how present this animation will be in the final animation.
          "a2e_streaming_smoothing": 0,         * Only for streaming
          "a2e_streaming_update_period": 0,
          "a2e_streaming_transition_time": 0
        """

        # Default Generate From
        default_settings = {
            "a2f_instance": "/World/audio2face/CoreFullface",
            "a2e_window_size": 1.4,
            "a2e_stride": 1,
            "a2e_emotion_strength": 0.5,
            "a2e_smoothing_exp": 0.0,
            "a2e_max_emotions": 5,
            "a2e_contrast": 1.0,
        }

        # Apply default settings if no specific settings provided
        if settings is None:
            settings = default_settings
        else:
            # Update only the keys that are provided, keep others as default
            for key, value in default_settings.items():
                settings.setdefault(key, value)

        self.post("A2F/A2E/GenerateKeys",payload=settings)

    def set_auto_emotion(self, enable:bool=True):
        """
        Enable or disable the automatic generation of A2E keys on track change.
        Available settings:
            "a2f_instance": "string",
            "enable": true
        """

        payload = {
            "a2f_instance": "/World/audio2face/CoreFullface",
            "emotions": enable
        }

        self.post("A2F/A2E/SetEmotion", payload=payload)


    def export_blend_shape(self, output_path: str, fps: int = 60, format: str ="usd"):

        payload = {
            "solver_node": "/World/audio2face/BlendshapeSolve",
            "export_directory": os.path.dirname(output_path),
            "file_name": os.path.basename(output_path),
            "format": format,
            "batch": False,
            "fps": fps
        }

        self.post("A2F/Exporter/ExportBlendshapes", payload=payload)

    def get_emotion_names(self):
        return self.make_request("A2F/A2E/GetEmotionNames")
    
    def get_emotion(self, frame: int = 0):

        payload = {
            "a2f_instance": "/World/audio2face/CoreFullface",
            "as_vector": True,
            "frame": frame,
            "as_timestamp": False
            }
        
        return self.post("A2F/A2E/GetEmotion", payload=payload)

    def init_a2f(self):
        self.start_headless_server()
        self.load_scene(self.mark_usd_file)

    def audio2face_single(self, audio_file_path: str, output_path: str, fps: int = 60):
        self.init_a2f()

        self.set_root_path(os.path.dirname(audio_file_path))
        self.set_track(audio_file_path)
        # convert
        if not os.path.isdir(os.path.dirname(output_path)):
            print("creating output dir")
            os.makedirs(os.path.dirname(output_path))

        self.export_blend_shape(output_path=output_path, fps = fps)

    def audio2face_single_emotion(self, audio_file_path: str, output_path: str, fps: int = 60, emo_settings: dict=None):

        self.init_a2f()

        self.set_root_path(os.path.dirname(audio_file_path))
        self.set_track(audio_file_path)
        # convert
        if not os.path.isdir(output_path):
            print("creating output dir")
            os.makedirs(os.path.dirname(output_path))

        self.generate_emotion_keys(settings=emo_settings)

        self.export_blend_shape(output_path=output_path, fps = fps)

    def audio2face_folder(self, input_folder: str, output_folder: str):
        self.init_a2f()
        self.set_root_path(input_folder)
        audio_files = utils.get_files_in_dir(input_folder, [".wav", ".mp3"])

        # create output folder if not exists
        if not os.path.isdir(output_folder):
            print(f"creating output dir {output_folder}")
            os.makedirs(output_folder)

        # iterate and convert files
        audio_files_tqdm = tqdm.tqdm(audio_files)
        for af in audio_files_tqdm:
            audio_files_tqdm.set_description(f"Processing {af}")
            self.set_track(af)

            # outfile name will be base file name of af_a2f_animation
            outfile_name, ext = os.path.basename(af).split(".")
            outfile_name = f"{output_folder}/{outfile_name}_a2f_animation"
            self.export_blend_shape(outfile_name)
