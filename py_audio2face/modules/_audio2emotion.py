from __future__ import annotations  # avoid circular import with import py_audio2face 
import py_audio2face.audio2face as a2f

from settings import DEFAULT_A2E_INSTANCE

# Default generate settings
"""
The settings for the audio2emotion generation
Available settings:
    "a2f_instance": "/World/audio2face/CoreFullface",                   * Necessary, default to be /World/audio2face/CoreFullface
    "a2e_window_size": 1.4,                 Emotion Detection Range     Sets the size, in seconds, of an audio chunk used to predict a single emotion per keyframe.
    "a2e_stride": 1,                        Keyframe Interval           Sets the number of seconds between adjacent automated keyframes.
    "a2e_emotion_strength": 0.5,            Emotion Strength            Sets the strength of the generated emotions relative to the neutral emotion.
    "a2e_smoothing_kernel_radius": 0,       * WTF?!
    "a2e_smoothing_exp": 0,                 Smoothing(Exp)              Sets the number of neighboring keyframes used for emotion smoothing.
    "a2e_max_emotions": 5,                  Max Emotions                Sets a hard limit on the quantity of emotions that Audio2Emotion will engage at one time. (Emotions are prioritized by their strength.)
    "a2e_contrast": 1,                      Emotion Contrast            Controls the emotion spread - pushing higher and lower values.
    "preferred_emotion": [                  Preferred Emotion           Sets a single emotion as the base emotion for the character animation. The preferred emotion is taken from the current settings in the Emotion widget and is mixed with generated emotions throughout the animation. (is not set indicates whether or not you’ve set a preferred emotion.)
    0
    ],
    "a2e_preferred_emotion_strength": 0,    Strength                    Sets the strength of the preferred emotion. This determines how present this animation will be in the final animation.
    "a2e_streaming_smoothing": 0,           * Only for streaming
    "a2e_streaming_update_period": 0,
    "a2e_streaming_transition_time": 0
"""



class _A2F_Audio2Emotion:
    # Implement of A2F/A2E/SetSettings

    @staticmethod
    def get_default_a2e_settings():
        return {
            "a2f_instance": DEFAULT_A2E_INSTANCE,
            "a2e_window_size": 1.4,
            "a2e_stride": 1,
            "a2e_emotion_strength": 0.5,
            "a2e_smoothing_exp": 0.0,
            "a2e_max_emotions": 5,
            "a2e_contrast": 1.0,
        }

    def a2e_set_settings_from_dict(self: a2f.Audio2Face, settings: dict):
        """
        Sets the settings for the audio2emotion generation
        Available settings:
            "a2f_instance": "string",
            "a2e_window_size": 0,
            "a2e_stride": 0,
            "a2e_emotion_strength": 0,
            "a2e_smoothing_kernel_radius": 0,
            "a2e_smoothing_exp": 0,
            "a2e_max_emotions": 0,
            "a2e_contrast": 0,
            "preferred_emotion": [
            0
            ],
            "a2e_preferred_emotion_strength": 0,
            "a2e_streaming_smoothing": 0,
            "a2e_streaming_update_period": 0,
            "a2e_streaming_transition_time": 0
        """
        # Apply default settings if no specific settings provided
        # Update only the keys that are provided, keep others as default
        self.a2e_settings.update(settings)

        return self.post("A2F/A2E/SetSettings", payload=settings)

    def a2e_set_settings(
            self: a2f.Audio2Face,
            a2f_instance: str = None,
            a2e_window_size: float = None,
            a2e_stride: int = None,
            a2e_emotion_strength: int = None,
            a2e_smoothing_kernel_radius: int = None,
            a2e_smoothing_exp: int = None,
            a2e_max_emotions: int = None,
            a2e_contrast: int = None,
            preferred_emotion: list = None,
            a2e_preferred_emotion_strength: int = None,
            a2e_streaming_smoothing: int = None,
            a2e_streaming_update_period: int = None,
            a2e_streaming_transition_time: int = None):
        """
        Change an a2e setting. If a value is None it won't be changed.
        """
        kwargs = locals()
        del kwargs["self"]

        settings = {k: v for k, v in kwargs.items() if v is not None}
        self.a2e_set_settings_from_dict(settings)


    # Implement of A2F/A2E/EnableAutoGenerateOnTrackChange
    def set_auto_emotion(self: a2f.Audio2Face, enable: bool = True):
        """
        Enable or disable the automatic generation of A2E keys on track change.
        Available settings:
            "a2f_instance": "string",
            "enable": true
        """

        payload = {
            "a2f_instance": DEFAULT_A2E_INSTANCE,
            "emotions": enable
        }

        return self.post("A2F/A2E/EnableAutoGenerateOnTrackChange", payload=payload)

    # Implement of A2F/A2E/SetEmotion
    def set_emotions(self: a2f.Audio2Face, emotions_strength: dict):
        """
        Sets the emotions on a global level for the whole track
        emotions_strength: dict with emotion names and strength between 0..1 like {"Amazement": 0.5, "Anger": 0.2, ...}
        available emotions: "Amazement", "Anger", "Cheekiness", "Disgust",
            "Fear", "Grief", "Joy", "Outofbreath", "Pain", "Sadness"
            check also get_emotion_names() to get the available emotions
        """

        payload = {
            "a2f_instance": DEFAULT_A2E_INSTANCE,
            "emotions": emotions_strength
        }

        return self.post("A2F/A2E/SetEmotion", payload=payload)

    def generate_emotion_keys(self: a2f.Audio2Face, settings: dict = None):
        """
        Sets the settings for the audio2emotion generation
        It's an implement of A2F/A2E/GenerateKeys
        Available settings:
            "a2f_instance": "/World/audio2face/CoreFullface",                   * Necessary, default to be /World/audio2face/CoreFullface
            "a2e_window_size": 1.4,                 Emotion Detection Range     Sets the size, in seconds, of an audio chunk used to predict a single emotion per keyframe.
            "a2e_stride": 1,                        Keyframe Interval           Sets the number of seconds between adjacent automated keyframes.
            "a2e_emotion_strength": 0.5,            Emotion Strength            Sets the strength of the generated emotions relative to the neutral emotion.
            "a2e_smoothing_kernel_radius": 0,       * WTF?!
            "a2e_smoothing_exp": 0,                 Smoothing(Exp)              Sets the number of neighboring keyframes used for emotion smoothing.
            "a2e_max_emotions": 5,                  Max Emotions                Sets a hard limit on the quantity of emotions that Audio2Emotion will engage at one time. (Emotions are prioritized by their strength.)
            "a2e_contrast": 1,                      Emotion Contrast            Controls the emotion spread - pushing higher and lower values.
            "preferred_emotion": [                  Preferred Emotion           Sets a single emotion as the base emotion for the character animation. The preferred emotion is taken from the current settings in the Emotion widget and is mixed with generated emotions throughout the animation. (is not set indicates whether or not you’ve set a preferred emotion.)
            0
            ],
            "a2e_preferred_emotion_strength": 0,    Strength                    Sets the strength of the preferred emotion. This determines how present this animation will be in the final animation.
            "a2e_streaming_smoothing": 0,           * Only for streaming
            "a2e_streaming_update_period": 0,
            "a2e_streaming_transition_time": 0
        """

        self.a2e_set_settings_from_dict(self.a2e_settings)
        return self.post("A2F/A2E/GenerateKeys", payload=settings)

    def get_emotion_names(self: a2f.Audio2Face):
        """
        List the available emotion names
        It's an implement of A2F/A2E/GetEmotionNames
        """
        return self.make_request("A2F/A2E/GetEmotionNames")

    def get_emotion(self: a2f.Audio2Face, frame: int = 0):
        """
        List the emotion weights at a given frame. If a frame is not specified the emotions at current frame are returned
        returns a list or a dictionary {"emotion":weight}
        It's an implement of A2F/A2E/GetEmotion
        Available settings:
            "a2f_instance": "/World/audio2face/CoreFullface",
            "as_vector": true,
            "frame": 0,
            "as_timestamp": false
        """

        payload = {
            "a2f_instance": DEFAULT_A2E_INSTANCE,
            "as_vector": True,
            "frame": frame,
            "as_timestamp": False
        }

        return self.post("A2F/A2E/GetEmotion", payload=payload)
