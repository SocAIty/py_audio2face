from __future__ import annotations  # avoid circular import with import py_audio2face
import py_audio2face.audio2face as a2f

import os
from settings import DEFAULT_SOLVER_INSTANCE


class _A2FExport:
    def export(self: a2f.Audio2Face, output_path: str, fps: int = 60, format: str = "usd", emotion: bool = False):

        # avoid non absolute paths
        if not os.path.isabs(output_path):
            output_path = os.path.join(os.getcwd(), output_path)

        if not os.path.isdir(os.path.dirname(output_path)):
            print(f"creating output dir: {output_path}")
            os.makedirs(os.path.dirname(output_path))

        if emotion:
            self.generate_emotion_keys()

        self.export_blend_shape(output_path=output_path, fps=fps, format=format)

    def export_blend_shape(self: a2f.Audio2Face, output_path: str, fps: int = 60, format: str = "usd"):
        payload = {
            "solver_node": DEFAULT_SOLVER_INSTANCE,
            "export_directory": os.path.dirname(output_path),
            "file_name": os.path.basename(output_path),
            "format": format,
            "batch": False,
            "fps": fps
        }

        self.post("A2F/Exporter/ExportBlendshapes", payload=payload)
