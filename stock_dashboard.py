import streamlit as st
import yfinance as yf
import altair as alt
import plotly.graph_objects as go

# from test import stock

@st.cache_data
def fetch_stock__info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

@st.cache_data
def fetch_quarterly_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

@st.cache_data
def fetch_annual_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.financials.T

@st.cache_data
def fetch_weekly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='1y', interval='1wk')

# UI
st.title('Stock Dashboard')
symbol = st.text_input('Enter stock symbol (e.g., AAPL, MSFT):', 'AAPL')

information = fetch_stock__info(symbol)

st.header('Company Information')

st.subheader(f'Name: {information["longName"]}')
st.subheader(f'Market Cap: ${information["marketCap"]:,}')
st.subheader(f'PE Ratio: {information["forwardPE"]}')

price_history = fetch_weekly_price_history(symbol)
st.header('Chart')

price_history = price_history.rename_axis('Date').reset_index()
candle_stick_chart = go.Figure(data=[go.Candlestick(x=price_history['Date'],
                                open=price_history['Open'],
                                high=price_history['High'],
                                low=price_history['Low'],
                                close=price_history['Close'])])

st.plotly_chart(candle_stick_chart, use_container_width=True)

quarterly_financials = fetch_quarterly_financials(symbol)
annual_financials = fetch_annual_financials(symbol)

st.header('Financials')
selection = st.segmented_control(label='Period', options=['Quarterly', 'Annual'], default='Annual', key='period')

if selection == 'Quarterly':
    quarterly_financials = quarterly_financials.rename_axis('Quarter').reset_index()
    
    quarterly_financials['Quarter'] = quarterly_financials['Quarter'].astype(str)

    revenue_chart = alt.Chart(quarterly_financials).mark_bar(color='red').encode(
        x='Quarter:O',
        y='Total Revenue:Q'
    )
    st.altair_chart(revenue_chart, use_container_width=True)

    net_income = alt.Chart(quarterly_financials).mark_bar(color='orange').encode(
        x='Quarter:O',
        y='Net Income:Q'
    )
    st.altair_chart(net_income, use_container_width=True)

if selection == 'Annual':
    annual_financials = annual_financials.rename_axis('Year').reset_index()

    annual_financials['Year'] = annual_financials['Year'].astype(str).transform(lambda year: year.split('-')[0])

    revenue_chart = alt.Chart(annual_financials).mark_bar().encode(
        x='Year:O',
        y='Total Revenue:Q'
    )
    st.altair_chart(revenue_chart, use_container_width=True)
    
    net_income = alt.Chart(annual_financials).mark_bar().encode(
        x='Year:O',
        y='Net Income:Q'
    )
    st.altair_chart(net_income, use_container_width=True)