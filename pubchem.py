import urllib
import pandas as pd
import csv
from shutil import copyfile
# from chemspipy import ChemSpider
import pubchempy as pcp
import time

# upload chemicals list
# opening file
filename = "temp.csv"
# creating new file
newfile = "output.csv"
# extract data from file
# copy imported file
copyfile(filename, newfile)
filereader = pd.read_csv(filename, encoding='latin1')
# size of data frame
counter = len(filereader)
print(counter)


def name_search(compound):
    try:
        results = pcp.get_compounds(compound, 'name')
    except IndexError as e:
        print("ERROR!", e)
    else:
        pass
    return results


def cas_search(cas):
    try:
        results = pcp.get_compounds(cas, 'cas')
    except IndexError as e:
        print("ERROR!", e)
    else:
        pass
    return results


def inchikey_search(inchikey):
    try:
        results = pcp.get_compounds(inchikey, 'inchikey')
    except IndexError as e:
        print("ERROR!", e)
    else:
        pass
    return results


def cid_based_search(cid, filereader):
    try:
        result = pcp.Compound.from_cid(cid)
        filereader.loc[i, "Pubchem_CID"] = found_cid
        filereader.loc[i, "iupac_name"] = result.iupac_name
        filereader.loc[i, "synonyms"] = '; '.join(result.synonyms)
        filereader.loc[i, "inchikey"] = result.inchikey
        filereader.loc[i, "mf"] = result.molecular_formula
        filereader.loc[i, "mw"] = result.molecular_weight
        filereader.loc[i, "canonical_smiles"] = result.canonical_smiles
        filereader.loc[i, "xlogP"] = result.xlogp
        filereader.loc[i, 'status'] = 'complete'
    except (pcp.HTTPError, IndexError, pcp.BadRequestError, urllib.error.URLError) as err:
        print(err)
    else:
        pass


for i in range(0, counter):
    my_cid = filereader.at[i, "Pubchem_CID"]
    my_cas = filereader.at[i, "CAS_NO"]
    my_name = filereader.at[i, "formatted_name"]
    my_inchi = filereader.at[i, "inchikey"]
    print(i)
    if i % 25 == 0:
        filereader.to_csv('output.csv')
        # time.sleep(10)
        print("I was resting")
    elif i % 225 == 0:
        filereader.to_csv('output.csv')
        time.sleep(60)
        print("PubMed was resting")
    else:
        pass
    if my_cid == 0 or pd.isnull(my_cid):
        if my_inchi:
            # get properties based on inchikey
            found_cid = inchikey_search(my_inchi)
            filereader.loc[i, "search_type"] = "inchikey"
        elif my_name:
            # get properties based on name
            found_cid = name_search(my_name)
            filereader.loc[i, "search_type"] = "name"
        elif my_cas:
            # get properties based on name
            found_cid = cas_search(my_cas)
            filereader.loc[i, "search_type"] = "cas"
        else:
            pass
        print(found_cid)
        if found_cid[0]:
            # retains only the first result
            cid_based_search(int(found_cid[0]),filereader)

    elif my_cid:
        print('here')
        cid_based_search(int(my_cid), filereader)
    else:
        pass

filereader.to_csv('output.csv')
