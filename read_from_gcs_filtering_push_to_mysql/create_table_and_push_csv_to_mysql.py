import mysql.connector
import pandas as pd

config = {
    'user': 'root',
    'password': 'joniwhfe',
    'host': '104.197.46.213',
    'database' : 'mobile'
}

hadoop_redwine = mysql.connector.connect(**config)
cursor = hadoop_redwine.cursor()

# cursor.execute("CREATE TABLE mobile_filtered ("
#                "品牌 VARCHAR(255),"
#                "名稱 VARCHAR(255),"
#                "價格 VARCHAR(255),"
#                "上市年份 VARCHAR(255),"
#                "上市日期 VARCHAR(255),"
#                "4G VARCHAR(255),"
#                "5G VARCHAR(255),"
#                "處理器 VARCHAR(255),"
#                "顯示屏_吋 VARCHAR(255),"
#                "解像度 VARCHAR(255),"
#                "螢幕刷新率_Hz VARCHAR(255),"
#                "前鏡頭_萬像素 VARCHAR(255),"
#                "後鏡頭_萬像素 VARCHAR(255),"
#                "記憶體_GB VARCHAR(255),"
#                "容量_GB VARCHAR(255),"
#                "快充功率_W VARCHAR(255),"
#                "重量_g VARCHAR(255),"
#                "尺寸_mm VARCHAR(255),"
#                "電池容量_mAh VARCHAR(255),"
#                "雙卡 VARCHAR(255),"
#                "指紋解鎖 VARCHAR(255),"
#                "面部解鎖 VARCHAR(255),"
#                "SD卡槽 VARCHAR(255),"
#                "NFC VARCHAR(255),"
#                "快速充電 VARCHAR(255),"
#                "插頭 VARCHAR(255),"
#                "立體聲喇叭 VARCHAR(255) )")
#
# hadoop_redwine.commit()
#
df = pd.read_csv("Mobile_filtered_from_gcs.csv")
df = df.astype({col: 'string' for col in df.select_dtypes('int64').columns})
query = (
        "INSERT INTO mobile_filtered (品牌,名稱,價格,上市年份,上市日期,4G,5G,處理器,顯示屏_吋,解像度,螢幕刷新率_Hz,前鏡頭_萬像素,後鏡頭_萬像素,記憶體_GB,容量_GB,快充功率_W,重量_g,尺寸_mm,電池容量_mAh,雙卡,指紋解鎖,面部解鎖,SD卡槽,NFC,快速充電,插頭,立體聲喇叭) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)")
cursor.executemany(query, list(df.to_records(index=False)))
hadoop_redwine.commit()