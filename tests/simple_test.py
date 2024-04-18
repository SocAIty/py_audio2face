import py_audio2face as pya2f

a2f = pya2f.Audio2Face()

#without_emotion = a2f.audio2face_single('full_interview.mp3_0.wav', 'myout1.usd', fps=60)
#with_emotion = a2f.audio2face_single('full_interview.mp3_0.wav',
#                                     'myoutemotion.usd', fps=60, emotion=True)

# testing the folder method
a2f.audio2face_folder('', '/output', fps=60)
