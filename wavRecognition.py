import speech_recognition as sr
r = sr.Recognizer()
with sr.WavFile("./mono/The-Dial-A-Poem-Poets_02_di_prima.wav") as source:              # use "test.wav" as the audio source
    audio = r.record(source)                        # extract audio data from the file

try:
    list = r.recognize(audio,True)                  # generate a list of possible transcriptions
    print("Possible transcriptions:")
    for prediction in list:
        print(" " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")
except LookupError:                                 # speech is unintelligible
    print("Could not understand audio")