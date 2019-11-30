"""
Lef Parser
Author: Tri Cao
Email: tricao@utdallas.edu
Date: August 2016
"""
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
        print ("Start parsing LEF file...")
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
        print ("Parsing LEF file done.")


# Main Class
if __name__ == '__main__':
    path = "osu018_stdcells.lef"
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
                
    print(metal_edgecapacitance)
                
        
    #print(via_resistance)
        
        


