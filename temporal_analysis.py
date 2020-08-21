
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import math
import matplotlib.pyplot as plt

st.title('Cord-19 data analysis')
read_and_cache_csv = st.cache(pd.read_csv)

@st.cache
def load_all():
    df_url = "https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/categorized_cord19_07_05.csv"
    df = pd.read_csv(df_url, error_bad_lines=False)
    df['publish_date'] = pd.to_datetime(df['publish_date'])
    return df

def load():
    df_url = "https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/categorized_cord19_07_05.csv"
    df_only_month = pd.read_csv(df_url, error_bad_lines=False)
    df_only_month = df_only_month.loc[df_only_month['publish_date'].str.len() > 4]
    df_only_month['publish_date'] = pd.to_datetime(df_only_month['publish_date'])
    return df_only_month

def load_country():
    dfa_url = 'https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/country_cord19.csv'
    df_a = pd.read_csv(dfa_url, error_bad_lines=False)
    df_a['publish_date'] = pd.to_datetime(df_a['publish_date'])
    return df_a

def load_country_only():
    dfa_url = 'https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/country_cord19.csv'
    df_ao = pd.read_csv(dfa_url, error_bad_lines=False)
    df_ao = df_ao.loc[df_ao['publish_date'].str.len() > 4]
    df_ao['publish_date'] = pd.to_datetime(df_ao['publish_date'])
    return df_ao

def load_length():
    dfl_url = 'https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/length.csv'
    df_l = pd.read_csv(dfl_url, error_bad_lines=False)
    return df_l

def load_area():
    dfa_url = 'https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/area_cord19.csv'
    df_a = pd.read_csv(dfa_url, error_bad_lines=False)
    df_a['publish_date'] = pd.to_datetime(df_a['publish_date'])
    return df_a

def load_area_only():
    dfa_url = 'https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/area_cord19.csv'
    df_ao = pd.read_csv(dfa_url, error_bad_lines=False)
    df_ao = df_ao.loc[df_ao['publish_date'].str.len() > 4]
    df_ao['publish_date'] = pd.to_datetime(df_ao['publish_date'])
    return df_ao

df = load_all()
df_only_month = load()
df_a = load_country()
df_ao = load_country_only()
df_l = load_length()
df_area = load_area()
df_area_only = load_area_only()

lt = st.sidebar.selectbox('Do you want to see temporal analysis or length outlier analysis?',
                          ('temporal analysis','length outlier analysis')
                          )

if (lt == 'temporal analysis'):
    cat = st.sidebar.selectbox('Which category standard you would like to see?',
                           ('Peer reviewed/not', 'area')
                           )

    granularity = st.selectbox(
        'What granularity you would like to see?',
        ("Yearly", "Monthly", "Weekly", "Daily")
        )

    if(cat == 'area'):
        ac = st.selectbox(
            "Do you want to see in area or country granularity?",
            ('area','country')
        )

    if (cat =='Peer reviewed/not' ):
        peer_reviewed = st.checkbox('peer_reviewed', value=True)
        ABM = st.checkbox('ArXiv/BioRxiv/MedExiv')
    elif (cat == 'area'):
        if (ac == 'area'):
            cp = st.checkbox('Canadian Province', value=False)
            uss = st.checkbox('US State', value=False)
            if(cp):
                on = st.checkbox('ON,CA', value = True)
                qc = st.checkbox('QC,CA', value = True)
                bc = st.checkbox('BC,CA', value = True)
                otca = st.checkbox('Others,CA', value = False)
            if(uss):
                caus = st.checkbox('CA,US', value = True)
                ny = st.checkbox('NY,US', value = True)
                otus = st.checkbox('others,US', value = False)
                #PEI, AB, MB, NS, NL, Saskatchewan, NB, Nunavut, Yukon
        elif(ac == 'country'):
            italy = st.checkbox('Italy', value=True)
            china = st.checkbox('China', value=True)
            usa = st.checkbox('US', value=True)
            ca = st.checkbox('Canada', value=True)

def selected_df(df_new, df_old):
    if (cat == 'Peer reviewed/not'):
        if (peer_reviewed):
            df_new['peer_reviewed'] = df_old['peer_reviewed']
        if (ABM):
            df_new['ArXiv/BioRxiv/MedExiv'] = df_old['ArXiv/BioRxiv/MedExiv']
    elif (cat == 'area'):
        if (ac == 'area'):
            if(cp):
                if (on):
                    df_new['ON'] = df_old['ON']
                if (qc):
                    df_new['QC'] = df_old['QC']
                if (bc):
                    df_new['BC'] = df_old['BC']
                if (otca):
                    cols = ['PEI', 'AB', 'MB', 'NS', 'NL', 'Saskatchewan', 'NB', 'Nunavut', 'Yukon']
                    df_new[cols] = df_old[cols]
            if(uss):
                if (caus):
                    df_new['CA'] = df_old['CA']
                if (ny):
                    df_new['NY'] = df_old['NY']
                if (otus):
                    cols = ['IL','MD','MS','OR','PA','SD','AK','HI','NJ','GA','AL','MA','TX','ND','MT','ID','SC','NE','CT','AR','FL','VT','CO','WA','IN','LA','AZ','NV','NM','DE','MN','ME','NH','WY','MI','UT','VA','RI','OH','WV','WI','IA','MO','KY','OK']
                    df_new[cols] = df_old[cols]

        elif (ac == 'country'):
            if(china):
                df_new['China'] = df_old['China']
            if (italy):
                df_new['Italy'] = df_old['Italy']
            if(usa):
                df_new['US'] = df_old['US']
            if(ca):
                df_new['Canada'] = df_old['Canada']

if(lt =='temporal analysis'):
    if (granularity == 'Yearly'):
        st.subheader('Number of published documents in each year')
        if (cat == 'Peer reviewed/not'):
            start_year, end_year = st.slider("Select year Range:", 1870, 2021, (2003, 2020), 1)
            df_yearly = df.loc[(df['publish_date'].dt.year >= start_year) & (df['publish_date'].dt.year <= end_year)]
        else:
            start_year, end_year = st.slider("Select year Range:", 1992, 2021, (2003, 2020), 1)
            if(ac == 'country'):
                df_yearly = df_a.loc[(df_a['publish_date'].dt.year >= start_year) & (df_a['publish_date'].dt.year <= end_year)]
            else:
                df_yearly = df_area.loc[(df_area['publish_date'].dt.year >= start_year) & (df_area['publish_date'].dt.year <= end_year)]
        if (cat == 'Peer reviewed/not'):
            df_yearly = df_yearly.groupby(pd.Grouper(key='publish_date', freq='Y'))['peer_reviewed','ArXiv/BioRxiv/MedExiv'].agg('sum').reset_index('publish_date')
        else:
            df_yearly = df_yearly.groupby(pd.Grouper(key='publish_date', freq='Y')).agg('sum').reset_index('publish_date')

        df_yearly['publish_date'] = df_yearly['publish_date'].dt.year
        df_yearly = df_yearly.set_index('publish_date')
        df_d_yearly = pd.DataFrame(index=df_yearly.index)
        selected_df(df_d_yearly, df_yearly)
        st.bar_chart(df_d_yearly)

    if (granularity == 'Monthly'):
        st.subheader('Number of published documents in monthly granularity')
        start_m, end_m = st.slider("Select date range to see monthly granularity plot:", 1955.0+10/12, 2022.0-1/12, (2003+1/12, 2020.0+1/12), 1/12, format = '')
        ms = math.ceil((start_m - int(start_m)) * 12)
        me = math.ceil((end_m - int(end_m)) * 12)
        start_month = datetime.date(int(start_m), ms, 1)
        end_month = datetime.date(int(end_m), me, 1)
        st.text(f"From: {start_month:%Y}-{start_month:%m} to {end_month:%Y}-{end_month:%m} ")

        if (cat == 'Peer reviewed/not'):
            df_monthly = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_month]
            df_monthly = df_monthly.loc[df_monthly['publish_date'].dt.date <= end_month]
            df_monthly = df_monthly.groupby(pd.Grouper(key='publish_date', freq='M'))[
                'peer_reviewed', 'ArXiv/BioRxiv/MedExiv'].agg('sum').reset_index('publish_date')
        else:
            if(ac == 'country'):
                df_monthly = df_ao.loc[df_ao['publish_date'].dt.date >= start_month]
            else:
                df_monthly = df_area_only.loc[df_area_only['publish_date'].dt.date >= start_month]
            df_monthly = df_monthly.loc[df_monthly['publish_date'].dt.date <= end_month]
            df_monthly = df_monthly.groupby(pd.Grouper(key='publish_date', freq='M')).agg('sum').reset_index('publish_date')
        df_monthly = df_monthly.set_index('publish_date')
        df_d_monthly = pd.DataFrame(index=df_monthly.index)
        selected_df(df_d_monthly, df_monthly)
        st.bar_chart(df_d_monthly)

    if (granularity == 'Weekly'):
        st.subheader('Number of published documents in weekly granularity')
        start_w, end_w = st.slider("Select date range to see weekly granularity plot:", 1955.0+10/12, 2022.0-1/12, (2010+10/12, 2020.0+1/12), 1/12,format = '')
        ws = math.ceil((start_w - int(start_w)) * 12)
        we = math.ceil((end_w - int(end_w)) * 12)
        start_week = datetime.date(int(start_w), ws, 1)
        end_week = datetime.date(int(end_w), we, 1)
        st.text(f"From: {start_week:%Y}-{start_week:%m} to {end_week:%Y}-{end_week:%m} ")

        if (cat == 'Peer reviewed/not'):
            df_weekly = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_week]
            df_weekly = df_weekly.loc[df_weekly['publish_date'].dt.date <= end_week]
            df_weekly = df_weekly.groupby(pd.Grouper(key='publish_date', freq='W'))[
                'peer_reviewed', 'ArXiv/BioRxiv/MedExiv'].agg('sum').reset_index('publish_date')
        else:
            if (ac == 'country'):
                df_weekly = df_ao.loc[df_ao['publish_date'].dt.date >= start_week]
            else:
                df_weekly = df_area_only.loc[df_area_only['publish_date'].dt.date >= start_week]
            df_weekly = df_weekly.loc[df_weekly['publish_date'].dt.date <= end_week]
            df_weekly = df_weekly.groupby(pd.Grouper(key='publish_date', freq='W')).agg('sum').reset_index('publish_date')

        df_weekly = df_weekly.set_index('publish_date')
        df_d_weekly = pd.DataFrame(index=df_weekly.index)
        selected_df(df_d_weekly, df_weekly)
        st.bar_chart(df_d_weekly)

    if (granularity == 'Daily'):
        st.subheader('Number of published documents in daily granularity')
        start_d, end_d = st.slider("Select date range to see daily granularity plot:", 1955.0+10/12, 2022.0-1/12, (2014+10/12, 2020.0+1/12), 1/12,format = '')
        ds = math.ceil((start_d - int(start_d)) * 12)
        de = math.ceil((end_d - int(end_d)) * 12)
        start_day = datetime.date(int(start_d), ds, 1)
        end_day = datetime.date(int(end_d), de, 1)
        st.text(f"From: {start_day:%Y}-{start_day:%m} to {end_day:%Y}-{end_day:%m} ")
        if (cat == 'Peer reviewed/not'):
            df_daily = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_day]
            df_daily = df_daily.loc[df_daily['publish_date'].dt.date <= end_day]
        else:
            if(ac == 'country'):
                df_daily = df_ao.loc[df_ao['publish_date'].dt.date >= start_day]
            else:
                df_daily = df_area_only.loc[df_area_only['publish_date'].dt.date >= start_day]
            df_daily = df_daily.loc[df_daily['publish_date'].dt.date <= end_day]
        df_daily = df_daily.set_index('publish_date')
        df_d_daily = pd.DataFrame(index=df_daily.index)
        selected_df(df_d_daily, df_daily)
        st.bar_chart(df_d_daily)

elif(lt == 'length outlier analysis'):
    st.subheader('histogram for abstract length per documents')
    df_l.hist(column = 'abstract',bins = 300,figsize=(15,5))
    plt.show()
    st.pyplot()

    q1 = df_l['abstract'].quantile(0.25)
    q3 = df_l['abstract'].quantile(0.75)
    iqr = q3 - q1
    # I only consider extreme big value, since small value will not cause file explosion
    filter = df_l[
                 'abstract'] >= q3 + iqr
    # abstract outlier
    outlier = df_l.loc[filter]
    sorted = outlier.sort_values(by=['abstract'], ascending=False)
    top = st.number_input('number of extreme outliers',value=10)
    tops = sorted.head(int(top))
    tops = tops[['docid','DOI','abstract','num_paragraph']]
    tops = tops.set_index('docid')
    st.write(tops)






