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
            
        