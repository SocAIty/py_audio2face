import os
import py_audio2face as pya2f
from py_audio2face.settings import ASSETS_DIR
from media_toolkit import AudioFile

test_audio_0 = os.path.join(ASSETS_DIR, "test_audio_0.wav")
test_audio_1 = os.path.join(ASSETS_DIR, "test_audio_1.wav")
test_audio_2 = os.path.join(ASSETS_DIR, "test_audio_2.wav")

a2f = pya2f.Audio2Face()

def test_file_methods():
    # testing the single method
    without_emotion = a2f.audio2face_single(test_audio_0, 'emotion_less.usd', fps=60, emotion_auto_detect=False)
    # Testing with expressive emotions. Applies a preferred emotion even in emotion_auto_detect with update_settings=True
    a2f.set_emotion(anger=0.9, disgust=0.5, fear=0.1, sadness=0.2, update_settings=True)
    with_emotion = a2f.audio2face_single(test_audio_1,'emotion_full.usd', fps=60, emotion_auto_detect=True)
    # testing the folder method
    all_converted = a2f.audio2face_folder(input_folder=ASSETS_DIR, output_folder='/output', fps=60)

def test_streaming():
    my_audio = AudioFile().from_file(test_audio_0)
    audio_stream = my_audio.to_stream()
    a2f.set_emotion(anger=0.9, disgust=0.5, fear=0.1, sadness=0.2, update_settings=True)
    success = a2f.stream_audio(audio_stream=audio_stream, samplerate=audio_stream.sample_rate)


# test_file_methods()
test_streaming()
