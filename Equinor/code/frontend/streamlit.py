import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import streamlit.components.v1 as components
from scipy.signal import savgol_filter

import plotly.graph_objects as go

st.set_page_config(layout="wide")
now = datetime.now() - timedelta(days=2)
today = datetime(now.year, now.month, now.day)
st.markdown(f"<h1 style='text-align: center; color: black;'>Twitter News Dashboard: {str(today).split(' ')[0]}</h1>", unsafe_allow_html=True)
#st.header(f"Twitter News Dashboard: {str(today).split(' ')[0]}")
st.header("#")



st.subheader("Entity Tracker")


col1, col2, col3, col4, col5, col6 = st.columns(6)



with open(f"./data/daily_data/ner_changes/{today}_ner_changes.json", "r") as f:
    d = json.load(f)

df = pd.read_json(f"./data/topics_over_time2.json")
df = df[df.index <= now]
topics = df.columns.tolist()
#selected_options = col1.multiselect('topic:',topics)
option2 = col1.selectbox(
    'Select Entity',
    ('GPE', 'PERSON', 'NORP', 'ORG'))
cols = [col2,col3,col4,col5,col6]
i=0
for x, y in zip(list(d[option2].keys())[0:5], list(d[option2].values())[0:5]):
    cols[i].metric(label=x.title(), value=y["Quantity"], delta=str(y["%Change"]) + '%')
    i = i+1


col1.markdown("#")
col1.subheader("Topic Tracker")
col4.header("#")
col4.header("#")
col4.header("#")
col4.header("#")
container = col4.container()

all = col4.checkbox("Select all")
if all:
    selected_options = container.multiselect("Select one or more options:", topics, topics)
else:
    selected_options = container.multiselect("Select one or more options:",
                                             topics)
#df2 = df[df["topic"].isin(selected_options)]
df2 = df[selected_options]
smooth = col4.checkbox("Smoothing")
if smooth:
    window = col4.select_slider('Smoothing Level', options=[i for i in range(5,51)])
    df_filtered = df2.apply(lambda x: [max(y, 0) for y in savgol_filter(x, window, 4)])
    fig = px.line(df_filtered, width=800, height=400)
else:
    fig = px.line(df2, width=800, height=400, labels={'x' : "Date", 'y' : "Frequency"})
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([

                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=2,
                     label="2m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="ytd",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="All",
                     step="all")

            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
fig.update_layout(
    xaxis_title="Date", yaxis_title="Frequency")
col1.plotly_chart(fig)
col1.subheader("TTF Front Month Price Data")
with col1:
    components.html(
        """
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
        <div id="tradingview_78fe8"></div>
        <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/ICEEUR-TFM1!/" rel="noopener" target="_blank"><span class="blue-text">TFM1! Chart</span></a> by TradingView</div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget(
        {
            "width": 800,
            "height": 300,
            "symbol": "ICEEUR:TFM1!",
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "2",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "range":"12m",
            "enable_publishing": false,
            "hide_top_toolbar": true,
            "allow_symbol_change": true,
            "container_id": "tradingview_78fe8"
        }
        );
      </script>
        </div>
        <!-- TradingView Widget END -->
                """,
        height=300,
        width=800,
    )
with open("./data/monthly_data/words_per_class_wednesday.json") as f:
    keywords = pd.read_json(f)

keywords = {k: [x for x in v] for k, v in keywords.items()}
#keywords =keywords.pop('-1')
col5.header("#")
col5.header("#")
col5.header("#")
col5.header("#")

option = col5.selectbox("Topic Keywords", topics)
#for word in keywords[option]:
 #   st.markdown(word.title())
col5.markdown(", ".join([x.title() for x in keywords[option]]))





