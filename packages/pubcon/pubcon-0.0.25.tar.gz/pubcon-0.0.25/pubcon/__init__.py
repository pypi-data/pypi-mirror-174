import requests
import time 
def help():
  print("Here are several conversion function to use these function follow these instruction \n ")
  print("You should know what domain  do you have Ex: if you have compound name whcih is water \n ")
  print("You should know what domain <namespace> do you have Ex: if have cid compound whcih is 964d \n ")
  print("You should know what domain <operation specification> do you have Ex: do you want get property for water\n ")
  print("In this case you write in your code \n")
  print( "compound_cid_to_property(water)"" \n ")
  print("You can see all function avaialbe in this package in this following google sheet link ")
  print("https://docs.google.com/spreadsheets/d/1Lc6dTcneR2KLtnT3zkLMn7jPOlFOznIy/edit?usp=sharing&ouid=118019681680310111518&rtpof=true&sd=true")
#help()


"""### **General function which allows fro user to choose their output formal and operation and operation options**"""

#ne or more cid to properties cvs file
def generalpubchemconversion(inputsoecification, inputoperationsoecification,operationsoecification , outputwithoperationoption,*d):
  #input soecification,You have input formula and you want to get other formula ex compound, substance..assay, .....

  #input domain: type of your input identifer Ex cid or aid or sid, fastsmilarity...

  #input soecification: convert to other formula Ex record, description, assaysummary, sids, cids,aids,synonyms....
  #operation:
  #output with operation option Ex: xml, cvs,png,....
  #*input data: Ex list of cid, aid,sid, name,smiles, formula molecule........
  w=str(inputsoecification)
  p=str(inputoperationsoecification)
  h=str(operationsoecification)
  ut=str(outputwithoperationoption)
  #print(type(d))
  strrl=[]# to save list to make one file
  for x in d:
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
          #print(x)
          strrl.append(x)
    else:
      #print("l")
      for m in x:
          x=str(m)
          #print(x)
          strrl.append(x)

      
  f= ",".join(strrl)
  a   = w +"/"+ p +"/"+ f+"/"+h+'/' + ut
  url     = str("https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + a)
  return url
#print(generalpubchemconversion("compound" ,"cid","sids","xml","180"))



"""**compound name conversion**"""

#ne or more cid to properties cvs file
def compound_name_to_property(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)

  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "property/Title,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey,IUPACName,XLogP,ExactMass,MonoisotopicMass,TPSA,Complexity,Charge,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,IsotopeAtomCount,AtomStereoCount,DefinedAtomStereoCount,UndefinedAtomStereoCount,BondStereoCount,DefinedBondStereoCount,UndefinedBondStereoCount,CovalentUnitCount,Volume3D,XStericQuadrupole3D,YStericQuadrupole3D,ZStericQuadrupole3D,FeatureCount3D,FeatureAcceptorCount3D,FeatureDonorCount3D,FeatureAnionCount3D,FeatureCationCount3D,FeatureRingCount3D,FeatureHydrophobeCount3D,ConformerModelRMSD3D,EffectiveRotorCount3D,ConformerCount3D,Fingerprint2D" + '/' + "CSV"
          url.append(ur)
  return url
#print(compound_name_to_property("water",'buatne'))



def compound_name_to_record(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)

  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record" + '/' + "xml"
          url.append(ur)
  return url
#print(compound_name_to_record(["water",'buatne']))
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/record/xml

def compound_name_to_synonym(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
          url.append(ur)
  return url
#print(compound_name_to_synonym(['water','octanol']))
#['https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/synonyms/xml', 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/buatne/synonyms/xml']

def compound_name_to_aid(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
          url.append(ur)
  return url
#print(compound_name_to_aid("water",'butane'))
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/aids/xml

def compound_name_to_assaysummary(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m) 
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "assaysummary" + '/' + "xml"
          url.append(ur)

  return url

#compound_name_to_assaysummary()

def compound_name_to_classification(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "classification" + '/' + "xml"
          url.append(ur)
  return url


#print(compound_name_to_classification(['water','butane']))
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/classification/xml

def compound_name_to_description(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
          url.append(ur)
  return url

#compound_name_to_description(['water','butane'])

def compound_name_to_sid(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
          url.append(ur)
  return url
#compound_name_to_sid()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/sids/xml

def compound_name_to_cid(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids" + '/' + "txt"
          url.append(ur)
  return url
#compound_name_to_cid()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/cids/xml



def compound_name_to_conformer(*d):

  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
        strrl.append(m)

    
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "conformers" + '/' + "xml"
          url.append(ur)
  return url
#k=["water","butane"]
#m="octnaol","butanol"
#n="methanol"

#compound_name_to_conformer(n,m,k)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/conformers/xml

def compound_name_to_png(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
      #print(1)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        strrl.append(m)

  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/name/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "png"
          url.append(ur)
  return url
#k=["water","butane"]
#m="octnaol","butanol"
#n="methanol"

#compound_name_to_png(k,m,n)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/png



"""## **compound cid conversion**"""

#ne or more cid to properties cvs file
def compound_cid_to_property(*d):
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
        strrl.append(m) 
  url=[]
  for x in strrl:
          x=str(x)
          #print(x)
          pugin   = "compound/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "property/Title,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey,IUPACName,XLogP,ExactMass,MonoisotopicMass,TPSA,Complexity,Charge,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,IsotopeAtomCount,AtomStereoCount,DefinedAtomStereoCount,UndefinedAtomStereoCount,BondStereoCount,DefinedBondStereoCount,UndefinedBondStereoCount,CovalentUnitCount,Volume3D,XStericQuadrupole3D,YStericQuadrupole3D,ZStericQuadrupole3D,FeatureCount3D,FeatureAcceptorCount3D,FeatureDonorCount3D,FeatureAnionCount3D,FeatureCationCount3D,FeatureRingCount3D,FeatureHydrophobeCount3D,ConformerModelRMSD3D,EffectiveRotorCount3D,ConformerCount3D,Fingerprint2D" + '/' + "CSV"
          url.append(ur)
  return url
#k=["180","940"]
#m="180","940"
#l="180"
#compound_cid_to_property(k,m,l)

def compound_cid_to_record(*d):
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
        strrl.append(m) 

  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "compound/cid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record" + '/' + "xml"
  return url
#k=["180","940"]
#m="200","300"
#l="500"
#compound_cid_to_record(m,k,l)
#compoundcidtorecord()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,964/record/xml



def compound_cid_to_synonym(*d):
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
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        strrl.append(m) 
  url=[]
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "compound/cid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
  return url
#k=["180","940"]
#m="200","300"
#l="500"
#compound_cid_to_synonym(m,k,l)

#compound_cid_to_synonym()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,964/synonyms/xml





def compound_cid_to_sid(*d):
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
    else:
      for m in x:
        strrl.append(m) 
  url=[]
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "compound/cid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
  return url

#compound_cid_to_sid()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180/sids/xml

def compound_cid_to_aid(*d):
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
        strrl.append(m) 
  url=[]
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "compound/cid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
  return url


#compound_cid_to_assay()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,964/assaysummary/xml
def compound_cid_to_png(*d):
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
        strrl.append(m) 
  url=[]
  for f in strrl:
    pugin   = "compound/cid/" + f
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "png" 
    url.append(ur)
  return url


#compound_cid_to_assay()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,964/assaysummary/xml

def compound_cid_to_classification(*d):
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
        strrl.append(m) 
  url=[]
  for f in strrl:
    pugin   = "compound/cid/" + f
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "classification" + '/' + "xml"
    url.append(ur)
  return url

#compound_cid_to_classification()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180/classification/xml

def compound_cid_to_description(*d):
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
        strrl.append(m) 
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "compound/cid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
  return url
#A=["100","200"]
#B="300","400"
#C="500"
#print(compound_cid_to_description(A,B,C))
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/190,180/description/xml

def compound_cid_to_conformer(*d):
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
        strrl.append(m) 
  url=[]
  if len(strrl)>0:
    
    f= ",".join(strrl)
    pugin   = "compound/cid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "conformers" + '/' + "xml"
  return url

#compound_cid_to_conformer()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,190=/conformers/xml

"""### **compound smile**"""

def compound_smile_to_record(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "record" + '/' + "xml"
          url.append(ur)
  return url
#k=["CN",'CO']
#m="CN",'CO'
#l="CN"
#compound_smile_to_record(k,m,l)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/cco/record/xml





def compound_smile_to_synonym(*d):
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "synonyms" + '/' + "xml"
          url.append(ur)
  return url
#print(compounds_smile_to_synonym(["CO",'CN']))
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/co/synonyms/xml



def compound_smile_to_sid(*d):
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "sids" + '/' + "txt"
          url.append(ur)
  return url

#compound_smile_to_sid()

def compound_smile_to_cid(*d):
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "cids" + '/' + "txt"
          print(url)
          url.append(ur)
  return url

#compound_smile_to_cid()

def compound_smile_to_aid(*d):
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "aids" + '/' + "txt"
          #print(url)
          url.append(ur)
  return url
#compound_smile_to_aid("CO", "CN","CCC")
#compound_smile_to_aid()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/co/aids/xml

def compound_smile_to_assaysummary(*d):
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "assaysummary" + '/' + "xml"
          #print(url)
          url.append(ur)
  return url
#compound_smile_to_assaysummary()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/co/assaysummary/xml



def compound_smile_to_classification(*d):
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "classification" + '/' + "xml"
          #print(url)
          url.append(ur)
  return url

#compound_smile_to_classification()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/co/classification/xml

def compound_smile_to_description(*d):
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "description" + '/' + "xml"
          #print(url)
          url.append(ur)
  return url

#compound_smile_to_description()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/co/description/xml

def compound_smile_to_conformer(*d):
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "conformers" + '/' + "xml"
          #print(url)
          url.append(ur)
  return url

#compound_smile_to_conformer()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/co/description/xml

def compound_smile_to_png(*d):
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
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
  url=[]
  if len(strrl)>0:
      for x in strrl:
          pugin   = "compound/smiles/" + str(x)
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "png"
          #print(url)
          url.append(ur)
  return url

#compound_smile_to_png()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/co/png



"""### ***fastidentity ***"""

def compound_fastidenity_cid_to_cid(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastidentity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids/txt"
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"

#compound_fastidenity_cid_to_cid(k,m,l)# accept one cid pers request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

#{smiles | smarts | inchi | sdf | cid}



def compound_fastidenity_cid_to_sid(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastidentity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids/txt"
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"

#compound_fastidenity_cid_to_sid(k,m,l)# accept one cid pers request



#compoundfastidenitycidtosid()# accept one cid pers request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

#{smiles | smarts | inchi | sdf | cid}

#@title Default title text
def compound_fastsimilarity_2dcid_Threshold95(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastidentity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/cids/txt?Threshold=95'
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"


#compound_fastsimilarity_2dcid_Threshold95()#one cid per requests
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/190/cids/txt?Threshold=95
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/180/cids/txt?Threshold=95
def compound_fastidenity_cid_to_aid(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastidentity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/aids/txt'
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"
#compound_fastidenity_cid_to_aid()

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

#{smiles | smarts | inchi | sdf | cid}

def compound_fastidenity_cid_to_assaysummary(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastidentity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/assaysummary/xml'
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"
#compound_fastidenity_cid_to_assaysummary(k,m,l)


#compoundfastidenitycidtoassaysummary()# accept one cid pers request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

#{smiles | smarts | inchi | sdf | cid}

def compound_fastidenity_cid_to_synonym(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastidentity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/synonyms/xml'
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"
#compound_fastidenity_cid_to_synonym(k,m,l)

#compoundfastidenitycidtosynonyms()# accept one cid pers request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

#{smiles | smarts | inchi | sdf | cid}

"""### **fastsimilarity_2d **"""
def compound_fastsimilarity_3d_to_cid(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_2d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/synonyms/txt'
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"

#compound_fastsimilarity_3d_to_cid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_2d_to_sid(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_2d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/sids/txt'
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"
#compound_fastsimilarity_2d_to_sid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_2d_to_aid(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_2d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/aids/txt'
          url.append(ur)
  return url

#compound_fastsimilarity_2d_to_aid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_2d_to_record(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_2d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/record/xml'
          url.append(ur)
  return url

#compound_fastsimilarity_2d_to_record()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_2d_to_synonym(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_2d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/synonyms/xml'
          url.append(ur)
  return url

#compound_fastsimilarity_2d_to_synonym()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_2d_to_description(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_2d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/description/xml'
          url.append(ur)
  return url
#compound_fastsimilarity_2d_to_description()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_2d_to_conformer(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_2d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/conformers/xml'
          url.append(ur)
  return url

#compound_fastsimilarity_2d_to_conformer()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml



"""### **fastsimilarity_3d **"""

def compound_fastsimilarity_3d_to_sid(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_3d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/sids/txt'
          url.append(ur)
  return url


#compound_fastsimilarity_3d_to_sid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_3d_to_aid(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_3d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/aids/txt'
          url.append(ur)
  return url
#k=["1","2"]
#l="3","4"
#m="5"
#compound_fastsimilarity_3d_to_aid(k,l,m)#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml





def compound_fastsimilarity_3d_to_record(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_3d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/record/xml'
          url.append(ur)
  return url
#k=["1","2"]
#l="3","4"
#m="5"
#compound_fastsimilarity_3d_to_record(k,l,m)#one per request

#compound_fastsimilarity_3d_to_record()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml



def compound_fastsimilarity_3d_to_synonym(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_3d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/synonyms/xml'
          url.append(ur)
  return url


#compound_fastsimilarity_3d_to_synonym()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_3d_to_description(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_3d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/description/xml'
          url.append(ur)
  return url

#compound_fastsimilarity_3d_to_description()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsimilarity_3d_to_conformer(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/fastsimilarity_3d/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +'/conformers/xml'
          url.append(ur)
  return url

#compound_fastsimilarity_3d_to_conformer()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

"""### **compound identity cid **"""

#ne or more cid to properties cvs file#################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def compound_identity_cid_to_property(*d):
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
        strrl.append(str(m)) 

  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/identity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "property/Title,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey,IUPACName,XLogP,ExactMass,MonoisotopicMass,TPSA,Complexity,Charge,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,IsotopeAtomCount,AtomStereoCount,DefinedAtomStereoCount,UndefinedAtomStereoCount,BondStereoCount,DefinedBondStereoCount,UndefinedBondStereoCount,CovalentUnitCount,Volume3D,XStericQuadrupole3D,YStericQuadrupole3D,ZStericQuadrupole3D,FeatureCount3D,FeatureAcceptorCount3D,FeatureDonorCount3D,FeatureAnionCount3D,FeatureCationCount3D,FeatureRingCount3D,FeatureHydrophobeCount3D,ConformerModelRMSD3D,EffectiveRotorCount3D,ConformerCount3D,Fingerprint2D" + '/' + "CSV"
          url.append(ur)
  return url

#compound_identity_cid_to_property()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/BPGDAMSIGCZZLK-UHFFFAOYSA-N/SDF

def compound_identity_cid_to_description(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/identity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +"description/xml"
          url.append(ur)
  return url

#compound_identity_cid_to_description(180)



def compound_identity_cid_to_conformer(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/identity/cid/" +x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +"conformers/xml"
          url.append(ur)
  return url   

#compound_identity_cid_to_conformer()

def compound_identity_cid_to_sid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/identity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +"sids/txt"
          url.append(ur)
  return url

#compound_identity_cid_to_sid()# accept one cid pers request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

def compound_identity_cid_to_aid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/identity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +"aids/txt"
          url.append(ur)
  return url

#compound_identity_cid_to_aid()# accept one cid pers request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

def compound_identity_cid_to_synonym(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/identity/cid/" + x
          ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +"synonyms/xml"
          url.append(ur)
  return url

#compound_identity_cid_to_synonym()# accept one cid pers request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

def compound_identity_cid_to_assaysummary(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/identity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +"assaysummary/xml"
          url.append(ur)
  return url          

#compound_identity_cid_to_assaysummary()# accept one cid pers request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/180/cids/xml

def compound_identity_cid_to_cid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
          pugin   = "compound/identity/cid/" + x
          ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +"cids/txt"
          url.append(ur)
  return url
#k=["1","2"]
#m="3","4"
#l="5"
#compound_identity_cid_to_cid(k,m,l)#one per request

#compound_identity_cid_to_cid()#one request

"""# **compound inchikey**"""

def compound_inchikey_to_record(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record/xml" 
    url.append(ur)
  return url
#k=["XLYOFNOQVPJJNP-UHFFFAOYSA-N","XLYOFNOQVPJJNP-UHFFFAOYSA-N"]
#m="XLYOFNOQVPJJNP-UHFFFAOYSA-N","XLYOFNOQVPJJNP-UHFFFAOYSA-N"
#l="v"
#compound_inchikey_to_record(k,m,l)#one per request
#compoundinchikeytorecord()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N/record/xml/xml



def compound_inchikey_to_synonyms(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms/xml" 
    url.append(ur)
  return url
#k=["XLYOFNOQVPJJNP-UHFFFAOYSA-N","XLYOFNOQVPJJNP-UHFFFAOYSA-N"]
#m="XLYOFNOQVPJJNP-UHFFFAOYSA-N","XLYOFNOQVPJJNP-UHFFFAOYSA-N"
#l="v"
#compound_inchikey_to_synonyms(k,m,l)#one per request

#compound_inchikey_to_synonyms()#many inchikey per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N/synonyms/xml



def compound_inchikey_to_sid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids/txt" 
    url.append(ur)
  return url

#compound_inchikey_to_sid()#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N,XLYOFNOQVPJJNP-UHFF/sids/xml

def compound_inchikey_to_aid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids/txt" 
    url.append(ur)
  return url

#compound_inchikey_to_aid()#many inchikey per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N,IJDNQMDRQITEOD-UHFFFAOYSA-N/aids/xml





def compound_inchikey_to_assaysummary(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "assaysummary/xml" 
    url.append(ur)
  return url

#compound_inchikey_to_assaysummary()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N/assaysummary/xml



def compound_inchikey_to_cid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids/txt" 
    url.append(ur)
  return url


#compound_inchikey_to_cid()#many inchikey per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N,IJDNQMDRQITEOD-UHFFFAOYSA-N/cids/xml

def compound_inchikey_to_classification(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "classification/xml" 
    url.append(ur)
  return url
#compound_inchikey_to_classification()#<Details>Output of classifications is not currently supported for multiple CIDs</Details>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N/classification/xml

def compound_inchikey_to_description(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description/xml" 
    url.append(ur)
  return url

#compound_inchikey_to_description()# many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N,XLYOFNOQVPJJNP-UHFF/description/xml

def compound_inchikey_to_conformer(*d):
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
        strrl.append(str(m)) 
  url=[]
  for x in strrl:
          #print(x)
    pugin   = "compound/inchikey/" + x
    ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "conformers/xml" 
    url.append(ur)

  return url

#compound_inchikey_to_conformer()# one per reqesut
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/XLYOFNOQVPJJNP-UHFFFAOYSA-N/conformers/xml





"""### **compound_substructure_to**"""

def compound_substructure_to_sid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
              pugin   = "compound/substructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
              url.append(ur)

  return url


#compound_substructure_to_cid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid//cids/xml

def compound_substructure_to_aid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
              pugin   = "compound/substructure/cid/" + i
              ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "xml"
              url.append(ur)

  return url

def compound_substructure_to_record(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
              pugin   = "compound/substructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record" + '/' + "xml"
              url.append(ur)
  return url

#compound_substructure_to_record()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_substructure_to_synonyms(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
              pugin   = "compound/substructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
              url.append(ur)
  return url


#compound_substructure_to_synonyms()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_substructure_to_description(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
              pugin   = "compound/substructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
              url.append(ur)
  return url

#compoundsubstructuretodescription()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_substructure_to_conformer(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
              pugin   = "compound/substructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "conformers" + '/' + "xml"
              url.append(ur)
  return url

#compound_substructure_to_conformer()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_substructure_to_cids(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
              pugin   = "compound/substructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids" + '/' + "txt"
              url.append(ur)
  return url

#compound_substructure_to_cids()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml



"""### **cell**

"""

def cell_cellacc_to_aid(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  print(strrl)
  for x in strrl:
    pugin   = "cell/cellacc/" + str(x)
    ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  'aids/' + "txt"
    url.append(ur)
  return url
#cell_cellacc_to_aid(k,l,m)#<Message>operation `aids` only supports for one entry a time</Message>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/cellacc/CVCL_0045/aids/xml

def cell_cellacc_to_summary(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  print(strrl)
  for x in strrl:
    pugin   = "cell/cellacc/" + str(x)
    ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  'summary/' + "xml"
    url.append(ur)
  return url

#cell_cellacc_to_summary()#many callacc per time
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/cellacc/CVCL_0045,CVCL_0045/summary/xml

def cell_synonym_to_aids(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  print(strrl)
  for x in strrl:
    pugin   = "cell/synonym/" + x
    ur  = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  'aids/' + "txt"
    url.append(ur)
  return url

#cell_cellacc_to_aids() #<Message>operation `aids` only supports for one entry a time</Message>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/synonym/HeLa/aids/xml

def cell_synyom_to_summary(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  print(strrl)
  for x in strrl:
    pugin   = "cell/synonym/" + x
    ur  = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  'summary/' + "xml"
    url.append(ur)
  
  return url

#cellsynyomtoaid() #<Message>operation `aids` only supports for one entry a time</Message>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/synonym/HeLa/aids/xml

def cell_synyom_to_aids(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  print(strrl)
  for x in strrl:
    pugin   = "cell/synonym/" + x
    ur  = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  'aids/' + "txt"
    url.append(ur)
    return url

#cellsynyomtosummary() #<`synonym` only supports one entry a time>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/synonym/HeLa/aids/xml

"""### **taxonomy**"""

def taxonomy_taxid_to_summary(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  print(strrl)
  for x in strrl:
    if len(strrl)>0:
      f= ",".join(strrl)
      pugin   = "taxonomy/taxid/" + f
      url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "summary/xml"
    # print(url)
  return url
#k=["1","2"]
#l="3","4"
#m="5"
#taxonomy_taxid_to_summary(k,l,m)# support mnny entery
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/taxid/9606,9606/summary/xml

def taxonomy_taxid_to_aid(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:

      pugin   = "taxonomy/taxid/" + i
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "aids/txt"
      url.append(ur)
  return url

#taxonomy_taxid_to_aid() #operation `aids` only supports for one entry a time
##https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/taxid/9606/aids/xml

def taxonomy_synonym_to_summary(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  print(strrl)
  url=[]
  for i in strrl:

      pugin   = "taxonomy/taxid/" + i
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  "summary/xml"
      url.append(ur)
  return url
  
#taxonomy_synonym_to_summary()#idNamespace `synonym` only supports one entry a time
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/synonym/9606/summary/xml

def taxonomy_synonym_to_aid(*d):#done
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
        strrl.append(str(m)) 
  for f in strrl:
    pugin   = "taxonomy/synonym/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' +  'aids/' + "txt"
    #print(url)
  return url


#taxonomy_synonym_to_aid()#<Message>idNamespace `synonym` only supports one entry a time</Message>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/synonym/9606/aids/xml

"""### *pathway*"""


def pathway_pwacc_to_summary(*d):#done
  print(4)
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
        strrl.append(str(m)) 
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "pathway/pwacc" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/'  + "/summary/JSON"
    #print(url)
  return url
#pathway_pwacc_to_summary(k,l,m)# support many enter per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983//summary/JSON



def pathway_pwacc_to_accessions(*d):#done
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
        strrl.append(str(m)) 
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "pathway/pwacc" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/'  + "/accessions/JSON"
    #print(url)
  return url


#pathway_pwacc_to_accessions("Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983","pathway_pwacc_to_accessions")#many per requests
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983//accessions/JSON

def pathway_pwacc_to_aid(*d):#done
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
        strrl.append(str(m)) 
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "pathway/pwacc/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/'  + "geneids/txt"
  #  print(url)
  return url

#pathwaypwacctogeneids()#many per requests
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983,Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983//geneids/JSON

def pathway_pwacc_to_cid(*d):#done
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
        strrl.append(str(m)) 
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "pathway/pwacc/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/'  + "cids/txt"
    #print(url)
  return url

#pathwaypwacctocids()#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983,Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983/cids/JSON

"""### **substance **"""

#ne or more cid to properties cvs file
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/123656,123656//xml

def substance_sid_to_synonym(*d):#done
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
        strrl.append(str(m)) 
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "substance/sid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
   # print(url)
  return url

#substancessidtosynonym()#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/123656,123656/synonyms/txt

def substance_sid_to_record(*d):
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
        strrl.append(str(m)) 
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "substance/sid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record" + '/' + "xml"
    #print(url)
  return url

#substancessidtorecord()#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/123656,123656/record/xml

def substance_sid_to_cid(*d):#done
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
        strrl.append(str(m)) 
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "substance/sid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids" + '/' + "txt"
    #print(url)
  return url

#substancessidtocid()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/53789435/cids/xml

def substance_sid_to_description(*d):#<Message>There is no longer a formal description for substances.</Message>

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
        strrl.append(str(m)) 
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "substance/sid/" + f
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#substancesidtodescription()
##https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/123656,123656/description/xml

def substance_sid_to_classification(*d):#done
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
        strrl.append(str(m)) 
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "substance/sid/" + f
      ur   = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "classification" + '/' + "xml"
      url.append(ur)
  return url

#substancesidtoclassification()#<Details>Output of classifications is not currently supported for multiple SIDs</Details>

def substance_sid_to_assaysummary(*d):#done
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
        strrl.append(str(m)) 
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "substance/sid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "assaysummary" + '/' + "xml"
   # print(url)
  return url

#substancesidtoassaysummary()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/123656,123656/assaysummary/xml

def substance_sid_to_sid(*d):
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
        strrl.append(str(m)) 
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "substance/sid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
   # print(url)
  return url

#substancesidtosid()#

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/123656,123656/sids/xml

#ne or more cid to properties cvs file#######################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def substance_sourceid_to_cid(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
      pugin   = "substance/sourceid/" + i
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids" + '/' + "txt"
      url.append(ur)
  return url

#substancesourceidtocid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/cids/txt

def substance_sourceid_to_synonym(*d):
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
        strrl.append(str(m)) 
  url=[]
  for i in strrl:
      pugin   = "substance/sourceid/" + i
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
      url.append(ur)
  return url

#substancessourceidtosynonyms()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/synonyms/txt

def substance_sourceid_to_record(*d):
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
        strrl.append(str(m))
  url=[]
 
  for i in strrl:
      pugin   = "substance/sourceid/" + i
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record" + '/' + "xml"
     # print(url)
      url.append(ur)
  return url
#substance_sourceid_to_record(k,l,m)#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/record/xml

"""# *protein** **"""

def protein_accession_to_summary(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:
  
    f= ",".join(strrl)
    pugin   = "protein/accession/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "summary" + '/' + "xml"
    #print(url)
  return url

#proteinaccessiontosummary()#many per request
##https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/P00533,P01422/summary/JSON

def protein_accession_to_aid(*d):#donedoesnt work
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
        strrl.append(str(m))
  url=[]
  for x in strrl:
  
    pugin   = "protein/accession/" + x
    ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
    url.append(ur)
  return url

#proteinaccessiontoaids() #operation `aids` only supports for one entry a time
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/P00533,P01422/summary/JSON

def protein_accession_to_concise(*d):#done
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    f= ",".join(strrl)
  

    if type(x) is int:
      #print("n")
      x=str(x)
      strrl.append(x)
    f= ",".join(strrl)


    if type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          #print(x)
          strrl.append(x)
  if len(strrl)>0:
  
    f= ",".join(strrl)
    pugin   = "protein/accession/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "concise" + '/' + "xml"
    #print(url)
  return url

#proteinaccessiontoconcise()#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/P01422/concise/xml

def protein_gi_to_summary(*d):#done
  strrl=[]# to save compound name to retrive link date later

  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    f= ",".join(strrl)
  

    if type(x) is int:
      #print("n")
      x=str(x)
      strrl.append(x)
    f= ",".join(strrl)


    if type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          #print(x)
          strrl.append(x)
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "protein/gi/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "summary" + '/' + "xml"
    #print(url)
  return url

#proteingitosummary()#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/gi/116516899,116516899/summary/xml

def protein_gi_to_aid(*d):#done
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
        strrl.append(str(m))
  url=[]
  for x in strrl:
  
    pugin   = "protein/gi/" + x
    ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
    url.append(ur)
  return url

#proteingitoaid()#operation `aids` only supports for one entry a time</Message>
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/gi/116516899/aids/xml

def protein_gi_to_concise(*d):#done
  strrl=[]# to save compound name to retrive link date later

  #print(type(d))
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
  url=[]
  for x in strrl:
    pugin   = "protein/gi/" + x
    ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "concise" + '/' + "xml"
    url.append(ur)
  return url

#protein_gi_to_concise("116516899","116516899")#<Message>operation `concise` only supports for one entry a time</Message>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/gi/116516899,116516899/concise/xml

def protein_synonym_to_aid(*d):#done
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
        strrl.append(str(m))
  url=[]
  for x in strrl:
    pugin   = "gene/synonym/" + x
    ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
    url.append(ur)
  return url

#proteinsynonymtoaids()#<Message>idNamespace `synonym` only supports one entry a time</Message>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/EGFR/aids/xml

def protein_synonym_to_summary(*d):#done
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
        strrl.append(str(m))
  url=[]
  for x in strrl:
    pugin   = "gene/synonym/" + x
    ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "summary" + '/' + "xml"
    url.append(ur)
  return url
#protein_synonym_to_summary()
#proteinsynonymtosummary()#<Message>idNamespace `synonym` only supports one entry a time</Message>
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/EGFR/summary/xml

"""### ***gene***"""

def gene_symbol_to_summary(*d):#done
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
        strrl.append(str(m))

  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "gene/genesymbol/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "summary" + '/' + "xml"
   # print(url)
  return url

#genegenesymboltosummary()#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR,EGFR/summary/xml

def gene_symbol_to_aid(*d):#done
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
        strrl.append(str(m))
  url=[]
  for x in strrl:
      pugin   = "gene/genesymbol/" + x
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
      url.append(ur)
  return url

#genegenesymboltoaid()#<Message>operation `aids` only supports for one entry a time</Message>

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/53789435/synonyms/TXT

"""### **assay**"""

def assay_target_gi_to_sid(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "assay/target/gi/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +  '/' + "sids/txt"
  return url

#assaytargetgitosid()#Assay record retrieval is limited to 10000 SIDs
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/gi/116516899,116516899/sids/xml

def assay_target_protein_name_to_record(*d):#done$$$$$$$$$$$$$$$$$$$$$$$$###############################
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
        strrl.append(str(m))
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "assay/target/proteinname" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/'  + "xml"
    #print(url)
  return url

#assaytargetproteinnametorecord()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/proteinname/mevalonatekinase,mevalonatekinase//xml

def assay_target_geneid_to_record(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "assay/target/geneid" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin  +  '/' + "xml"
    #print(url)
  return url

#assaytargetgeneidtorecord()#many per requests
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/geneid/1956,1956//xml

def assay_target_gene_symbol_xml(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "assay/target/genesymbol/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +  '/' + "xml"
  return url
##assaytargetgenesymbolxml()#many per requests
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/genesymbol/EGFR,EGFR//xml



def assay_type_all_to_description(*d): #done##################@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/all/" + f
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#assaytypealltodescription()

def assay_type_confirmatory_to_description(*d):#done##################@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/confirmatory/" + f
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#assaytypeconfirmatorytodescription()


def assay_type_doeresponse_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/doseresponse/" + f
      ur   = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)

  return url

#assaytypedoeresponsetodescription()

def assay_type_onhold_to_description(*d):#done##################@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/onhold/" + f
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#assaytypeonholdtodescription()



def assay_type_panel_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/panel/" + f
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#assaytypepaneltodescription()

def assay_type_rnai_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/rnai/" + f
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#assaytypernaitodescription()

def assay_screening_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/screening/" + f
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)  
  return url

#assayscreeningtodescription()

def assay_type_summary_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/summary/" + f
      ur   = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)  
  return url

#assaytypesummarytodescription()

def assay_type_biochemmical_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/biochemical/" + f
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)  
  return url

#assaytypesummarytodescription()

def assay_type_invivo_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/invivo/" + f
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#assaytypeinvivotodescription()

def assay_type_invitro_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/invitro/" + f
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#assaytypeinvitrotodescription()

def assay_type_active_concentrationspecified_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/type/activeconcentrationspecified/" + f
      ur   = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)
  return url

#assaytypeactiveconcentrationspecifiedtodescription()

def assay_activeity_to_date(*d):#done
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/activity/" + f
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "date" + '/' + "xml"
      url.append(ur)
  return url

#assayactiveitytodate()###No assays found with the given activity name

def assay_sourceall_to_sid(*d):#done
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/sourceall/" + f
      ur   = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
      url.append(ur)

  return url

#assaysourcealltosid()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/sourceall/DTP.NCI/sids/xml

def assay_aid_to_cid(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:
      f= ",".join(strrl)
      pugin   = "assay/aid/" + f
      url  = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids" + '/' + "txt"
  return url

#assay_aid_to_cid(980,1000)#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000,964/cids/xml






def assay_aid_to_target_proteinGI(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:

      f= ",".join(strrl)
      pugin   = "assay/aid/" + f
      url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "targets/ProteinGI,ProteinName,GeneID,GeneSymbol" + '/' + "xml"
      print(url)
  return 

#assay_aid_to_target_proteinGI(1000,980)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000,2548//targets/ProteinGI,ProteinName,GeneID,GeneSymbol/xml

def assay_aid_to_record(*d):#done#Full-record Retrieval
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      f= ",".join(strrl)

      pugin   = "assay/aid/" + f
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/record/'  + "xml"
      url.append(ur)
  return url

#assay_aid_to_record(1000,980)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/100,200/xml

def assay_aid_to_concise(*d):#done#Full-record Retrieval$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      print("s")
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
  url=[]
  if len(strrl)>0:
      f= ",".join(strrl)
      pugin   = "assay/aid/" + f
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + "/concise/xml"
      url.append(ur)
  return (url)

#assay_aid_to_concise(1000)

#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/100,2000/concise/xml

def assay_aid_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      f= ",".join(strrl)
      pugin   = "assay/aid/" + f
      ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
      url.append(ur)

  return url

#print(assay_aid_to_description(['1188', '1495714']))#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/100,200/description/xml



def assay_aid_to_doseresponse(*d):#done
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
    for f in strrl:
      pugin   = "assay/aid/" + f
      ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "doseresponse" + '/' + "xml"
      url.append(ur)
  return url

#assay_aid_to_doseresponse(1000,988)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000/doseresponse/xml

def assay_aid_to_sid(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "assay/aid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
    #print(url)
  return url

#assay_aid_to_sid((1000,980))#many per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000,980/sids/xml






def assay_aid_to_ProteinGI_ProteinName_GeneID_GeneSymbol(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "assay/aid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "/targets/ProteinGI,ProteinName,GeneID,GeneSymbol" + '/' + "xml"
  #  print(url)#many per request
  return url

#assay_aid_to_ProteinGI_ProteinName_GeneID_GeneSymbol(1000,968)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000,986//targets/ProteinGI,ProteinName,GeneID,GeneSymbol/xml

"""# compound formula 


"""

#ne or more cid to properties cvs file
def compound_fastformula_to_property(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
        pugin   = "compound/fastformula/" + f
        ur  = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "property/Title,Molecularformula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey,IUPACName,XLogP,ExactMass,MonoisotopicMass,TPSA,Complexity,Charge,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,IsotopeAtomCount,AtomStereoCount,DefinedAtomStereoCount,UndefinedAtomStereoCount,BondStereoCount,DefinedBondStereoCount,UndefinedBondStereoCount,CovalentUnitCount,Volume3D,XStericQuadrupole3D,YStericQuadrupole3D,ZStericQuadrupole3D,FeatureCount3D,FeatureAcceptorCount3D,FeatureDonorCount3D,FeatureAnionCount3D,FeatureCationCount3D,FeatureRingCount3D,FeatureHydrophobeCount3D,ConformerModelRMSD3D,EffectiveRotorCount3D,ConformerCount3D,Fingerprint2D" + '/' + "CSV"
        url.append(ur)
  return url

#print(compound_fastformula_to_property("CH4"))
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/BPGDAMSIGCZZLK-UHFFFAOYSA-N/SDF

def compound_fastformula_to_synonym(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
        pugin   = "compound/fastformula/" + f
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
        url.append(ur)
  return url

#compoundfastformulatosynonyms()

def compound_fastformula_to_sid(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
        pugin   = "compound/fastformula/" + f
        ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
        url.append(ur)
  return url

#compoundfastformulatosids()

def compound_fastformula_to_aid(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
        pugin   = "compound/fastformula/" + f
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
        url.append(ur)
  return url

#compoundfastformulatoaid()

def compound_fastformula_to_assaysummary(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
          pugin   = "compound/fastformula/" + f
          ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "assaysummary" + '/' + "xml"
          url.append(ur)
  return url

#compoundfastformulatoassaysummary()

def compound_fastformula_to_classification(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
        pugin   = "compound/fastformula/" + f
        ur   = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "classification" + '/' + "xml"
        url.append(ur)
  return url

#compoundfastformulatoclassification()

def compound_fastformula_to_description(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
        pugin   = "compound/fastformula/" + f
        ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
        url.append(ur)
  return url

#print(compound_fastformula_to_description("CH4"))


def compound_fastformula_to_dconformer(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
        pugin   = "compound/fastformula/" + f
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "conformers" + '/' + "xml"
        url.append(ur)
  return url

#compoundfastformulatodconformer()

"""## **fast search

### **fastsubstructure
"""

def compound_fastsubstructure_to_cid(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
        pugin   = "compound/fastsubstructure/cid/" + f
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids" + '/' + "txt"
        url.append(ur)
  return url

#compoundfastsubstructuretocid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsubstructure_to_aid(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
              pugin   = "compound/fastsubstructure/cid/" + f
              ur   = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
              url.append(ur)
  return url

#compoundfastsubstructuretoaid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsubstructure_to_record(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for f in strrl:
              pugin   = "compound/fastsubstructure/cid/" + f
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsubstructuretorecord()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsubstructure_to_synonym(*d):
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
        strrl.append(str(m))
  url=[]
  if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/fastsubstructure/cid/" + i
              ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsubstructuretosynonym()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsubstructure_to_description(*d):
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
        strrl.append(str(m))
  url=[]

  if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/fastsubstructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsubstructuretodescription()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsubstructure_to_conformer(*d):
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
        strrl.append(str(m))
  url=[]

  if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/fastsubstructure/cid/" + i
              ur   = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "conformers" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsubstructuretoconformer()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

"""### **fastsuperstructure**"""

def compound_fastsubstructure_to_cid(*d):
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
        strrl.append(str(m))
  url=[]

  if len(strrl)>0:
      for f in strrl:
                pugin   = "compound/fastsubstructure/cid/" + f
                ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids" + '/' + "xml"
                url.append(ur)
  return url

#compoundfastsubstructuretocid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml





def compound_fastsuperstructure_to_aid(*d):
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
        strrl.append(str(m))
  url=[]

  if len(strrl)>0:
    for i in strrl:
                pugin   = "compound/fastsuperstructure/cid/" + i
                ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
                url.append(ur)
  return url

#compoundfastsuperstructuretoaid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml





def compound_fastsuperstructure_to_sid(*d):
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
        strrl.append(str(m))
  url=[]

  if len(strrl)>0:
    for i in strrl:
              pugin   = "compound/fastsuperstructure/cid/" + i
              ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
              url.append(ur)
  return url

#compoundfastsuperstructuretosid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml



def compound_fastsuperstructure_to_synonym(*d):
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
        strrl.append(str(m))
  url=[]

  if len(strrl)>0:

    for i in strrl:
              pugin   = "compound/fastsuperstructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsuperstructuretosynonym( )#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml





def compound_fastsuperstructure_to_record(*d):
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
        strrl.append(str(m))
    url=[]

    if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/fastsuperstructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsuperstructuretorecord()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_fastsuperstructure_to_description(*d):
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
        strrl.append(str(m))
    url=[]

    if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/fastsuperstructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsuperstructuretodescription()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml



def compound_fastsuperstructure_to_assaysummary(*d):
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
        strrl.append(str(m))
    url=[]

    if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/fastsuperstructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "assaysummary" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsuperstructuretoassaysummary()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

"""### **structure search**"""

def compound_superstructure_to_aid(*d):
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
        strrl.append(str(m))
    url=[]

    if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/superstructure/cid/" + i
              ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt"
              url.append(ur)
  return url

#compoundsuperstructuretoaid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml



def compound_superstructure_to_sid(*d):
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
        strrl.append(str(m))
    url=[]

    if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/superstructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
              url.append(ur)
  return url

#compoundsuperstructuretosid()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml





def compound_superstructure_to_synonym(*d):
  strrl=[]# to save compound name to retrive link date later

  #print(type(d))
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
    url=[]

    if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/superstructure/cid/" + i
              ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
              url.append(ur)
  return url

#compoundfastsuperstructuretosynonym()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml



def compound_superstructure_to_record(*d):
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
        strrl.append(str(m))
    url=[]

    if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/superstructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record" + '/' + "xml"
              url.append(ur)
  return url

#compoundsuperstructuretorecord()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml



def compound_superstructure_to_description(*d):
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
        strrl.append(str(m))
    url=[]
    if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/superstructure/cid/" + i
              ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
              url.append(ur)
  return url

#compoundsuperstructuretodescription()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

def compound_superstructure_to_assaysummary(*d):
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
        strrl.append(str(m))
    url=[]
  url=[]

  if len(strrl)>0:
      for i in strrl:
              pugin   = "compound/superstructure/cid/" + i
              ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "assaysummary" + '/' + "xml"
              url.append(ur)
  return url

#compoundsuperstructuretoassaysummary()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/180/cids/xml

"""inchi # **compound inchi **"""

#ne or more cid to properties cvs file
def compound_inchikey_to_property(*d):
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
        strrl.append(str(m))
      
  f= ",".join(strrl)
  pugin   = "compound/inchi/" + f
  url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "property/Title,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey,IUPACName,XLogP,ExactMass,MonoisotopicMass,TPSA,Complexity,Charge,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,IsotopeAtomCount,AtomStereoCount,DefinedAtomStereoCount,UndefinedAtomStereoCount,BondStereoCount,DefinedBondStereoCount,UndefinedBondStereoCount,CovalentUnitCount,Volume3D,XStericQuadrupole3D,YStericQuadrupole3D,ZStericQuadrupole3D,FeatureCount3D,FeatureAcceptorCount3D,FeatureDonorCount3D,FeatureAnionCount3D,FeatureCationCount3D,FeatureRingCount3D,FeatureHydrophobeCount3D,ConformerModelRMSD3D,EffectiveRotorCount3D,ConformerCount3D,Fingerprint2D" + '/' + "CSV"
    #print(url)
  return url

#compoundinchikeytoproperty()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/BPGDAMSIGCZZLK-UHFFFAOYSA-N/SDF

def compound_listkey_to_record(*d):
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
        strrl.append(str(m))
      
  f= ",".join(strrl)
  pugin   = "compound/inchi/" + f
  url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "record/xml" + '/' + "xml"
    #print(url)
  return url

#compoundlistkeytorecord()



def compound_listkey_to_synonym(*d):
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
        strrl.append(str(m))
      
  f= ",".join(strrl)
  pugin   = "compound/inchi/" + f
  url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "synonyms" + '/' + "xml"
    #print(url)  
  return url

#compoundlistkeytosynonym()

def substance_sourceid_to_cid(*d):#done
  strrl=[]# to save list to make one file
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
    url=[]
    if len(strrl)>0:
      for i in strrl:
        pugin   = "substance/sourceid/" + i
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids" + '/' + "txt"
        url.append(ur)
  return url

#substancesourceidtocids()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/cids/xml

def substance_sourceid_to_descritption(*d):#done
  strrl=[]# to save list to make one file
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
    url=[]
    if len(strrl)>0:
      for i in strrl:
        pugin   = "substance/sourceid/" + i
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "description" + '/' + "xml"
        url.append(ur)
  return url

#substancesourceidtodescritption()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/description/xml

def substance_sourceid_to_classification(*d):#done
  strrl=[]# to save list to make one file
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
    url=[]
    if len(strrl)>0:
      for i in strrl:
        pugin   = "substance/sourceid/" + i
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "classification" + '/' + "xml"
        url.append(ur)
  return url

#substancesourceidtoclassification()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/classification/xml

def substance_sourceid_to_assaysummary(*d):#done
  strrl=[]# to save list to make one file
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
    url=[]
    if len(strrl)>0:
      for i in strrl:
        pugin   = "substance/sourceid/" + i
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "assaysummary" + '/' + "xml"
        url.append(ur)
  return url

#substancesourceidtoassaysummary()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/assaysummary/xml

def substance_ssourceid_to_sids(*d):
  strrl=[]# to save list to make one file
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
    url=[]
    if len(strrl)>0:
      for i in strrl:
        pugin   = "substance/sourceid/" + i
        ur     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "sids" + '/' + "txt"
        url.append(ur)
  return url

#substancessourceidtosids()
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/sids/xml

#compound fastsimilarity_2d cid()

#ne or more cid to properties cvs file#############################
def compoundfastsimilarity_2dcid_to_property(*d):
  strrl=[]# to save list to make one file
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
    url=[]
    if len(strrl)>0:
      for i in strrl:
        pugin   = "compound/fastsimilarity_2d/cid/" + i
        ur    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "cids/xml"
        url.append(ur)
  return url

#compoundfastsimilarity_2dcidtoproperty()#one per request
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/2244/property/Title,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey,IUPACName,XLogP,ExactMass,MonoisotopicMass,TPSA,Complexity,Charge,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,IsotopeAtomCount,AtomStereoCount,DefinedAtomStereoCount,UndefinedAtomStereoCount,BondStereoCount,DefinedBondStereoCount,UndefinedBondStereoCount,CovalentUnitCount,Volume3D,XStericQuadrupole3D,YStericQuadrupole3D,ZStericQuadrupole3D,FeatureCount3D,FeatureAcceptorCount3D,FeatureDonorCount3D,FeatureAnionCount3D,FeatureCationCount3D,FeatureRingCount3D,FeatureHydrophobeCount3D,ConformerModelRMSD3D,EffectiveRotorCount3D,ConformerCount3D,Fingerprint2D/xml

"""inchi # **compound inchi **"""

def compound_cid_to_aid_active(*d):
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
        strrl.append(str(m)) 
  url=[]
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "compound/cid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt?aids_type=active"
  return url

#print(compound_cid_to_aid_active("180"))
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,964/aids/xml
def compound_cid_to_aid_inactive(*d):
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
        strrl.append(str(m)) 
  url=[]
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "compound/cid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt?aids_type=inactive"
  return url

#print(compound_cid_to_aid_inactive(180))
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,964/aids/xml
def subtance_sid_to_aid_active(*d):
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
        strrl.append(str(m)) 
  url=[]
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "substance/sid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt?aids_type=active"
  return url

#subtance_sid_to_aid_active(74912918)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,964/aids/xml
def subtance_sid_to_aid_inactive(*d):
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
        strrl.append(str(m)) 
  url=[]
  if len(strrl)>0:

    f= ",".join(strrl)
    pugin   = "substance/sid/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin + '/' + "aids" + '/' + "txt?aids_type=inactive"
  return url

#subtance_sid_to_aid_active(180)
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/180,964/aids/xml
def assay_target_gi_to_aid(*d):#done
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
        strrl.append(str(m))
  if len(strrl)>0:
    f= ",".join(strrl)
    pugin   = "assay/target/gi/" + f
    url     = "https://pubchem.ncbi.nlm.nih.gov/rest/pug" + '/' + pugin +  '/' + "aids/txt"
  return url


# In[2]:


import requests
def get_text_list(*m):
  st=[]
  for f in m:
    #f=(str(f))
    if type(f) is str:
              a=(requests.get(f))
              if a.status_code == 200: 
                  q=a.text
                  q=q.split()
                  st.append(q)
                  #print(x)
                  if ( (m.index(f)) % 5 == 4 ) :  # the % is the modulo operator and returns the remainder of a calculation (if i = 4, 9, ...)
                      time.sleep(1) 
    elif type(f) is list:
          for n in f:
              n=str(n)
              a=(requests.get(n))
              if a.status_code == 200: 
                  q=a.text
                  q=q.split()
                  st.append(q)
                  #print(n)
                  if ((f.index((n))) % 5 == 4 ):  # the % is the modulo operator and returns the remainder of a calculation (if i = 4, 9, ...)
                      time.sleep(10) 
  flat_list = []
  if len(st)>0:
    for sublist in st:
        for item in sublist:
            flat_list.append(item)

  #print(st)
  #print(flat_list)
  return (flat_list)
#get_text_list(['https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/aids/txt','https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/aids/txt','https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/aids/txt','https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/aids/txt','https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/water/aids/txt','https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/butane/aids/txt','https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/octanol/aids/txt'])


# In[3]:

def chunk(chunk_size,cids):
  #print(type(chunk_size))
  chunk_size = chunk_size
  chunk_list=[]
  if ( len(cids) % chunk_size == 0 ) : # check if total number of cids is divisible by 10 with no remainder
      num_chunks = len(cids) // chunk_size # sets number of chunks
  else : # if divide by 10 results in remainder
      num_chunks = len(cids) // chunk_size + 1 # add one more chunk

  for i in range(num_chunks) : # sets number of requests to number of data chunks as determined above
      
      idx1 = chunk_size * i        # sets a variable for a moving window of cids to start in a data chunk
      idx2 = chunk_size * (i + 1)  # sets a variable for a moving window of cids to end ina data chunk

      ch=( ",".join([ str(x) for x in cids[idx1:idx2] ])) # build pug input for chunks of data
      #print(str(ch))
      #str.split(sep=None, maxsplit=-1)
      chunk_list.append(ch.split(","))
  #print(type(chunk_list))
  return chunk_list
#m=chunk(10)
#print(m)
