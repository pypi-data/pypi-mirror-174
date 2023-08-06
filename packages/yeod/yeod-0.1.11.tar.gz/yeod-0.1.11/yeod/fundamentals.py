import pandas as _pd
from functools import reduce
import json
import logging
from datetime import datetime

colmap={}

colmap["bal_yr"]=['date', 'filing_date', 'currency_symbol', 'totalAssets',  'totalStockholderEquity',  'cash',  'totalCurrentAssets',  'longTermDebt', 'commonStockSharesOutstanding']
colmap["bal_qtr"]=['date', 'filing_date','currency_symbol', 'totalAssets','earningAssets','totalStockholderEquity','shortLongTermDebt','commonStockSharesOutstanding']
colmap["cf_qtr"]=['date', 'filing_date', 'currency_symbol','dividendsPaid','freeCashFlow']#'netIncome',
colmap["inc_qtr"]=['date', 'filing_date', 'currency_symbol','incomeBeforeTax','netIncome','grossProfit','ebit', 'ebitda',     'operatingIncome', 'totalRevenue', 'totalOperatingExpenses', 'costOfRevenue']
colmap["inc_yr"]=['date', 'filing_date', 'currency_symbol','incomeBeforeTax','netIncome','grossProfit', 'ebit', 'ebitda',     'operatingIncome',  'totalRevenue', 'totalOperatingExpenses', 'costOfRevenue']
colmap["earn_hist"]=['filing_date', 'date',  'currency', 'epsActual', 'epsEstimate']
colmap["earn_trend"]=['date', 'filing_date','period', 'growth', 'earningsEstimateAvg','earningsEstimateGrowth', 'revenueEstimateAvg','revenueEstimateGrowth' ]

idx_map={}

idx_map["inc_qtr"]='filing_date'
idx_map["bal_yr"]= 'filing_date'
idx_map["bal_qtr"]='filing_date'
idx_map["cf_qtr"]='filing_date'
idx_map["inc_qtr"]='filing_date'
idx_map["inc_yr"]='filing_date'
idx_map["earn_hist"]='filing_date'##'reportDate'
idx_map["earn_trend"]='filing_date'#'date'




def xxbuild(df,date_column,prefix=""):
    df.to_csv("xa.csv")
    df.loc[df[date_column].isna(),date_column]=df["date"]
    df['Datetime'] = _pd.to_datetime(df[date_column])
    df['year']=_pd.to_datetime(df['date']).dt.year
    df=df.sort_values(by=['Datetime'])
    df=df.groupby(by=['Datetime']).last()
    #logging.info("DFX")
    #logging.info(df.head(5))
    #df = df.set_index('Datetime')

    if "commonStockSharesOutstanding" in df.columns:
        df["shares"]=df["commonStockSharesOutstanding"]
        df = df.drop(['commonStockSharesOutstanding'], axis=1)

    if "currency_symbol" in df.columns:
        df = df.drop(['date',date_column,'currency_symbol'], axis=1)
    else:
        df = df.drop(['date',date_column], axis=1)
    df = df.astype(float)
    df=df.fillna(method="ffill").fillna(0)
    # for col in df.columns:
    #     print(col)
    if prefix != "":
        df = df.add_prefix(prefix)
    return df

def xxbuild2(dfin,key):
    logging.info(f"Building {key}")
    columns=colmap[key]
    date_column = idx_map[key]
    
    df=dfin[columns].copy()


    df.loc[df[date_column].isna(),date_column]=df["date"]
    df['Datetime'] = _pd.to_datetime(df[date_column])
    df['year']=_pd.to_datetime(df['date']).dt.year
    df=df.sort_values(by=['Datetime'])
    df=df.groupby(by=['Datetime']).last()

    if "commonStockSharesOutstanding" in df.columns:
        df["shares"]=df["commonStockSharesOutstanding"]

    dropcols=[]

    for dcol in ["reportDate","filing_date","date","commonStockSharesOutstanding","currency_symbol","currency"]:
        if dcol in df.columns:
            dropcols.append(dcol)

    df=df.drop(columns=dropcols,axis=1)

    #logging.info(df.dtypes)
    
    df = df.astype(float)
    df=df.fillna(method="ffill").fillna(0)

    if key != "":
        df = df.add_prefix(f"{key}_")

    #logging.info(df.tail(2))
    return df.copy()



def xxcreate_date_map_df(df):
    date_df=df[["date","filing_date"]].copy()
    date_df=date_df.rename(columns={"filing_date" : "filing_date_ref"})
    return date_df


def xxadjust_filingdate(dfyi,date_df):
    #dfy=_pd.merge(dfyi,date_df,how="left",left_on='date',right_on='date',left_index=False,right_index=False,sort=True)
    dfy=_pd.merge(dfyi,date_df,how="left",left_index=True,right_index=True,sort=True)
    dfy['filing_date_x'] = _pd.to_datetime(dfy['filing_date_x'])
    dfy["filing_date_fin"]=dfy[["filing_date_x", "filing_date_y"]].max(axis=1)
    dfy["filing_date"]=dfy["filing_date_fin"]
    dfy["date"]=dfy["date_x"]
    dxx=dfy[["filing_date_fin","filing_date","filing_date_x","filing_date_y","date"]]
    # logging.info(dxx.dtypes)
    # logging.info(f"\n{dxx}")

    columns=["filing_date_fin","filing_date_x","filing_date_y"]

    if "date_x" in dfy.columns:
        columns.append("date_x")
    if "date_y" in dfy.columns:
        columns.append("date_y")

    dfy=dfy.drop(columns=columns,axis=1)
    logging.info(dfy)
    return dfy


def xxake_date(dfi):
    df=dfi[["date","filing_date"]].copy()
    df.set_index("date",inplace=True)
    df["filing_date"]=_pd.to_datetime(df["filing_date"])
    return df

def xxxjoin(df,df2):
    df4=df.join(df2, on=None, how='outer', lsuffix='', rsuffix='x', sort=False)
    df4["fdate"]=df4[["filing_date","filing_datex"]].max(axis=1)
    df4["filing_date"]=df4["fdate"]
    df4=df4.drop(columns=["fdate","filing_datex"])
    df4["date"]=df4.index
    return df4.copy()


def load(dfxmap,key):
   

    df=dfxmap[key]
    dropcols=[]
    if "commonStockSharesOutstanding" in df.columns:
        df["shares"]=df["commonStockSharesOutstanding"]
        dropcols.append("commonStockSharesOutstanding")
    if "currency" in df.columns:
        df=df.rename(columns={"currency" : "currency_symbol"})

    df=df.add_prefix(f"{key}_")
    return df.copy()

def merge_by_index(dfs):
     dfall = reduce(
        lambda left,right: _pd.merge(
            left,
            right,
            left_index=True, 
            right_index=True, 
            how='outer',
            suffixes=('', '_drop')
        ), 
        dfs
     )
     return dfall.copy()

def load_earnings_trend(json):
    trend=None
    if "Earnings" in json.keys():
        if "Trend" in json["Earnings"].keys():
            trend = _pd.DataFrame(json['Earnings']['Trend']).T
            trend=trend[["date","period","earningsEstimateAvg"]]
            trend=trend.loc[(trend["period"] == "0y") | (trend["period"] == "+1y")]
            trend["dttm"]=_pd.to_datetime(trend["date"])
            #df_years["Datetime"]=df_years["Datetimex"] + _pd.DateOffset(months=-12)
            trend["filing_date"]=trend["dttm"]+ _pd.DateOffset(months=-12)
            trend["date"]=trend["filing_date"].dt.strftime("%Y-%m-%d")
            trend=trend.rename(columns={"earningsEstimateAvg":"eps_ttm_+1"})
            trend=trend.sort_values(by=['date'])
            trend=trend.groupby(by=['date']).last()
            trend=trend.drop(columns=["period","dttm"])
    return trend    



    #logging.info(trend)
    return trend


def load_fundamentals(filepath):
    jpath=filepath
    data=None
    if jpath is not None:
        with open(jpath) as jj:
            data=json.load(jj)

    if data is not None:
        return load_fundamentals_json(data)
    else:
        return None

def load_fundamentals_json(json):
    df=unify_fundamentals(json)

    types={}
    for col in df.columns:
        #print(col)
        if "bal" in col or "inc" in col or "cf_" in col or "earn" in col:
            if "currency" not in col:
                types[col]="float"

    df=df.astype(types)

    #logging.info(df[["eps_ttm_+1"]])

    

    #Eigenkapitalrendite LJ
    #the netIncom must be summed up to get a ytd value.
    #totalStockHolderEquity is aleady a total
    keeps=["currency_symbol","eps_ttm_+1"]



    df = df.rename(columns={"inc_qtr_netIncome" : "netIncome" , "bal_qtr_shares" : "shares", "inc_qtr_currency_symbol" : "currency_symbol","earn_trend_eps_ttm_+1":"eps_ttm_+1", "cf_qtr_totalCashFromOperatingActivities":"totalCashFromOperatingActivities"})
    df["netIncome_ytd"]=df.groupby(["year"])["netIncome"].cumsum()
    df["netIncome_ttm"]=df["netIncome"]+df["netIncome"].shift(1)+df["netIncome"].shift(2)+df["netIncome"].shift(3)
    df["roe"]=df["netIncome_ytd"] / df["bal_qtr_totalStockholderEquity"]
    keeps.extend(["netIncome","netIncome_ytd","netIncome_ttm","roe","shares","totalCashFromOperatingActivities"])

    #create eps
    df["eps_ttm"]=df["netIncome_ttm"] / df["shares"]
    df["eps_ttm_1"]=df["eps_ttm"].shift(4)
    df["eps_ttm_2"]=df["eps_ttm"].shift(8)
    df["eps_ttm_3"]=df["eps_ttm"].shift(12)

    #might be that Earnings/Trend is not filled so we build something
    if "eps_ttm_+1" not in df.columns:
        df["eps_ttm_+1"]=df["eps_ttm"]+df["eps_ttm"].shift(1)+df["eps_ttm"].shift(2)+df["eps_ttm"].shift(3)



    df["estimatedGrowth"]=(df["eps_ttm_+1"]-df["eps_ttm"])/df["eps_ttm"]
    #we need the eps for the last 3 years in ttm
    keeps.extend(["eps_ttm","eps_ttm_1","eps_ttm_2","eps_ttm_3","estimatedGrowth"])

    #Ebit Marge LJ
    #yr_totalRevenue
    #yr_operatingIncome
    df["operatingIncome_ytd"]=df.groupby(["year"])["inc_qtr_operatingIncome"].cumsum()
    df["totalRevenue_ytd"]=df.groupby(["year"])["inc_qtr_totalRevenue"].cumsum()
    df["ebit_marge_lj"]= df["operatingIncome_ytd"] / df["totalRevenue_ytd"]
    keeps.extend(["ebit_marge_lj","operatingIncome_ytd","totalRevenue_ytd"])



    
    
    df["eigenkapitalrendit_ytd"]=df["roe"]
    keeps.append("eigenkapitalrendit_ytd")
    

    #Equity Ratio (Eigenkapitalquote LJ)
    df["equity_ratio"]=df["bal_qtr_totalStockholderEquity"] / df["bal_qtr_totalAssets"]
    keeps.extend(["equity_ratio","bal_qtr_totalStockholderEquity","bal_qtr_totalAssets","year","date"])


    #df['eps_current'] = df.groupby(['Year','Customer'])['TotalMonthlySales'].cumsum()


    #logging.info(dxorig)
    #logging.info(dftx[["equity_ratio","ebit_marge_lj","roe","eps_qtr","eps","inc_yr_netIncome","bal_yr_shares","bal_yr_totalStockholderEquity","inc_yr_totalRevenue","inc_yr_operatingIncome"]].tail(13))
    #logging.info(df[["eigenkapitalrendit_ytd","ebit_marge_ytd","year","roe","eps_ytd","eps","netIncome_ytd","bal_qtr_shares","bal_qtr_totalStockholderEquity"]].tail(15))
    #logging.info(df[["eigenkapitalrendit_ytd","year","roe","netIncome_ytd","inc_qtr_netIncome","bal_qtr_totalStockholderEquity"]].tail(15))

    dfx=df[keeps]
    dfx=dfx.fillna(method="ffill")


    #epsx=[i for i in dfx.columns if "eps" in i]
    #logging.info(dfx[epsx].tail(20))


    #xa.to_excel("amzn.xlsx")

    #eigenkapitalrendit_ytd = roe = Levermann 1 OK
    #EBIT Marge LJ = ebit_marge_lj = Levermann 2 OK
    #Eigenkapitalquote LJ  = equity ratio = Levermann 3 OK
    #eps_ttm f+r PE_ttm  OK
    logging.debug(keeps)

    
    return df[keeps].copy()

def unify_fundamentals(json):
    """
    a datum is know after the filing_date. However for a reporting 
    period we can have slightly different filing dates.
    Hence we adjust the filings dates before we do the actual manouvres.
    """

    dfxmap={}
    dfxmap["bal_qtr"]=_pd.DataFrame(json['Financials']['Balance_Sheet']['quarterly']).T
    dfxmap["bal_yr"]=_pd.DataFrame(json['Financials']['Balance_Sheet']['yearly']).T
    dfxmap["cf_qtr"]=_pd.DataFrame(json['Financials']['Cash_Flow']['quarterly']).T
    dfxmap["inc_qtr"]=_pd.DataFrame(json['Financials']['Income_Statement']['quarterly']).T
    dfxmap["inc_yr"]=_pd.DataFrame(json['Financials']['Income_Statement']['yearly']).T

    earnings_trend=load_earnings_trend(json)
    if earnings_trend is not None:
        dfxmap["earn_trend"]=earnings_trend

    dfs=[]
    for key in dfxmap.keys():
        dfs.append(load(dfxmap,key))

    #dfs.append(load_earnings_trend(json))


    df=merge_by_index(dfs)
    logging.debug(df)

    filing_dates=[col for col in df.columns if "filing" in col]
    

    for filing_date in filing_dates:
        df[filing_date]= _pd.to_datetime(df[filing_date])


    df["filing_date"]=df[filing_dates].max(axis=1)
    #interested after 1.1.2017
    df=df.loc[df["filing_date"] > datetime.strptime("2010-12-31","%Y-%m-%d")]
    
    df=df.drop(columns=filing_dates)
    dropdates=[col for col in df.columns if "r_date" in col]
    df=df.drop(columns=dropdates)
    df["date"]=_pd.to_datetime(df.index)
    df["year"]=df["date"].dt.year
    df["filing_date"]=_pd.to_datetime(df["filing_date"])
    df=df.sort_values(by=['filing_date'])
    #now the index is by filing_date but we have a date and a year column,
    df=df.groupby(by=['filing_date']).last()
    


    #logging.info(df[["date","year"]])
    return df




if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    jpath="data/eod/fundamental/AMZN.US.json"
    dx=load_fundamentals(jpath)
