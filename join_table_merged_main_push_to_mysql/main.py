import re
import pandas as pd
import mysql.connector
from gcloud import storage
import os
from datetime import datetime, timedelta
import numpy as np

data_cpu = pd.read_csv('Mobile_merged_cpu.csv')
data_mobile = pd.read_csv('Mobile_filtered_from_gcs.csv')




merged_table = data_cpu.merge(data_mobile,left_on="名稱",right_on="名稱")
merged_table = merged_table.drop(['處理器_y'], axis=1)
merged_table = merged_table.drop(['品牌_y'], axis=1)
merged_table = merged_table.drop(['Processor'], axis=1)
merged_table.columns = merged_table.columns.str.replace('品牌_x', '品牌')
merged_table.columns = merged_table.columns.str.replace('處理器_x', '處理器')

merged_table.to_csv("mobile_final.csv",index=False)
