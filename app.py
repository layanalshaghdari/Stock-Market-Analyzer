import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Stock Market Analyzer",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)
def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

def calculate_rsi(data, periods=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast=12, slow=26, signal=9):
    ema_fast = data['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

st.markdown('<h1 class="main-header">📈 Stock Market Analyzer Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced stock analysis with real-time data and technical indicators</p>', unsafe_allow_html=True)

st.sidebar.header("⚙️ Configuration")

symbol = st.sidebar.text_input(
    "📊 Stock Symbol:",
    value="AAPL",
    help="Enter stock ticker (e.g.: AAPL, GOOGL, MSFT, TSLA, 2222.SR for Saudi stocks)"
).upper()

period_options = {
    "1 Week": "5d", 
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "Max": "max"
}

selected_period = st.sidebar.selectbox(
    "⏳ Time Period:",
    options=list(period_options.keys()),
    index=2
)
period = period_options[selected_period]

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Technical Indicators")

show_ma = st.sidebar.checkbox("Show Moving Average", value=True)
show_rsi = st.sidebar.checkbox("Show RSI", value=True)
show_macd = st.sidebar.checkbox("Show MACD", value=True)
show_volume = st.sidebar.checkbox("Show Volume", value=True)

st.markdown("---")
st.sidebar.subheader("🔄 Compare Stocks")
compare_mode = st.sidebar.checkbox("Enable Comparison Mode", value=False)
compare_symbols = []
if compare_mode:
    compare_input = st.sidebar.text_input(
        "Compare with (comma-separated):",
        placeholder="MSFT, GOOGL, TSLA",
        help="Enter multiple stock symbols separated by commas"
    )
    if compare_input:
        compare_symbols = [s.strip().upper() for s in compare_input.split(",") if s.strip()]
analyze_button = st.sidebar.button("🔍 Analyze Stock", type="primary", use_container_width=True)

if symbol and (analyze_button or True):
    try:
        with st.spinner(f"📥 Fetching data for {symbol}..."):
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            info = stock.info

            if df.empty:
                st.success(f"❌ No data found for '{symbol}'. Please check the ticker symbol.")
            else:
                st.success(f"✅ Data loaded successfully for {symbol}")

                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    current_price = df['Close'][-1]
                    st.metric(
                        label="💰 Current Price",
                        value=f"${current_price:.2f}"
                    )
                with col2:
                    if len(df) > 1:
                        prev_close = df['Close'][-2]
                        change = current_price - prev_close
                        change_percent = (change / prev_close) * 100
                        st.metric(
                            label="📊 Daily Change",
                            value=f"${change:.2f}",
                            delta=f"{change_percent:.2f}%"
                        )
                with col3:
                    volume = df['Volume'][-1]
                    st.metric(
                        label="📦 Volume",
                        value=f"{volume:,.0f}"
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
                        label="💼 Market Cap",
                        value=market_cap_display
                    )
                with col5:
                    pe_ratio = info.get("trailingPE", "N/A")
                    if pe_ratio != "N/A":
                        pe_ratio_display = f"{pe_ratio:.2f}"
                    else:
                        pe_ratio_display = "N/A"
                    st.metric(
                        label="📈 P/E Ratio",
                        value=pe_ratio_display
                    )
                st.markdown("-------")

                company_name = info.get("longName", symbol)
                st.subheader(f"📊 {company_name}")
                info_col1, info_col2, info_col3, info_col4 = st.columns(4)

                with info_col1:
                    st.write(f"**Sector:**", f"{info.get('sector', 'N/A')}")
                    st.write(f"**Industry:**", f"{info.get('industry', 'N/A')}")

                with info_col2:
                    st.write(f"**Country:**", f"{info.get('country', 'N/A')}")
                    st.write(f"**Employees:**", f"{info.get('fullTimeEmployees', 'N/A')}")if info.get('fullTimeEmployees') else "N/A"

                with info_col3:
                    st.write("**52W High:**", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
                    st.write("**52W Low:**", f"${info.get('fiftyTwoWeekLow', 'N/A')}")

                with info_col4:
                    st.write("**Dividend Yield:**", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else 'N/A')
                    st.write("**Beta:**", f"{info.get('beta', 'N/A')}")
                st.markdown("-------")

                if show_ma and len(df) >= 50:
                    df['MA50'] = calculate_moving_average(df, 50)
                    if len(df) >= 200:
                        df['MA200'] = calculate_moving_average(df, 200)
                if show_rsi:
                    df['RSI'] = calculate_rsi(df)
                if show_macd:
                    df['MACD'], df['Signal'], df['Histogram'] = calculate_macd(df)
                st.subheader(f"📊 Price Chart & Technical Analysis - {selected_period}")

                num_rows = 1
                row_heights = [0.7]

                if show_volume:
                    num_rows += 1
                    row_heights.append(0.15)

                if show_rsi:
                    num_rows += 1
                    row_heights.append(0.15)
                
                if show_macd:
                    num_rows += 1
                    row_heights.append(0.15)
                row_heights = [h / sum(row_heights) for h in row_heights]

                fig = make_subplots(
                    rows=num_rows,
                    cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.05,
                    row_heights=row_heights,
                    subplot_titles=['Price'] + 
                                   (['Volume'] if show_volume else []) +
                                   (['RSI'] if show_rsi else []) +
                                   (['MACD'] if show_macd else [])
                )
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['Close'],
                        mode='lines+markers',
                        name='Closing Price',
                        line=dict(color='#2E86DE', width=2),
                        marker=dict(size=4),
                        hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: $%{y:.2f}<extra></extra>'
                    ),
                    row=1,col=1
                )
                if show_ma and 'MA50' in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df['MA50'],
                            mode='lines',
                            name='MA 50',
                            line=dict(color='#FFA502', width=1.5, dash='dash'),
                            hovertemplate='<b>MA50</b>: $%{y:.2f}<extra></extra>'
                        ),
                        row=1, col=1
                    )
                    if 'MA200' in df.columns:
                        fig.add_trace(
                            go.Scatter(
                                x=df.index,
                                y=df['MA200'],
                                mode='lines',
                                name='MA 200',
                                line=dict(color='#FF6348', width=1.5, dash='dash'),
                                hovertemplate='<b>MA200</b>: $%{y:.2f}<extra></extra>'
                            ),
                            row=1, col=1
                        )
                    if compare_mode and compare_symbols:
                        for comp_symbol in compare_symbols:
                            try:
                                comp_stock = yf.Ticker(comp_symbol)
                                comp_df = comp_stock.history(period=period)
                                if not comp_df.empty:
                                    normalized = (comp_df['Close'] / comp_df['Close'][0]) * df['Close'][0]
                                    fig.add_trace(
                                        go.Scatter(
                                            x=comp_df.index,
                                            y=normalized,
                                            mode='lines',
                                            name=f'{comp_symbol} (normalized)',
                                            line=dict(width=1.5),
                                            hovertemplate=f'<b>{comp_symbol}</b>: $%{{y:.2f}}<extra></extra>'
                                    ),
                                        row=1, col=1
                                )
                            except:
                                st.warning(f"⚠️ Could not fetch data for comparison symbol '{comp_symbol}'.")
                current_row = 2
                if show_volume:
                    colors=["red" if row['Close'] < row['Open'] else "green" for index, row in df.iterrows()]
                    fig.add_trace(
                        go.Bar(
                            x=df.index,
                            y=df['Volume'],
                            name='Volume',
                            marker_color=colors,
                            showlegend=False,
                            hovertemplate='<b>Volume</b>: %{y:,.0f}<extra></extra>'
                        ),
                        row=current_row, col=1
                    )
                    current_row += 1

                if show_rsi and 'RSI' in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df['RSI'],
                            mode='lines',
                            name='RSI',
                            line=dict(color='#9B59B6', width=2),
                            hovertemplate='<b>RSI</b>: %{y:.2f}<extra></extra>'
                        ),
                        row=current_row, col=1
                    )
                    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=current_row, col=1)
                    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=current_row, col=1)
                    fig.update_yaxes(title_text="RSI", range=[0,100], row=current_row, col=1)
                    current_row += 1
                    
                if show_macd and 'MACD' in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df['MACD'],
                            mode='lines',
                            name='MACD',
                            line=dict(color='#3498DB', width=2)
                        ),
                    row=current_row, col=1
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df['Signal'],
                            mode='lines',
                            name='Signal Line',
                            line=dict(color='#E74C3C', width=2)
                        ),
                        row=current_row, col=1
                    )
                    fig.add_trace(
                        go.Bar(
                            x=df.index,
                            y=df['Histogram'],
                            name='Histogram',
                            marker_color=df['Histogram'].apply(lambda x: 'green' if x > 0 else 'red')
                        ),
                        row=current_row, col=1
                    )
                    fig.update_yaxes(title_text="MACD", row=current_row, col=1)

                fig.update_layout(
                    title=f'{symbol} Stock Analysis - {selected_period}',
                    hovermode='x unified',
                    template='plotly_white',
                    height=800 if num_rows > 2 else 600,
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),   
                )
                fig.update_xaxes(title_text="Date", row=num_rows, col=1)
                fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("-------")
                st.subheader("📊 Key Statistics")

                stats_col1, stats_col2, stats_col3, stats_col4, stats_col5 = st.columns(5)
                with stats_col1:
                    st.metric("📈 Highest", f"${df['High'].max():.2f}")
                with stats_col2:
                    st.metric("📉 Lowest", f"${df['Low'].min():.2f}")
                with stats_col3:
                    st.metric("📊 Average", f"${df['Close'].mean():.2f}")
                with stats_col4:
                    start_price = df['Close'][0]
                    end_price = df['Close'][-1]
                    period_change = ((end_price - start_price) / start_price ) * 100
                    st.metric("📈 Period Change", f"{period_change:.2f}%")
                with stats_col5:
                    volatility = df['Close'].pct_change().std() * np.sqrt(252) * 100
                    st.metric("⚡ Volatility (Annualized)", f"{volatility:.2f}%")
                if show_rsi or show_ma:
                    st.markdown("-------")
                    st.subheader("🎯 Trading Signals")
                    signal_col1, signal_col2, signal_col3 = st.columns(3)
                    with signal_col1:
                        if show_rsi and 'RSI' in df.columns:
                            current_rsi = df['RSI'][-1]
                            if current_rsi > 70:
                                st.error(f"🚨  **RSI Signal:** Overbought ({current_rsi:.2f})")
                            elif current_rsi < 30:
                                st.success(f"✅  **RSI Signal:** Oversold ({current_rsi:.2f}) - Consider Buying.")
                            else:
                                st.info(f"ℹ️  **RSI Signal:** Neutral ({current_rsi:.2f}).")
                    with signal_col2:
                        if show_ma and "MA50" in df.columns and "MA200" in df.columns:
                            ma50_current = df['MA50'][-1]
                            ma200_current = df['MA200'][-1]
                            if ma50_current > ma200_current:
                                st.success("✅ **MA Signal:** Bullish (Golden Cross)")
                            else:
                                st.error("🚨 **MA Signal:** Bearish (Death Cross)")
                    with signal_col3:
                        current_price = df['Close'][-1]
                        if "MA50" in df.columns:
                            ma50 = df['MA50'][-1]
                            if current_price > ma50:
                                st.success(f"✅ **Price vs MA50:** Above ({((current_price/ma50-1)*100):.2f}%)")
                            else:
                                st.error(f"🚨 **Price vs MA50:** Below ({((current_price/ma50-1)*100):.2f}%)")
                    with st.expander("📋 View Historical Data"):
                        display_df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
                        display_df.index = display_df.index.strftime("%Y-%m-%d")
                        st.dataframe(display_df, use_container_width=True)
                        csv = df.to_csv().encode('utf-8')
                        st.download_button(
                            label="📥 Download Data as CSV",
                            data=csv,
                        file_name=f"{symbol}_data_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime='text/csv',
                            use_container_width=True
                        )
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("💡 Please check the ticker symbol and try again.")
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 2rem 0;'>
        <p>📊 <b>Data Source:</b> Yahoo Finance via yfinance | <b>Built with:</b> Streamlit & Plotly</p>
        <p>⚠️ <b>Disclaimer:</b> This tool is for educational purposes only. Not financial advice.</p>
        <p>💡 <b>Tip:</b> Enable technical indicators from the sidebar for advanced analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)