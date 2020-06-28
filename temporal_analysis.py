
import streamlit as st
import argparse
import pandas as pd
import datetime

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

st.subheader('Number of published documents in each year')
start_year = st.slider('What is the start year you want to see distribution?', 1870, 2020, 2000)
end_year = st.slider('What is the end year you want to see distribution?', 1871, 2021, 2020)
df_yearly = df.loc[(df['publish_date'].dt.year >= start_year) & (df['publish_date'].dt.year <= end_year)]
df_yearly = df_yearly.groupby(pd.Grouper(key='publish_date', freq='Y'))['counts'].agg('sum').reset_index('publish_date')
df_yearly = df_yearly.set_index('publish_date')
st.bar_chart(df_yearly)

st.subheader('Number of published documents in monthly granularity')
start_month = st.date_input('what start date you want to see for bars in monthly granularity?', datetime.date(2019, 7, 1), datetime.date(1955, 10, 31),datetime.date(2021, 11, 30))
end_month = st.date_input('what end date you want to see for bars in monthly granularity?', datetime.date(2020, 7, 1), datetime.date(1957, 8, 1), datetime.date(2021, 12, 31))
df_monthly = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_month]
df_monthly = df_monthly.loc[df_monthly['publish_date'].dt.date <= end_month]
df_monthly = df_monthly.groupby(pd.Grouper(key='publish_date', freq='M'))['counts'].agg('sum').reset_index('publish_date')
df_monthly = df_monthly.set_index('publish_date')
st.bar_chart(df_monthly)


st.subheader('Number of published documents in weekly granularity')
start_week = st.date_input('what start date you want to see for bars in weekly granularity?', datetime.date(2020, 1, 1), datetime.date(1955, 10, 31), datetime.date(2021, 11, 30))
end_week = st.date_input('what end date you want to see for bars in weekly granularity?', datetime.date(2020, 7, 1), datetime.date(1957, 8, 1), datetime.date(2021, 12, 31))
df_weekly = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_week]
df_weekly = df_weekly.loc[df_weekly['publish_date'].dt.date <= end_week]
df_weekly = df_weekly.groupby(pd.Grouper(key='publish_date', freq='W'))['counts'].agg('sum').reset_index('publish_date')
df_weekly = df_weekly.set_index('publish_date')
st.bar_chart(df_weekly)

st.subheader('Number of published documents in daily granularity')
start_day = st.date_input('what start date you want to see for bars in daily granularity?', datetime.date(2020, 3, 1), datetime.date(1955, 10, 31), datetime.date(2021, 11, 30))
end_day = st.date_input('what end date you want to see for bars in daily granularity?', datetime.date(2020, 3, 31), datetime.date(1957, 8, 1), datetime.date(2021, 12, 31))
df_daily = df_only_month.loc[df_only_month['publish_date'].dt.date >= start_day]
df_daily = df_daily.loc[df_daily['publish_date'].dt.date <= end_day]
df_daily = df_daily.set_index('publish_date')
st.bar_chart(df_daily)







