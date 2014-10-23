import wave, sys

handle = wave.open(sys.argv[1], 'r')

# for i in range(handle.getnframes()):
frame = handle.readframes(10000)
# print frame
zero = True
print ord(frame[10000])


    # if zero:
      # print 'Silence found at frame {0}'.format(handle.tell())