"""
The gRPC client is needed to send requests to the streaming instances like audiostreaming player.

"""

import socket
import struct
from typing import Generator, Union
import numpy as np


class _A2F_GRPCClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def _send_message(self, message_type: int, payload: bytes) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            header = struct.pack('>II', message_type, len(payload))
            s.sendall(header + payload)

    def push_audio_stream(self,
                          audio_stream: Generator[Union[np.ndarray, bytes], None, None],
                          instance_name: str,
                          samplerate: int,
                          block_until_playback_is_finished: bool) -> bool:
        # Send start marker
        start_marker = struct.pack('>I?', samplerate, block_until_playback_is_finished)
        start_marker += instance_name.encode('utf-8')
        self._send_message(1, start_marker)

        # Stream audio data
        for chunk in audio_stream:
            if isinstance(chunk, np.ndarray):
                chunk = chunk.astype(np.float32).tobytes()
            self._send_message(2, chunk)

        # Send end marker
        self._send_message(3, b'')

        # Receive response
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            response = s.recv(1024)
            return struct.unpack('>?', response[:1])[0]