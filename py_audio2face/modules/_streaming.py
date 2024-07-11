
from __future__ import annotations
import py_audio2face.audio2face as a2f
from typing import Generator, Union
import numpy as np
from modules.clients._grpc_client import _A2F_GRPCClient


class _A2FStreaming:
    def stream_audio(self: a2f.Audio2Face,
                     audio_stream: Generator[Union[np.ndarray, bytes], None, None],
                     instance_name: str,
                     samplerate: int,
                     block_until_playback_is_finished: bool = True) -> bool:
        """
        Stream audio data to Audio2Face Streaming Audio Player.

        :param audio_stream: Generator yielding audio chunks (numpy arrays or bytes)
        :param instance_name: Prim path of the Audio2Face Streaming Audio Player
        :param samplerate: Sampling rate of the audio data
        :param block_until_playback_is_finished: If True, blocks until playback is finished
        :return: True if clients was successful, False otherwise
        """
        host, port = self.api_url.replace('http://', '').split(':')
        client = _A2F_GRPCClient(host, int(port))

        return client.push_audio_stream(
            audio_stream,
            instance_name,
            samplerate,
            block_until_playback_is_finished
        )