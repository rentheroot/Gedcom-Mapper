#imports
import csv
from itertools import tee
import subprocess
import string

#set console encoding to utf-8
Command = "chcp 65001"
subprocess.call(Command, shell=True)

filename = input("What is the name of your gedcom file?(ex. YourGedcomFile)")
filename = filename + ".ged"
with open ('output.txt' , "w") as output_file:
    output_file.close()
#Function to return the id number and name of each person in the file
def indi_number_list(filename):
    with open(filename, 'r') as the_file:
        
        individual_numbers = []
        individual_names = []
        for line in the_file:
            if '0 @I' in line:
                
                handle1, handle2 = tee(the_file)
                next_line = (next(handle1))

                
                a,b,c = line.split(' ')
                individual_numbers.append(b)

                a,b = next_line.split('1 NAME ')
                full_name_unformatted = b
                full_name = full_name_unformatted.replace('/', '')
                full_name2 = full_name.replace('\n', '')
                individual_names.append(full_name2)
            else:
                pass

        #return number , name    
        return(individual_numbers, individual_names)

#pair each source name and number with the destination name and number    
def find_shared(number_name):
    with open(filename, 'r') as the_file:
        with open('output.txt', 'a') as output_file:
            other_shared = []
            
            for line in the_file:
                
                if '0 @I' in line:
                    other_shared = []
                    iter_number = 0
                    
                    
                    a,b,c = line.split(' ')
                    actual_name = number_name.get(b , "")
                    source_name = actual_name + '(' + b + '),'

                #check line for gedcom shared tag
                elif '_SHAR @' in line:
                    iter_number = iter_number + 1
                    a,b,c = line.split(' ')
                    c_split = c.replace('\n', '')
                    actual_name2 = number_name.get(c_split , "")
                    destin_name = actual_name2 + '(' + c_split + ')'
                    output_file.write(source_name + destin_name + '\n')
                    other_shared.append(destin_name)
                    try:
                        for name in other_shared:
                            if name != destin_name:
                                output_file.write(name + ',' + destin_name + '\n')
                    except:
                        pass

                                
                else:
                    pass

                
#map the returned values from indi_number_list function to variables
indi_num, indi_name = indi_number_list(filename)

#dictionary of individual numbers and names
number_name = dict(zip(indi_num , indi_name))

#run the find_shared function
find_shared(number_name)
input("End Of File")


            
