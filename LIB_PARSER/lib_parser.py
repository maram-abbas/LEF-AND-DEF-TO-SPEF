# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 08:58:30 2019

@author: user
"""

lib_file = open("osu035.lib", "r") #opening the file


cell_name=[] #list of cell name
pin_name=[] #list of the pin names
direction=[] #list of the direction
pin_taken=0 # flag to see if line contain related or not then take pins only
counter=-1 # number of pins
counter2=0 
output=[]  #correct index to make all of them parrallel with the cell name
counter_2=[]
total=[]
capacitance=[] list #list of the capacitances of each pin 
cap_flag=0#flag for capacitance

for i, line in enumerate(lib_file): #passing at everyline of file
    if line:
        if line.find('Design') != -1 :   #if found design
            first_finder=line.find(':')    # finding :
            last_finder=line.find('*',first_finder)   #finding the * after :
            cell_name.append(line[first_finder+2:last_finder-1])  #taking the cell name
            counter+=1
            counter2=-1
            
            
        if line.find('_pin') !=-1 :  #if found related_pin or contsrained_pin
            pin_taken=0 #flag pin taken =0
        else:
            pin_taken=1 #related is not in the line
        
        if(pin_taken==1) and line.find('pin') !=-1:  #if found the word pin
            
            open_bracket=line.find('(')    # finding (
            end_bracket=line.find(')')   #finding the ) 
            my_pin_name=line[open_bracket+1:end_bracket] #taking pin name
            pin_name.append(my_pin_name)    #placing pin name inside the pin_name list
            output.append(counter)
            counter2+=1
            counter_2.append(counter2)
            
                
        if line.find('direction')  !=-1:  #if found direction
            one_find=line.find(':') #find :
            two_find=line.find(';') #find ;
            my_direction=line[one_find+2:two_find] #direction either input or output
            if (my_direction =="input"):
                updated_direction='I' #converting it to I
            else:# output
                updated_direction='O' #converting it to O
            direction.append(updated_direction) #taking direction
        if line.find('_capacitance')  !=-1:  #if found direction
            cap_flag=1 #flag to take capacitance only and ignore rise_capacitance and fall_cap..
        else:
            cap_flag=0
        if(cap_flag==0) and line.find('capacitance :') !=-1:
            ones_find=line.find(':') #find :
            twos_find=line.find(';') #find ;
            capacitance.append(line[ones_find+2:twos_find]) #placing capacitaice in the list
            
#calculating capacitance            
index_of_parsed_cell=cell_name.index(parsed_cell)   # get the index of the cell   
number_occupied=output.count(index_of_parsed_cell)   #index dah mawgoud kam mara ba2 fel output list  ex 3 times
first_occurance=output.index(index_of_parsed_cell)  #index of first occuance of that index 
current_cap=0

print(capacitance)            
print(counter_2)        
print('output',output)
print('direction',direction)
print("pin",pin_name)       
print("cell_name",cell_name)    
 
    

