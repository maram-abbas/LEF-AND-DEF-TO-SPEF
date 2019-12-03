# LEF-AND-DEF-TO-SPEF

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
  
  
  
 WHAT IS DONE: 
  - capacitance calculation
  - listing of cell names
  - listing of nets
  
  WHAT IS REMAINING:
  - resistance calculation
  - listing of ports


