#To modify the filenames in log folder.
for file in hw1-snaqTimeTests/log/*st[1,2,3,4,5,6,7,8,9]_snaq.log
do
    mv "${file}" "${file/timetest/timetest0}"
done

#To modify the filenames in 'out' folder.
for file in hw1-snaqTimeTests/out/*st[1,2,3,4,5,6,7,8,9]_snaq.out
do
    mv "${file}" "${file/timetest/timetest0}"
done
