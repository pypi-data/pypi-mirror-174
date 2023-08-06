# StockHero  
## Download market data from finance APIs and other sources
> It's an open-source tool that uses publicly available APIs and other sources, and is intended for research and educational purposes.  
  
[![Downloads](https://pepy.tech/badge/stockhero)](https://pepy.tech/project/stockhero)
  

## New Features in 0.4.1
* new stuff

### New Features planned for the next release
- fix more "features" (bugs)

## The Ticker module
The ```Ticker``` module, gets the financial data from nasdaq.com, morningstar.com, yahoo.com as a pandas.DataFrame <br>

```python

import StockHero as stock
nvda = stock.Ticker('NVDA') # e.g. NVIDIA Corp
#or
nvda = stock.Ticker('US67066G1040') # e.g. NVIDIA Corp

''' Morningstar - Down since 23.06.2022 '''
#nvda.morningstar.financials             # Financials
#nvda.morningstar.marginofsales          # Margins % of Sales
#nvda.morningstar.profitability          # Profitability
#nvda.morningstar.cf_ratios              # Cash Flow - Cash Flow Ratios
#nvda.morningstar.bs                     # Balance Sheet Items (in %)
#nvda.morningstar.li_fin                 # Liquidity/Financial Health
#nvda.morningstar.efficiency             # Efficiency

''' Morningstar '''
nvda.morningstar.quote                  # Quote
nvda.morningstar.growth_rev             # Growth - Revenue %
nvda.morningstar.growth_op_inc          # Growth - Operating Income %
nvda.morningstar.growth_net_inc         # Growth - Net Income %
nvda.morningstar.growth_eps             # Growth - EPS %

''' Yahoo Finance '''
nvda.yahoo.statistics                   # Statistics
nvda.yahoo.statistics_p                 # Statistics - PreProcessed

''' NASDAQ '''
nvda.nasdaq.summ                        # Summary
nvda.nasdaq.div_hist                    # Dividend History
nvda.nasdaq.hist_quotes_stock           # Historical Quotes for Stocks
nvda.nasdaq.hist_quotes_etf             # Historical Quotes for ETFs
nvda.nasdaq.hist_nocp                   # Historical Nasdaq Official Closing Price (NOCP)
nvda.nasdaq.fin_income_statement_y      # Financials - Income Statement - Yearly
nvda.nasdaq.fin_balance_sheet_y         # Financials - Balance Sheet    - Yearly
nvda.nasdaq.fin_cash_flow_y             # Financials - Cash Flow        - Yearly
nvda.nasdaq.fin_fin_ratios_y            # Financials - Financial Ratios - Yearly
nvda.nasdaq.fin_income_statement_q      # Financials - Income Statement - Quarterly
nvda.nasdaq.fin_balance_sheet_q         # Financials - Balance Sheet    - Quarterly
nvda.nasdaq.fin_cash_flow_q             # Financials - Cash Flow        - Quarterly
nvda.nasdaq.fin_fin_ratios_q            # Financials - Financial Ratios - Quarterly
nvda.nasdaq.earn_date_eps               # Earnings Date - Earnings Per Share
nvda.nasdaq.earn_date_surprise          # Earnings Date - Quarterly Earnings Surprise Amount
nvda.nasdaq.yearly_earn_forecast        # Earnings Date - Yearly Earnings Forecast 
nvda.nasdaq.quarterly_earn_forecast     # Earnings Date - Quarterly Earnings Forecast 
nvda.nasdaq.pe_peg_forecast             # Price/Earnings, PEG Ratios, Growth Rates Forecast

''' Gurufocus '''
nvda.gurufocus.pe_ratio_av              # Historical Average Price/Earnings-Ratio
nvda.gurufocus.debt_to_ebitda           # Debt-to-EBITDA Ratio
```

## The StockExchange module
The ```StockExchange``` module, gets the financial data from the NASDAQ Stock Screener, Börse Hamburg / Hannover as a pandas.DataFrame <br>
Added CNN Fear and Greed Index

```python
import StockHero as stock
t = stock.StockExchange('something') # e.g. Nasdaq

''' NASDAQ '''
t.nasdaq                              # Nasdaq Stock Market

''' CNN '''
t.cnn_fear_and_greed                  # CNN Fear and Greed Index

''' Börse Hamburg / Hannover - Down since 23.06.2022 '''
#t.dax                                 # DAX Performance-Index
#t.mdax                                # MDAX Performance-Index
#t.sdax                                # SDAX Performance-Index
#t.tecdax                              # TecDAX Performance-Index
#t.nisax                               # NISAX 20 Index
#t.eurostoxx                           # EURO STOXX 50 Index
#t.gcx                                 # GCX Global Challenges Performance-Index
#t.gevx                                # Global Ethical Values Index
#t.gergenx                             # German Gender Index
#t.dow_jones                           # Dow Jones Industrial Average Index (Attention ! - Index is not provided correctly from provider site)
#t.nasdaq_100                          # Nasdaq-100 Index (Attention ! - Index is not provided correctly from provider site)
```

## Combining both modules
You can combine both modules, for example
```python
import StockHero as stock
t = stock.StockExchange('something')
df = t.nasdaq
ticker = df.loc[df['Name'].str.contains('NVIDIA'), 'Symbol'].values[0]
n = stock.Ticker(ticker)
n.morningstar_quote
```

### Installing
https://pypi.org/project/StockHero/

### Legal Stuff

StockHero is distributed under the Apache Software License

### Any feedback or suggestions, let me know
Or in the words of Peter Thiel:
> We wanted flying cars, instead we got 140 characters
<br>
<br>
### Versions <br>
0.4.1  New stuff <br>
0.4.0  New architecture (again) <br>
0.3.3  Minor fixes (Morningstar) <br>
0.3.2  Minor fixes (Yahoo Finance) <br>
0.3.1  New architecture <br>
0.2.10 Minor fixes (Morningstar Quote) <br>
0.2.9  Minor fixes (Fear and Greed Index) <br>
0.2.8  Minor fixes <br>
0.2.7  Bug fixes, added indizies from Börse Hamburg / Hannover, added data from Gurufocus <br>
0.2.6  Bug fixes, Code Cleanup, added data from Gurufocus, added CNN Fear and Greed Index <br>
0.2.5  Bug fixes, Code cleanup <br>
0.2.4  Bug fixes <br>
0.2.3  Bug fixes and added first data from Yahoo Finance <br>
0.2.2  Bug fixes and added more data from Morningstar <br>
0.2.1  Added more data from nasdaq.com <br>
0.1.1  Bug fixes <br>
0.1.0  Added the StockExchange modul <br>
0.0.2  Bug fixes / Changed License <br>
0.0.1  First Release