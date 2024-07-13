## py_audio2face version 0.1.3
import py_audio2face as pya2f
from media_toolkit import AudioFile

test_audio_0 = "test_files/test_audio_0.wav"
test_audio_1 = "test_files/test_audio_1.wav"
test_audio_2 = "test_files/test_audio_2.wav"

a2f = pya2f.Audio2Face()

def test_file_methods():
    # create animations without detection emotions
    a2f.set_emotion(anger=0.9, disgust=0.5, fear=0.1, sadness=0.2, update_settings=True)
    # create animations without detection emotions, but by keeping the set emotions
    preset_emotion_animation = a2f.audio2face_single(
        audio_file_path=test_audio_0,
        output_path='emotion_less.usd',
        fps=60,
        emotion_auto_detect=False
    )
    # Automatically detect emotions from the audio. The set_emotions will be used as base emotion.
    autodetected_emotions = a2f.audio2face_single(
        audio_file_path=test_audio_2,
        output_path='emotion_less.usd',
        fps=60,
        emotion_auto_detect=True
    )

def test_streaming():
    # Load audio file and get an audio stream generator
    my_audio = AudioFile().from_file(test_audio_2)
    audio_stream = my_audio.to_stream()
    # Stream the audio to the Audio2Face StreamingPlayer
    a2f.stream_audio(audio_stream=audio_stream, samplerate=audio_stream.sample_rate)


test_file_methods()
test_streaming()
