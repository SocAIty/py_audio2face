import os
import py_audio2face as pya2f
from py_audio2face.settings import ASSETS_DIR, DEFAULT_AUDIO_STREAM_PLAYER_INSTANCE
from media_toolkit import AudioFile

test_audio_0 = os.path.join(ASSETS_DIR, "test_audio_0.wav")
test_audio_1 = os.path.join(ASSETS_DIR, "test_audio_1.wav")

a2f = pya2f.Audio2Face()
#a2f.init_a2f()
#without_emotion = a2f.audio2face_single(test_audio_0, 'myout1.usd', fps=60, emotion=False)
#with_emotion = a2f.audio2face_single(test_audio_0,'myoutemotion.usd', fps=60, emotion=True)

# testing the folder method
#test_folder = "assets/"
#all_converted = a2f.audio2face_folder(input_folder=test_folder, output_folder='/output', fps=60)

# testing clients


my_audio = AudioFile().from_file(test_audio_0)
audio_stream = my_audio.to_stream()

files, success = a2f.stream_audio(audio_stream, samplerate=audio_stream.sample_rate, export_blend_shape_interval=10)
a =1