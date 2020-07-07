
import streamlit as st
import pandas as pd
import datetime
import math

st.title('Cord-19 data analysis')
read_and_cache_csv = st.cache(pd.read_csv)

@st.cache
def load_all():
    df_url = "https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/date_05_26_df_counts.csv"
    df = pd.read_csv(df_url, error_bad_lines=False)
    df['publish_date'] = pd.to_datetime(df['publish_date'])
    return df

def load():
    df_url = "https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/date_05_26_df_counts.csv"
    df_only_month = pd.read_csv(df_url, error_bad_lines=False)
    df_only_month = df_only_month.loc[df_only_month['publish_date'].str.len() > 4]
    df_only_month['publish_date'] = pd.to_datetime(df_only_month['publish_date'])
    return df_only_month

data_load_state = st.text('Loading data...')
df = load_all()
df_only_month = load()
data_load_state.text("Done!")

granularity = st.selectbox(
    "What granularity you would like to see",
    ("Yearly", "Monthly", "Weekly", "Daily")
)

if (granularity == 'Yearly'):
    st.subheader('Number of published documents in each year')
    start_year, end_year = st.slider("Select year Range:", 1870, 2021, (2003, 2020), 1)
    df_yearly = df.loc[(df['publish_date'].dt.year >= start_year) & (df['publish_date'].dt.year <= end_year)]
    df_yearly = df_yearly.groupby(pd.Grouper(key='publish_date', freq='Y'))['counts'].agg('sum').reset_index('publish_date')
    df_yearly['publish_date'] = df_yearly['publish_date'].dt.year
    df_yearly = df_yearly.set_index('publish_date')
    st.bar_chart(df_yearly)

if (granularity == 'Monthly'):
    st.subheader('Number of published documents in monthly granularity')
    start_m, end_m = st.slider("Select date range to see monthly granularity plot:", 1955.0+10/12, 2022.0-1/12, (2003+1/12, 2020.0+1/12), 1/12, format = '')
    ms = math.ceil((start_m - int(start_m)) * 12)
    me = math.ceil((end_m - int(end_m)) * 12)
    start_month = datetime.date(int(start_m), ms, 1)
    end_month = datetime.date(int(end_m), me, 1)
    st.text(f"From: {start_month:%Y}-{start_month:%m} to {end_month:%Y}-{end_month:%m} ")
    df_monthly = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_month]
    df_monthly = df_monthly.loc[df_monthly['publish_date'].dt.date <= end_month]
    df_monthly = df_monthly.groupby(pd.Grouper(key='publish_date', freq='M'))['counts'].agg('sum').reset_index('publish_date')
    df_monthly = df_monthly.set_index('publish_date')
    st.bar_chart(df_monthly)

if (granularity == 'Weekly'):
    st.subheader('Number of published documents in weekly granularity')
    start_w, end_w = st.slider("Select date range to see weekly granularity plot:", 1955.0+10/12, 2022.0-1/12, (2010+10/12, 2020.0+1/12), 1/12,format = '')
    ws = math.ceil((start_w - int(start_w)) * 12)
    we = math.ceil((end_w - int(end_w)) * 12)
    start_week = datetime.date(int(start_w), ws, 1)
    end_week = datetime.date(int(end_w), we, 1)
    st.text(f"From: {start_week:%Y}-{start_week:%m} to {end_week:%Y}-{end_week:%m} ")
    df_weekly = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_week]
    df_weekly = df_weekly.loc[df_weekly['publish_date'].dt.date <= end_week]
    df_weekly = df_weekly.groupby(pd.Grouper(key='publish_date', freq='W'))['counts'].agg('sum').reset_index('publish_date')
    df_weekly = df_weekly.set_index('publish_date')
    st.bar_chart(df_weekly)

if (granularity == 'Daily'):
    st.subheader('Number of published documents in daily granularity')
    start_d, end_d = st.slider("Select date range to see daily granularity plot:", 1955.0+10/12, 2022.0-1/12, (2014+10/12, 2020.0+1/12), 1/12,format = '')
    ds = math.ceil((start_d - int(start_d)) * 12)
    de = math.ceil((end_d - int(end_d)) * 12)
    start_day = datetime.date(int(start_d), ds, 1)
    end_day = datetime.date(int(end_d), de, 1)
    st.text(f"From: {start_day:%Y}-{start_day:%m} to {end_day:%Y}-{end_day:%m} ")
    df_daily = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_day]
    df_daily = df_daily.loc[df_daily['publish_date'].dt.date <= end_day]
    df_daily = df_daily.set_index('publish_date')
    st.bar_chart(df_daily)







