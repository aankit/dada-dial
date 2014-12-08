from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys

params = {
	'file' : sys.argv[1],
	'min_silence_len': sys.argv[2],
	'silence_thresh': sys.argv[3]
}

sound = AudioSegment.from_wav(params['file'])
chunks = split_on_silence(sound, 
    # must be silent for at least half a second
    min_silence_len=params['min_silence_len'],

    # consider it silent if quieter than -16 dBFS
    silence_thresh=['silence_thresh']
)

for i, chunk in enumerate(chunks):
    chunk.export("./cutups/chunk{0}.wav".format(i), format="wav")