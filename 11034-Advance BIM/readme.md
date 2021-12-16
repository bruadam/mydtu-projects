# Group 3 : Validation U-values for Wall, Roof, Slab in an IFC file

## Table of contents

[TOC]

## Introduction

The following tool has been developped for the course [11034 : Advance Building Information Modelling](https://kurser.dtu.dk/course/11034) given by [Tim Pat McGinley](https://orbit.dtu.dk/en/persons/tim-pat-mcginley) at DTU. 

The tool adresses a specific BIM use case[^3] 

For instance, this tool is used for Energy Code Validation[^1] according to BR18. In a nutshell,  the tool provides an excel file which shows if the walls, slabs and roof fullfill the BR18 U-values requirements from IfcMaterialLayerSet data. It uses the thickness and the material to calculate the results.

---

## Forewords

The tool developped requires an input file which containts three sheets: 

- *Lambda* :  containing a material bank with respective [**thermal conductivity**][2] expressed in *W/(m.K)* 
- *U_value* : containing some BR18 U-values requirements[^4] for Walls, Roofs and Slabs. This U_value are found on this reference.
- *R_boundaries* : containing the [thermal resistances][1] on surface used to calculated the U_values.

The input file path should be like this `input/data_needed.xlsx`. 

Moreover, the following script ( commented on `main.py`) could help you to complete the thermal conductivity of active materials in the IFC file. 

```python
filename_input = 'data_needed.xlsx'
Material = []
for material in model.by_type('IfcMaterial'):
    U_value = input('Enter the thermal conductivity (W/(m.K)) for the Material - '+str(material.Name)+':')
    Material.append([str(material.Name), U_value])
Material = pd.DataFrame(Material, columns = ['Material Name','Thermal conductivity (W/(m.K))'])

with pd.ExcelWriter(filename_input, mode='a', if_sheet_exists = 'replace') as writer:  
    Material.to_excel(writer, sheet_name='Lambda', index=False, float_format="%.2f")
```

This tool was developped on the file **Duplex Appartment 201109071.ifc**. store with this file path `model/Duplex_A_201109071.ifc`. The tool could not be suited with other IFC files.

The tool has been developped on python 3.9. 

---

## Step-by-step	

1. Read the Forewords below.

2. Your input file is ready. You can now run `main.py` with python[^2]

3. You have to go through the menu to select the IfcEntities you want to validate.

   ```properties
   Choose by taping <Y> or <N> for Yes or No to the following IfcEntities you want to analyse:
   
   Do you want to validate the IfcRoof?Y
   
   Do you want to validate the IfcWallStandardCase?Y
   
   Do you want to validate the IfcRoof?Y
   
   Do you want to validate the IfcSlab?Y
   
   Thank you, you have chosen to analyse ['IfcWall', 'IfcWallStandardCase', 'IfcRoof', 'IfcSlab']
   
   Are you agree?<Y> or <N>Y
   ```

4. While running:

   ```properties
   Calculations in progress...
   ```

   1. The tool calculates the U_values for *IfcWallStandardCas, IfcWall, IfcRoof and IfcSlab*
   2. The tool writes some basic information to help identify every elements  (*GlobalID, Name*).
   3. The tool compares the U_values calculated with BR18 which is corresponding with the values written on the input file.
   4. The tool exports to excel in 4 sheets corresponding to the 4 IfcEntities.
   5. The command prompt displays:

   ```properties
   Your excel file is ready to be explored! 
   Verify the file to know which elements you have to modify to be correct with BR18.
   ```

5. You can now open the excel file `output/uvalue_validation.xlsx`

6. Finally, you can verify on the different sheet in the column **BR18 is Respected** if the IfcEntities respect BR18.

Note that different values are present on this column: 

- **Good** means that the IfcEntity verified the U_value
- **Not Good** means that you have to improve the U_value.
- *No value* means that this IfcEntity is written on an indicative basis. BR18 does not provide any requirements for this IfcEntity which often is an indoor partition.

The following table shows an overview of the results for *IfcWall*:

| GlobalID               | Name                                                         | IsExternal | IDMaterial | U value(W/(m2.K)) | BR18 requirement | BR18 is Respected |
| ---------------------- | ------------------------------------------------------------ | ---------- | ---------- | ----------------- | ---------------- | ----------------- |
| 2O2Fr$t4X7Zf8NOew3FNld | Basic Wall:Interior - Partition (92mm Stud):138584           | False      | 4202       | 2,85              |                  |                   |
| 2O2Fr$t4X7Zf8NOew3FNbT | Basic Wall:Party Wall - CMU Residential Unit Dimising Wall:139234 | True       | 4360       | 0,32              | 0,3              | Not Good          |

Congratulation for using the tool. 

The tool is developped to be easy to use. However, a good understanding of what happens behind the code is required. Some values and results might be inacccurate for some debugging reasons. 

---

## Future development

In the future development of this tool, we noticed different possible improvements. First, it might be interessant to include IfcDoors and IfcWindows in the process. Second, it might be useful to reach a next level by combining this tool with the unfinished development of our early-stage energy analysis[^1] to provide a documented feedback for the architects during the conception phase. This step has to resolte the geometry complexity of *ifcopenshell*. 

## Acknowledgement

This part is written to thank Ann-Britt Vejlgaard, Andrei-Cornel Danet and Tim Pat McGinley. 



## Legal

This tool has been developped by Bruno Marc J Adam (s212672) and Oswaldo Domingo Hernandez Bueno (s210361) , students in Architectural Engineering at the Technical University of Denmark (DTU) for the Fall 2021.

The tool should not be used for commercial purpose. 





[1]: https://www.firstinarchitecture.co.uk/a-quick-and-easy-guide-to-u-values	"A Quick and Easy Guide to U-Values"
[2]: https://material-properties.org/thermal-conductivity-of-materials/	"Thermal Conductivity of Materials | Material Properties"



[^1]: Mea culpa : normally, we were supposed to do an energy analysis use case. We were simulating a early-stage design energy simulation from IfcSpace data. However, this tools requires more information that we could not acquire. We decided to stop our modelling to a simple U-value calculation which belongs to a **Code Validation Use Case** and not anymore a Energy Analysis.
[^2]: You need to install this python modules[pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/), [ifcopenshell](http://www.ifcopenshell.org/)
[^4]: Ralph G Kreider and John I Messner, *The Uses of BIM Classifying and Selecting BIM Uses*, 2013, <http://bim.psu.edu>
[^3]: *Energy Requirements of BR18 A quick guide for the construction industry on the Danish Building Regulations 2018*, 2018, <https://byggeriogenergi.dk/media/2237/br18_uk.pdf>, accessed on 5. Dec 2021.



