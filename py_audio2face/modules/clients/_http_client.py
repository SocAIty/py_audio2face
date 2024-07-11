from __future__ import annotations  # avoid circular import with import py_audio2face
import py_audio2face.audio2face as a2f

from subprocess import Popen, CREATE_NEW_CONSOLE
import time
import requests
import os
from requests import JSONDecodeError


class _A2F_HTTP_CLIENT:
    def make_request(self: a2f.Audio2Face, api_route):
        url = f"{self.api_url}/{api_route}"
        try:
            response = requests.get(url)
            res = response.json()
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res


    def post(self: a2f.Audio2Face, api_route: str, payload):
        url = f"{self.api_url}/{api_route}"
        res = None
        try:
            response = requests.post(url, json=payload, headers="")
            res = response.json()
        except JSONDecodeError as e:
            print(f"Response of API {url} is not JSON format. Intended?")
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res


    def start_headless_server(self: a2f.Audio2Face):
        # check if already running
        status = self.make_request("status")
        if status == "OK":
            print("audio2face running")
            return status

        print("starting audio2face headless")
        batch_file = f"{self.a2f_install_path}/audio2face_headless.bat"
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


    def init_a2f(self: a2f.Audio2Face):
        self.start_headless_server()
        self.load_scene(self.mark_usd_file)


    def shutdown_a2f(self: a2f.Audio2Face):
        try:
            self.process_audio2face.kill()
        except:
            print("Can't kill a2f process. Was started separately?")
