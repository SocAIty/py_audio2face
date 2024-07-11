from __future__ import annotations  # avoid circular import with import py_audio2face
import py_audio2face.audio2face as a2f

import os
from py_audio2face.settings import DEFAULT_SOLVER_INSTANCE, DEFAULT_OUTPUT_DIR


class _A2FExport:
    def export(
            self: a2f.Audio2Face,
            output_path: str,
            fps: int = 60,
            format: str = "usd",
            emotion_auto_detect: bool = False
    ):
        """
        Export the blend shapes to a file.
        :param output_path: Path to the output file.
        :param fps: Frames per second of the output animation.
        :param format: Output format of the animation file.
        :param emotion_auto_detect: Whether to generate emotion_auto_detect keys from the audio.
            If a dictionary is provided, it will be used as the emotion_auto_detect settings.
        """

        if output_path is None:
            print(f"output path is not provided, using default: {DEFAULT_OUTPUT_DIR}")
            output_path = DEFAULT_OUTPUT_DIR

        # avoid non absolute paths
        if not os.path.isabs(output_path):
            output_path = os.path.join(os.getcwd(), output_path)

        if not os.path.isdir(os.path.dirname(output_path)):
            print(f"creating output dir: {output_path}")
            os.makedirs(os.path.dirname(output_path))

        if emotion_auto_detect:
            self.generate_emotion_keys()

        response = self.export_blend_shape(output_path=output_path, fps=fps, format=format)
        if 'status' not in response or response['status'] == 'ERROR':
            print(f"BlendShape Export failed: {response['message']}")

        return output_path

    def export_blend_shape(self: a2f.Audio2Face, output_path: str, fps: int = 60, format: str = "usd"):
        payload = {
            "solver_node": DEFAULT_SOLVER_INSTANCE,
            "export_directory": os.path.dirname(output_path),
            "file_name": os.path.basename(output_path),
            "format": format,
            "batch": False,
            "fps": fps
        }

        return self.post("A2F/Exporter/ExportBlendshapes", payload=payload)
