# stat679work

# Instructions

#### This folder contains the dataset of the homework and thw scripts that I wrote for it.

#### In the hw1/ folder, it contains:
* hw1-snaqTimeTests/ : This is a folder for the datasets we used for this homework.
  + log/ : it contains the datasets which have suffix of ".log"
  + out/ : it contains the datasets which have suffix of ".out"
* scripts/ : It contains the scripts written for this homework.
  + normalizeFileNames.sh: This script modifies the names of files in log/ and out/.
  + summatizeSNaQres.sh: This script greps some parameters in the datasets, such as: the name of each analysis--"analysis"; the total of running time--"cpu time"; hmax.
  + New.sh: It greps more parameters and writes them down in the "summary.csv". It optimize the methods used in "summatizeSNaQres.sh" in these places:
    + combine several loops into one "for" loop
    + use more regular expressions than the previous script
    + try to use "if-else" logical expressions in the script
    + use "grep", "cut", "sed" and other commands to extract the data that we need.
* results/: It contains the results of the shell scripts:
  + "combine.csv" : This is the result for exercise 2. It is a csv file contains the analysis name, cpu time and hmax.
  + "summary.csv" : This is the result for exercise 3. It contains more parameters than "combine.csv"

#### Execution instructions:
To run the codes, we may follow the commands below:

Suppose we are at the directory of hw1/

Modify the filenames:
```shell
bash scripts/normalizeFileNames.sh
```

Extract data as required in exercise2:
```shell
bash scripts/summatizeSNaQres.sh
```

Find more data as required in exercise 3:
```shell
bash scripts/New.sh
```

#### Quick view of the results:
** combine.csv **

|analysis       |hmax|CPU time   |
|---------------|----|-----------|
|bT1            |0   |103354.7604|
|net1_snaq      |1   |11648.98431|
|newtry1        |1   |88579.30634|
|timetest01_snaq|1   |16688.0151 |
|timetest02_snaq|1   |37137.96355|
|timetest03_snaq|1   |12630.99445|
|timetest04_snaq|1   |21942.3465 |
|timetest05_snaq|1   |23949.37503|
|timetest06_snaq|1   |39287.7962 |
|timetest07_snaq|1   |29822.1476 |
|timetest08_snaq|1   |51589.34232|
|timetest09_snaq|1   |34831.46593|
|timetest10_snaq|1   |29394.46349|
|timetest11_snaq|1   |67926.50206|
|timetest12_snaq|1   |18935.63057|
|timetest13_snaq|1   |31456.99368|

** Show the codes generating this table: **
##### summatizeSNaQres.sh
```shell
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
paste -d","  111.csv 222.csv 333.csv >combine.csv
```
** summary.csv **

|analysis       |hmax|cpu time          |Nruns|Nfail|fabs   |frel   |xabs   |xrel  |seed  |under 3460|under 3450|under 3440|
|---------------|-----|------------------|------|------|-------|-------|-------|------|------|-----------|-----------|-----------|
|bT1            |0    |103354.760381735|10    |100   |1.0e-6|1.0e-5|0.0001|0.001|66077|0          |0          |0          |
|net1_snaq      |1    |11648.984309726   |10    |100   |1.0e-6|1.0e-5|0.0001|0.001|3322  |1          |1          |0          |
|newtry1        |1    |88579.306341032   |10    |100   |1.0e-6|1.0e-5|0.0001|0.001|36252|4          |4          |2          |
|timetest01_snaq|1    |16688.01510346    |10    |10    |1.0e-6|1.0e-5|0.0001|0.001|30312|2          |1          |0          |
|timetest02_snaq|1    |37137.96354747    |10    |25    |1.0e-6|1.0e-5|0.0001|0.001|28669|4          |1          |0          |
|timetest03_snaq|1    |12630.994448551   |10    |100   |0.1    |0.1    |0.0001|0.001|66086|0          |0          |0          |
|timetest04_snaq|1    |21942.346502542   |10    |100   |0.01   |0.01   |0.0001|0.001|62366|0          |0          |0          |
|timetest05_snaq|1    |23949.375026384   |10    |100   |0.005  |0.005  |0.0001|0.001|3888  |2          |1          |0          |
|timetest06_snaq|1    |39287.796202476   |10    |25    |1.0e-6|1.0e-5|0.0001|0.001|14351|4          |3          |3          |
|timetest07_snaq|1    |29822.147601027   |10    |100   |0.005  |0.005  |0.0001|0.001|14351|5          |5          |0          |
|timetest08_snaq|1    |51589.342317181   |10    |100   |1.0e-6|1.0e-5|0.001  |0.1   |15989|3          |2          |1          |
|timetest09_snaq|1    |34831.465925074   |10    |50    |0.0001|1.0e-5|0.0001|0.001|45123|1          |0          |0          |
|timetest10_snaq|1    |29394.463493788   |10    |50    |1.0e-5|0.0001|0.0001|0.001|37792|0          |0          |0          |
|timetest11_snaq|1    |67926.502059791   |10    |50    |5.0e-6|1.0e-5|0.0001|0.001|25765|2          |2          |0          |
|timetest12_snaq|1    |18935.630572383   |10    |50    |1.0e-6|1.0e-5|0.01   |0.1   |39416|4          |0          |0          |
|timetest13_snaq|1    |31456.993676184   |10    |100   |1.0e-5|1.0e-5|0.01   |0.1   |38112|3          |1          |1          |


** Show the codes generating this table: **
##### New.sh
```shell
echo "analysis", "hmax", "cpu time", "Nruns", "Nfail", "fabs","frel", "xabs", "xrel", "seed", "under 3460", "under 3450", "under 3440" > results/summary.csv
#Print the column names of the file
for file in hw1-snaqTimeTests/log/*.log
do
  analysis=$(basename $file .log) # To extract the basename of the files.
  a="$(grep "hmax = " $file)"
  hmax="$(echo $a | sed 's/hmax = / /g' | sed 's/,/ /g')" # To find the values of hmax variable.
  #As Cpu and Nruns are in *.out files, I need to "cat" the contents of *.out files and then I can grep the data I need.
  cpu="$(cat hw1-snaqTimeTests/out/$analysis.out | grep "Elapsed time: "  | sed 's/Elapsed time: / /g' | sed 's/seconds.*/ /g')"
  Nruns="$(cat hw1-snaqTimeTests/out/$analysis.out | grep "seconds in "  | sed 's/.*in / /g' | sed 's/successful.*/ /g')"
  g="$(grep "max number of failed proposals = " $file)"
  #Find the max number of failed proposals: grep it first and use 'sed' to cut the useless parts.
  Nfail="$(echo $g | sed 's/max number of failed proposals = / /g' | sed 's/,.*/ /g')"
  #Find the tuning parameter called "ftolAbs" in the log file: grep 'ftolAbs' first and use 'cut' and 'sed' to cut down the useless parts.
  fabs="$(grep "ftolAbs" $file | cut -d "," -f 2 | sed 's/.*=//g')"
  #Find the parameter called "ftolRel" in the log file:
  frel="$(grep "ftolAbs" $file| cut -d "," -f 1 | sed 's/.*=//g')"
  # Find "xtolAbs", "xtolRel", "seed" parameter in the log file:
  xabs="$(grep "xtolAbs" $file| cut -d "," -f 1 | sed 's/.*=//g')"
  xrel="$(grep "xtolAbs" $file| cut -d "," -f 2 | sed 's/.*=//g' | sed 's/\.//2')"
  seed="$(grep -w  "seed: .*for run 1" $file | cut -d " " -f 2)"
  j="$(grep -w  "loglik of best" $file|cut -d " " -f 10 )"
  # Count the number of funs whose -loglik <3460, <3450, and <3440.
  count1=0
  count2=0
  count3=0
  for x in $j
  do
    if [ $(bc <<< "$x <= 3460") -eq 1 ]
    then
      count1=$((count1+1))
    fi
    if [ $(bc <<< "$x <= 3450") -eq 1 ]
    then
      count2=$((count2+1))
    fi
    if [ $(bc <<< "$x <= 3440") -eq 1 ]
    then
      count3=$((count3+1))
    fi
  done
echo $analysis, $hmax, $cpu, $Nruns, $Nfail, $fabs, $frel, $xabs, $xrel, $seed, $count1, $count2, $count3 >> results/summary.csv
done
```
