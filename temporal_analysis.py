#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import argparse
import pandas as pd

st.title('Cord-19 data analysis')
read_and_cache_csv = st.cache(pd.read_csv)

@st.cache
def load():
    df_url = "https://raw.githubusercontent.com/stephaniewhoo/streamlit/master/data_counts.csv"
    df = pd.read_csv(df_url, error_bad_lines=False)
    df['publish_date'] = pd.to_datetime(df['publish_date'])
    return df

data_load_state = st.text('Loading data...')
df = load()
data_load_state.text("Done! (using st.cache)")

st.subheader('Number of published documents in each year')
df_yearly = df.groupby(pd.Grouper(key='publish_date', freq='Y'))['counts_0512', 'counts_0519'].agg('sum').reset_index('publish_date')
df_yearly = df.set_index('publish_date')
st.bar_chart(df_yearly)

year = st.slider('Which year you want to see distribution in detail?', 1955, 2021, 2019)
df_monthly = df.loc[df['publish_date'].dt.year == year]
df_monthly = df_monthly.groupby(pd.Grouper(key='publish_date', freq='M'))['counts_0512', 'counts_0519'].agg('sum').reset_index('publish_date')
df_monthly = df_monthly.set_index('publish_date')
st.bar_chart(df_monthly)

month = st.slider('Which year you want to see distribution in detail?', 1, 12, 6)
df_weekly = df.loc[((df['publish_date'].dt.year == year) & (df['publish_date'].dt.month == month))]
df_monthly = df_weekly.groupby(pd.Grouper(key='publish_date', freq='W'))['counts_0512', 'counts_0519'].agg('sum').reset_index('publish_date')
df_weekly = df_weekly.set_index('publish_date')
st.bar_chart(df_weekly)





