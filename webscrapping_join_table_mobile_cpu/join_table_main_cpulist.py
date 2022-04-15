import re
import pandas as pd
import mysql.connector
from gcloud import storage
import os
from datetime import datetime, timedelta
import numpy as np
##############################################################################

data_cpu = pd.read_csv('CPU_list.csv')
data_mobile_cpu = pd.read_csv('Mobile_cpu.csv')

brand_list = ["Dimensity","Exynos","Helio","Google","Kirin","Snapdragon","snapdragon"]
##############################################################################
def filter(row):
    list_processor = row['處理器'].split(" ")
    if row['品牌'] == 'Apple':
        for element_01 in list_processor:
            if 'A' in element_01:
                if element_01 != 'Apple':
                    return element_01
    if 'HUAWEI' in list_processor:
        return row['處理器'].strip("HUAWEI")
    if 'Hisilicon' in list_processor:
        return row['處理器'].strip("Hisilicon ")
    if 'MediaTek' in list_processor or 'Mediatek' in list_processor:
        return row['處理器'].strip("MediaTek ")
    return row['處理器']

def filter_quotation(row):
    list_quote = row['處理器'].split(" ")
    for quote in list_quote:
        if "(" in quote or "（" in quote:
            temp = list_quote.index(quote)
            list_quote = " ".join(list_quote[:temp])
            return list_quote
    return row['處理器']

def brand_to_filter(row):
    list_brand = row['處理器'].split(" ")
    if row['品牌'] == 'Apple':
        for element_apple in list_brand:
            if 'A' in element_apple and element_apple != 'Apple':
                return element_apple
    else:
        for element_01 in brand_list:
            for element_02 in list_brand:
                if element_01 == element_02:
                    temp = list_brand.index(element_02)
                    return " ".join(list_brand[temp:temp+2])

def translate(row):
    dict = {'高通驍龍':'Snapdragon','麒麟':'Kirin',"驍龍":"Snapdragon"}
    list_translate = row['處理器'].split(" ")
    for element_00 in list_translate:
        for element in dict.keys():
            if element in element_00:
                temp = element_00.strip(element)
                if len(temp) == 0:
                    index = list_translate.index(element_00)
                    english = dict[element]
                    return (english+" "+list_translate[index+1])
                    break
                english = dict[element]
                return (english+" "+temp)
    return row['處理器']


##############################################################################
data_mobile_cpu['處理器'] = data_mobile_cpu.apply(filter,axis=1)
data_mobile_cpu['處理器'] = data_mobile_cpu.apply(filter_quotation,axis=1)
data_mobile_cpu['處理器'] = data_mobile_cpu.apply(translate,axis=1)
data_mobile_cpu['處理器'] = data_mobile_cpu.apply(brand_to_filter,axis=1)


data_cpu['Processor'] = data_cpu['Processor'].str.strip(" Fusion").str.strip(" Bionic")
data_cpu['Processor'] = data_cpu['Processor'].str.replace('Apple ','')
data_cpu['Processor'] = data_cpu['Processor'].str.replace(' Gen 1','')

data_mobile_cpu = data_mobile_cpu.sort_values('處理器')
##############################################################################

merged_table = data_mobile_cpu.merge(data_cpu,left_on="處理器",right_on="Processor")

data_cpu.to_csv("CPU_list_filtered.csv",index=False)
data_mobile_cpu.to_csv(f'Mobile_cpu_filtered.csv',index=False)
merged_table.to_csv(f'Mobile_Merged_cpu.csv',index=False)