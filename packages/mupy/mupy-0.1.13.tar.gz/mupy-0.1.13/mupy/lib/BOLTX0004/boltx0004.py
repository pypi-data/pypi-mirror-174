#!/usr/bin/env python3
import os, sys
import shutil

class BOLTX0004:
    """ This class builds digital representations of BOLTX0004 hardware elements. These representations contain varius objects which help simulate the part.
    """

    def __init__(self, hardware_code, directory): # Runs when object is initialized.
        """_summary_

        Args:
            hardware_code (_type_): _description_
            directory (_type_): _description_
        """
        self.id = id # This is a unique name or tag referencing a particular object in a set.
        self.hardware_code = hardware_code
        self.family_code = self.hardware_code.split("-")[0]
        self.type_code = self.hardware_code.split("-")[1]
        self.directory = directory
        self.scad_file_name = directory + "/" + hardware_code +".scad" # This scad file is used to build the stl. It can be deleted afterwards. # TODO : Delete this file after run() command is called.
        self.scad_file = open(self.scad_file_name, 'w+')  # open file in append mode

        os.system("cp -R "+os.path.dirname(__file__)+"/scad/ "+ self.directory) # Copies resouces into the workspace directory. These will be deletd later. TODO : Its not a general case that we are in the right directory for this command to work.
        # TODO : Mayneed to put in a double slash test ; replace with one slash incase too many were appended.
        self.scad_file.write('use <scad/BOLTX0004.scad>;\n\n')
        
        
        if (self.type_code=="B1024"): # Example B1024 hardware code : "BOLTX0004-B1024-HEX-L22D10H5"
            
            

            self.bolt_length = self.hardware_code.split("-")[3].split("L")[1].split("D")[0]
            self.head_diameter = self.hardware_code.split("-")[3].split("D")[1].split("H")[0]
            self.head_height =  self.hardware_code.split("-")[3].split("H")[1]
            self.head_shape =  self.hardware_code.split("-")[2]




            """Format Inputs"""

            self.bolt_length = self.bolt_length.replace("P", ".", 1)
            self.head_diameter = self.head_diameter.replace("P", ".", 1)
            self.head_height = self.head_height.replace("P", ".", 1)


            ''' Testing that code is parsed correctly.'''
            print("")
            print("    Parameterization Information")
            print("")
            print("    family_code = "+self.family_code)
            print("    type_code = "+self.type_code)
            print("    bolt_length = "+self.head_diameter+"mm")
            print("    head_height = "+self.head_height+"mm")
            print("    head_shape = "+self.head_shape)
            print("")
            
            ''' Rules logic goes here ; conditions of which parameters combinations can exist.   '''

            ''' Execute write scad functions.   '''

            self.BOLTX0004_B1024()
            self.scad_file.close()
            
        if (self.type_code=="B832"): # Example B832 hardware code : "BOLTX0004-B832-HEX-L22D10H5"
            
            

            self.bolt_length = self.hardware_code.split("-")[3].split("L")[1].split("D")[0]
            self.head_diameter = self.hardware_code.split("-")[3].split("D")[1].split("H")[0]
            self.head_height =  self.hardware_code.split("-")[3].split("H")[1]
            self.head_shape =  self.hardware_code.split("-")[2]


            """Format Inputs"""

            self.bolt_length = self.bolt_length.replace("P", ".", 1)
            self.head_diameter = self.head_diameter.replace("P", ".", 1)
            self.head_height = self.head_height.replace("P", ".", 1)


            ''' Testing that code is parsed correctly.'''
            print("")
            print("    Parameterization Information")
            print("")
            print("    family_code = "+self.family_code)
            print("    type_code = "+self.type_code)
            print("    bolt_length = "+self.head_diameter+"mm")
            print("    head_height = "+self.head_height+"mm")
            print("    head_shape = "+self.head_shape)
            print("")
            
            ''' Rules logic goes here ; conditions of which parameters combinations can exist.   '''

            ''' Execute write scad functions.   '''

            self.BOLTX0004_B832()
            self.scad_file.close()

        elif (self.type_code=="B632"):
            self.bolt_length = self.hardware_code.split("-")[3].split("L")[1].split("D")[0]
            self.head_diameter = self.hardware_code.split("-")[3].split("D")[1].split("H")[0]
            self.head_height =  self.hardware_code.split("-")[3].split("H")[1]
            self.head_shape =  self.hardware_code.split("-")[2]




            """Format Inputs"""

            self.bolt_length = self.bolt_length.replace("P", ".", 1)
            self.head_diameter = self.head_diameter.replace("P", ".", 1)
            self.head_height = self.head_height.replace("P", ".", 1)


            ''' Testing that code is parsed correctly.'''
            print("")
            print("    Parameterization Information")
            print("")
            print("    family_code = "+self.family_code)
            print("    type_code = "+self.type_code)
            print("    bolt_length = "+self.head_diameter+"mm")
            print("    head_height = "+self.head_height+"mm")
            print("    head_shape = "+self.head_shape)
            print("")
            
            ''' Rules logic goes here ; conditions of which parameters combinations can exist.   '''

            ''' Execute write scad functions.   '''

            self.BOLTX0004_B632()
            self.scad_file.close()
            
        if (self.type_code=="B256"):
            self.bolt_length = self.hardware_code.split("-")[3].split("L")[1].split("D")[0]
            self.head_diameter = self.hardware_code.split("-")[3].split("D")[1].split("H")[0]
            self.head_height =  self.hardware_code.split("-")[3].split("H")[1]
            self.head_shape =  self.hardware_code.split("-")[2]




            """Format Inputs"""

            self.bolt_length = self.bolt_length.replace("P", ".", 1)
            self.head_diameter = self.head_diameter.replace("P", ".", 1)
            self.head_height = self.head_height.replace("P", ".", 1)


            ''' Testing that code is parsed correctly.'''
            print("")
            print("    Parameterization Information")
            print("")
            print("    family_code = "+self.family_code)
            print("    type_code = "+self.type_code)
            print("    bolt_length = "+self.head_diameter+"mm")
            print("    head_height = "+self.head_height+"mm")
            print("    head_shape = "+self.head_shape)
            print("")
            
            ''' Rules logic goes here ; conditions of which parameters combinations can exist.   '''

            ''' Execute write scad functions.   '''

            self.BOLTX0004_B256()
            self.scad_file.close()
            
        
        if (self.type_code=="N1024"): # Example N1024 hardware code : BOLTX0004-N1024-HEX-D10H5

            self.head_diameter = self.hardware_code.split("-")[3].split("D")[1].split("H")[0]
            self.head_height =  self.hardware_code.split("-")[3].split("H")[1]
            self.head_shape =  self.hardware_code.split("-")[2]




            """Format Inputs"""

            self.head_diameter = self.head_diameter.replace("P", ".", 1)
            self.head_height = self.head_height.replace("P", ".", 1)


            ''' Testing that code is parsed correctly.'''
            print("")
            print("    Parameterization Information")
            print("")
            print("    family_code = "+self.family_code)
            print("    type_code = "+self.type_code)
            print("    head_height = "+self.head_height+"mm")
            print("    head_diameter = "+self.head_diameter+"mm")
            print("    head_shape = "+self.head_shape)
            print("")
            
            ''' Rules logic goes here ; conditions of which parameters combinations can exist.   '''

            ''' Execute write scad functions.   '''

            self.BOLTX0004_N1024()
            self.scad_file.close()
            
        if (self.type_code=="N832"): # Flywheel adapter.

            self.head_diameter = self.hardware_code.split("-")[3].split("D")[1].split("H")[0]
            self.head_height =  self.hardware_code.split("-")[3].split("H")[1]
            self.head_shape =  self.hardware_code.split("-")[2]


            """Format Inputs"""

            self.head_diameter = self.head_diameter.replace("P", ".", 1)
            self.head_height = self.head_height.replace("P", ".", 1)


            ''' Testing that code is parsed correctly.'''
            print("")
            print("    Parameterization Information")
            print("")
            print("    family_code = "+self.family_code)
            print("    type_code = "+self.type_code)
            print("    head_height = "+self.head_height+"mm")
            print("    head_diameter = "+self.head_diameter+"mm")
            print("    head_shape = "+self.head_shape)
            print("")
            
            ''' Rules logic goes here ; conditions of which parameters combinations can exist.   '''

            ''' Execute write scad functions.   '''

            self.BOLTX0004_N832()
            self.scad_file.close()
            
        if (self.type_code=="N632"): # Axle adapter.

            self.block_unit_length = self.hardware_code.split("-")[2].split("B")[1].split("SR")[0] # Block length.
            self.shaft_radius = self.hardware_code.split("-")[2].split("B")[1].split("SR")[1].replace("P", ".", 1) # Shaft radius.
            self.padding =  "0."+self.hardware_code.split("-")[3].split("PP")[1]
            ''' Rules logic goes here ; conditions of which parameters combinations can exist.   '''
            
            self.block_unit_length = self.block_unit_length.replace("P", ".", 1)
            self.threshaft_radiusad_starts = self.shaft_radius.replace("P", ".", 1)
            
            ''' Testing that code is parsed correctly.'''
            print("")
            print("    Parameterization Information")
            print("")
            print("    famliy_code = "+self.family_code)
            print("    type_code = "+self.type_code)
            print("    block_unit_length = "+self.block_unit_length+"mm")
            print("    shaft_radius = "+self.shaft_radius+"mm")
            print("    padding = "+self.padding+"mm")
            print("")
            
            ''' Execute write scad functions.   '''

            self.BOLTX0004_N632()
            self.scad_file.close()


    def BOLTX0004_B1024(self):
        """_summary_
        """        
        self.scad_file.write('BOLTX0004_B1024( bolt_length = '+self.bolt_length+', head_diameter = '+self.head_diameter+', head_height = '+self.head_height+', head_shape = "'+self.head_shape+'");\n')
   
    def BOLTX0004_B832(self):
        """_summary_
        """        
        self.scad_file.write('BOLTX0004_B832( bolt_length = '+self.bolt_length+', head_diameter = '+self.head_diameter+', head_height = '+self.head_height+', head_shape = "'+self.head_shape+'");\n')

    def BOLTX0004_B632(self):
        """_summary_
        """        
        self.scad_file.write('BOLTX0004_B632( bolt_length = '+self.bolt_length+', head_diameter = '+self.head_diameter+', head_height = '+self.head_height+', head_shape = "'+self.head_shape+'");\n')
        
    def BOLTX0004_N1024(self):
        """_summary_
        """        
        self.scad_file.write('BOLTX0004_N1024( head_diameter = '+self.head_diameter+', head_height = '+self.head_height+', head_shape = "'+self.head_shape+'" );\n')

    def BOLTX0004_N832(self):
        """_summary_
        """        
        self.scad_file.write('BOLTX0004_N832( head_diameter = '+self.head_diameter+', head_height = '+self.head_height+', head_shape = "'+self.head_shape+'" );\n')

    def BOLTX0004_B632(self):
        """_summary_
        """        
        self.scad_file.write('BOLTX0004_B632( head_diameter = '+self.head_diameter+', head_height = '+self.head_height+', head_shape = "'+self.head_shape+'" );\n')


class BOLTX0004_encoding:
    """_summary_
    """    
    def __init__(self):
        self.type_code
        self.system_code
    
    def encode_session(self):
        """_summary_
        """
        #type_code = SelectionBranch("Select CUBX0177 type:")
        #type_code.options.append(["1", "BP", "Box Panel", CUBX0177_BP_input.run])
        #type_code.options.append(["2", "SP", "Simple Panel", exit])
        #type_code.options.append(["3", "SQ", "Square Axle", exit])
        #type_code.options.append(["4", "AA", "Axle Adapter", exit])
        #type_code.options.append(["4", "FA", "Flywheel Adapter", exit])
        #type_code.options.append(["b", "Back", "Navigate to previous menu.", exit])
        
        if (self.type_code=="BPAN"): # Box panel.
            pass
        elif (self.type_code=="SPAN"): # Simple panel.
            pass
        elif (self.type_code=="AXLE"): # Square axle.
            pass
        elif (self.type_code=="FYAD"): # Flywheel adapter.
            pass
        elif (self.type_code=="AXAD"): # Axle adapter.
            pass
        else:
            pass