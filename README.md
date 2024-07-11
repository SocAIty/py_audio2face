  <h1 align="center" style="margin-top:-25px">py_Audio2Face</h1>
<p align="center">
  <img align="center" src="docs/py_audio2face_icon.png" height="250" />
</p>
  <h2 align="center" style="margin-top:-10px">Generate expressive facial animation from audio</h2>

# Overview

This Python script leverages the headless mode of [Audio2Face](https://www.nvidia.com/en-us/omniverse/apps/audio2face/) to generate animations for characters:
- lip movement animations
- face animations 
- emotions (new since 2023.2.0)
- It provides methods to control the [Audio2Face headless server](https://docs.omniverse.nvidia.com/audio2face/latest/user-manual/rest-api.html) and interact with it through a requests API.


Use cases:
- Power your games and movies with expressive facial animations. Create natural looking virtual avatars.
- Generate animations for characters and export them as USD files for example for Maya or Unreal Engine 5.
- Stream audio data to the Audio2Face server to generate animations in real-time.




# Installation

Install the `py_audio2face` package using pip:
```bash
# With pip. Note: this version does not include the streaming feature
pip install py_audio2face
# Install also the streaming feature. This includes additional dependencies like grpcio and protobuf
pip install py_audio2face[streaming]
# Or install the latest version from GitHub to work with the newest version of Audio2Face
pip install git+https://github.com/SocAIty/py_audio2face.git
```

Modify the `ROOT_DIR`, `DEFAULT_OUTPUT_DIR`, and `DEFAULT_AUDIO_STREAM_GRPC_PORT` variables in the `settings.py` file as needed.

## Prerequisites

- [Audio2Face](https://www.nvidia.com/en-us/omniverse/download/) installed on the system
- Python 3.x

# Usage

**Initialize Audio2Face instance:**
```python
import py_audio2face as pya2f
a2f = pya2f.Audio2Face()
```

**Generate animation for audio files:**
 ```python
# Generate animation for a single audio file
a2f.audio2face_single(audio_file_path="path/to/audio/file.wav", output_path="path/to/output/animation.usd", fps=60, emotion=True)
# Generate animation for an entire folder of audio files
a2f.audio2face_folder(input_folder="path/to/my/folder", output_folder='/output', fps=60)
```

**Stream audio to Audio2Face:**

Instead of providing paths to the a2f headless server, you can stream the audio data directly to the server. 
This is useful if you want to generate animations in real-time, for a live stream or in a server setting.

For this example we use the media-toolkit to stream audio data. Install it with `pip install media-toolkit[AudioFile]"`.

```python
from media_toolkit import AudioFile
audio = AudioFile().from_file("path/to/audio/file.wav")
audio_stream = audio.to_stream()  # note: this can be any python generator that yields numpy arrays/bytes of audio data
a2f.stream_audio(audio_data, output_path="path/to/output/animation.usd", fps=60)
```
For streaming under the hood, a different scene with a streaming audio player is loaded in the init method.
Then with gRPC requests, the audio data is streamed to the server.


**Shutdown Audio2Face Server:**
```python
a2f.shutdown_a2f()
```

# Related Projects

Why bother about recording audio files? 
- Convert text-to-speech with [SpeechCraft](https://github.com/SocAIty/SpeechCraft). Use the natural sounding speech and feed it into audio2face.
- Want sound natively like any other character? Use [RVC](https://github.com/SocAIty/Retrieval-based-Voice-Conversion-FastAPI) to clone any voice. This sounds so real, you'll not notice the difference to a real one.
- Create and animate realistic looking characters with [MetaHuman](https://metahuman.unrealengine.com/) and audio2face

# Contribute

Any contribution is appreciated.
- [x] streaming: upgrade to protobuf 5
- [x] streaming: allow streaming back of blendshapes or on the fly export
- [x] create working unit tests
- [x] Provide different characters not only mark.usd
- [x] Allow multiple generations / streams at the same time

Please raise an issue if you have any suggestions, feature requests or need help with the script.


# Acknowledgements

Big thank you for the NVIDIA Team who made Audio2Face a great tool.