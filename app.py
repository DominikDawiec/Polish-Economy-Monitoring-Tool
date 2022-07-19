import streamlit as st
from datetime import date

import yfinance as yf
from plotly import graph_objs as go

class Company:
    def __init__(self, ticker):
        price_df = si.get_data(ticker, dt.datetime.now()-dt.timedelta(days=2*365), dt.datetime.date(dt.datetime.now()))
        overview_df = si.get_stats(ticker)
        overview_df = overview_df.set_index('Attribute')
        overview_dict = si.get_quote_table(ticker)
        income_statement = si.get_income_statement(ticker)
        balance_sheet = si.get_balance_sheet(ticker)
        cash_flows = si.get_cash_flow(ticker)
        
        
        
self.year_end = overview_df.loc['Fiscal Year Ends'][0]
self.market_cap = get_integer(overview_dict['Market Cap'])
self.market_cap_cs = '{:,d}'.format(int(self.market_cap))
self.prices = price_df['adjclose']

self.sales = income_statement.loc['totalRevenue'][0]
self.gross_profit = income_statement.loc['grossProfit'][0]
self.ebit = income_statement.loc['ebit'][0]
self.interest = - income_statement.loc['interestExpense'][0]
self.net_profit = income_statement.loc['netIncome'][0]

def get_overview(self):
        self.price_earnings_ratio = self.market_cap/self.net_profit
        self.ev_sales_ratio = self.ev/self.sales
        self.overview_dict = {
            'Values' : [self.ev_cs, self.market_cap_cs, self.ev_sales_ratio, self.price_earnings_ratio]
            }

def get_profit_margins(self):
        self.gross_margin = self.gross_profit/self.sales
        self.operating_margin = self.ebit/self.sales
        self.net_margin = self.net_profit/self.sales
        self.profit_margin_dict = {
            'Values' : [self.gross_margin, self.operating_margin, self.net_margin]
            }
        
        
st.title('Financial Dashboard')
ticker_input = st.text_input('Please enter your company ticker:')
search_button = st.button('Search')

if search_button:
    company = Company(ticker_input)
    company.get_overview()
    company.get_profit_margins()
    company.get_liquidity_ratios()
    company.get_leverage_ratios()
    company.get_efficiency_ratios()
    
    
    
st.header('Company overview')
    overview_index = ['Enterprise value', 'Market cap', 'EV/sales ratio', 'P/E ratio']
    overview_df = pd.DataFrame(company.overview_dict, index = overview_index)
    st.line_chart(company.prices)
    st.table(overview_df)

    with st.beta_expander('Profit margins (as of {})'.format(company.year_end)):
        profit_margin_index = ['Gross margin', 'Operating margin', 'Net margin']
        profit_margin_df = pd.DataFrame(company.profit_margin_dict, index = profit_margin_index)
        st.table(profit_margin_df)
        st.bar_chart(profit_margin_df)
