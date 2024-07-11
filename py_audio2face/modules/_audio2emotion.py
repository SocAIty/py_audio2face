from __future__ import annotations  # avoid circular import with import py_audio2face 
import py_audio2face.audio2face as a2f

from py_audio2face.settings import DEFAULT_A2E_INSTANCE

# Default generate settings
"""
The settings for the audio2emotion generation
Available settings:
    "a2f_instance": "/World/audio2face/CoreFullface",                   * Necessary, default to be /World/audio2face/CoreFullface
    "a2e_window_size": 1.4,                 Emotion Detection Range     Sets the size, in seconds, of an audio chunk used to predict a single emotion_auto_detect per keyframe.
    "a2e_stride": 1,                        Keyframe Interval           Sets the number of seconds between adjacent automated keyframes.
    "a2e_emotion_strength": 0.5,            Emotion Strength            Sets the strength of the generated emotions relative to the neutral emotion_auto_detect.
    "a2e_smoothing_kernel_radius": 0,       * WTF?!
    "a2e_smoothing_exp": 0,                 Smoothing(Exp)              Sets the number of neighboring keyframes used for emotion_auto_detect smoothing.
    "a2e_max_emotions": 5,                  Max Emotions                Sets a hard limit on the quantity of emotions that Audio2Emotion will engage at one time. (Emotions are prioritized by their strength.)
    "a2e_contrast": 1,                      Emotion Contrast            Controls the emotion_auto_detect spread - pushing higher and lower values.
    "preferred_emotion": [                  Preferred Emotion           Sets a single emotion_auto_detect as the base emotion_auto_detect for the character animation. The preferred emotion_auto_detect is taken from the current settings in the Emotion widget and is mixed with generated emotions throughout the animation. (is not set indicates whether or not you’ve set a preferred emotion_auto_detect.)
    0
    ],
    "a2e_preferred_emotion_strength": 0,    Strength                    Sets the strength of the preferred emotion_auto_detect. This determines how present this animation will be in the final animation.
    "a2e_streaming_smoothing": 0,           * Only for clients
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
            "preferred_emotion": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "a2e_preferred_emotion_strength": 0.5
        }

    def a2e_set_settings(
            self: a2f.Audio2Face,
            a2e_emotion_strength: float = 0.5,
            a2e_smoothing_exp: int = 0,
            a2e_max_emotions: int = 5,
            a2e_contrast: float = 1.0,
            preferred_emotion: list = None,
            a2e_preferred_emotion_strength: float = 0.5,
            **kwargs
    ):
        """
        Sets the settings for the audio2emotion generation
        It's an implement of A2F/A2E/GenerateKeys
        :param a2e_emotion_strength: Emotion Strength
        :param a2e_smoothing_exp: Smoothing(Exp)
        :param a2e_max_emotions: Max Emotions
        :param a2e_contrast: Emotion Contrast
        :param preferred_emotion: List of emotion_auto_detect strengths, which is the default emotion_auto_detect
        :param a2e_preferred_emotion_strength: Strength
        """
        # quick hack to prevent the scene to be loaded twice when setting emotions
        # also prevents to change values if streaming is used.
        # ToDo: find a better solution
        if self.loaded_scene is None:
            self.init_a2f()

        settings = {}
        def add_to_dict(key, value):
            if value is not None:
                settings[key] = value

        add_to_dict("a2e_emotion_strength", a2e_emotion_strength)
        add_to_dict("a2e_smoothing_exp", a2e_smoothing_exp)
        add_to_dict("a2e_max_emotions", a2e_max_emotions)
        add_to_dict("a2e_contrast", a2e_contrast)
        add_to_dict("preferred_emotion", preferred_emotion)
        add_to_dict("a2e_preferred_emotion_strength", a2e_preferred_emotion_strength)

        self.a2e_settings.update(settings)
        return self.post("A2F/A2E/SetSettings", payload=settings)

    def a2e_set_settings_from_dict(self: a2f.Audio2Face, settings: dict):
        """
        Sets the settings for the audio2emotion generation
        """
        # Apply default settings if no specific settings provided
        # Update only the keys that are provided, keep others as default
        self.a2e_set_settings(**settings)


    # Implement of A2F/A2E/EnableAutoGenerateOnTrackChange
    def set_enable_auto_generate_on_track_change(self: a2f.Audio2Face, enable: bool = True):
        """
        Enable or disable the automatic generation of A2E keys on track change.
        Available settings:
            "a2f_instance": "string",
            "enable": true
        """

        payload = {
            "a2f_instance": DEFAULT_A2E_INSTANCE,
            "enable": enable
        }
        return self.post("A2F/A2E/EnableAutoGenerateOnTrackChange", payload=payload)

    # Implement of A2F/A2E/SetEmotion
    def set_emotion(
            self: a2f.Audio2Face,
            amazement: float | None = 0.0,
            anger: float | None = 0.0,
            cheekiness: float | None = 0.0,
            disgust: float | None = 0.0,
            fear: float | None = 0.0,
            grief: float | None = 0.0,
            joy: float | None = 0.0,
            outofbreath: float | None = 0.0,
            pain: float | None = 0.0,
            sadness: float | None = 0.0,
            update_settings: bool = True
    ):
        """
        Sets the emotions on a global level for the whole track.
        Values are between 0..1.
        If a value is None it will be set to 0. Use get_emotion_names() to get the available emotions
        """
        # quick hack to prevent the scene to be loaded twice when setting emotions
        # also prevents to change values if streaming is used.
        # ToDo: find a better solution
        if self.loaded_scene is None:
            self.init_a2f()

        emotion_strength = {}
        def add_to_dict(emotion, value):
            emotion_strength[emotion] = value if value is not None else 0.0

        add_to_dict("Amazement", amazement)
        add_to_dict("Anger", anger)
        add_to_dict("Cheekiness", cheekiness)
        add_to_dict("Disgust", disgust)
        add_to_dict("Fear", fear)
        add_to_dict("Grief", grief)
        add_to_dict("Joy", joy)
        add_to_dict("Outofbreath", outofbreath)
        add_to_dict("Pain", pain)
        add_to_dict("Sadness", sadness)

        if update_settings:
            self.a2e_set_settings(preferred_emotion=list(emotion_strength.values()))

        payload = {
            "a2f_instance": DEFAULT_A2E_INSTANCE,
            "emotion": list(emotion_strength.values())
        }
        response = self.post("A2F/A2E/SetEmotion", payload=payload)
        return response

    def generate_emotion_keys(self: a2f.Audio2Face):
        """
        Detects emotions in the audio and generates the keyframes.
        To change the default settings, use the a2e_set_settings method.
        """
        resp = self.post("A2F/A2E/GenerateKeys", payload=self.a2e_settings)
        return resp

    def get_emotion_names(self: a2f.Audio2Face):
        """
        List the available emotion_auto_detect names
        It's an implement of A2F/A2E/GetEmotionNames
        """
        return self.make_request("A2F/A2E/GetEmotionNames")

    def get_emotion(self: a2f.Audio2Face, frame: int = 0):
        """
        List the emotion_auto_detect weights at a given frame. If a frame is not specified the emotions at current frame are returned
        returns a list or a dictionary {"emotion_auto_detect":weight}
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
