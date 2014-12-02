for file in ./wav/*.wav
do
	echo $file
	#output=`expr match "$file" './wav/'`
	i=`expr "$file" : './wav/'`
	output="./mono/"${file:$i}
	echo $output
	sox $file -c 1 -r 8000 $output
	#we also want to cutup the file here too!
	cutup_stub="./cutups/"${file:$i}
	sox $output $cutup_stub silence 1 0.3 1% 1 0.15 1% : newfile : restart
done

