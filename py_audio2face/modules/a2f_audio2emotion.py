from ..audio2face import Audio2Face

DEFAULT_A2E_INSTANCE = "/World/audio2face/CoreFullface"


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
default_settings = {
        "a2f_instance": DEFAULT_A2E_INSTANCE,
        "a2e_window_size": 1.4,
        "a2e_stride": 1,
        "a2e_emotion_strength": 0.5,
        "a2e_smoothing_exp": 0.0,
        "a2e_max_emotions": 5,
        "a2e_contrast": 1.0,
    }


# Implement of A2F/A2E/SetSettings
def a2e_set_settings(a2f: Audio2Face, settings: dict):
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
    if settings is None:
        settings = default_settings
    else:
        # Update only the keys that are provided, keep others as default
        for key, value in default_settings.items():
            settings.setdefault(key, value)


    return a2f.post("A2F/A2E/SetSettings", payload=settings)

# Implement of A2F/A2E/EnableAutoGenerateOnTrackChange
def set_auto_emotion(a2f: Audio2Face, enable:bool=True):
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

    return a2f.post("A2F/A2E/EnableAutoGenerateOnTrackChange", payload=payload)


# Implement of A2F/A2E/SetEmotion
def set_emotions(a2f: Audio2Face, emotions_strength: dict):
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

    return a2f.post("A2F/A2E/SetEmotion", payload=payload)


# Implement of A2F/A2E/GenerateKeys
def generate_emotion_keys(a2f: Audio2Face, settings: dict=None):
    """
    Sets the settings for the audio2emotion generation
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

    # Apply default settings if no specific settings provided
    if settings is None:
        settings = default_settings
    else:
        # Update only the keys that are provided, keep others as default
        for key, value in default_settings.items():
            settings.setdefault(key, value)

    return a2f.post("A2F/A2E/GenerateKeys",payload=settings)


# Implement of A2F/A2E/GetEmotionNames
def get_emotion_names(a2f: Audio2Face):
    """
    List the available emotion names
    """
    return a2f.make_request("A2F/A2E/GetEmotionNames")


# Implement of A2F/A2E/GetEmotion
def get_emotion(a2f: Audio2Face, frame: int = 0):
    """
    List the emotion weights at a given frame. If a frame is not specified the emotions at current frame are returned
    returns a list or a dictionary {"emotion":weight}
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
    
    return a2f.post("A2F/A2E/GetEmotion", payload=payload)

