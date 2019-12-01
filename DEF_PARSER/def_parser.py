#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 18:18:14 2019
@author: maramabbas
"""

class DefParser:
    def __init__(self):
        #self.def_path = def_file
        # dictionaries to map the definitions
        self.pin_name = []
        self.components_name = []
        self.metal = {}
        self.nets = []
        self.net_cell_instance = {}

#pin_name = []
        
    def parse(self):
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
                self.pin_name.append(name)
            
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
        #print(self.pin_name)
        
        #GETTING COMPONENTS  
        z = 0  
        start = 100000000
        #components_name = []
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
                self.components_name.append(comp_n)
                components_cell.append(comp_c)
                #print(components_cell)
            
        file.close()
        
        #GETTING NETS
        start = 100000000
        #net_cell_instance = {}
        net = ""
        cell_name = ""
        instance = ""
        start_again = 0
        nothing = 0
        counter = 0
        #metal = {}
        #nets = []
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
                self.nets.append(net)
                self.net_cell_instance[net] = {}
                self.net_cell_instance[net]["cell_name"] = []
                self.net_cell_instance[net]["instance"] = []
                self.metal[net] = {}
                #net_cell_instance["pin" + str(counter)]["pin"] = net
                #print(net_cell_instance)
               
            if start_again == 1:
                
                if line.startswith("  ( PIN"):
                    #do nothing
                    nothing += nothing
                    
                elif line.startswith("  ( "):
                    cell_name = line[4:line.find(" ",4)]
                    instance = line[5 + len(cell_name):line.find(" )")]
                    self.net_cell_instance[net]["cell_name"].append(cell_name)
                    self.net_cell_instance[net]["instance"].append(instance)
                    
                    
                elif line.startswith("+ ROUTED"):
                    z += 1
                    routed = "+ ROUTED "
                    #metal_name = line[len(routed):line.find(" (")] + "_" + str(z)
                    metal_name = line[len(routed):line.find(" (")] 
                    
                    index = line.find(" ( ") + 3
                    x1 = line[index:line.find(" ",index)]
                    
                    y1 = line[line.find(x1) + len(x1):line.find(" )")]
                    #print(y1)
                    
                    self.metal[net][str(z)] = {}
                    self.metal[net][str(z)]["metal"] = metal_name
                    self.metal[net][str(z)]["x1"] = x1
                    self.metal[net][str(z)]["y1"] = y1[1:]
                    self.metal[net][str(z)]["other_x"] = []
                    self.metal[net][str(z)]["other_y"] = []
                    self.metal[net][str(z)]["merge"] = ""
                    
                    
                    for j,charac in enumerate(line):
                        
                        if charac == "(" and j != 16:   #not first bracket
                            
                            if line[j + 2] == '*':
                                self.metal[net][str(z)]["other_x"].append(x1)
                                
                                if line[j + 4] == '*':
                                    self.metal[net][str(z)]["other_y"].append(y1[1:])
                                else:
                                    number = line[j + 4:line.find(" )",j + 4)]
                                    self.metal[net][str(z)]["other_y"].append(number)
                            else:
                                number = line[j + 2:line.find(" ",j + 2)]
                                self.metal[net][str(z)]["other_x"].append(number)
                                
                                if line[j + len(number) + 3] == '*':
                                    self.metal[net][str(z)]["other_y"].append(y1[1:])
                                else:
                                    number = line[j + len(number) + 3:line.find(" )",j + len(number) + 3)]
                                    self.metal[net][str(z)]["other_y"].append(number)
                                    
                        if charac == "M":
                            #print(line[j:-2])
                            if line.find(";") != -1:
                                self.metal[net][str(z)]["merge"] = line[j:-3]
                            else:
                                self.metal[net][str(z)]["merge"] = line[j:-2]
                                
                            break
                    
                    
                elif line.startswith("  NEW metal"):
                    z += 1
                    new_metal = "  NEW "
                    metal_name = line[len(new_metal):line.find(" (")] 
                    
                    index = line.find(" ( ") + 3
                    x1 = line[index:line.find(" ",index)]
                    
                    y1 = line[line.find(x1) + len(x1) + 1:line.find(" )")]
                    #print(x1)
                    
                    self.metal[net][str(z)] = {}
                    self.metal[net][str(z)]["metal"] = metal_name
                    self.metal[net][str(z)]["x1"] = x1
                    self.metal[net][str(z)]["y1"] = y1
                    self.metal[net][str(z)]["other_x"] = []
                    self.metal[net][str(z)]["other_y"] = []
                    self.metal[net][str(z)]["merge"] = ""
                    
                    
                    for j,charac in enumerate(line):
                        
                        if charac == "(" and j != 13:   #not first bracket
                            
                            if line[j + 2] == '*':
                                self.metal[net][str(z)]["other_x"].append(x1)
                                
                                if line[j + 4] == '*':
                                    self.metal[net][str(z)]["other_y"].append(y1)
                                else:
                                    number = line[j + 4:line.find(" )",j + 4)]
                                    self.metal[net][str(z)]["other_y"].append(number)
                            else:
                                number = line[j + 2:line.find(" ",j + 2)]
                                self.metal[net][str(z)]["other_x"].append(number)
                                
                                if line[j + len(number) + 3] == '*':
                                    self.metal[net][str(z)]["other_y"].append(y1)
                                else:
                                    number = line[j + len(number) + 3:line.find(" )",j + len(number) + 3)]
                                    self.metal[net][str(z)]["other_y"].append(number)
                                    
                        if charac == "M":
                            #print(line[j:-2])
                            if line.find(";") != -1:
                                self.metal[net][str(z)]["merge"] = line[j:-3]
                            else:
                                self.metal[net][str(z)]["merge"] = line[j:-2]
                                
                            break
            
            if line.find(";") != -1:
                start_again = 0
                z = 0
              
            #print(net_cell_instance)
                    
                              
        file.close()
        
        #print(self.metal)
        #print(pin_name)
        #print(components_name)
        #print(nets)
        
        #print(net_cell_instance['cell_name'])
        
        #for i in metal["RDY"]:
        #    print(str(i), "\t", metal["RDY"][str(i)])
        
        #print(metal["RDY"]['metal2_2']['other_x'][1])