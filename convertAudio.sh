for file in ./wav/*.wav
do
	echo $file
	#output=`expr match "$file" './wav/'`
	i=`expr "$file" : './wav/'`
	output="./mono/"${file:$i}
	echo $output
	sox $file -c 1 -r 8000 $output
	#we also want to cutup the file here too!
	sox ./mono/The-Dial-A-Poem-Poets_04_waldman.wav ./cutups/${file:$i}.wav silence 1 0.2 1% 1 0.1 1% : newfile : restart
done

