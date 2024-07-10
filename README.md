# py_audio2face

## Overview

This Python script leverages the headless mode of [Audio2Face](https://www.nvidia.com/en-us/omniverse/apps/audio2face/) to generate animations for characters:
- lip movement animations
- face animations 
- emotions (new since 2023.2.0)
It provides methods to control the [Audio2Face headless server](https://docs.omniverse.nvidia.com/audio2face/latest/user-manual/rest-api.html) and interact with it through a requests API. 

A use case is to generate animations for a batch of audio files and export them as USD files for example for Maya or Unreal Engine 5.

Big thank you for the NVIDIA Team who made Audio2Face a great tool.


## Prerequisites

- Python 3.x
- Audio2Face installed on the system


## Important Note
 
- Modify the `ROOT_DIR` and `DEFAULT_OUTPUT_DIR` variables in the `settings.py` file as needed.

Feel free to explore and customize the script based on your project requirements. Enjoy animating your characters with Audio2Face!



## Installation

Install the `py_audio2face` package using pip:
```bash
pip install py_audio2face
or 
pip install git+https://github.com/SocAIty/py_audio2face.git
```

## Usage

1. **Initialize Audio2Face instance:**
```python
import py_audio2face as pya2f
a2f = pya2f.Audio2Face()
```

2. **Generate animation for a single audio file:**
 ```python
audio_file_path = "path/to/audio/file.wav"
output_path = "path/to/output/animation.usd"
a2f.audio2face_single(audio_file_path, output_path, fps=60)
```

To generate it including emotions use:
```python
a2f.audio2face_single(audio_file_path, output_path, fps=60, emotions=True)
```
You can also specify if emotions should be included and modify their settings:
```python
a2f.a2e_set_settings(a2e_emotion_strength=0.8, a2e_max_emotions=2)  # optionally modify emotion settings
a2f.audio2face_single(audio_file_path, output_path, fps=60, emotions=True, emotions_list=["happy", "sad"])
```


3. **Generate Animations for an Entire Folder:**
```python
input_folder = "path/to/audio/folder"
output_folder = "path/to/output/folder"
a2f.audio2face_folder(input_folder, output_folder)
   ```

4. **Shutdown Audio2Face Server:**
```python
a2f.shutdown_a2f()
   ```

This example initializes an `Audio2Face` instance, processes audio files in a specified folder, and shuts down the Audio2Face server.

# Related Projects

Why bother about recording audio files? 
- Convert text-to-speech with [SpeechCraft](https://github.com/SocAIty/SpeechCraft). Use the natural sounding speech and feed it into audio2face.
- Want sound natively like any other character? Use [RVC](https://github.com/SocAIty/Retrieval-based-Voice-Conversion-FastAPI) to clone any voice. This sounds so real, you'll not notice the difference to a real one.


## TODOs

Any contribution is appretiatet. At the moment the tests are not working and should be added. Also the communication with the headless.bat file and shutting down the server can be improved. 
Files with presettings for different characters would be great.

Me the author plans to use the package in another package that handles audio generation with tts and bark and transforms them instantly with a2f.
