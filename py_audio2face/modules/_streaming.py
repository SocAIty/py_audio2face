# The gRPC client is needed to send requests to the streaming instances like the audiostreaming player.
# This is inspired by the official NVIDIA test streaming client:
# C:\Users\...\AppData\Local\ov\pkg\audio2face-2023.1.1\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server
# Also there's a youtube video that helped to implement it: https://www.youtube.com/watch?v=qKhPwdcOG_w

from __future__ import annotations  # avoid circular import with import py_audio2face
import py_audio2face.audio2face as a2f

from py_audio2face.settings import DEFAULT_AUDIO_STREAM_PLAYER_INSTANCE, DEFAULT_AUDIO_STREAM_GRPC_PORT
from typing import Generator, Union

try:
    import grpc
    import numpy as np
    from py_audio2face.modules.clients.grpc_stub import audio2face_pb2, audio2face_pb2_grpc
    streaming_installed = True
except:
    streaming_installed = False


class _A2F_streaming:

    def stream_audio(
            self: a2f,
            audio_stream: Generator[Union[np.ndarray, bytes], None, None],
            samplerate: int,
            block_until_playback_is_finished: bool = True,
            instance_name: str = DEFAULT_AUDIO_STREAM_PLAYER_INSTANCE,
            grpc_port: int = DEFAULT_AUDIO_STREAM_GRPC_PORT
    ) -> (list, bool):
        """
        Stream audio data to Audio2Face Streaming Audio Player.

        :param audio_stream: Generator yielding audio chunks (numpy arrays or bytes)
        :param samplerate: Sampling rate of the audio data
        :param block_until_playback_is_finished: If True, blocks until playback is finished
        :param instance_name: Prim path of the Audio2Face Streaming Audio Player
        :param grpc_port: Port of the gRPC server
        :return: True if streaming was successful, False otherwise
        """
        if not streaming_installed:
            raise ImportError(
                "py_audio2face[streaming] is not installed. "
                "Please install it via 'pip install py_audio2face[streaming]'"
            )

        self.init_a2f(streaming=True)
        url = f"localhost:{grpc_port}"

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
                for i, chunk in enumerate(audio_stream):
                    if isinstance(chunk, np.ndarray):
                        chunk = chunk.astype(np.float32).tobytes()
                    res = audio2face_pb2.PushAudioStreamRequest(audio_data=chunk)
                    yield res

            response = stub.PushAudioStream(request_generator())
            return response.success

    #def stream_audio(
    #        self: a2f,
    #        audio_stream: Generator[Union[np.ndarray, bytes], None, None],
    #        samplerate: int,
    #        export_blend_shape_interval: int | None = None,
    #        export_fps: int = 60,
    #        export_path: str | None = None,
    #        export_emotion: bool = False,
    #        export_format: str = "usd",
    #        block_until_playback_is_finished: bool = True,
    #        instance_name: str = DEFAULT_AUDIO_STREAM_PLAYER_INSTANCE,
    #        grpc_port: int = DEFAULT_AUDIO_STREAM_GRPC_PORT
    #) -> (list, bool):
    #    """
    #    Stream audio data to Audio2Face Streaming Audio Player.
#
    #    :param audio_stream: Generator yielding audio chunks (numpy arrays or bytes)
    #    :param samplerate: Sampling rate of the audio data
    #    :param export_blend_shape_interval: Interval to export blend shapes. If None, no blend shapes are exported
    #    :param export_fps: FPS of the exported animation
    #    :param export_path: Path to export the animation
    #    :param export_emotion: Whether to generate emotion_auto_detect keys from the audio
    #    :param export_format: Format of the exported animation
    #    :param block_until_playback_is_finished: If True, blocks until playback is finished
    #    :param instance_name: Prim path of the Audio2Face Streaming Audio Player
    #    :param grpc_port: Port of the gRPC server
    #    :return: True if streaming was successful, False otherwise
    #    """
    #    self.init_a2f(streaming=True)
    #    a2f_instance = utils.get_mark_usd_file_path(streaming=True)
    #    url = f"localhost:{grpc_port}"
#
    #    if export_blend_shape_interval is not None and export_path is None:
    #        print(f"output path is not provided, using default: {DEFAULT_OUTPUT_DIR}")
    #        export_path = DEFAULT_OUTPUT_DIR
#
    #    generated_blendshapes = []
    #    with grpc.insecure_channel(url) as channel:
    #        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)
#
    #        def request_generator():
    #            # Send start marker
    #            start_marker = audio2face_pb2.PushAudioRequestStart(
    #                samplerate=samplerate,
    #                instance_name=instance_name,
    #                block_until_playback_is_finished=block_until_playback_is_finished
    #            )
    #            yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)
#
    #            # Stream audio data
    #            last_export_frame = 0
    #            for i, chunk in enumerate(audio_stream):
    #                if isinstance(chunk, np.ndarray):
    #                    chunk = chunk.astype(np.float32).tobytes()
    #                res = audio2face_pb2.PushAudioStreamRequest(audio_data=chunk)
#
    #                # export blendshapes and clear the buffer if interval
    #                if export_blend_shape_interval is not None and i % export_blend_shape_interval == 0:
    #                    self.set_frame(frame=last_export_frame, a2f_instance=a2f_instance, as_timestamp=False)
    #                    f = self.export(
    #                        output_path=f"{export_path}_{i}.{export_format}",
    #                        fps=export_fps, format=export_format, emotion_auto_detect=export_emotion
    #                    )
    #                    generated_blendshapes.append(f)
    #                    last_export_frame = i
#
    #                yield res
#
    #        response = stub.PushAudioStream(request_generator())
    #        return generated_blendshapes, response.success
#

