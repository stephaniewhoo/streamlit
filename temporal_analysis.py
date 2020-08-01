
import streamlit as st
import pandas as pd
import datetime
import math

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

data_load_state = st.text('Loading data...')
df = load_all()
df_only_month = load()
df_a = load_area()
df_ao = load_area_only()
data_load_state.text("Done!")

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
        wuhan = st.checkbox('Wuhan', value=True)
        italy = st.checkbox('Italy', value=True)
        ca = st.checkbox('California', value=True)
        ny = st.checkbox('New York', value=True)
    elif(ac == 'country'):
        italy = st.checkbox('Italy', value=True)
        china = st.checkbox('China', value=True)
        usa = st.checkbox('USA', value=True)

def selected_df(df_new, df_old):
    if (cat == 'Peer reviewed/not'):
        if (peer_reviewed):
            df_new['peer_reviewed'] = df_old['peer_reviewed']
        if (ABM):
            df_new['ArXiv/BioRxiv/MedExiv'] = df_old['ArXiv/BioRxiv/MedExiv']
    elif (cat == 'area'):
        if (ac == 'area'):
            if (wuhan):
                df_new['Wuhan'] = df_old['Wuhan']
            if (italy):
                df_new['Italy'] = df_old['Italy']
            if (ca):
                df_new['California'] = df_old['California']
            if (ny):
                df_new['New York'] = df_old['New York']
        elif (ac == 'country'):
            if(china):
                df_new['China'] = df_old['China_all']
            if (italy):
                df_new['Italy'] = df_old['Italy']
            if(usa):
                df_new['USA'] = df_old['USA']

if (granularity == 'Yearly'):
    st.subheader('Number of published documents in each year')
    if (cat == 'Peer reviewed/not'):
        start_year, end_year = st.slider("Select year Range:", 1870, 2021, (2003, 2020), 1)
        df_yearly = df.loc[(df['publish_date'].dt.year >= start_year) & (df['publish_date'].dt.year <= end_year)]
    else:
        start_year, end_year = st.slider("Select year Range:", 1992, 2021, (2003, 2020), 1)
        df_yearly = df_a.loc[(df_a['publish_date'].dt.year >= start_year) & (df_a['publish_date'].dt.year <= end_year)]
    if (cat == 'Peer reviewed/not'):
        df_yearly = df_yearly.groupby(pd.Grouper(key='publish_date', freq='Y'))['peer_reviewed','ArXiv/BioRxiv/MedExiv'].agg('sum').reset_index('publish_date')
    else:
        df_yearly = df_yearly.groupby(pd.Grouper(key='publish_date', freq='Y'))['Wuhan', 'Italy','China','California','New York','China_all','USA'].agg('sum').reset_index('publish_date')
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
        df_monthly = df_ao.loc[df_ao['publish_date'].dt.date >= start_month]
        df_monthly = df_monthly.loc[df_monthly['publish_date'].dt.date <= end_month]
        df_monthly = df_monthly.groupby(pd.Grouper(key='publish_date', freq='M'))['Wuhan', 'Italy', 'China', 'California','New York','China_all','USA'].agg('sum').reset_index('publish_date')

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
        df_weekly = df_ao.loc[df_ao['publish_date'].dt.date >= start_week]
        df_weekly = df_weekly.loc[df_weekly['publish_date'].dt.date <= end_week]
        df_weekly = df_weekly.groupby(pd.Grouper(key='publish_date', freq='W'))['Wuhan', 'Italy', 'China', 'California','New York','China_all','USA'].agg(
            'sum').reset_index('publish_date')

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
        df_daily = df_ao.loc[df_ao['publish_date'].dt.date >= start_day]
        df_daily = df_daily.loc[df_daily['publish_date'].dt.date <= end_day]
    df_daily = df_daily.set_index('publish_date')
    df_d_daily = pd.DataFrame(index=df_daily.index)
    selected_df(df_d_daily, df_daily)
    st.bar_chart(df_d_daily)







