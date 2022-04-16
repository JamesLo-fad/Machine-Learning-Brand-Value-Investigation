from sqlalchemy import create_engine
import pandas as pd
import pymysql
import functools
import operator
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from scipy.cluster.vq import kmeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error

#1.loading data from MySQL######################################################################################

@st.cache(allow_output_mutation=True)
def load_all_data():
    db_connection_str = 'mysql+pymysql://root:joniwhfe@104.197.46.213/mobile'
    db_connection = create_engine(db_connection_str)
    df = pd.read_sql('SELECT * FROM mobile_filtered', con=db_connection)
    # df_02 = pd.read_sql('SELECT * FROM Final_join_table', con=db_connection)
    return df
def load_all_data_02():
    db_connection_str = 'mysql+pymysql://root:joniwhfe@104.197.46.213/mobile'
    db_connection = create_engine(db_connection_str)
    df_02 = pd.read_sql('SELECT * FROM mobile_final', con=db_connection)
    return df_02
#2.Streamlit displaay function######################################################################################
def year_brand(mobile_overview):
    st.subheader('Production v.s. Year')
    mobile_yrbr = mobile_overview[mobile_overview['上市年份']!='no']
    mobile_yrbr = mobile_yrbr.groupby(['上市年份', '品牌'], as_index=False).size()
    mobile_yrbr = mobile_yrbr.groupby('上市年份')[['size']].sum().reset_index()
    fig = plt.figure(figsize=(20, 10))
    sns.barplot(x="上市年份", y="size", data=mobile_yrbr)
    plt.xlabel("Year")
    st.pyplot(fig)

def most_product_band(mobile_overview):
    st.subheader('Top 10 Production brand (2007-2022)')
    mobile_pd = mobile_overview.groupby(['品牌'], as_index=False).size().sort_values('size',ascending=False).head(10)
    st.table(mobile_pd)
    fig = plt.figure(figsize=(20, 10))
    sns.barplot(x="品牌", y="size", data=mobile_pd)
    plt.xlabel("Brand")
    st.pyplot(fig)

def biggest_monitor(mobile_overview):
    st.subheader('Top 5 brand selling largest monitor (2007-2022)')
    mobile_monitor = mobile_overview[['品牌','名稱','價格','顯示屏_吋']]
    mobile_monitor = mobile_monitor[mobile_monitor['顯示屏_吋'] != 'no']
    mobile_monitor = mobile_monitor.sort_values('顯示屏_吋',ascending=False).head(5)
    st.table(mobile_monitor)

def most_function(mobile_overview):
    st.subheader('Top 3 brand selling most function (2007-2022)')
    mobile_function = mobile_overview[['品牌','價格','sum_of_function']].sort_values('sum_of_function',ascending=False)
    st.table(mobile_function.head(3))

def lightest_mobile(mobile_overview):
    st.subheader('Top 5 lightest mobile (2007-2022)')
    light_mobile = mobile_overview[['品牌','價格','重量_g']]
    light_mobile = light_mobile[light_mobile['重量_g'] != 'no']
    light_mobile = light_mobile[light_mobile['重量_g'].str.isdigit()]
    light_mobile = light_mobile.sort_values('重量_g')
    st.table(light_mobile.head(5))

def resolution_mobile(mobile_overview):
    st.subheader('Top 5 resolution mobile (2007-2022)')
    clear_mobile = mobile_overview[['品牌','名稱', '價格', 'resolution']]
    clear_mobile = clear_mobile[clear_mobile['resolution'] != 'no']
    clear_mobile['resolution'] = clear_mobile['resolution'].astype(int)
    clear_mobile = clear_mobile.sort_values('resolution',ascending=False)
    st.table(clear_mobile.head(5))

def processor_brand_number(row):
    st.subheader('Processor Brand products variation (2007-2022)')
    process_brand = row[['Processor_brand', '處理器']]
    process_brand = process_brand.groupby(['Processor_brand', '處理器'], as_index=False).nunique()
    process_brand = process_brand.groupby(['Processor_brand']).count().reset_index()
    fig = plt.figure(figsize=(20, 10))
    sns.barplot(x="Processor_brand", y="處理器", data=process_brand)
    st.pyplot(fig)

def brand_core(cpu_rating):
    st.subheader('Processor Brand core (2007-2022)')
    core = cpu_rating[['Processor_brand','Cores']]
    core = core.groupby(['Processor_brand', 'Cores'], as_index=False).size()
    fig = plt.figure(figsize=(20, 10))
    sns.barplot(x="Processor_brand", y="size",hue='Cores', data=core)
    st.pyplot(fig)

def rating_rank(cpu_rating):
    st.subheader('Processor rating (2007-2022)')
    cpu_rating = cpu_rating[['品牌','名稱','Rating','價格']]
    cpu_rating = cpu_rating.sort_values('Rating',ascending=False).head(5)
    st.table(cpu_rating)

def antutu(cpu_rating):
    st.subheader('Processor antutu (2007-2022)')
    antutu = cpu_rating[['品牌','名稱','AnTuTu_9','價格']]
    antutu = antutu.sort_values('AnTuTu_9',ascending=False).head(5)
    st.table(antutu)

def geekbench(cpu_rating):
    st.subheader('Processor geekbench_single (2007-2022)')
    geekbench_single = cpu_rating[['品牌', '名稱', 'Geekbench_5_single', '價格']]
    geekbench_single = geekbench_single.sort_values('Geekbench_5_single',ascending=False).head(5)
    st.table(geekbench_single)
    st.subheader('Processor geekbench_multi (2007-2022)')
    geekbench_multi = cpu_rating[['品牌', '名稱', 'Geekbench_5_multi', '價格']]
    geekbench_multi = geekbench_multi.sort_values('Geekbench_5_multi',ascending=False).head(5)
    st.table(geekbench_multi)

def clock(cpu_rating):
    st.subheader('Processor Clock_MHz (2007-2022)')
    clock_Hz = cpu_rating[['品牌', '名稱', 'Clock_MHz', '價格']]
    clock_Hz = clock_Hz.sort_values('Clock_MHz',ascending=False).head(5)
    st.table(clock_Hz)

#3.Data Cleansing######################################################################################
mobile_overview = load_all_data()
# mobile_overview = mobile_overview.drop(['sum_of_function'],axis=1)
mobile_overview['解像度'] = mobile_overview['解像度'].str.strip('FHD+ ').str.strip("(").str.replace(")","").str.replace("p","")
mobile_overview['解像度'] = mobile_overview['解像度'].str.replace("*"," ").str.replace("，"," ").str.replace(","," ")

cpu_overview = load_all_data_02()
cpu_rating = cpu_overview.drop(cpu_overview.columns[11:], axis=1)

#4.Add columns function######################################################################################

def addfunction(row):
    list = row.astype(int).sum()
    return list

def resolution_product(row):
    list_reso = row.split(" ")
    if row != 'no' and len(list_reso)>2:
        int_01 = int(list_reso[0])
        int_02 = int(list_reso[2])
        product = int_01*int_02
        return str(product)
    return 'no'

def processor_brand(row):
    brand = row.split(" ")[0]
    if 'A' in brand:
        return 'Apple'
    return brand



#5.Adding columns for analysis(aggregation)######################################################################################
mobile_overview['sum_of_function'] = mobile_overview.iloc[:,19:27].apply(addfunction,axis=1)
mobile_overview['resolution'] = mobile_overview['解像度'].apply(resolution_product)

cpu_rating.insert(2,'Processor_brand','')
cpu_rating['Processor_brand'] = cpu_rating['處理器'].apply(processor_brand)
cpu_rating['AnTuTu_9'] = cpu_rating['AnTuTu_9'].astype(int)
cpu_rating['Geekbench_5_single'] = cpu_rating['Geekbench_5_single'].astype(int)
cpu_rating['Geekbench_5_multi'] = cpu_rating['Geekbench_5_multi'].astype(int)
#6.Streamlit main function######################################################################################
st.title("Mobile_price_analysis")

add_selectbox = st.sidebar.selectbox("Mobile_price_analysis",("Overview", "Mobile_CPU_rating","Machine_Learning"))

if add_selectbox == 'Overview':
    st.subheader("Overview")
    if st.checkbox(label="Raw data"):
        st.write(mobile_overview)
    year_brand(mobile_overview)
    most_product_band(mobile_overview)
    biggest_monitor(mobile_overview)
    most_function(mobile_overview)
    lightest_mobile(mobile_overview)
    resolution_mobile(mobile_overview)

if add_selectbox == 'Mobile_CPU_rating':
    st.subheader("Mobile_CPU_rating")
    if st.checkbox(label="Raw data"):
        st.write(cpu_rating)
    processor_brand_number(cpu_rating)
    brand_core(cpu_rating)
    rating_rank(cpu_rating)
    antutu(cpu_rating)
    geekbench(cpu_rating)
    clock(cpu_rating)

if add_selectbox == 'Machine_Learning':
    st.subheader("Machine Learning")
    if st.checkbox(label="Raw data"):
        st.write(cpu_rating)
    enc = OneHotEncoder()
    one_hot_features = pd.DataFrame(enc.fit_transform(cpu_rating[['處理器','Processor_brand']]).toarray(),
                                    columns=enc.get_feature_names_out())
    machine = pd.concat([cpu_rating, one_hot_features], axis=1)
    main_menu = machine.iloc[:, 4:-1].drop('上市年份', 1)
    scaler = MinMaxScaler()
    X_model = scaler.fit(main_menu.drop('價格',1))
    Y_model = main_menu[['價格']]
    X_model = scaler.transform(main_menu.drop('價格',1))
    X_train, X_test, y_train, y_test = train_test_split(X_model, Y_model)
    classifier = RandomForestClassifier()
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    concat_01 = pd.DataFrame(y_test).reset_index()
    concat_02 = pd.DataFrame(y_pred)
    comparison = pd.concat([concat_01, concat_02],axis=1,ignore_index=True)
    comparison = comparison.drop([0], axis=1).rename({1:'Real data', 2:'Prediction'}, axis=1)
    st.subheader("Price prediction for All")
    st.write(comparison)
    st.subheader('Mean square error')
    rms = np.sqrt(mean_squared_error(y_test, y_pred))
    st.write(rms)
    st.subheader('Features Importance Rank(Top 10)')
    feature_pd = pd.DataFrame(classifier.feature_importances_).reset_index(drop=True)
    columns_name = pd.DataFrame(main_menu.drop('價格',1).columns).reset_index(drop=True)
    feature = pd.concat([columns_name, feature_pd],axis=1,ignore_index=True).sort_values(1,ascending=False).head(10)
    feature = feature.rename({0: 'Feature name', 1: 'Contribution'}, axis=1)
    st.table(feature)
