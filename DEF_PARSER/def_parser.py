#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 18:18:14 2019

@author: maramabbas
"""
pin_name = []
pin_layer = []
pin_placement_x = []
pin_placement_y = []
start = 100000000
end = 0
stop = 0

#GETTING PINS
file = open("cpu.def", "r")
for i, line in enumerate(file):
    if line.find("PINS") != -1:
        start = i
        
    if line.find("NETS") != -1:
            break;
            
    if line.startswith("-") and i > start:
        name = line[2:line.find(" ",2)]
        #print(name)
        pin_name.append(name)
    
    if line.startswith("  + LAYER") and i > start:
        layer = line[10:line.find(" ",10)]
        #print(layer)
        pin_layer.append(layer)
    
    if line.startswith("  + PLACED") and i > start:
        placed_x = line[13:line.find(" ",13)]
        #print(placed_x)
        pin_placement_x.append(placed_x)
        
        begin_y = line.find(" ",13) + 1
        placed_y = line[begin_y:line.find(" ",begin_y)]
        #print(placed_y)
        pin_placement_y.append(placed_y)
        
file.close()
   

#GETTING COMPONENTS  
z = 0  
start = 100000000
components_name = []
components_cell = []
comp_n = ""
comp_c = ""
file = open("cpu.def", "r")
for i, line in enumerate(file):
    if line.find("COMPONENTS") != -1:
        start = i
        
    if line.find("PINS") != -1:
        break
        
    if line.startswith("-") and i > start:
        comp_n = line[2:line.find(" ",2)]
        comp_c = line[2 + len(comp_n):line.find(" +")]
        components_name.append(comp_n)
        components_cell.append(comp_c)
        #print(components_cell)
    
file.close()

#GETTING NETS
start = 100000000
net_cell_instance = {}
net = ""
cell_name = ""
instance = ""
start_again = 0
nothing = 0
counter = 0
metal = {}
file = open("cpu.def", "r")
for i, line in enumerate(file):
    if line.find("NETS") != -1:
        start = i
        
    if line.find("END NETS") != -1:
        break
        
    if line.startswith("-") and i > start:
        start_again = 1
        counter += 1
        net = line[2:-1]
        net_cell_instance[net] = {}
        net_cell_instance[net]["cell_name"] = []
        net_cell_instance[net]["instance"] = []
        metal[net] = {}
        #net_cell_instance["pin" + str(counter)]["pin"] = net
        #print(net_cell_instance)
       
    if start_again == 1:
        
        if line.startswith("  ( PIN"):
            #do nothing
            nothing += nothing
            
        elif line.startswith("  ( "):
            cell_name = line[4:line.find(" ",4)]
            instance = line[5 + len(cell_name):line.find(" )")]
            net_cell_instance[net]["cell_name"].append(cell_name)
            net_cell_instance[net]["instance"].append(instance)
            
        elif line.startswith("+ ROUTED"):
            z += 1
            routed = "+ ROUTED "
            metal_name = line[len(routed):line.find(" (")] + "_" + str(z)
            
            index = line.find(" ( ") + 3
            x1 = line[index:line.find(" ",index)]
            
            y1 = line[line.find(x1) + len(x1):line.find(" )")]
            #print(y1)
            
            metal[net][metal_name] = {}
            metal[net][metal_name]["x1"] = x1
            metal[net][metal_name]["y1"] = y1[1:]
            metal[net][metal_name]["other_x"] = []
            metal[net][metal_name]["other_y"] = []
            metal[net][metal_name]["merge"] = ""
            
            
            for j,charac in enumerate(line):
                
                if charac == "(" and j != 16:   #not first bracket
                    
                    if line[j + 2] == '*':
                        metal[net][metal_name]["other_x"].append(x1)
                        
                        if line[j + 4] == '*':
                            metal[net][metal_name]["other_y"].append(y1[1:])
                        else:
                            number = line[j + 4:line.find(" )",j + 4)]
                            metal[net][metal_name]["other_y"].append(number)
                    else:
                        number = line[j + 2:line.find(" ",j + 2)]
                        metal[net][metal_name]["other_x"].append(number)
                        
                        if line[j + len(number) + 3] == '*':
                            metal[net][metal_name]["other_y"].append(y1[1:])
                        else:
                            number = line[j + len(number) + 3:line.find(" )",j + len(number) + 3)]
                            metal[net][metal_name]["other_y"].append(number)
                            
                if charac == "M":
                    #print(line[j:-2])
                    metal[net][metal_name]["merge"] = line[j:-2]
                    break
            
            
        elif line.startswith("  NEW metal"):
            z += 1
            new_metal = "  NEW "
            metal_name = line[len(new_metal):line.find(" (")] + "_" + str(z)
            
            index = line.find(" ( ") + 3
            x1 = line[index:line.find(" ",index)]
            
            y1 = line[line.find(x1) + len(x1) + 1:line.find(" )")]
            #print(x1)
            
            metal[net][metal_name] = {}
            metal[net][metal_name]["x1"] = x1
            metal[net][metal_name]["y1"] = y1
            metal[net][metal_name]["other_x"] = []
            metal[net][metal_name]["other_y"] = []
            metal[net][metal_name]["merge"] = ""
            
            
            for j,charac in enumerate(line):
                
                if charac == "(" and j != 13:   #not first bracket
                    
                    if line[j + 2] == '*':
                        metal[net][metal_name]["other_x"].append(x1)
                        
                        if line[j + 4] == '*':
                            metal[net][metal_name]["other_y"].append(y1)
                        else:
                            number = line[j + 4:line.find(" )",j + 4)]
                            metal[net][metal_name]["other_y"].append(number)
                    else:
                        number = line[j + 2:line.find(" ",j + 2)]
                        metal[net][metal_name]["other_x"].append(number)
                        
                        if line[j + len(number) + 3] == '*':
                            metal[net][metal_name]["other_y"].append(y1)
                        else:
                            number = line[j + len(number) + 3:line.find(" )",j + len(number) + 3)]
                            metal[net][metal_name]["other_y"].append(number)
                            
                if charac == "M":
                    #print(line[j:-2])
                    if line.find(";"):
                        metal[net][metal_name]["merge"] = line[j:-3]
                    else:
                        metal[net][metal_name]["merge"] = line[j:-2]
                        
                    break
    
    if line.find(";") != -1:
        start_again = 0
        z = 0
      
    #print(net_cell_instance)
            
                      
file.close()

print(metal["RDY"])