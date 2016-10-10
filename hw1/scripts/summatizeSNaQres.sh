#To get the filenames of each file, we need to cut the directory and the suffix.
echo "analysis" > 111.csv
for file in hw1-snaqTimeTests/log/*.log
do
  t=${file/hw1-snaqTimeTests\/log\//}
  analysis="${t%.*}"
  echo $analysis >> 111.csv
done

# Get the data of hmax in the 'log' folder.
echo "hmax" > 222.csv
for file in hw1-snaqTimeTests/log/*.log
do
  a="$(grep "hmax = " $file)"
  b="$(echo ${a/hmax = / })"
  echo ${b/,/} >> 222.csv
done

#Get the data of CPU time in the 'out' folder.
echo "CPU time" > 333.csv
for filename in hw1-snaqTimeTests/out/*.out
do
  c="$(grep "Elapsed time: " $filename)"
  d="$(echo ${c/Elapsed time: / })"
  echo ${d/seconds*/ } >> 333.csv
done

#Combine the 3 columns into one csv file.
paste -d","  111.csv 222.csv 333.csv > results/combine.csv
