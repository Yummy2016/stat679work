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
