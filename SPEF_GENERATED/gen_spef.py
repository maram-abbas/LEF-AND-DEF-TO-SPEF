#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:13:22 2019
@author: maramabbas
"""

#class for lef parser
from lef_util import *
from util import *

SCALE = 2000

class LefParser:
    """
    LefParser object will parse the LEF file and store information about the
    cell library.
    """
    def __init__(self, lef_file):
        self.lef_path = lef_file
        # dictionaries to map the definitions
        self.macro_dict = {}
        self.layer_dict = {}
        self.via_dict = {}
        # can make the stack to be an object if needed
        self.stack = []
        # store the statements info in a list
        self.statements = []
        self.cell_height = -1

    def get_cell_height(self):
        """
        Get the general cell height in the library
        :return: void
        """
        for macro in self.macro_dict:
            self.cell_height = self.macro_dict[macro].info["SIZE"][1]
            #print (self.cell_height)
            break

    def parse(self):
        # Now try using my data structure to parse
        # open the file and start reading
        #print ("Start parsing LEF file...")
        f = open(self.lef_path, "r")
        # the program will run until the end of file f
        for line in f:
            #print (line)
            info = str_to_list(line)
            #print (info)
            if len(info) != 0:
                # if info is a blank line, then move to next line
                # check if the program is processing a statement
                #print (info)
                if len(self.stack) != 0:
                    curState = self.stack[len(self.stack) - 1]
                    #print (curState)
                    nextState = curState.parse_next(info)
                    #print (nextState)
                else:
                    curState = Statement()
                    nextState = curState.parse_next(info)
                # check the status return from parse_next function
                if nextState == 0:
                    # continue as normal
                    pass
                elif nextState == 1:
                    # remove the done statement from stack, and add it to the statements
                    # list
                    if len(self.stack) != 0:
                        # add the done statement to a dictionary
                        
                        done_obj = self.stack.pop()
                        #print(done_obj)
                        if isinstance(done_obj, Macro):
                            self.macro_dict[done_obj.name] = done_obj
                        elif isinstance(done_obj, Layer):
                            self.layer_dict[done_obj.name] = done_obj
                            #print(self.layer_dict[done_obj.name])
                            
                        elif isinstance(done_obj, Via):
                            self.via_dict[done_obj.name] = done_obj
                        self.statements.append(done_obj)
                elif nextState == -1:
                    pass
                else:
                    self.stack.append(nextState)
                    # print (nextState)
        f.close()
        # get the cell height of the library
        self.get_cell_height()
        #print ("Parsing LEF file done.")
        

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
        self.pin_layer = []
        pin_placement_x = []
        pin_placement_y = []
        start = 100000000
        end = 0
        stop = 0
        
        #GETTING PINS
        file = open("spi_master.def", "r")
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
                self.pin_layer.append(layer)
            
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
        self.components_cell = []
        comp_n = ""
        comp_c = ""
        file = open("spi_master.def", "r")
        for i, line in enumerate(file):
            if line.find("COMPONENTS") != -1:
                start = i
                
            if line.find("PINS") != -1:
                break
                
            if line.startswith("-") and i > start:
                comp_n = line[2:line.find(" ",2)]
                comp_c = line[2 + len(comp_n):line.find(" +")]
                self.components_name.append(comp_n)
                self.components_cell.append(comp_c)
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
        file = open("spi_master.def", "r")
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
                                if len(self.metal[net][str(z)]["other_x"]) == 0:
                                    self.metal[net][str(z)]["other_x"].append(x1)
                                    
                                    if line[j + 4] == '*':
                                        self.metal[net][str(z)]["other_y"].append(y1[1:])
                                    else:
                                        number = line[j + 4:line.find(" )",j + 4)]
                                        self.metal[net][str(z)]["other_y"].append(number)
                                else:
                                    self.metal[net][str(z)]["other_x"].append(self.metal[net][str(z)]["other_x"][-1])
                                    
                                    if line[j + 4] == '*':
                                        self.metal[net][str(z)]["other_y"].append(self.metal[net][str(z)]["other_y"][-1])
                                    else:
                                        number = line[j + 4:line.find(" )",j + 4)]
                                        self.metal[net][str(z)]["other_y"].append(number)
                            else:
                                number = line[j + 2:line.find(" ",j + 2)]
                                self.metal[net][str(z)]["other_x"].append(number)
                                
                                if line[j + len(number) + 3] == '*':
                                    if len(self.metal[net][str(z)]["other_y"]) == 0:
                                        self.metal[net][str(z)]["other_y"].append(y1[1:])
                                    else:
                                        self.metal[net][str(z)]["other_y"].append(self.metal[net][str(z)]["other_y"][-1])
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
                                if len(self.metal[net][str(z)]["other_x"]) == 0:
                                    self.metal[net][str(z)]["other_x"].append(x1)
                                    
                                    if line[j + 4] == '*':
                                        self.metal[net][str(z)]["other_y"].append(y1)
                                    else:
                                        number = line[j + 4:line.find(" )",j + 4)]
                                        self.metal[net][str(z)]["other_y"].append(number)
                                else:
                                    self.metal[net][str(z)]["other_x"].append(self.metal[net][str(z)]["other_x"][-1])
                                    
                                    if line[j + 4] == '*':
                                        self.metal[net][str(z)]["other_y"].append(self.metal[net][str(z)]["other_y"][-1])
                                    else:
                                        number = line[j + 4:line.find(" )",j + 4)]
                                        self.metal[net][str(z)]["other_y"].append(number)
                            else:
                                number = line[j + 2:line.find(" ",j + 2)]
                                self.metal[net][str(z)]["other_x"].append(number)
                                
                                if line[j + len(number) + 3] == '*':
                                    if len(self.metal[net][str(z)]["other_y"]) == 0:
                                        self.metal[net][str(z)]["other_y"].append(y1)
                                    else:
                                        self.metal[net][str(z)]["other_y"].append(self.metal[net][str(z)]["other_y"][-1])
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


class LibParser:
    
    def parse (self):
        lib_file = open("osu035.lib", "r") #opening the file
    
        self.cell_name=[] #list of cell name
        self.pin_name=[] #list the pin names
        self.direction=[] #list the direction
        pin_taken=0 # flag to see if line contain related or not then take pins only
        counter=-1 # number of pins
        counter2=0
        self.output=[]  #correct index
        counter_2=[]
        total=[]
        self.capacitance=[]
        cap_flag=0#flag for capacitance
        total_cap=0
        
        for i, line in enumerate(lib_file): #passing at everyline of file
            if line:
                if line.find('Design') != -1 :   #if found design
                    first_finder=line.find(':')    # finding :
                    last_finder=line.find('*',first_finder)   #finding the * after :
                    self.cell_name.append(line[first_finder+2:last_finder-1])  #taking the cell name
                    counter+=1
                    counter2=-1
                    
                    
                if line.find('_pin') !=-1 :  #if found related_pin or contsrained_pin
                    pin_taken=0 #flag pin taken =0
                else:
                    pin_taken=1 #related is not in the line
                
                if(pin_taken==1) and line.find('pin') != -1:
                    
                    open_bracket=line.find('(')    # finding (
                    end_bracket=line.find(')')   #finding the ) 
                    my_pin_name=line[open_bracket+1:end_bracket]
                    self.pin_name.append(my_pin_name)    #taking pin name
                    self.output.append(counter)
                    counter2+=1
                    counter_2.append(counter2)
                    
                        
                if line.find('direction')  !=-1:
                    one_find=line.find(':') #find :
                    two_find=line.find(';') #find ;
                    my_direction=line[one_find+2:two_find] #direction either input or output
                    if (my_direction =="input"):
                        updated_direction='I' #conerting it to I
                    else:# output
                        updated_direction='O' #conerting it to O
                    self.direction.append(updated_direction) #taking direction
                if line.find('_capacitance')  !=-1:  #if found _capacitance this is not the one i want
                    cap_flag=1 #flag to take capacitance only and ignore rise_capacitance and fall_cap..
                else:
                    cap_flag=0
                if(cap_flag==0) and line.find('capacitance :') !=-1:
                    ones_find=line.find(':') #find :
                    twos_find=line.find(';') #find ;
                    cap=line[ones_find+2:twos_find]
                    self.capacitance.append(cap) #taking the capacitance

if __name__ == '__main__':
    #LEF EXTRACTIONS
    #path = "osu018_stdcells.lef"
    path = "osu035.lef"
    lef_parser = LefParser(path)
    lef_parser.parse()
    
    #GETTING RESISTANCE OF METALS AND VIA LAYERS    
    layer_metal = []
    metal_resistance = []
    metal_capacitance = []
    metal_edgecapacitance = []
    
    total_metal_number = 1  
    while(1):
        
        if "metal" + str(total_metal_number) in lef_parser.layer_dict:
            print("YES")
            total_metal_number += 1
        else:
            break
        
    print (total_metal_number)      #becomes 7
    
    for i in range(1,total_metal_number):
        layer_metal.append(lef_parser.layer_dict["metal" + str(i)])
        metal_resistance.append(layer_metal[i - 1].resistance[1])
        metal_capacitance.append(layer_metal[i - 1].capacitance[1])
        #metal_edgecapacitance.append(layer_metal[i - 1].edgecapacitance[1])
        #print(lef_parser.layer_dict["metal" + str(i)])
        
    layer_via = []
    via_resistance = []
    layer_via.append(lef_parser.layer_dict["via1"])
    via_resistance.append(layer_via[0].resistance)
    
    for i in range(2,total_metal_number - 1):
        layer_via.append(lef_parser.layer_dict["via" + str(i)])
        via_resistance.append(layer_via[i - 1].resistance)
        
    lef = open(path,"r")
    start = 100000000
    end = 0
    edge_capacitance = 0
    for i in range (1,total_metal_number):
        for c,line in enumerate(lef):
            if line.startswith("LAYER metal" + str(i)):
                start = c
                
            if line.startswith("  EDGECAPACITANCE") and c > start:
                temp = "  EDGECAPACITANCE "
                edge_capacitance = line[len(temp):-2]
                metal_edgecapacitance.append(edge_capacitance)
                #print(edge_capacitance)
                break
            
     #IF THERE IS NO EDGECAPACITANCE IN LEF FILE       
    if len(metal_edgecapacitance) == 0:
        for i in range (1,total_metal_number):
            metal_edgecapacitance.append(0)
                
    #print(metal_edgecapacitance)
    """
    via = []
    
    via2_1 = lef_parser.via_dict["M2_M1"]
    
    for e, each in enumerate(via2_1.layers):
        if e == 1:
            v_temp = each.name
            via.append(v_temp)
            
    via3_2 = lef_parser.via_dict["M3_M2"]
    
    for e, each in enumerate(via3_2.layers):
        if e == 1:
            v_temp = each.name
            via.append(v_temp)
            
    via4_3 = lef_parser.via_dict["M4_M3"]
       
    for e, each in enumerate(via4_3.layers):
        if e == 1:
            v_temp = each.name
            via.append(v_temp)
    
    via5_4 = lef_parser.via_dict["M5_M4"]
       
    for e, each in enumerate(via5_4.layers):
        if e == 1:
            v_temp = each.name
            via.append(v_temp)
            
    via6_5 = lef_parser.via_dict["M6_M5"]
       
    for e, each in enumerate(via6_5.layers):
        if e == 1:
            v_temp = each.name
            via.append(v_temp)
            
    #print(v_temp)
    """
        
    
    
    
    
    path = "osu035.lef"
    lef_parser = LefParser(path)
    lef_parser.parse()  
    
    def_parser = DefParser()
    def_parser.parse()
    
    lib_parser = LibParser()
    lib_parser.parse()
    
    #print(def_parser.pin_name)
    
    spef = open("spi_master.spef", "w+")
    
    
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
    
    total_cap = 0
    
    length = 1
    width = 1
    pin_cap = []
    pc = ""
    
    #GETTING TOTAL CAPACITANCE FROM PIN LAYERS
    for pn,val in enumerate(def_parser.pin_name):
        pl = def_parser.pin_layer[pn]
        cap_here = float(metal_capacitance[int(pl[5:]) - 1]) * length * width + float(metal_edgecapacitance[int(pl[5:]) - 1]) * length
        pc = val + " " + str(cap_here)
        pin_cap.append(pc)
        
    #print(pin_cap)
        
    width = 0.3 
    metal_width = []
        
    for i in range(1,total_metal_number):
        metal_width.append(lef_parser.layer_dict["metal" + str(i)].width)
        
        
    for j in def_parser.metal:
        net_cap = []
        #total_cap = 0
    
        for each_index in def_parser.metal[j]:
            metal = def_parser.metal[j][each_index]['metal']
            metal0 = metal[len(metal)-1:len(metal)]
            edge_cap = metal_edgecapacitance[int(metal0)-1]
            metal_cap = metal_capacitance[int(metal0) - 1]
            
            x1 = float(def_parser.metal[j][each_index]["x1"])
            y1 = float(def_parser.metal[j][each_index]["y1"])
            
            if len(def_parser.metal[j][each_index]["other_x"]) != 0:
                ox_0 = float(def_parser.metal[j][each_index]["other_x"][0])
                oy_0 = float(def_parser.metal[j][each_index]["other_y"][0])
                
                wire_length = math.sqrt((x1 - ox_0)**2 + (y1 - oy_0)**2)
                cap = float(metal_cap)*wire_length*metal_width[int(metal0)-1] + float(edge_cap)*wire_length
                total_cap = total_cap + cap
                net_cap.append(cap)
                if j == "RDY":
                    print("metal: " +  metal0+" length: " + str(wire_length) + "  cap = " + str(cap))
                    print(def_parser.metal[j][each_index]["other_x"])
                    print(def_parser.metal[j][each_index]["other_y"])

            
            for en_ox, ox in enumerate(def_parser.metal[j][each_index]["other_x"]):
                if en_ox + 1 < len(def_parser.metal[j][each_index]["other_x"]) :
                    #print(en_ox)
                    #print(len(def_parser.metal[j][each_index]["other_x"]))
                    oy = float(def_parser.metal[j][each_index]["other_y"][en_ox])
                    ox_1 = float(def_parser.metal[j][each_index]["other_x"][en_ox + 1])
                    oy_1 = float(def_parser.metal[j][each_index]["other_y"][en_ox + 1])
                    ox = float(ox)
                    
                    wire_length = math.sqrt((ox - ox_1)**2 + (oy - oy_1)**2)
                    #print(j+" x1: " + str(ox) + " x2: " + str(ox_1) + " y1: " + str(oy) + " y2: " + str(oy_1))
                    cap = float(metal_cap)*wire_length*metal_width[int(metal0)-1] + float(edge_cap)*wire_length
                
                    #print("cap: ", cap)
                    if j == "RDY":
                        print(" x1: " + str(ox) + " x2: " + str(ox_1) + " y1: " + str(oy) + " y2: " + str(oy_1))
                        print("metal: " +  metal0+" length: " + str(wire_length) + "  cap = " + str(cap))
                    total_cap = total_cap + cap
                    net_cap.append(cap)
       
        index = def_parser.nets.index(j)
        net_name = "*"+str(index+len(def_parser.components_name)+1)
        #print(j)
        #print(def_parser.nets[int(j)])
        #print(def_parser.components_name)
        
        #GETTING TOTAL CAPACITANCE OF CELL INSTANCE
        for k4,k5 in enumerate(def_parser.net_cell_instance[j]["cell_name"]):
            
            #print(def_parser.components_name)
            cap_ind = def_parser.components_name.index(k5)
            cell_name = def_parser.components_cell[cap_ind]
            #print(cell_name)
            
            cell_index = lib_parser.cell_name.index(cell_name[1:])
            occurance_number = lib_parser.output.count(cell_index)
            first_occurance = lib_parser.output.index(cell_index)
                
            while (occurance_number > 0):
                
                if  def_parser.net_cell_instance[j]["instance"][k4] == lib_parser.pin_name[first_occurance]:
                    capacitance_here = float(lib_parser.capacitance[first_occurance])
                    total_cap += capacitance_here
                    
                first_occurance += 1
                occurance_number -= 1
    
                
        
        #PIN CAPACITANCE
        for pin_c in pin_cap:
            space = pin_c.find(" ")
            if pin_c[:space] == j:
                #print(pin_c[space + 1:])
                total_cap += float(pin_c[space + 1:])
                
        spef.write("*D_NET "+net_name+ " " + str(total_cap)+"\n\n")
        
        """
        ------------------------------------------ CONNECTIONS PART -------------------------------------------
        """
        
        spef.write("*CONN\n")
        
        #print(def_parser.net_cell_instance)
        
        #print(j)
        if j in def_parser.pin_name:
            io = ""
            for cell_name in enumerate(def_parser.net_cell_instance[j]["cell_name"]):
                #print(cell_name[1])
                comp_ind = def_parser.components_name.index(cell_name[1])
                comp_cell = def_parser.components_cell[comp_ind]
                
                
                #FROM LIB PARSER FIND IF ITS INPUT OR OUTPUT
                lib_ind = lib_parser.cell_name.index(comp_cell[1:])
                for cell_place_1,cell_place_2 in enumerate(lib_parser.output):
                    if cell_place_2 == lib_ind:
                        ins = def_parser.net_cell_instance[j]["instance"][0]
                        #print(ins)
                        if lib_parser.pin_name[cell_place_1] == ins:
                            io = lib_parser.direction[cell_place_1]
                            #print(io)
                        
                
            spef.write("*P " + net_name + " " + io + "\n")
        
        counter2 = 0
        for k4,k5 in enumerate(def_parser.net_cell_instance[j]["cell_name"]):
            index2 = def_parser.components_name.index(k5)
            cell_name = "*"+str(index2+1) + ":" + def_parser.net_cell_instance[j]["instance"][k4]
            spef.write("*I "+ cell_name + "\n")
            counter2= k4+1
        
        """
        for k2, k3 in enumerate(net_cap):
            spef.write( "*N "+ net_name + ":" + str(k2+counter2+1) +" *C"+"\n")
        """
        
        
        """
        ------------------------------------------ CAPACITANCE PART -------------------------------------------
        """
        
        spef.write("\n*CAP\n")
        counter2 = 0
        capacitance_here = 0
        
        for k4,k5 in enumerate(def_parser.net_cell_instance[j]["cell_name"]):
            
            
            cap_ind = def_parser.components_name.index(k5)
            cell_name = def_parser.components_cell[cap_ind]
            #print(cell_name)
            
            cell_index = lib_parser.cell_name.index(cell_name[1:])
            occurance_number = lib_parser.output.count(cell_index)
            first_occurance = lib_parser.output.index(cell_index)
                
            while (occurance_number > 0):
                
                if  def_parser.net_cell_instance[j]["instance"][k4] == lib_parser.pin_name[first_occurance]:
                    capacitance_here = float(lib_parser.capacitance[first_occurance])
                    total_cap += capacitance_here
                    
                first_occurance += 1
                occurance_number -= 1
            
            
            index2 = def_parser.components_name.index(k5)
            cell_name = "*"+str(index2+1) + ":" + def_parser.net_cell_instance[j]["instance"][k4]
            spef.write(str(k4+1) +" "+ cell_name + " " + str(capacitance_here) + "\n")
            counter2= k4+1
                
        
        for k2, k3 in enumerate(net_cap):
            spef.write(str(k2+counter2+1) + " "+ net_name + ":" + str(k2+counter2+1) +" " + str(k3)+"\n")
            
               
            
        """
        ------------------------------------------ RESISTANCE PART -------------------------------------------
        """
        
        spef.write("\n*RES\n")
        count_res = 0
        
        #metal_width = []
        #wire_length = []
        m_l = 0
        
        #for i in range(1,7):
            #metal_width.append(lef_parser.layer_dict["metal" + str(i)].width)
            
         
        for each_index in def_parser.metal[j]:
            #print(def_parser.metal[j])
            
            for m_i in range(1,total_metal_number):
                if def_parser.metal[j][each_index]["metal"] == "metal" + str(m_i):
                    m_l = m_i - 1
                    #print("m_L",m_i,m_l)
                
                
            x1 = float(def_parser.metal[j][each_index]["x1"])
            y1 = float(def_parser.metal[j][each_index]["y1"])
            
            if len(def_parser.metal[j][each_index]["other_x"]) != 0:
                ox_0 = float(def_parser.metal[j][each_index]["other_x"][0])
                oy_0 = float(def_parser.metal[j][each_index]["other_y"][0])
                
                wire_length = math.sqrt((x1 - ox_0)**2 + (y1 - oy_0)**2)
                metal_r = metal_resistance[m_l]
                metal_w = metal_width[m_l]
                
                resistance = metal_r * wire_length / metal_w
                
                count_res += 1
                
                spef.write(str(count_res) + " " + net_name + ":" + str(count_res) + " " + net_name + ":" + str(count_res + 1) + " " + str(resistance) + "\n")
                #print(wire_length)
                #if j == "load":
                    #print(resistance)
                
                for en_ox, ox in enumerate(def_parser.metal[j][each_index]["other_x"]):
                    if en_ox + 1 < len(def_parser.metal[j][each_index]["other_x"]) :
                        #print(en_ox)
                        #print(len(def_parser.metal[j][each_index]["other_x"]))
                        oy = float(def_parser.metal[j][each_index]["other_y"][en_ox])
                        ox_1 = float(def_parser.metal[j][each_index]["other_x"][en_ox + 1])
                        oy_1 = float(def_parser.metal[j][each_index]["other_y"][en_ox + 1])
                        ox = float(ox)
                        
                        wire_length = math.sqrt((ox - ox_1)**2 + (oy - oy_1)**2)
                        
                        metal_r = metal_resistance[m_l]
                        metal_w = metal_width[m_l]
                
                        resistance = metal_r * wire_length / metal_w
                        
                        count_res += 1
                
                        spef.write(str(count_res) + " " + net_name + ":" + str(count_res) + " " + net_name + ":" + str(count_res + 1) + " " + str(resistance) + "\n")
                        
                        #if j == "load":
                            #print(resistance)
            for v_i in range(2, total_metal_number - 1):
                if def_parser.metal[j][each_index]["merge"] == "M" + str(v_i) + "_M" + str(v_i - 1):
                    v_l = v_i - 2
            
            if def_parser.metal[j][each_index]["merge"] != "":
                resistance_via = via_resistance[v_l]
                
                count_res += 1
                
                spef.write(str(count_res) + " " + net_name + ":" + str(count_res) + " " + net_name + ":" + str(count_res + 1) + " " + str(resistance_via) + "\n")
            else:
                resistance_via = 0
                
            #if j == "load":
                #print(resistance_via)
                        
                #resistance = 
                        
            
        #print(metal_width)
        spef.write("\n*END\n\n")
        
    spef.close()
        