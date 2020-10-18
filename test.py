# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 15:21:15 2020

@author: Gebruiker
"""
import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime

HAL_list = listdir("HAL")
HAL_dict = {}
for i in range(len(HAL_list)):
    key = HAL_list[i].replace("HAL.tsv.","")
    key = key.replace("-", " ")
    #date = datetime.strptime(key, "%Y %m %d")
    HAL_dict[key] = HAL_list[i]
    

sel = "2020 09 29"
df = pd.read_csv("HAL"+"/"+HAL_dict[sel], sep="\t", index_col=0, parse_dates=True)

#Select your HAL files
#selection = ["2020 09 29", "2020 09 30"]
#for sel in selection:

    