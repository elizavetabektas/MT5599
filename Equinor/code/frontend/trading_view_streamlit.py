# embedding trading view live chart
# code source: https://www.tradingview.com/widget/advanced-chart/
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# formatting
st.title('TTF Daily Price Chart')
st.write('Data from TradingView - 2 Months')
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
        "height": 400,
        "symbol": "ICEEUR:TFM1!",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "light",
        "style": "2",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "range":"2M",
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
    height=600,
    width=900,
)