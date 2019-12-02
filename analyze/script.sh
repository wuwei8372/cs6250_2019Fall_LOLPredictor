for parallelism in 2 4 8 16
do 
	for partitions in 100 200 400 500 800 1000 
	do
		time spark-submit \
			--conf spark.default.parallelism=$parallelism \
			--conf spark.sql.shuffle.partitions=$partitions \
			./analyze.py \
			1>output/log-$parallelism-$partitions 2>output/err-$parallelism-$partitions
	done
done 
