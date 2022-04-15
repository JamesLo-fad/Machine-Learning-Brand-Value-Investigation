import re
import pandas as pd
import mysql.connector
from gcloud import storage
import os
import pandas as pd
import gcsfs
import io
########################################################################################

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './heroic-climber-347106-b0f1ec68d8cc.json'
storage_client = storage.Client()
bucket = storage_client.bucket('mobile_raw')
blob = bucket.blob("Mobile_raw.csv")
data = blob.download_as_string()
data = pd.read_csv(io.BytesIO(data))

########################################################################################
def filter(row):
    doublecard = 0
    finger = 0
    face = 0
    SD = 0
    NFC = 0
    charge = 0
    plug = 0
    speaker = 0
    if '雙卡' in row:
        doublecard = 1
    if '指紋解鎖' in row:
        finger = 1
    if '面部解鎖' in row:
        face = 1
    if 'SD卡槽' in row:
        SD = 1
    if 'NFC' in row:
        NFC = 1
    if '快速充電' in row:
        charge = 1
    if '3.5mm插頭' in row:
        plug = 1
    if '立體聲喇叭' in row:
        speaker = 1
    return pd.Series([doublecard,finger,face,SD,NFC,charge,plug,speaker])

def brand(row):
    list_element = row.split(" ")
    return list_element[0]

def year(row):
    year_element = row.split("-")
    return year_element[0]

def internet(row):
    four_g = 0
    five_g = 0
    if '4G' in row.split(','):
        four_g = 1
    if '5G' in row.split(','):
        five_g = 1

    return pd.Series([four_g,five_g])

########################################################################################

data.rename(columns={'電池容量':'電池容量(mAh)','尺寸':'尺寸(mm)','重量':'重量(g)','快充功率':'快充功率(W)','容量':'容量(GB)','記憶體':'記憶體(GB)'}, inplace=True)
data.rename(columns={'後鏡頭':"後鏡頭(萬像素)","前鏡頭":"前鏡頭(萬像素)","螢幕刷新率":"螢幕刷新率(Hz)","顯示屏":"顯示屏(吋)"}, inplace=True)

################################################################
data['電池容量(mAh)'] = data['電池容量(mAh)'].str.strip("mAh")
data['尺寸(mm)'] = data['尺寸(mm)'].str.strip("mm")
data['重量(g)'] = data['重量(g)'].str.strip("g")
data['快充功率(W)'] = data['快充功率(W)'].str.strip("W").str.strip("Max ")
data['容量(GB)'] = data['容量(GB)'].str.strip("GB")
data['記憶體(GB)'] = data['記憶體(GB)'].str.strip("GB")
data['後鏡頭(萬像素)'] = data['後鏡頭(萬像素)'].str.strip("萬像素")
data['前鏡頭(萬像素)'] = data['前鏡頭(萬像素)'].str.strip("萬像素")
data['螢幕刷新率(Hz)'] = data['螢幕刷新率(Hz)'].str.replace(" / 90","").str.strip("Hz")
data['上市日期'] = data['上市日期'].str.replace("年","-").str.replace("月","")
data['顯示屏(吋)'] = data['顯示屏(吋)'].str.strip("吋")

data = data.fillna("no")


data[['雙卡','指紋解鎖','面部解鎖','SD卡槽','NFC','快速充電','3.5mm插頭','立體聲喇叭']] = data['功能'].apply(filter)
data.insert(0,'品牌','')
data['品牌'] = data['名稱'].apply(brand)
data.insert(3,'上市年份','')
data['上市年份'] = data['上市日期'].apply(year)
data.insert(5,'4G','')
data.insert(6,'5G','')
data[['4G','5G']] = data['網絡制式'].apply(internet)


data = data.drop(['功能'], axis=1)
data = data.drop(['作業系統'], axis=1)
data = data.drop(['Wi-Fi 制式'], axis=1)
data = data.drop(['藍牙版本'], axis=1)
data = data.drop(['防塵/防水等級'], axis=1)
data = data.drop(['網絡制式'], axis=1)

data = data.sort_values('品牌')

################################################################


data.to_csv(f'Mobile_filtered_from_gcs.csv',index=False)