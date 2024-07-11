import os
import py_audio2face as pya2f
from py_audio2face.settings import ASSETS_DIR

test_audio_0 = os.path.join(ASSETS_DIR, "test_audio_0.wav")
test_audio_1 = os.path.join(ASSETS_DIR, "test_audio_1.wav")

a2f = pya2f.Audio2Face()

without_emotion = a2f.audio2face_single(test_audio_0, 'myout1.usd', fps=60, emotion=False)
#with_emotion = a2f.audio2face_single(test_audio_0,'myoutemotion.usd', fps=60, emotion=True)

# testing the folder method
#test_folder = "assets/"
#all_converted = a2f.audio2face_folder(test_folder, '/output', fps=60)

# testing clients
