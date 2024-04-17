import os
from audio2face import Audio2Face

DEFAULT_SOLVER_INSTANCE = "/World/audio2face/BlendshapeSolve"


def export_blend_shape(a2f: Audio2Face, output_path: str, fps: int = 60, format: str ="usd"):

    payload = {
        "solver_node": DEFAULT_SOLVER_INSTANCE,
        "export_directory": os.path.dirname(output_path),
        "file_name": os.path.basename(output_path),
        "format": format,
        "batch": False,
        "fps": fps
    }

    a2f.post("A2F/Exporter/ExportBlendshapes", payload=payload)
    