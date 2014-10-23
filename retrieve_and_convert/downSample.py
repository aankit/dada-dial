import audioop , struct , os
   
wavdir44 = './mono/'
wavdir8 = './8kmono/'
 
def downsample(wave):
    newrate = audioop.ratecv(wave[ 44:] , 2 , 1 , 44100 , 8000 , None , 1 , 1 )[ 0 ]     #Audiodaten start from 44th position Up to 44 header
    print newrate
    newlength = len ( newrate )
    print newlength
    NEWHEADER = wave[:24]+ struct.pack('l',8000) + wave[28:40] + struct.pack( 'l' , newlength )   #Samplerate 24-28, size 40-44 audio data
    result = NEWHEADER + newrate
    return result
 
allwavs = os.listdir(wavdir44)
print allwavs
for name in allwavs:
    print name[-4:]
    if name[-3:] == 'wav':
        print 'stuff'
        sound1 = open(wavdir44 + name, "rb" ).read()
        sound2 = downsample(sound1)
        open(wavdir8+name, "wb").write(sound2)
        print wavdir8 + name     #Kontrollausgabe