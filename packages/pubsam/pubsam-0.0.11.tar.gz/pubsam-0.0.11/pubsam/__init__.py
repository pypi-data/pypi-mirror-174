from rdkit import Chem
from rdkit.Chem import Draw
import requests
from rdkit.Chem import MACCSkeys 
from rdkit.Chem import AllChem
from rdkit.Chem import rdmolops
from base64 import b64decode
from rdkit import DataStructs
from rdkit.Chem import Draw
from PIL import Image
from IPython.display import display
from rdkit.Chem.AtomPairs import Pairs
from rdkit.Chem.Fingerprints import FingerprintMols
#from rdkit.Chem import MCS
from rdkit.Chem import rdFMCS
from IPython.display import Image 
from mordred import WienerIndex
from mordred import ZagrebIndex
import pandas as pd 
#from rdkit import MCS
import statsmodels as sm 
from mordred import Calculator, descriptors
import matplotlib.pyplot as plt
from rdkit.Chem import rdFMCS 
def PCFP_BitString(pcfp_base64) :

    pcfp_bitstring = "".join( ["{:08b}".format(x) for x in b64decode( pcfp_base64 )] )[32:913]
    return pcfp_bitstring

from rdkit import Chem

def bioactiveity_active_cid__inactive_cid_smliarity(e):
    ########################################find description link sids #####################################################
    sc=[]
    print("This code find active and inactive substance for given assay they it measure the smilarity between these inactive and active substance")

    description= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+"/description/xml"
    print("Here is link descript your entery assay ")
    print("")
    print(description)
    print("")
    #print("Here is list of substances are active in your assay ")
    print("")
    ########################################find active sids #####################################################

    active= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?sids_type=active"
    url=requests.get(active)
    cidactive= (url.text.split())
    #print(cids)
    ########################################find inactive sids #####################################################
    inactive= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?sids_type=inactive"
    url=requests.get(inactive)
    cidinactive= (url.text.split())
    ########################################find active Fingerprint2D #####################################################
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    str_cid = ",".join([ str(x) for x in cidactive])
    url = prolog + "/compound/cid/" + str_cid + "/property/Fingerprint2D/txt"
    res = requests.get(url)
    Fingerprint2Dactive = res.text.split()
    ########################################find inactive Fingerprint2D #####################################################
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    str_cid = ",".join([ str(x) for x in cidinactive])
    url = prolog + "/compound/cid/" + str_cid + "/property/Fingerprint2D/txt"
    res = requests.get(url)
    Fingerprint2Dinactive = res.text.split()
    ########################################find inactive & active snilarity score #####################################################

    for i in range(len(Fingerprint2Dactive)):
            for j in range(len(Fingerprint2Dinactive)) :
                fps1=(DataStructs.CreateFromBitString(PCFP_BitString(Fingerprint2Dactive[i])))
                fps2=(DataStructs.CreateFromBitString(PCFP_BitString(Fingerprint2Dinactive[j])))
                score = DataStructs.FingerprintSimilarity(fps1, fps2)
                print("active cid", cidactive[i], "vs.", "inactive", cidinactive[j], ":", round(score,3), end='')
                sc.append(str(score))
                    ########################################draw active structure #####################################################
                print("")

                print("Active molecule structure")
                print("")
                w1="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+ cidactive[i] +"/property/isomericsmiles/txt"
                res1 = requests.get(w1)
                img1 = Chem.Draw.MolToImage( Chem.MolFromSmiles( res1.text.rstrip() ), size=(200, 100)) 
                display(img1)

    ########################################draw inactive structure #####################################################
                print("Inactive molecule structure")
                print("")
                w2="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+ cidinactive[j] +"/property/isomericsmiles/txt"
                res2 = requests.get(w2)
                
                img2 = Chem.Draw.MolToImage( Chem.MolFromSmiles( res2.text.rstrip() ), size=(200, 100) )
                display(img2)
    ########################################print inactive & active snilarity score #####################################################

                if ( score >= 0.85 ):
                    print(" ****")
                elif ( score >= 0.75 ):
                    print(" ***")
                elif ( score >= 0.65 ):
                    print(" **")
                elif ( score >= 0.55 ):
                    print(" *")
                else:
                    print(" ")
    return
#bioactiveity_active__inactive_smliarity(1000)

    ########################################find description link sids #####################################################
def assay_aid_to_active_cid_common_substracture(e):

    study= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(1000)+ "/cids/txt?sids_type=active"
    url=requests.get(study)
    cids= (url.text.split())
        #print(cidactive)
    str_cid = ",".join([ str(x) for x in cids])
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str_cid + "/property/IsomericSMILES/txt"
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    str_cid = ",".join([ str(x) for x in cids])

    url = prolog + "/compound/cid/" + str_cid + "/property/isomericsmiles/txt"
    res = requests.get(url)
    ms = res.text.split()
        #print(smiles)
        ########################################find active sids #####################################################

    ms = res.text.split()
    ms = list(map(rdkit.Chem.MolFromSmiles, ms))
    i = Chem.Draw.MolsToGridImage(ms, subImgSize=(400,400))
    r = MCS.FindMCS(ms, threshold=0.5)
    display(i)
    #rdkit.Chem.Draw.MolToImage(r.queryMol, size=(400,400))
    res = MCS.FindMCS(ms, threshold=0.7)
    ii= Chem.MolFromSmarts(res.smarts)
    Chem.MolFromSmarts(res.smarts)
    display(ii)
    return
#find_active_sids_for_aid(180)

    ########################################find description link sids #####################################################
def assay_aid_to_inactive_cid_common_substracture(e):

    study= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(1000)+ "/cids/txt?sids_type=inactive"
    url=requests.get(study)
    cids= (url.text.split())
        #print(cidactive)
    str_cid = ",".join([ str(x) for x in cids])
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str_cid + "/property/IsomericSMILES/txt"
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    str_cid = ",".join([ str(x) for x in cids])

    url = prolog + "/compound/cid/" + str_cid + "/property/isomericsmiles/txt"
    res = requests.get(url)
    ms = res.text.split()
        #print(smiles)
        ########################################find active sids #####################################################

    ms = res.text.split()
    ms = list(map(rdkit.Chem.MolFromSmiles, ms))
    i = Chem.Draw.MolsToGridImage(ms, subImgSize=(400,400))
    r = MCS.FindMCS(ms, threshold=0.5)
    display(i)
    #rdkit.Chem.Draw.MolToImage(r.queryMol, size=(400,400))
    res = MCS.FindMCS(ms, threshold=0.7)
    ii= Chem.MolFromSmarts(res.smarts)
    Chem.MolFromSmarts(res.smarts)
    display(ii)
    return
#find_active_sids_for_aid(180)#find_active_sids_for_aid(100)
def assay_aid_to_cid_active(e):
    e=str(e)
    url= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?cids_type=active"

    return url

def assay_aid_to_cid_inactive(e):
    e=str(e)
    url= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?cids_type=inactive"
    return url
#assay_aid_to_cid_inactive(1000)

def compound_smile_to_morgan_atom_topological(a,b): 
    ms = [Chem.MolFromSmiles(a), Chem.MolFromSmiles(b)]
    fig=Draw.MolsToGridImage(ms[:],molsPerRow=2,subImgSize=(400,200))
    display(fig)
    from rdkit.Chem.AtomPairs import Pairs
    from rdkit.Chem import AllChem
    from rdkit.Chem.Fingerprints import FingerprintMols
    from rdkit import DataStructs

    radius = 2

    fpatom = [Pairs.GetAtomPairFingerprintAsBitVect(x) for x in ms]
    fpatom = [Pairs.GetAtomPairFingerprintAsBitVect(x) for x in ms]

    print("atom pair score: {:8.4f}".format(DataStructs.TanimotoSimilarity(fpatom[0], fpatom[1])))
    fpmorg = [AllChem.GetMorganFingerprint(ms[0],radius,useFeatures=True),
              AllChem.GetMorganFingerprint(ms[1],radius,useFeatures=True)]
    fptopo = [FingerprintMols.FingerprintMol(x) for x in ms]
    print("morgan score: {:11.4f}".format(DataStructs.TanimotoSimilarity(fpmorg[0], fpmorg[1])))
    print("topological score: {:3.4f}".format(DataStructs.TanimotoSimilarity(fptopo[0], fptopo[1])))
    return
#compound_smile_to_morgan_atom_topological("CCO","CNCN")
def show_csv_file(a):# show csv file 
  import pandas as pd        # import the Python Data Analysis Library with the shortened name pd
  df = pd.read_csv(a) # read in the file into a pandas dataframe
  (df)
  return df
#show_csv_file("ahmed.csv")
def plot_from_csv_file(file_name, xscat,yscat,xla,yla):#plot from csv file
    df = pd.read_csv(file_name) # read in the file into a pandas dataframe
    plt.scatter(xscat, yscat)     # plot of boiling point (in K) vs molecular weight
    plt.xlabel(xla)
    plt.ylabel(yla)
    plt.show()
    return 
#plot_from_csv_file("ahmed.csv",df.MolecularWeight,df.XLogP, 'Wiener Index', 'Boiling Point in Kelvin')

# Adding descriptors to the dataset

def Add_Wiener_Z1_Z2_to_dataset(file_name, SMILE_row):## Adding descriptors to the dataset and then get csv file with your new adding

  df = pd.read_csv(file_name) # read in the file into a pandas dataframe

  wiener_index = WienerIndex.WienerIndex()               # create descriptor instance for Wiener index
  zagreb_index1 = ZagrebIndex.ZagrebIndex(version = 1)            # create descriptor instance for Zagreb index 1
  zagreb_index2 = ZagrebIndex.ZagrebIndex(version = 2)            # create descriptor instance for Zagreb index 1
  result_Wiener= []
  result_Z1= []
  result_Z2= []

  for index, row in df.iterrows():                # iterate through each row of the CSV data
      SMILE = row[SMILE_row]                       # get SMILES string from row
      mol = Chem.MolFromSmiles(SMILE)             # convert smiles string to mol file
      result_Wiener.append(wiener_index(mol))     # calculate Wiener index descripter value
      result_Z1.append(zagreb_index1(mol))        # calculate zagreb (Z1) descriptor value
      result_Z2.append(zagreb_index2(mol))        # calculate zagreb (Z2) descriptor value

  df['Wiener'] = result_Wiener           # add the results for WienerIndex to dataframe
  df['Z1'] = result_Z1                   # add the results for Zagreb 1 to dataframe
  df['Z2'] = result_Z2                   # add the results for Zagreb 2 to dataframe
  df
  file= df.to_csv('file1.csv')# it will save automatically 
  return file
######################
def Mulitple_regression_analysis_csv_file_using_statsmodels(file_name, a,*d):# Mulitple_regression_analysis_using_statsmodels
  #a=dependent variable
  #*d=independent variables
  df = pd.read_csv(file_name) # read in the file into a pandas dataframe

  strrl=[]
  a=str(a)
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      #print("s")
      x=str(x)
      strrl.append(x)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        strrl.append(str(m)) 
  X = df[strrl]   # select our independent variables
  X = sm.add_constant(X)                 # add an intercept to our model
  y = df[[a]]                       # select BP as our dependent variable
  model = sm.OLS(y,X).fit()              # set up our model
  predictions = model.predict(X)         # make the predictions
  print(model.summary())                 # print out statistical summary
  return                  # print out statistical summary
#Mulitple_regression_analysis_using_statsmodels("BP.CSV","BP_C", ["MW","BP_C"])

################################
def Delete_Substruct(Substruct,*d):
  from rdkit import Chem
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      #print("s")
      x=str(x)
      strrl.append(x)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        #print(6)
        strrl.append(str(m)) 
  #print(strrl,"ll")
  de=[]
  if len(strrl)>0:
    for i in strrl:
      m = Chem.MolFromSmiles(i)
      patt = Chem.MolFromSmarts(Substruct)
      rm = AllChem.DeleteSubstructs(m,patt)
      de.append(Chem.MolToSmiles(rm))
      #print(Chem.MolToSmiles(rm))
  mol=[]
  print(de)
  for i in de:
        m = Chem.MolFromSmiles(i)
        mol.append(m)
  return mol
#CD=Delete_Substruct('O=C1:C2:C:C:C:C:C:2:S:N:1C1:C:C:C:C:C:1',smiles)
#print(m)
#f#or i in CD:
  #m=Draw.MolToImage(i)
  #display(m)
#Delete_Substruct('C(=O)[OH]','CC(=O)O', 'CC(=O)')



def has_Substruct_or_not(Substruct,*d):
  
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      #print("s")
      x=str(x)
      strrl.append(x)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        #print(6)
        strrl.append(str(m)) 
  #print(strrl)
  de=[]
  if len(strrl)>0:
    for i in strrl:
      m = Chem.MolFromSmiles(i)
      patt = Chem.MolFromSmarts(Substruct)
      rm=m.HasSubstructMatch(patt)
      de.append(rm)
      #print(rm)
  return de

#print(has_Substruct_or_not('C(=O)[OH]','CC(=O)O', 'CC(=O)'))

def Maximum_common_substructure(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      #print("s")
      x=str(x)
      strrl.append(x)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        #print(6)
        strrl.append(str(m)) 
  mols=[]
  for i in strrl:
      mol = Chem.MolFromSmiles(i)
      mols.append(mol)

  if len(mols)>0:
    r = rdFMCS.FindMCS(mols, threshold=0.9)
    m1 = Chem.MolFromSmarts(r.smartsString)
    #print(m1)
  return m1
#m1=(Maximum_common_substructure(smiles))
#print(m1)
#m= Draw.MolToImage(m1, legend="MCS1")
#m
def structure_picture_by_smile(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      #print("s")
      x=str(x)
      strrl.append(x)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        #print(6)
        strrl.append(str(m)) 
    for i in strrl:
        #print(i)
        m = Chem.MolFromSmiles(i)
        Draw.MolToMPL(m,(200,200)).show()
    return m
#structure_picture_by_smile(smiles)#structure_picture_by_smile("CN","CO")



def draw_list_of_smile(smiles_list):
    mol_list = [Chem.MolFromSmiles(smiles) for smiles in smiles_list]
    m=Chem.Draw.MolsToGridImage(mol_list)
    #print(m)
    return (m)
#draw_list_of_smile( [ 'C', 'CC', 'CCC', 'CCCC', 'CCCCC', 'C1CCCCC1' ])
from rdkit import Chem
from rdkit import Chem
def find_hybridization(*d):
    
    strrl=[]
    for x in d:
        #print(x)
        if type(x) is str:
          #print("s")
          x=str(x)
          strrl.append(x)

        elif type(x) is int:
          #print("n")
          x=str(x)
          strrl.append(x)
        elif type(x) is list:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)
        else:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)


    #print(strrl)
    Hybridization=[]

    mols=[]
   # print(type(f))
   # print(f)
    for i in strrl:
        #print(i)
        m = Chem.MolFromSmiles(i)
        for x in m.GetAtoms():
            value= (x.GetIdx(), x.GetHybridization())
            Hybridization.append(value)
    return (Hybridization)
#k=["CN","CO","CCN","CC","CCO","CCN"]
#m="CC","CCCC","CC","CCCCC","CC","CCCC"
#l="CN"

#(find_hybridization(k,l,m))

def view_difference_two_smiles(mol1, mol2):
    mol1 = Chem.MolFromSmiles(mol1)
    mol2 = Chem.MolFromSmiles(mol2)
    mcs = rdFMCS.FindMCS([mol1,mol2])
    mcs_mol = Chem.MolFromSmarts(mcs.smartsString)
    match1 = mol1.GetSubstructMatch(mcs_mol)
    target_atm1 = []
    for atom in mol1.GetAtoms():
        if atom.GetIdx() not in match1:
            target_atm1.append(atom.GetIdx())
    match2 = mol2.GetSubstructMatch(mcs_mol)
    target_atm2 = []
    for atom in mol2.GetAtoms():
        if atom.GetIdx() not in match2:
            target_atm2.append(atom.GetIdx())
    return Draw.MolsToGridImage([mol1, mol2],highlightAtomLists=[target_atm1, target_atm2])
#mol1 = ('CCO')
#mol2 = ('CN')
#view_difference_two_smiles(mol1, mol2)
#view_difference(mol1,mol2)
def multiple_list_to_one_list(d):
  flat_list = []
  for sublist in d:
      for item in sublist:
          flat_list.append(item)
  return (flat_list)
