# LEF-AND-DEF-TO-SPEF

This project uses LEF, DEF, and LIB files in order to generate a SPEF file. This project is done for the Digital Design II course at the American University in Cairo.

This SPEF extractor uses three input files:
- LEF
- DEF
- LIB

The following information was parsed from these three input files:
- LEF: 
  - Capacitance of metal layer
  - Edgecapacitance of metal layer
  - Resistance of metal layer
  - Resistance of via layer
  - Width of metal layer
- DEF:
  - Names of components
  - All info in nets section
- LIB:
  - Capacitance of all pins
  - Direction of all pins
  
  
HOW TO RUN?
- Open terminal to the directory where all your files are found
- Make sure you have python installed since the source code of this project is written in python
- Write on the terminal the following:
  python gen_spef.py [def_path] [lib_path] [lef_path] [spef_path]
- Check spef file for output

 
 For testing syntax correctness: https://github.com/The-OpenROAD-Project/Resizer
  
 References: https://github.com/trimcao/lef-parser


