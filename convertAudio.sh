for file in ./wav/*.wav
do
	echo $file
	#output=`expr match "$file" './wav/'`
	i=`expr "$file" : './wav/'`
	output="./mono/"${file:$i}
	echo $output
	sox $file -c 1 -r 8000 $output
done

