# The gRPC client is needed to send requests to the streaming instances like the audiostreaming player.
# This is inspired by the official NVIDIA test streaming client:
# C:\Users\...\AppData\Local\ov\pkg\audio2face-2023.1.1\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server
# Also there's a youtube video that helped to implement it: https://www.youtube.com/watch?v=qKhPwdcOG_w

from __future__ import annotations  # avoid circular import with import py_audio2face
import py_audio2face.audio2face as a2f

import grpc
from typing import Generator, Union
import numpy as np

from modules.clients.grpc_stub import audio2face_pb2, audio2face_pb2_grpc
from settings import DEFAULT_AUDIO_STREAM_PLAYER_INSTANCE, DEFAULT_AUDIO_STREAM_GRPC_PORT


class _A2F_GRPC_Client:
    def stream_audio(
            self: a2f,
            audio_stream: Generator[Union[np.ndarray, bytes], None, None],
            samplerate: int,
            block_until_playback_is_finished: bool = True,
            instance_name: str = DEFAULT_AUDIO_STREAM_PLAYER_INSTANCE,
            grpc_port: int = DEFAULT_AUDIO_STREAM_GRPC_PORT
    ) -> bool:
        """
        Stream audio data to Audio2Face Streaming Audio Player.

        :param audio_stream: Generator yielding audio chunks (numpy arrays or bytes)
        :param samplerate: Sampling rate of the audio data
        :param block_until_playback_is_finished: If True, blocks until playback is finished
        :param instance_name: Prim path of the Audio2Face Streaming Audio Player
        :param grpc_port: Port of the gRPC server
        :return: True if streaming was successful, False otherwise
        """
        self.init_a2f()

        url = f"localhost:{grpc_port}" #f"{self.api_url.replace('http://', '')}"  # Remove 'http://' from the URL

        with grpc.insecure_channel(url) as channel:
            stub = audio2face_pb2_grpc.Audio2FaceStub(channel)

            def request_generator():
                # Send start marker
                start_marker = audio2face_pb2.PushAudioRequestStart(
                    samplerate=samplerate,
                    instance_name=instance_name,
                    block_until_playback_is_finished=block_until_playback_is_finished
                )
                yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)

                # Stream audio data
                for chunk in audio_stream:
                    if isinstance(chunk, np.ndarray):
                        chunk = chunk.astype(np.float32).tobytes()
                    yield audio2face_pb2.PushAudioStreamRequest(audio_data=chunk)

            response = stub.PushAudioStream(request_generator())
            return response.success

