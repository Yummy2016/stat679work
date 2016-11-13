homework 2: merging data files
==============================

background (may be skipped)
----------

These data give an example of a common task, where data are collected
from different sources and at different rates, but need to be combined
for downstream analyses.
On the same roof, two different solar collector systems are installed,
one to heat water and the other to provide electricity.
Data are collected every month from each system:

- hot water: hourly data on the hot water *temperature*
- electricity: daily data on the *energy* produced by a photovoltaic system.

Merging data files from these 2 data loggers is necessary for downstream
analyses, such as correlation between the 2 systems. Doing any downstream
analysis is *not* the goal of the exercise.

The goal of the exercise is to produce a script that could be used monthly
to merge the 2 data files of the month, where the energy value from each day
is matched to the temperature value at the nearest time, with no need for any
manual copy-paste operation. The script is meant to be used repeatedly,
so it should accept 2 file names as arguments:
the names of the temperature file and of the energy file.


data files
----------

This directory contains one file with water [temperature](waterTemperature.csv)
data and another file with [energy](energy.csv) data
(received by email on 2016-08-17).

exercise
--------

Write a Python script that takes 2 file names as arguments, and creates
an output with the merged data, in csv format (comma-separated variables).

- The output should contain all of the information in the temperature file.
- The energy values in Wh should be divided by 1000 and written in an additional column.
- The energy value for a particular time should be matched with
  (placed on the same row as) the temperature data logged just before that time.
  For instance, the energy value at 2016-07-30 00:00:00 -0500 (9468 Wh / 1000)
  should be matched with the water temperature at
  07/29/16 11:26:34 PM (row numbered 14 in the temperature file).
- The temperature file name should be the first argument; the energy file name should be the second.

Extra desired features:

- Check for potential errors, such as data files with
  non-overlapping dates, or with an unexpected format, etc.
- Add a third argument for the script, for the output file name.
  If missing, the script should return the output to the STDOUT stream.
- Be should be safe for user: not overwriting existing files
  unintentionally.
- Have an option to append to (or to overwrite) the output file.

The last point is to let the user run the script on multiple pairs of files,
such as from multiple months, and always append the merged data onto the
same output file, which could then contain data from a whole year.

The **learning goal** (for yourself, not the script user) is to learn Python,
get more experience with git, think about algorithm strategy,
and get good habits of computing practices like project management,
code documentation, writing code for humans, planning for errors, etc.  
Therefore, do *not* use pre-defined modules for handling data arrays or
merging data files. Use this exercise to practice low-level python functions.

suggested algorithm
-------------------

This is just a suggestion of steps that your script could take.
There are always many ways to get the job done.
These steps below do not require pre-defined modules
(except to handle dates), with the intention to provide a richer
coding experience.

1. read the energy file: store data in 2 arrays: one with the dates,
  one with the energy values. Assume (but check) that all dates are at
  00:00:00 (midnight, morning of the given day, Wisconsin time).
  check that dates are ordered (row `n` has an earlier date than row `n+1`)

2. set `n_energy=1` and set a variable `currentEnergyDay` to day `1`
  (midnight morning), as read in the first row of the energy file.
  In general, we mean `currentEnergyDay` to be the day on line `n_energy`
  of the energy file, and the energy value on that day is the next
  energy value to be added to the temperature information.

3. read the next line in the temperature file (read the first line, at first)

  - strip the end-of-line character from this line
  - get the day corresponding to this line of temperature data
  - if this day is greater than or equal to `currentEnergyDay`:
    * quit with an error if this day is not equal to `currentEnergyDay`
    * write the energy value number `n_energy` to the output
    * increment `n_energy` by one and
      update `currentEnergyDay`: make it the day number `n_energy` for the
      energy data
  - write a newline character to the output
  - write the line to the output (no end of line)
  - write a comma to the output
