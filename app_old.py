import yfinance as yf   
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Stock Market Analyzer",
    layout="wide",
    page_icon="📈"
)
st.title("📈 Stock Market Analyzer" )
st.markdown("*Analyze stock performance with real-time data and interactive charts*")

st.sidebar.header("Stock Selection")

symbol = st.sidebar.text_input(
    "Enter Stock Ticker Symbol: ",
    value="AAPL",
    help="Example: AAPL, GOOGL, MSFT, TSLA"  
).upper()

period_options = {
    "1 Week": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "Max": "max"
}

selected_period = st.sidebar.selectbox(
    "Select Time Period:",
    options=list(period_options.keys()),
    index=1
)
period = period_options[selected_period]

search_button = st.sidebar.button("🔍 Analyze Stock", type="primary")

if symbol and (search_button or True):
    try:

        with st.spinner(f"Fetching data for {symbol}..."):
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            info = stock.info

            if df.empty:
                st.error(f"No data found for symbol '{symbol}'. Please check the ticker and try again.")
            else:
                st.success(f"Data for {symbol} loaded successfully!")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    current_price = df['Close'][-1]
                    st.metric(
                        label="Current Price",
                        value=f"${current_price:.2f}"
                    )
                with col2:
                    if len(df) > 1:
                        prev_close = df['Close'][-2]
                        change = current_price - prev_close
                        change_percent = (change / prev_close) * 100
                        st.metric(
                            label="Daily Change",
                            value=f"${change:.2f}",
                            delta=f"{change_percent:.2f}%"
                        )
                with col3:
                    volume = df['Volume'][-1]
                    st.metric(
                        label="Volume",
                        value=f"{volume:,}"
                    )
                with col4:
                    market_cap = info.get("marketCap", "N/A")
                    if market_cap != "N/A":
                        if market_cap >= 1e12:
                            market_cap_display = f"${market_cap/1e12:.2f}T"
                        elif market_cap >= 1e9:
                            market_cap_display = f"${market_cap/1e9:.2f}B"
                        elif market_cap >= 1e6:
                            market_cap_display = f"${market_cap/1e6:.2f}M"
                        else:
                            market_cap_display = f"${market_cap}" 
                    else:
                        market_cap_display = "N/A"  
                    st.metric(
                        label="Market Cap",
                        value=market_cap_display
                    )
                st.markdown("-------")

                company_name = info.get("longName", symbol)
                st.subheader(f"📊 {company_name}")
                info_col1, info_col2, info_col3 = st.columns(3)

                with info_col1:
                    st.write(f"**52 Week High:**", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
                    st.write(f"**52 Week Low:**", f"${info.get('fiftyTwoWeekLow', 'N/A')}")
                with info_col2:
                    st.write(f"**PE Ratio:**", f"{info.get('trailingPE', 'N/A')}")
                    st.write(f"**EPS:**", f"${info.get('trailingEps', 'N/A')}")
                with info_col3:
                    st.write("**Industry:**", info.get('industry', 'N/A'))
                    st.write("**Country:**", info.get('country', 'N/A'))
                st.markdown("-------")
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['Close'],
                        mode='lines+markers',
                        name='Closing Price',
                        line=dict(color='#1f77b4', width=2),
                        marker=dict(size=4),
                        hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: $%{y:.2f}<extra></extra>'
                    )
                )
                fig.update_layout(
                    title=f"{symbol} Stock Price -  {selected_period}",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    template="plotly_white",
                    hovermode="x unified",
                    height=500,
                    showlegend=True,
                    xaxis=dict(
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='LightGray'
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='LightGray'
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("-------")
                st.subheader("📊 Statistics")
                stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                with stats_col1:
                    st.metric("Highest Price", f"${df['High'].max():.2f}")
                with stats_col2:
                    st.metric("Lowest Price", f"${df['Low'].min():.2f}")
                with stats_col3:
                    st.metric("Average Price", f"${df['Close'].mean():.2f}")
                with stats_col4:
                    start_price = df['Close'][0]
                    end_price = df['Close'][-1]
                    period_change = ((end_price - start_price) / start_price * 100) if start_price != 0 else 0
                    st.metric("Price Change", f"{period_change:.2f}%")
                st.markdown("-------")
                with st.expander("📄 View Raw Data"):
                    st.dataframe(df.tail(10), use_container_width=True)

                    csv = df.to_csv(index=True).encode('utf-8')
                    st .download_button(
                        label="📥 Download Data as CSV",
                        data=csv,
                        file_name=f"{symbol}_stock_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check if the ticker symbol is correct and try again.")
st.markdown("-------")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>📊 Data provided by Yahoo Finance | Built with Streamlit & yfinance</p>
        <p>⚠️ This tool is for educational purposes only. Not financial advice.</p>
    </div>
    """,
    unsafe_allow_html=True
)
                 