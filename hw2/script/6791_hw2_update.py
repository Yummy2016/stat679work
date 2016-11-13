import numpy
import time
import re
import datetime
import sys
import os.path

def main(**filenames):#'filesnames' is a dicitionary, which indexes are sorted by month
    for keys in filenames: #loop through the keys in the dictionary so that we can handle multiple pairs of files.
        x = len(filenames[keys])
        if x < 2 or x > 3: #if in one key, the list has less than 2 files or more than 3 files, it will break with an error.
            print('error with files')
            break
        elif x ==2: #if the third argument(output file) is missing, we will return the results to the STDOUT stream.
            first = filenames[keys][0] #first argument is the water temeprature file, for example.
            second = filenames[keys][1]#second argument is the energy file, for example.
            third = sys.stdout #third is missing. so we set it as stdout.
        else:
            first = filenames[keys][0]
            second = filenames[keys][1]
            third = filenames[keys][2]#third argument is the output filename.

        with open(second)as fh:
            """ open the energy file and manipulate it."""
            linelist = fh.readlines() #put the lines into a list-linelist.
            date = [] #to save the dates, we start with an empty list
            energy = [] # to save the nergy value.
            for line in linelist:
                a = re.search(r'^(\d+)',line) #find out the lines starting with digits(to exclude the header lines or the 'total' lines.)
                if a: # if true.
                    energy_pattern = re.compile('^(\d{4})-(\d{2})-(\d{2})\s(\d+):(\d+):(\d+)\s-(\d+)\,(\d+)') #check if the format matches well.
                    if energy_pattern.match(line):
                        pre_d = re.sub(r'\,(\d+)','', line)
                        d = re.sub(r'\s(\d+):(\d+):(\d+)\s-(\d+)',"",pre_d) #extract the dates in energy file.
                        e = re.sub(r'.*\,','',line)
                        e = int(e) #extract the energy value in the energy file and cast it as a string.
                        date.append(d.rstrip())
                        energy.append(e)
                    else:
                        print('energy file: format error!')
                        break
                else:
                    continue

            energy_date = []
            for time in date:
                """change the date format so that it can match with the dates in the water temeprature file."""
                new_date = datetime.datetime.strptime(time, '%Y-%m-%d').strftime('%m/%d/%y')
                energy_date.append(new_date)# new date list.


            for i in range(len(energy_date)-1):
                """  check if the energy dates are sorted"""
                if energy_date[i] > energy_date[i+1]: #if not, sort it.
                    energy_date.sort(key=lambda x: time.mktime(time.strptime(x,'%m/%d/%y')))
                else:
                    continue


            with open(first) as w :
                """ open the water temeprature file."""
                water_linelist = w.readlines()
                new_linelist = []
                water_date = []
                merge_list = []
                n_energy = 1
                currentEnergyDay = energy_date[n_energy-1]
                for line in water_linelist:
                    """find out all the lines which start with digits and save them in the new_linelist."""
                    b = re.search(r'^(\d+)',line)
                    if b:
                        new_linelist.append(line.rstrip())

                    else:
                        continue

                for item in new_linelist:
                    """ check if water.csv has an unexpected format"""
                    water_pattern = re.compile('^(\d+)\,(\d+)\/(\d+)\/(\d+)\s(\d+):(\d+):(\d+)\s(\w+)\,(\d+).(\d+)')
                    if water_pattern.match(item):
                        continue
                    else:
                        print('water temperature file: format error!')
                        break

                for l in new_linelist:
                    """ check if water.csv has non-overlapping date"""
                    pre_day = re.sub(r'^(\d+)\,','',l)
                    pre_day = re.sub(r'\,(\d+).(\d+)','',pre_day)
                    day = re.sub(r'\s(\d+):(\d+):(\d+)\s(\w+)',"",pre_day)#manipulate with the dates in the water* file: extract them and save in the water_date list.
                    day = day.rstrip() # cut the '\n' off.
                    water_date.append(day)

                for x in range(len(water_date)-1):
                    """ check if the dates are non-overlapping."""
                    if x == 0:
                        if water_date[0] == water_date[1]:
                            continue
                        else:
                            print('Error:non-overlapping dates')
                            break
                    else:
                        if water_date[x] == water_date[x-1] or water_date[x] == water_date[x+1]:
                            continue
                        else:
                            print('Error: non-overlapping dates')
                            break


                for i in range(len(new_linelist)-1):
                    """ match the energy value with the water temperature by dates. """
                    while n_energy <= len(energy):
                        line1 = new_linelist[i]
                        line2 = new_linelist[i+1] #read in the nextline with the pointer is still at the previous line.
                        pre_day2 = re.sub(r'^(\d+)\,','',line2)
                        pre_day2 = re.sub(r'\,(\d+).(\d+)','',pre_day2)
                        day2 = re.sub(r'\s(\d+):(\d+):(\d+)\s(\w+)',"",pre_day2)
                        day2 = day2.rstrip() # find out the dates of next line.
                        while day2 >= currentEnergyDay:
                            if day2 == currentEnergyDay:#if they are the same, it means the dates are not changed. this is not the last line of that day.
                                merge_line = line1 + "," #if it's not the last line of that day ,we do not need to add the energy value of that day, just append this line with a comma to the linelist.
                                merge_list.append(merge_line)
                                break
                            else:#the date of nextline changed, which means the previous line is the last line of that date. we need to match the energy value to it and append the line with energy value to the linelist.
                                energy_of_the_day = energy[n_energy]
                                energy_divided = float(energy_of_the_day)/1000 #change the unit of energy value by dividing 1000.
                                merge_line = line1 +","+ str(energy_divided)
                                merge_list.append(merge_line)
                                n_energy += 1 # increment of n_energy
                                currentEnergyDay = energy_date[n_energy - 1] # update the current energy day.
                                break
                        break
                merge_list.append(new_linelist[len(new_linelist) - 1]+',') # append the last line of the temperature file to the list.
                header_list = ['Index',',','Date Time',',','Temperature',',','energy_value(Wh/1000)']

            #write the files
            if third == sys.stdout: # write the results in the stdout stream
                for i in range(len(header_list)):#write the headers
                    third.write(header_list[i])
                third.write('\n')
                for j in merge_list: #write the data.
                    third.write(j)
                    third.write('\n')
            else:
                if os.path.isfile(third) == True:
                    choice = input('The filename exists, do you want to append on it or overwrite it? (append(a)/overwrite(o))')#choose 'a' if we want to append it, choose 'o' if we want to overwrite it.
                    # if the file alreay exists in the current directory, we need to confirm if the user still want to use this filename.
                    if choice == 'a':# choose to append the merged data onto the same output file
                        with open(third,'a') as output:#'a' means append to the files.
                            for j in range(len(merge_list)):
                                output.write(merge_list[j])
                                output.write('\n')
                    else: #if choose to overwriting it.
                        with open(third,'w') as output: #'w' will let us overwrite the file.
                            for i in range(len(header_list)):#write the headers.
                                output.write(header_list[i])
                            output.write('\n')
                            for k in range(len(merge_list)):#write the merged data.
                                output.write(merge_list[k])
                                output.write('\n')

                else: # if the filename is a totally new one, then open and write it directly.
                    with open(third,'w') as output:
                            for i in range(len(header_list)): #write the headers
                                output.write(header_list[i])
                            output.write('\n')
                            for k in range(len(merge_list)):#write the merged data.
                                output.write(merge_list[k])
                                output.write('\n')

#run the code
filenames = {'1':["waterTemperature.csv","energy.csv","merged.csv"]}
main(**filenames)
