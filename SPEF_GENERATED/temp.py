# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 23:34:10 2019

@author: Tasneem
"""
import math
from lefparser import *

#path=input("Enter LEF file: ")

path = "./osu018_stdcells.lef"
lef_parser = LefParser(path)
lef_parser.parse()

    
#GETTING RESISTANCE OF METALS AND VIA LAYERS    
layer_metal = []
metal_resistance = []
metal_capacitance = []
metal_edgecapacitance = []
    
for i in range(1,7):
     layer_metal.append(lef_parser.layer_dict["metal" + str(i)])
     metal_resistance.append(layer_metal[i - 1].resistance[1])
     metal_capacitance.append(layer_metal[i - 1].capacitance[1])
        #metal_edgecapacitance.append(layer_metal[i - 1].edgecapacitance[1])
        #print(lef_parser.layer_dict["metal" + str(i)])
        
layer_via = []
via_resistance = []
layer_via.append(lef_parser.layer_dict["via"])
via_resistance.append(layer_via[0].resistance)
    
for i in range(2,6):
    layer_via.append(lef_parser.layer_dict["via" + str(i)])
    via_resistance.append(layer_via[i - 1].resistance)
        
lef = open(path,"r")
start = 100000000
end = 0
edge_capacitance = 0
for i in range (1,7):
    for c,line in enumerate(lef):
            if line.startswith("LAYER metal" + str(i)):
                start = c
                
            if line.startswith("  EDGECAPACITANCE") and c > start:
                temp = "  EDGECAPACITANCE "
                edge_capacitance = line[len(temp):-2]
                metal_edgecapacitance.append(edge_capacitance)
                #print(edge_capacitance)
                break
                

                
        
    #print(via_resistance)
"""
print(metal_capacitance)
print (metal_edgecapacitance)
print(metal_resistance)
"""
##############################################################################################


from def_parser import *


def_parser = DefParser()
def_parser.parse()
#print(def_parser.pin_name)

spef = open("spef.txt", "w+")


spef.write("*SPEF \"IEEE 1481-2009\" \n")

spef.write("*DESIGN \n*DATE \n*VENDOR \n*PROGRAM \n*VERSION \"0.0\"\n*DESIGN_FLOW\n*DIVIDER /\n*DELIMITER :\n*BUS_DELIMITER <>\n*T_UNIT 1 PS\n*C_UNIT 1 FF\n*R_UNIT 1 KOHM\n*L_UNIT 1 UH\n")


spef.write("\n*NAME_MAP\n\n")

counter = 0
for i in def_parser.components_name:
    counter = counter +1
    #print(str(counter), i)
    spef.write("*"+str(counter)+" "+i+"\n")
    

for i in def_parser.nets:
    counter = counter +1
    spef.write("*"+str(counter)+" "+i+"\n")
    #print(str(counter), i)
    #print(i)
    #print(def_parser.metal[i])
    
    
spef.write("\n*PORTS\n")

spef.write("\n*END\n\n")
"""
for i in def_parser.nets:
    index = def_parser.nets.index(i)
    spef.write("*D_NET *"+str(index+len(def_parser.components_name)+1)+"\n")
    #for j in def_parser.metal[i]:
"""
width = 0.3
for j in def_parser.metal:
    net_cap = []
    total_cap = 0
    for i in def_parser.metal[j]:
        x1 = def_parser.metal[j][i]['x1']
        y1 = def_parser.metal[j][i]['y1']
        other_x = []
        other_y=[]
        metal = def_parser.metal[j][i]['metal']
        #print( def_parser.metal['RDY'][i])
        for k in def_parser.metal[j][i]['other_x']:
            other_x.append(k)
        for k1 in def_parser.metal[j][i]['other_y']:
            other_y.append(k1)
        #print(other_x)
        #print(other_y)
        metal0 = metal[len(metal)-1:len(metal)]
        
        edge_cap = metal_edgecapacitance[int(metal0)-1]
        metal_cap = metal_capacitance[int(metal0) - 1]
        
        for c1, c in enumerate(other_x):
            if abs(int(c)-int(x1)) == 0:
                length = abs(int(other_y[c1])-int(y1))
                             
            else:
                length = abs(int(c)-int(x1))
            cap = float(metal_cap)*length*width + float(edge_cap)*length
            #print(cap)
            total_cap = total_cap + cap
            net_cap.append(cap)
    #print(net_cap)
    #print(len(net_cap))
    index = def_parser.nets.index(j)
    net_name = "*"+str(index+len(def_parser.components_name)+1)
    spef.write("*D_NET "+net_name+ " " + str(total_cap)+"\n\n")
    
    spef.write("*CONN\n")
    
    counter2 = 0
    for k4,k5 in enumerate(def_parser.net_cell_instance[j]["cell_name"]):
        index2 = def_parser.components_name.index(k5)
        cell_name = "*"+str(index2+1) + ":" + def_parser.net_cell_instance[j]["instance"][k4]
        spef.write("*I "+ cell_name +" *L"+ "\n")
        counter2= k4+1
        
    for k2, k3 in enumerate(net_cap):
        spef.write( "*N "+ net_name + ":" + str(k2+counter2+1) +" *C"+"\n")
    
    spef.write("\n*CAP\n")
    counter2 = 0
    for k4,k5 in enumerate(def_parser.net_cell_instance[j]["cell_name"]):
        index2 = def_parser.components_name.index(k5)
        cell_name = "*"+str(index2+1) + ":" + def_parser.net_cell_instance[j]["instance"][k4]
        spef.write(str(k4+1) +" "+ cell_name + " " + "\n")
        counter2= k4+1
            
    
    for k2, k3 in enumerate(net_cap):
        spef.write(str(k2+counter2+1) + " "+ net_name + ":" + str(k2+counter2+1) +" " + str(k3)+"\n")
        
        
    spef.write("\n*END\n\n")
    
