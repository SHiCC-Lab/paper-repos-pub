import pandas as pd
import numpy as np
import os
import glob
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stat
import statsmodels.api as sm
from statsmodels.formula.api import ols
import pingouin as pg
import math
from tabulate import tabulate
import seaborn as sns
import hashlib

def filter_hash(cell_val):
    '''
    Quick function to filter out nan (numpy) or na (pandas). Or hash values
    Used by lambda function below
    Arguments:
        cell_val - Some value assumedly from a dataframe cell
    '''

    if (pd.isna(cell_val)):
        return ""
    else:
        print(type(cell_val))
        return "{0} {1}".format(hash(cell_val[0:(cell_val.find("-"))]), cell_val[cell_val.find("-"):])

pd.set_option("display.max_rows", None)

PYTHONHASHSEED = 11082021

path = "/Users/cld028/Research-Repos/human-ai-race/Quantitative Analysis/"
os.chdir(path)

prolific = pd.read_csv("data/Prolific/prolific_data_with_groups copy.csv")
prolific.rename(columns={"participant_id" : "PROLIFIC_PID"}, inplace=True)
prolific["PROLIFIC_PID"] = prolific["PROLIFIC_PID"].apply(lambda x: hash(x))
pid_list = prolific.PROLIFIC_PID.to_list()
prolific.to_csv("/Users/cld028/Research-Repos/paper-repos-internal/SBP-BRiMS-21_AtkinsBD/Data_Analysis/Prolific_Data.csv")

#this gets all of the seperate pavlovia files, compares them to the prolific ids and drops all of the partial runs
#then it drops the practice trials and the attention check trials
files = glob.glob("data/Pavlovia/*.csv")
pav_list = []

i = 0
while i < len(files):
    temp = pd.read_csv(files[i])
    i += 1
    temp["PROLIFIC_PID"] = temp["PROLIFIC_PID"].apply(lambda x: hash(x))
    if len(temp) == 15 and temp.PROLIFIC_PID[1] in pid_list:
        temp.drop([0,1,2,7],inplace=True)

        pav_list.append(temp)
    else:
        pass

#this checks to make sure there aren't multiple complete runs for the same participant. this happened a few times due to pavlovia errors
#if anything prints here, check the files and make sure any duplicates or extra runs are removed
j = 0
find_dup = {}
while j < len(pav_list):
    if pav_list[j].PROLIFIC_PID[3] in find_dup:
        find_dup[pav_list[j].PROLIFIC_PID[3]] += 1
    else:
        find_dup[pav_list[j].PROLIFIC_PID[3]] = 1
    j += 1

for key in find_dup:
    if find_dup[key] > 1:
        print(key)

i = 0

while i < len(pav_list):
    index = prolific.loc[(prolific.PROLIFIC_PID == pav_list[i].PROLIFIC_PID[3])].index
    ind = index[0]
    demo = prolific.at[ind,"Demographic"]
    group = prolific.at[ind,"GROUP"]
    temp = pav_list[i]
    temp["PROLIFIC_PID"] = temp["PROLIFIC_PID"].apply(lambda x: hash(x))
    temp["participant"] = temp["participant"].apply(lambda x: hash(x))
    temp["UUID"] = temp["UUID"].apply(lambda x: hash(x))
    temp["date"] = ""
    #print(temp.head())
    temp.to_csv("/Users/cld028/Research-Repos/paper-repos-internal/SBP-BRiMS-21_AtkinsBD/Data_Analysis/pav_data/{0}.csv".format(temp["PROLIFIC_PID"].iat[0]))
    i += 1

#Qual Data Anon Section
columnNames = ["AINotIntelligent", "AINoPattern","AIUserDependent","FocusedOwnMovement","Vague","AICoop","AIAgainstHuman"]
sortedData = pd.read_csv("/Users/cld028/Research-Repos/paper-repos-internal/SBP-BRiMS-21_AtkinsBD/Data_Analysis/Labelled Qual Data.csv", names=columnNames, skiprows=1)

#print(sortedData.head())

#Hash Prolific ID portion of cell
sortedData = sortedData.applymap(lambda x: "{0} {1}".format(hash(x[0:(x.find("-"))]), x[x.find("-"):]), na_action="ignore")

#print(sortedData)

sortedData.to_csv("/Users/cld028/Research-Repos/paper-repos-internal/SBP-BRiMS-21_AtkinsBD/Data_Analysis/Coded_Qual_Data.csv")
