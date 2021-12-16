# # Group 3 - validation U-Value(Walls, Slabs, Roof)
# 
# This script is elaborated for the course 11034 - Advance Building Information Modelling. 
# 
# The code is written by Bruno Adam and Oswaldo Hernandez. 
# 
# We are not responsible by the relevancy of the values used for this code. The code has been developped for an educational purpose. It can not be used for any commercial purpose.
# 
# The code has to be lauch in the correct folder organisation.

# ### Import packages

# In[1]:


import ifcopenshell
import numpy as np
import pandas as pd


# ### Import model IFC

# In[2]:


model = ifcopenshell.open('model/Duplex_A_201109071.ifc')

project = (model.by_type('IfcProject'))
project_address = model.by_type('IfcPostalAddress')
print('You are working on : ' + project[0].LongName)
print('You are working in : ' + project_address[0].Town)


# ## Menu

# In[ ]:


ifctype = []
print('\n\n Choose by taping <Y> or <N> for Yes or No to the following IfcEntities you want to analyse:')
k = 0
while k == 0:
    IfcWall = str(input('Do you want to validate the IfcRoof?'))
    IfcWallStandardCase = str(input('Do you want to validate the IfcWallStandardCase?'))
    IfcRoof = str(input('Do you want to validate the IfcRoof?'))
    IfcSlab = str(input('Do you want to validate the IfcSlab?'))
    if IfcWall == 'Y':
        ifctype.append('IfcWall')
    if IfcWallStandardCase == 'Y':
        ifctype.append('IfcWallStandardCase')
    if IfcRoof == 'Y':
        ifctype.append('IfcRoof')
    if IfcSlab == 'Y':
        ifctype.append('IfcSlab')
    print('\nThank you, you have chosen to analyse {}'.format(ifctype))
    agree = str(input('Are you agree?<Y> or <N>'))
    if agree == 'Y':
        k=1
    else:
        k=0
print('\n\nCalculations in progress...')


# ### The following has to be activate for upgrading the material bank on excel! 

# In[3]:


# filename_input = 'data_needed.xlsx'
# Material = []
# for material in model.by_type('IfcMaterial'):
#     U_value = input('Enter the thermal conductivity (W/(m.K)) for the Material - '+str(material.Name)+':')
#     Material.append([str(material.Name), U_value])
# Material = pd.DataFrame(Material, columns = ['Material Name','Thermal conductivity (W/(m.K))'])

# with pd.ExcelWriter(filename_input, mode='a', if_sheet_exists = 'replace') as writer:  
#     Material.to_excel(writer, sheet_name='Lambda', index=False, float_format="%.2f")


# ## (Module) Get the U-values from IFC model
# You need to get a material bank with the thermal conductivity of different materials.
# Run this module before all the others! 

# In[3]:


def get_uvalue(globalid, model, Material, Rsi=0.12, Rso=0.06):
    th_rest = Rsi + Rso
    for entity in model.by_id(globalid).MaterialLayers:
        th_cond = float(Material[np.where(Material == str(entity.Material.Name))[0][0]][1])
        if th_cond != 0:
            th_rest = th_rest + (entity.LayerThickness / th_cond)
        else:
            th_rest = th_rest
    U_value = 1/th_rest
    return(U_value)


# ## (Module) Get the data from ifc_model
# 
# Import an model (ifc) and the R_si and R_so from the input file to calculate the U-value depending on the layers thickness and materials (also in input file).

# In[4]:


def get_data(ifc_entity, R_boundaries, model, Material):
    data_ifctype = []
    for entity in model.by_type(ifc_entity):
        if ifc_entity == 'IfcRoof':
            for relAssociatesMaterial in entity.HasAssociations:
                for MaterialLayerSet in relAssociatesMaterial.RelatingMaterial:
                    if (type(MaterialLayerSet) is not str) and (type(MaterialLayerSet) is not float):
                        mat_identity = MaterialLayerSet.id()
            isexternal = True
            data_entity = [entity.GlobalId, entity.Name, isexternal, mat_identity]
            data_ifctype.append(data_entity)
        if ifc_entity == 'IfcSlab':
            if entity.PredefinedType == 'FLOOR':
                for relAssociatesMaterial in entity.HasAssociations:
                    for MaterialLayerSet in relAssociatesMaterial.RelatingMaterial:
                        if (type(MaterialLayerSet) is not str) and (type(MaterialLayerSet) is not float):
                            mat_identity = MaterialLayerSet.id()
                for prop in entity.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties:
                    if prop.Name == 'IsExternal':
                        isexternal = prop.NominalValue.wrappedValue
                    if 'Ext' in entity.Name:
                        isexternal = True
                data_entity = [entity.GlobalId, entity.Name, isexternal, mat_identity]
                data_ifctype.append(data_entity)
            else: 
                data_entity = [entity.GlobalId, entity.Name, 'NaN', 'NaN']#Exclude the roof 
        else: 
            for relAssociatesMaterial in entity.HasAssociations:
                for MaterialLayerSet in relAssociatesMaterial.RelatingMaterial:
                    if (type(MaterialLayerSet) is not str) and (type(MaterialLayerSet) is not float):
                        mat_identity = MaterialLayerSet.id()
            for prop in entity.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties:
                if prop.Name == 'IsExternal':
                    isexternal = prop.NominalValue.wrappedValue
                if 'Ext' in entity.Name:
                    isexternal = True
            data_entity = [entity.GlobalId, entity.Name, isexternal, mat_identity]
            data_ifctype.append(data_entity)
    data_ifctype = np.asarray(data_ifctype)
    # Calculation of U_values
    U_value = []
    X = len(data_ifctype)
    for entity in range(X):
            if ifc_entity == 'IfcWallStandardCase':
                Rsi = R_boundaries[1][1]
                Rso = R_boundaries[1][2]
                U_value.append(get_uvalue(int(data_ifctype[entity][3]),model,Material,Rsi=Rsi,Rso=Rso))
            if ifc_entity == 'IfcWall':
                Rsi = R_boundaries[1][1]
                Rso = R_boundaries[1][2]
                U_value.append(get_uvalue(int(data_ifctype[entity][3]),model,Material,Rsi=Rsi,Rso=Rso))
            if ifc_entity == 'IfcSlab':
                Rsi = R_boundaries[2][1]
                Rso = R_boundaries[2][2]
                U_value.append(get_uvalue(int(data_ifctype[entity][3]),model,Material,Rsi=Rsi,Rso=Rso))
            if ifc_entity == 'IfcRoof':
                Rsi = R_boundaries[0][1]
                Rso = R_boundaries[0][2]
                U_value.append(get_uvalue(int(data_ifctype[entity][3]),model,Material,Rsi=Rsi,Rso=Rso))
    data_ifctype = pd.DataFrame(data_ifctype, columns = ['GlobalID', 'Name', 'IsExternal', 'ID Material'])
    data_ifctype.insert(4,'U value(W/(m2.K))',U_value)
    return (data_ifctype)


# ## (Module) verification U-values comparing with the input file
# 
# run this module after the module "get_data"

# In[5]:


def get_target(ifc_entity, br18_uvalue, data_ifctype):
    BR18_target = []
    BR18_verif = []
    ind_ext = data_ifctype.columns.get_loc('IsExternal')
    ind_uval = data_ifctype.columns.get_loc('U value(W/(m2.K))')
    raw_data = data_ifctype.values
    M = len(data_ifctype)
    for k in range(M):
        external = raw_data[k][ind_ext]
        if ifc_entity == 'IfcWallStandardCase':
            requirement = float(br18_uvalue[1][0])
        if ifc_entity == 'IfcWall':
            requirement = float(br18_uvalue[1][0])
        if ifc_entity == 'IfcRoof':
            requirement = float(br18_uvalue[1][2])
        if ifc_entity == 'IfcSlab':
            requirement = float(br18_uvalue[1][1])
        if external == 'True':
            uvalue = float(raw_data[k][ind_uval])
            if uvalue <= requirement:
                BR18_verif.append('Good')
            if uvalue > requirement:
                BR18_verif.append('Not good')
        if external == 'True':
            BR18_target.append(requirement)
        if external != 'True':
            BR18_verif.append(' ')
            BR18_target.append(' ')
    
    data_ifctype.insert(5, 'BR18 requirement', BR18_target)
    data_ifctype.insert(6, 'BR18 is Respected', BR18_verif)
    return(data_ifctype)


# ## (Module) export .xlsx
# This module import the values from the file "input" to verify the u-value.
# Run this file after the module "get_target".

# In[6]:


def uvalue_excel(model, ifc_entity, file_input, file_output):
    #import values
    br18_uvalue = pd.read_excel(file_input, sheet_name='U_value', header = None)
    R_boundaries = pd.read_excel(file_input, sheet_name='R_boundaries', header = 0)
    Material = pd.read_excel(file_input, sheet_name='Lambda', header = None)
    Material = np.asarray(Material)
    R_boundaries = R_boundaries.values
    for ifctype in ifc_entity:
        # Calculations
        data_type = get_data(ifctype, R_boundaries, model, Material)
        # Verifications
        table = get_target(ifctype, br18_uvalue, data_type)
        with pd.ExcelWriter(file_output, mode='a', if_sheet_exists = 'replace', engine ='openpyxl') as writer:  
            table.to_excel(writer, sheet_name=ifctype, index =False, float_format="%.2f")


# ## Export Excel - U value verification
# 
# Select IfcEntities that you want to explore in the vector "ifctype".

# In[7]:


filename_input = 'input/data_needed.xlsx'
filename_output = 'output/uvalue_validation.xlsx'

uvalue_excel(model, ifctype, filename_input, filename_output)

print('\n\n\nYour excel file is ready to be explored! \nVerify the file to know which elements you have to modify to be correct with BR18.')

