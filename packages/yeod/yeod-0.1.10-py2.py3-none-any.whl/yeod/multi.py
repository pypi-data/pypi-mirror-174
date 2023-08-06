#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yahoo! Finance market data downloader (+fix for Pandas Datareader)
# https://github.com/ranaroussi/yeod
#
# Copyright 2010-2019 Ran Aroussi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function
from abc import abstractmethod
import time as _time
from dateutil.relativedelta import *
import multitasking as _multitasking
import pandas as _pd
import numpy as _np
import requests
import json
import os.path
import os
from functools import reduce


from . import Ticker, utils, fundamentals
from . import shared
from datetime import datetime
import logging

def mkdirs(str):
    paths=str.split("/")    
    pp="."
    for p in paths:
        pp="/".join([pp,p])        
        if not os.path.exists(pp):            
            os.mkdir(pp)


def build(df,date_column):
    df.to_csv("xa.csv")
    df.loc[df[date_column].isna(),date_column]=df["date"]
    df['Datetime'] = _pd.to_datetime(df[date_column])
    df=df.sort_values(by=['Datetime'])
    df=df.groupby(by=['Datetime']).last()
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
    return df

def xxtransform_fundamentals2df(json):
    #filing_date
    df = _pd.DataFrame(json['Financials']['Balance_Sheet']['quarterly']).T


    #print("Balance-Sheet:##############")
    bal = build(df,"filing_date")

    #print(df)

    cf = _pd.DataFrame(json['Financials']['Cash_Flow']['quarterly']).T
    #print("Cashflow:##############")

    cf = build(cf,"filing_date")

    logging.debug(f"Cashflow…\n{cf}")

        
    inc = _pd.DataFrame(json['Financials']['Income_Statement']['quarterly']).T
    #print("IncomeStatement:##############")
    inc = build(inc,"filing_date")

    #print(inc)
        
    # # Earnings
    earn = _pd.DataFrame(json['Earnings']['History']).T
    # #reportDate
    earn=earn.drop(["beforeAfterMarket"],axis=1)
    earn=earn.rename(columns={"currency":"currency_symbol"})
    #print("Earnings:##############")
    logging.debug(f"Earning columns\n:{earn.columns}")
    earn = build(earn,"reportDate")

    #print(earn)

    # print(earn.head(5))

    # Merging them together
    #print("Concat bal,cf,inc and earn")
    dfall = reduce(
        lambda left,right: _pd.merge(
            left,
            right,
            left_index=True, 
            right_index=True, 
            how='outer',
            suffixes=('', '_drop')
        ), 
        [bal, cf, inc, earn]
    )
    #print("Concat bal,cf,inc and earn DONE")

    #print(df.tail(10))

    trend = _pd.DataFrame(json['Earnings']['Trend']).T

    allx=[]
    if len(trend.columns) > 0:
        trend=trend[["date","period","earningsEstimateGrowth","earningsEstimateAvg","growth"]]

        years=(trend["period"] == "+1y") | (trend["period"] == "0y")

        adf_years=trend[years].copy()
        adf_years=adf_years[["date","earningsEstimateGrowth","earningsEstimateAvg"]]
        adf_years["Datetime"]=_pd.to_datetime(adf_years["date"]) #+ relativedelta(months=-12)
        adf_years=adf_years.sort_values(by=['Datetime'])
        adf_years=adf_years.set_index("Datetime")

        df_years=trend[years].copy()
        df_years["Datetimex"]=_pd.to_datetime(df_years["date"]) #+ relativedelta(months=-12)
        df_years["Datetime"]=df_years["Datetimex"] + _pd.DateOffset(months=-12)
        df_years["earningsEstimateGrowth_+1y"]=df_years["earningsEstimateGrowth"]
        df_years["earningsEstimateAvg_+1y"]=df_years["earningsEstimateAvg"]
        df_years=df_years.sort_values(by=['Datetime'])
        df_years=df_years.set_index("Datetime")
        df_years=df_years.drop(["earningsEstimateGrowth","earningsEstimateAvg","growth","period","Datetimex"],axis=1)

        allx=[df_years,adf_years,dfall]
        for idx in [1,2,3]:
            xdf=trend[years].copy()
            xdf["Datetimex"]=_pd.to_datetime(xdf["date"]) 
            xdf["Datetime"]=xdf["Datetimex"] + _pd.DateOffset(months=12*idx)
            xdf[f"earningsEstimateGrowth{idx}"]=xdf["earningsEstimateGrowth"]
            xdf[f"earningsEstimateAvg{idx}"]=xdf["earningsEstimateAvg"]
            xdf=xdf.sort_values(by=['Datetime'])
            xdf=xdf.set_index("Datetime")
            xdf=xdf.drop(["earningsEstimateGrowth","earningsEstimateAvg","growth","period","Datetimex"],axis=1)
            allx.append(xdf)
    else:
        dfall["earningsEstimateAvg_+1y"]=0
        dfall["earningsEstimateGrowth_+1y"]=0
        dfall["earningsEstimateAvg"]=0
        dfall["earningsEstimateAvg1"]=0
        dfall["earningsEstimateAvg2"]=0
        dfall["earningsEstimateAvg3"]=0
        dfall["earningsEstimateGrowth1"]=0
        dfall["earningsEstimateGrowth2"]=0
        dfall["earningsEstimateGrowth3"]=0
        allx=[dfall]

    #print("CONCAT MAIN")
    dftx = reduce(
        lambda left,right: _pd.merge(
            left,
            right,
            left_index=True, 
            right_index=True, 
            how='outer',
            suffixes=('', '_drop')
        ), 
        allx
    )
    #print("CONCAT MAIN DONE!")

    dup_cols = [i for i in dftx.columns if "date" in i or "Date" in i or "_drop" in i]
        
    dftx = dftx.drop(dup_cols, axis=1)

    dftx=dftx.fillna(method="ffill")
    dftx=dftx.fillna(0)

    #logging.info(dftx)
    return dftx.copy()

def fillup(master,df,fix=True):
    idx=_pd.DataFrame(index=master.index,columns={"__IDX"})
    dx = _pd.concat([idx,df],axis=1, join="outer").drop(columns=["__IDX"]).fillna(method='ffill')
    #dx = pd.concat([idx,df],axis=1, join="outer").drop(columns=["__IDX"]).interpolate(method="linear").fillna(method='ffill')
    if fix:
        dx.columns=_pd.MultiIndex.from_tuples(dx.columns)
    return dx

def create_levermann(dx,df,gspc,start,financial_flag=False):
    """
        dx=data
        df=fundamental
        gspcx=index data
    """

    first_data=dx.index[0]

    # print(f"data {type(first_data)}")

    first_fund=df.index[0]
    first_index=gspc.index[0]


    # print(f"fund {type(first_fund)}")
    # print(f"index {type(first_index)}")

    first_data=max([first_data,first_fund,first_index])

    # dx=dx[dx.index >= first_data]
    # df=df[df.index >= first_data]
    # gspc=gspc[gspc.index >= first_data]

    # print("After shrinkage")
    # print(dx)


    gspc=gspc[["Adjusted_Close"]].copy()
    gspc=gspc.rename(columns={"Adjusted_Close":"NORM"})

    # print("Index now:")
    # print(gspc)

    dxx=_pd.concat([df,dx],axis=1).fillna(method="ffill")
    dxx2=_pd.concat([dxx,gspc],axis=1).fillna(method="ffill")


    dxx2=dxx2[dxx2.index >= first_data]


    # print(df[df.index >= first_data])

    #dxx2.set_index("Date",inplace=True)



    dxx2=dxx2.copy()
    dxx2["PE_forward"]=dxx2["Adjusted_Close"]/dxx2["earningsEstimateAvg"]



    # print(dxx2[["PE_forward","Adjusted_Close","earningsEstimateAvg"]])
    
    # print("OK 1")
    now = datetime.now()


#    dxx2=dxx2[dxx2.index >= start].copy()

    dxx2["pe_5years"]=dxx2["Adjusted_Close"]/dxx2["earningsEstimateAvg5"]
    #print(dxx2[["PE_forward","Adjusted_Close","earningsEstimateAvg","earningsEstimateAvg5"]])

    dxx2["perf_6m"]=dxx2["Adjusted_Close"].pct_change(150)
    dxx2["perf_1y"]=dxx2["Adjusted_Close"].pct_change(300)

    #1. Levermann Eigenkapitalrendite LJ, gp, equity_ratio
    dxx2["l1_equity_ratio"]=0
    dxx2.loc[dxx2["gp"]>0.2,"l1_equity_ratio"]=1
    dxx2.loc[dxx2["gp"]<0.1,"l1_equity_ratio"]=-1    

    #2. EBIT Marge LJ, ebit_margin
    dxx2["l2_ebit_margin"]=0
    if financial_flag == False:
        dxx2.loc[dxx2["ebit_margin"]>0.12,"l2_ebit_margin"]=1
        dxx2.loc[dxx2["ebit_margin"]<0.06,"l2_ebit_margin"]=-1 

    #3. Eigenkapitalquote LJ, equity_ratio
    dxx2["l3_equity_ratio"]=0
    if financial_flag == False:
        dxx2.loc[dxx2["equity_ratio"]>0.25,"l3_equity_ratio"]=1
        dxx2.loc[dxx2["equity_ratio"]<0.15,"l3_equity_ratio"]=-1 
    else:
        dxx2.loc[dxx2["equity_ratio"]>0.10,"l3_equity_ratio"]=1
        dxx2.loc[dxx2["equity_ratio"]<0.05,"l3_equity_ratio"]=-1 


    #Stole from Piotrosky-Score
    #f totalCashFromOperatingActivities is greater than netIncome, it gains 1 point towards the score.
    dxx2["l_pio1_4"]=0
    dxx2.loc[dxx2["totalCashFromOperatingActivities"] > dxx2["netIncome"],"l_pio1_4"]=1
    
    #9 Kurs heute gg. Kurs vor 6 Monaten, 
    dxx2["l9_perf_6m"]=0
    dxx2.loc[dxx2["perf_6m"]>0.05,"l9_perf_6m"]=1
    dxx2.loc[dxx2["perf_6m"]<-0.05,"l9_perf_6m"]=-1 

    #10 Kurs heute gg. Kurs vor 12 Monaten, 
    dxx2["l10_perf_1y"]=0
    dxx2.loc[dxx2["perf_1y"]>0.05,"l10_perf_1y"]=1
    dxx2.loc[dxx2["perf_1y"]<-0.05,"l10_perf_1y"]=-1 

    #11 Kursmomentum
    dxx2["l11_momentum"]=0
    dxx2.loc[(dxx2["l9_perf_6m"] == 1) & (dxx2["l9_perf_6m"] != dxx2["l10_perf_1y"]),"l11_momentum"]=1
    dxx2.loc[(dxx2["l10_perf_1y"] == 1) & (dxx2["l9_perf_6m"] != dxx2["l10_perf_1y"]),"l11_momentum"]=-1 


    #12 3 Monatsreversal
    #find the first day where we have data
    sameday=dxx2[["Adjusted_Close","NORM"]].dropna().index[0]


    dxx2["cn"]=dxx2["Adjusted_Close"]/dxx2["Adjusted_Close"].loc[sameday]
    dxx2["nx"]=dxx2["NORM"]/dxx2["NORM"].loc[sameday]
    dxx2=dxx2.fillna(method="ffill")

        
    dxx2["l12_reversal"]=0
    dxx2.loc[(dxx2["cn"]>dxx2["nx"]) & (dxx2["cn"].shift(30)>dxx2["nx"].shift(30)) & (dxx2["cn"].shift(60)>dxx2["nx"].shift(60)),"l12_reversal"]=-1
    dxx2.loc[(dxx2["cn"]<dxx2["nx"]) & (dxx2["cn"].shift(30)<dxx2["nx"].shift(30)) & (dxx2["cn"].shift(60)<dxx2["nx"].shift(60)),"l12_reversal"]=1
    
    #13 Growth
    dxx2["l13_growth"]=0
    dxx2.loc[dxx2["estimatedGrowth"]>0.05,"l13_growth"]=1
    dxx2.loc[dxx2["estimatedGrowth"]<-0.05,"l13_growth"]=-1

    #5 PE 
    dxx2["l5_pe_forward"]=0
    dxx2.loc[dxx2["PE_forward"]>12,"l5_pe_forward"]=1
    dxx2.loc[dxx2["PE_forward"]>16,"l5_pe_forward"]=-1
    dxx2.loc[dxx2["PE_forward"]<0,"l5_pe_forward"]=-1
    
    #4 PE 5 Jahre 
    dxx2["l4_pe_5years"]=0
    dxx2.loc[dxx2["pe_5years"].isna(),"pe_5years"]=dxx2["PE_forward"]
    dxx2.loc[dxx2["pe_5years"]>12,"l4_pe_5years"]=1
    dxx2.loc[dxx2["pe_5years"]>16,"l4_pe_5years"]=-1
    dxx2.loc[dxx2["pe_5years"]<0,"l4_pe_5years"]=-1


    #dxx2=dxx2[dxx2.index <= now]

    #print(dxx3.columns.values)

    #we 10 Leverman Ratios of 13  
    #Large-Caps: L Buy >= 4 -> 3
    #Mid-Caps: L Buy >= 7 -> 5


    #market-cap - wir müssen erst in EUr umrechnen.
    #dxx2["market_cap"]=dxx2["shares"]*dxx2["Adjusted_Close"]
    #dxx2[]

    #"l1_equity_ratio","l2_ebit_margin","l3_equity_ratio","l4_pe_5years","l5_pe_forward","l9_perf_6m","l10_perf_1y","l11_momentum","l12_reversal","l13_growth"
    #we do not have all for levermann
    """
    l_pio1_4 if totalCashFromOperatingActivities > netIncome
    l1_equity_ratio
    l2_ebit_margin
    l3_equity_ratio
    l4_pe_5years
    l5_pe_forward
    l9_perf_6m
    l10_perf_1y
    l11_momentum
    l12_reversal
    l13_growth
    = 11 KPIs in total. (Levermann has 13)
    """
    dxx2["levermann_score"]=dxx2["l_pio1_4"]+dxx2["l1_equity_ratio"]+dxx2["l2_ebit_margin"]+dxx2["l3_equity_ratio"]+dxx2["l4_pe_5years"]+dxx2["l5_pe_forward"]+dxx2["l9_perf_6m"]+dxx2["l10_perf_1y"]+dxx2["l11_momentum"]+dxx2["l12_reversal"]+dxx2["l13_growth"]
    
    #dxx2.to_parquet("data/eod/levermann.parquet")
    
    return dxx2

class Resolver():
    def __init__(self,path,rebuild=False,extension="json"):
        self.path=path
        self.extension=extension
        self.rebuild=rebuild

    def __call__(self,ticker) -> _pd.DataFrame:
        return self.resolve(ticker)

    @abstractmethod
    def iresolve():
        pass

    
    def extension(self):
        return self.extension

    def empty_df(self,index=[]):
        empty = _pd.DataFrame(index=index, data={
            'Open': _np.nan, 'High': _np.nan, 'Low': _np.nan,
            'Close': _np.nan, 'Adj Close': _np.nan, 'Volume': _np.nan})
        empty.index.name = 'Date'
        return empty


    def resolve(self,ticker,api_token,start=None,end=None) -> _pd.DataFrame:
        #print(f"Resolving {ticker} {self.rebuild} from {start} to {end}")
        if end is None:
            end = datetime.now().strftime("%Y-%m-%d")
        if start is None:
            start="2018-01-01"  

        mkdirs(self.path)  
        filepath = f"{self.path}/{ticker}.{self.extension}"
        dx = None
        if not self.rebuild and os.path.exists(filepath):
            #print(f"resolve existing {filepath}")
            dx = self.resolveexisting(filepath)
        else:
            #print(f"resolve new {filepath}")
            dx = self.iresolve(ticker,api_token,start,end,filepath)
            #print("result")
            #print(dx)
        if dx is None:
            shared._ERRORS[ticker]="Empty"
            return self.empty_df()
        return dx

    def makepath(self,ticker,start,end):
        if os.path.exists(self.path) == False:
            if os.path.exists("data") == False:
                os.mkdir("data")
            if os.path.exists(f"data/{self.path}") == False:
                os.mkdir(f"data/{self.path}")
        return f"data/{self.path}/{ticker}_{end}.{self.extension}"

    def resolveexisting(self,filepath):
        # print(f"use existing....{filepath}")
        dx = _pd.read_parquet(filepath)
        # dx.set_index("date",inplace=True)
        return dx.fillna(method='ffill').interpolate(method='linear')




class EurConvertingResolver(Resolver):
    def __init__(self,root="data/eod/core_eur",rebuild=False,asset_forex_map=None):
        super().__init__(path=f"{root}",rebuild=rebuild,extension="parquet")
        self.asset_forex_map=asset_forex_map
        self.root=root

    def iresolve(self,ticker,api_token,start,end,filepath) -> _pd.DataFrame:
        """
        1. loading data from core 
        2. then retrieving the forex data from the supplied map
        """
        all_df=None
        try:
            datapath=f"data/eod/core/{ticker}.parquet"
            df = _pd.read_parquet(datapath)


            #print(df.tail())

            forex_df = self.asset_forex_map[ticker]

            eur_df=forex_df.rename(columns={"Adjusted_Close" : "FOREX","Open":"OpenFOREX"})

            eur_df=eur_df[["FOREX","OpenFOREX"]]

            #print(eur_df.head(5))
            df = df.rename(columns={"Adjusted_Close" : "Adjusted_Close_ORIG","Open":"OpenORIG","Low":"LowORIG","High":"HighORIG","Close":"CloseORIG"})

            all_df = _pd.concat([df,eur_df],axis=1)


            #print(all_df.columns.values)

            all_df=all_df.fillna(method="ffill")

            all_df["Adjusted_Close"]=all_df["Adjusted_Close_ORIG"]*all_df["FOREX"]
            all_df["Close"]=all_df["CloseORIG"]*all_df["FOREX"]
            all_df["Open"]=all_df["OpenORIG"]*all_df["FOREX"]
            all_df["High"]=all_df["HighORIG"]*all_df["FOREX"]
            all_df["Low"]=all_df["LowORIG"]*all_df["FOREX"]
            all_df["market_cap"]=all_df["Adjusted_Close"]*all_df["shares"]

            all_df["levermann_threshold_ratio"]=1000
            all_df.loc[all_df["market_cap"] >= 2000000000,"levermann_threshold_ratio"]=7
            all_df.loc[all_df["market_cap"] >= 5000000000,"levermann_threshold_ratio"]=4            
            all_df.loc[all_df["market_cap"] < 2000000000,"levermann_threshold_ratio"]=10

            #we scale levermann from threshold = 0 to max = 1
            #out scale reaches from 0 .. 11
            #m = 1/(11-tx) c = - tx / (11-tx)
            all_df.loc[all_df["market_cap"] >= 2000000000,"lm"]=1/(11-7)
            all_df.loc[all_df["market_cap"] >= 2000000000,"lc"]=-7/(11-7)
  
  
            all_df.loc[all_df["market_cap"] >= 5000000000,"lm"]=1/(11-4)
            all_df.loc[all_df["market_cap"] >= 5000000000,"lc"]=-4/(11-4)            
            
            all_df.loc[all_df["market_cap"] < 2000000000,"lm"]=1/(11-9)
            all_df.loc[all_df["market_cap"] < 2000000000,"lc"]=-9/(11-9)

            all_df["levermann_score_adjusted"]=all_df["lm"] * all_df["levermann_score"] + all_df["lc"]
            #all_df["levermann_score_adjusted"]=all_df["levermann_score"] / all_df["levermann_threshold_ratio"]



            all_df= all_df.drop(columns=["FOREX","OpenFOREX","OpenORIG","HighORIG","LowORIG","CloseORIG","Adjusted_Close_ORIG","NORM"])


            all_df.to_parquet(f"{self.root}/{ticker}.parquet")
            #print(all_df.tail())
        except Exception as ex:
            print(f"ERROR {ex} on {ticker}")
            return None

        return all_df





class OptionResolver(Resolver):
    def __init__(self,root="data/eod",rebuild=False):
        super().__init__(path=f"{root}/options",rebuild=rebuild,extension="parquet")

    def iresolve(self,ticker,api_token,start,end,filepath) -> _pd.DataFrame:
        url=f"https://eodhistoricaldata.com/api/options/{ticker}?api_token={api_token}&from={start}&to={end}"

        logging.debug(f"{url}")

        okay=False
        try:
            response=requests.get(url)
            okay=True
        except Exception as ex:
            print(f"{ex}")
            okay=False

        
        #print(url)
        if okay == False or response.status_code != 200 or response.status_code >= 400:
             return None
        else:    
            jx=response.json()
            #print(jx)
            datax=[]
            if "data" in jx.keys():                
                data=jx["data"]
                if len(data) == 0:
                    return None
                for values in data:
                   #expirationDate, impliedVolatility, putCallVolumeRatio, putCallOpenInterestRatio
                   map={}
                   map["Date"]=values["expirationDate"]
                   map["iv"]=values["impliedVolatility"]
                   map["pcr"]=values["putCallVolumeRatio"]
                   map["pcr_oi"]=values["putCallOpenInterestRatio"]
                   map["call_oi"]=values["callOpenInterest"]
                   map["put_oi"]=values["putOpenInterest"]                                      

                   datax.append(map)
            jx=json.dumps(datax)
            
            dx=_pd.read_json(jx)
            dx.set_index("Date",inplace=True)
            dx.to_parquet(filepath)
            return dx

    def empty_df(self,index=[]):
        #implied_volatility          pcr  pcr_open_interest
        empty = _pd.DataFrame(index=index, data={
            'iv': _np.nan, 'pcr': _np.nan, 'pcr_oi': _np.nan,"call_oi": _np.nan, "put_oi": _np.nan})
        empty.index.name = 'Date'
        return empty

class DataframeResolver(Resolver):
    def __init__(self,root="date/eod"):
        super().__init__(path=f"{root}/core_eur",extension="parquet")

    def resolve(self,ticker,api_token,start=None,end=None) -> _pd.DataFrame:
        file=f"{self.path}/{ticker}.parquet"
        return _pd.read_parquet(file)


class PathResolver(Resolver):
    def __init__(self,path):
        super().__init__(path,extension="parquet")

    def resolve(self,ticker,api_token,start=None,end=None) -> _pd.DataFrame:
        file=f"{self.path}/{ticker}.parquet"

        if os.path.exists(file):
            return _pd.read_parquet(file)
        else:
            logging.info(f"{file} does not exist")
        
        return None
        

class StockResolver(Resolver):
    def __init__(self,root="data/eod",rebuild=False):
        super().__init__(path=f"{root}/ticker",rebuild=rebuild,extension="parquet")

    def iresolve(self,ticker,api_token,start,end,filepath) -> _pd.DataFrame:
        result=None
        try:
            logging.debug(f"Stockresolver.resolve {ticker} {start} {end} {filepath}")
            url=f"https://eodhistoricaldata.com/api/eod/{ticker}?from={start}&to={end}&fmt=json&period=d&api_token={api_token}"

            try:
                response = requests.get(url)   
                #print(f"got {ticker} response {response.json()}")
            except Exception as iex:
                print(response.json())

            # en(f"{filepath}.json","w") as jfile:
            #     jsonstring=json.dumps(reswith opponse.json())
            #     json.dump(jsonstring,jfile)

            jx=json.dumps(response.json())
            if isinstance(jx,str) and f"{jx}" == "[]":
                result=None
            else:
                #print(f"{ticker} type is {type(jx)}")
                dx=_pd.read_json(jx)
                dx=dx.rename(columns={"date":"Date","open":"Open","high":"High","low":"Low","close":"Close","adjusted_close":"Adjusted_Close","volume":"Volume"})
                dx.set_index("Date",inplace=True)        
                dx.to_parquet(filepath)
                result= dx.fillna(method='ffill').interpolate(method='linear')
                print(f"{ticker} result:")
                print(result.tail(5))
        except Exception as ex:
            logging.error(f"EXCEPTION {ex} error in {url} using {filepath}")
            result=None
        finally:
            return result
    
class ForexResolver(Resolver):
    def __init__(self,root="data/eod",rebuild=False):
        super().__init__(path=f"{root}/forex",rebuild=rebuild,extension="parquet")

    def iresolve(self,ticker,api_token,start,end,filepath) -> _pd.DataFrame:
        result=None
        try:
            #print(f"Stockresolver.resolve {ticker} {start} {end} {filepath}")
            url=f"https://eodhistoricaldata.com/api/eod/{ticker}?from={start}&to={end}&fmt=json&period=d&api_token={api_token}"

            try:
                response = requests.get(url)   
                #print(f"got {ticker} response {response.json()}")
            except Exception as iex:
                logging.error(response.json())

            # with open(f"{filepath}.json","w") as jfile:
            #     jsonstring=json.dumps(response.json())
            #     json.dump(jsonstring,jfile)

            jx=json.dumps(response.json())
            if isinstance(jx,str) and f"{jx}" == "[]":
                result=None
            else:
                #print(f"{ticker} type is {type(jx)}")
                dx=_pd.read_json(jx)
                dx=dx.rename(columns={"date":"Date","open":"Open","high":"High","low":"Low","close":"Close","adjusted_close":"Adjusted_Close","volume":"Volume"})
                dx.set_index("Date",inplace=True)        
                dx.to_parquet(filepath)
                result= dx.fillna(method='ffill').interpolate(method='linear')
        except Exception as ex:
            logging.error(f"EXCEPTION {ex} error in {url} using {filepath}")
            result=None
        finally:
            return result



class EURStockResolver(Resolver):
    """Load a ticker an convert it to EUR"""
    def __init__(self,root="data/eod/ticker_eur",rebuild=False):
        super().__init__(path=f"{root}",rebuild=rebuild,extension="parquet")
        self.stockResolver=StockResolver(rebuild=rebuild)
        self.forexResolver=ForexResolver(rebuild=rebuild)
        self.forex_dfx=load_exchanges()

    def iresolve(self,ticker,api_token,start,end,filepath) -> _pd.DataFrame:
        df = self.stockResolver.resolve(ticker,api_token,start,end)
        
        currency = self.forex_dfx[self.forex_dfx["SYMBOL"]==ticker]["Currency"].values[0]

        if currency == "EUR":
            return df

        if currency is None:
            return None


        forexTicker = f"{currency}EUR.FOREX"
        forex_df = self.forexResolver.resolve(forexTicker,api_token,start,end)


        eur_df=forex_df.rename(columns={"Adjusted_Close" : "FOREX","Open":"OpenFOREX"})

        eur_df=eur_df[["FOREX","OpenFOREX"]]

        df = df.rename(columns={"Adjusted_Close" : "Adjusted_Close_ORIG","Open":"OpenORIG","Low":"LowORIG","High":"HighORIG","Close":"CloseORIG"})

        all_df = _pd.concat([df,eur_df],axis=1)

        all_df=all_df.fillna(method="ffill")

        all_df["Adjusted_Close"]=all_df["Adjusted_Close_ORIG"]*all_df["FOREX"]
        all_df["Close"]=all_df["CloseORIG"]*all_df["FOREX"]
        all_df["Open"]=all_df["OpenORIG"]*all_df["FOREX"]
        all_df["High"]=all_df["HighORIG"]*all_df["FOREX"]
        all_df["Low"]=all_df["LowORIG"]*all_df["FOREX"]

        all_df=all_df.drop(["Adjusted_Close_ORIG","OpenORIG","LowORIG","HighORIG","CloseORIG","FOREX","OpenFOREX"],axis=1)

        all_df.to_parquet(filepath)
        return all_df







def load_exchange(ex):
    with open(f"data/eod/ex/{ex}.json") as f:
        data = json.load(f)

    dfus = _pd.DataFrame(data)
    dfus["Exchange"] = f"{ex}"
    dfus["SYMBOL"] = dfus["Code"].astype(str) + f".{ex}"
    return dfus


def load_exchanges():
    exchanges=["F","BE","MU","HM","HA","STU","XETRA","US"]

    exdf=[]
    for ex in exchanges:
        exdf.append(load_exchange(ex))


    return _pd.concat(exdf)


def threem(str):
    dttm = datetime.strptime(str,"%Y-%m-%d")
    dttm2= dttm + relativedelta(months=-3)
    return datetime.strftime(dttm2,"%Y-%m-%d")

def shiftm(str,amount,start=False):
    dttm = datetime.strptime(str,"%Y-%m-%d")
    dttm2= dttm + relativedelta(months=amount)
    if start == False:
        return datetime.strftime(dttm2,"%Y-%m-%d")
    else:
        return datetime.strftime(dttm2,"%Y-01-01")

def shifty(str,years,start=False):
    return shiftm(str,years*12,start)

def getmap(date,jdata):
    #print(f"get data {date}")
    if date in jdata.keys():
        valuemap=jdata[date]
    else:
        valuemap={}                        
        jdata[date]=valuemap
    return valuemap

def put(data,date,col,value):    
    if value is not None:
        _map = getmap(date,data)
        _map["date"]=date
        _map[col]=value


def value(str,map):
    """returns the value using a path description in a dict"""
    path=str.split("/")
    value = None
    _cmap=map
    for p in path:
        if p == path[-1]:
            if p in _cmap.keys():
                value=_cmap[p]
        elif p in _cmap.keys():
            _cmap = _cmap[p]
    return value

class MissingFieldException(Exception):
    def __init__(self,msg):         
        self.msg = msg
    
    def __repr__(self) -> str:
        return self.msg

    def __str__(self) -> str:
        return self.msg

def processOLD(jsonstr,filepath,jpath : str = None):
    if jpath is not None:
        with open(jpath) as jj:
            data=json.load(jj)
    else:
        data = jsonstr #json.loads(jsonstr)
    #Financals/Balance_Sheet/quarterly

    jdata={}
    valid=True


    # isin = value("General/ISIN",data)

    # if isin is None:
    #     raise MissingFieldException("General/ISIN")

    currencyCode = value("General/CurrencyCode",data)

    if currencyCode is None:
        
        raise MissingFieldException("General/CurrencyCode")

    #clear_directory("data/eod/core")
    mandatories=["Financials/Income_Statement/yearly","Financials/Balance_Sheet/yearly"]

    for p in mandatories:
        valuex =value(p,data)
        if valuex is None or bool(valuex) == False:            
            raise  MissingFieldException(p)
    

    shares=value("SharesStats/SharesOutstanding",data)

    #print("here")

    if shares is not None:
        _map=getmap("2017-01-01",jdata)
        _map["shares"]=shares
        _map["date"]="2017-01-01"



    if "outstandingShares" in data.keys():
            if "quarterly" in data["outstandingShares"]:
                for k in data["outstandingShares"]["quarterly"]:
                    dFormatted = data["outstandingShares"]["quarterly"][k]["dateFormatted"]
                    shares = data["outstandingShares"]["quarterly"][k]["shares"]
                    if dFormatted > "2010-01-01":  
                        #print(f"out shares {dFormatted}")              
                        valuemap=getmap(dFormatted,jdata)
                        valuemap["shares"]=shares
                        valuemap["date"]=dFormatted
            elif "annual" in data["outstandingShares"]:
                for k in data["outstandingShares"]["annual"]:
                    dFormatted = data["outstandingShares"]["annual"][k]["dateFormatted"]
                    shares = data["outstandingShares"]["quarterly"][k]["shares"]  
                    if dFormatted > "2010-01-01":    
                        #print(f"out shares annual {dFormatted}")                               
                        valuemap=getmap(dFormatted,jdata)
                        valuemap["shares"]=shares
                        valuemap["date"]=dFormatted

    if "Earnings" in data.keys():        
        if "History" in data["Earnings"].keys():
            for date in data["Earnings"]["History"]:
                if date > "2010-01-01":                     
                    earnings=data["Earnings"]["History"][date]

                    epsActual=earnings["epsActual"]
                    epsEstimate=earnings["epsEstimate"]
                    reportDate=earnings["reportDate"]
                    tdate=earnings["date"]

                    #print(f"Earnings History {date} {reportDate}")

                    if earnings["epsDifference"] is not None:                        
                        _map=getmap(reportDate,jdata)
                        _map["epsDifference"]=earnings["epsDifference"]
                        _map["date"]=reportDate
                    if earnings["surprisePercent"] is not None:
                        _map=getmap(reportDate,jdata)
                        _map["epsSurprisePercent"]=earnings["surprisePercent"]
                        _map["date"]=reportDate
                    if epsActual is not None:
                        _map=getmap(reportDate,jdata)
                        _map["epsActual"]=epsActual
                        _map["date"]=reportDate
                        written=True
                    if epsEstimate is not None:
                        _map=getmap(reportDate,jdata)
                        _map["epsEstimate"]=epsEstimate
                        _map["date"]=reportDate
                        written=True
        if "Trend" in data["Earnings"].keys():
            for date in data["Earnings"]["Trend"]:
                if date > "2010-01-01":
                    prefix=data["Earnings"]["Trend"][date]["period"]
                    earnings=data["Earnings"]["Trend"][date]
                    _map=getmap(date,jdata)
                    _map["date"]=date

                    #print(f"Earnings Trend {date}")


                    if "+1y" == prefix:
                        earningsEstimateAvg = earnings["earningsEstimateAvg"]
                        current_year = shifty(date,-1,True)
                        put(jdata,current_year,"earningsEstimateAvg_+1y",earningsEstimateAvg) 
                        put(jdata,date,"earningsEstimateAvg",earningsEstimateAvg) 
                        shifts=[1,2,3]
                        for shift in shifts:
                            ndate=shifty(date,shift)
                            idx=shifts.index(shift)+1
                            put(jdata,ndate,f"earningsEstimateAvg{idx}",earningsEstimateAvg)  
                    if "0y" == prefix:
                        earningsEstimateAvg = earnings["earningsEstimateAvg"]
                        put(jdata,date,"earningsEstimateAvg",earningsEstimateAvg)  
                        current_year = shifty(date,-1,True)
                        put(jdata,current_year,"earningsEstimateAvg_+1y",earningsEstimateAvg) 
                        shifts=[1,2,3]
                        for shift in shifts:
                            ndate=shifty(date,shift)
                            idx=shifts.index(shift)+1
                            put(jdata,ndate,f"earningsEstimateAvg{idx}",earningsEstimateAvg)  
                        earningsEstimateGrowth = earnings["earningsEstimateGrowth"]
                        ndate=shifty(date,1,start=True)
                        put(jdata,ndate,f"earningsEstimateGrowth_+1y",earningsEstimateGrowth)  
                    
                           

    if "Financials" in data.keys():
        fdata=data["Financials"]
        if "Cash_Flow" in fdata.keys():
            cashflow=fdata["Cash_Flow"]
            if "quarterly" in cashflow.keys():
                qc=cashflow["quarterly"]
                for date in qc.keys():
                    qdata=qc[date]
                    xdate = qdata["date"]
                    filedate=qdata["filing_date"]
                    if filedate is None:
                        filedate=xdate
                    _map=getmap(filedate,jdata)
                    _map["date"]=filedate
                    netIncome = qdata["netIncome"]
                    if netIncome is not None:
                        _map["netIncome_q"]=netIncome
                    totalCashFromFinancingActivities = qdata["totalCashFromFinancingActivities"]
                    if totalCashFromFinancingActivities is not None:
                        _map["totalCashFromFinancingActivities_q"]=totalCashFromFinancingActivities



        if "Balance_Sheet" in fdata.keys():
            bdata=fdata["Balance_Sheet"]
            if "yearly" in bdata.keys():
                ydata=bdata["yearly"]
                for date in ydata:
                    #print(f"Financials Balance_sheet {date}")
                    yydata=ydata[date]
                    filing_date = yydata["filing_date"]
                    if filing_date is None:
                        filing_date = date
                    totalStockholderEquity = yydata["totalStockholderEquity"]
                    totalAssets = yydata["totalAssets"]

                    yshares=yydata["commonStockSharesOutstanding"]

                    commonStockSharesOutstanding=yydata["commonStockSharesOutstanding"]


                    value_map=getmap(filing_date,jdata)


                    if commonStockSharesOutstanding is not None:
                        if not "shares" in value_map.keys():
                            value_map["shares"]=commonStockSharesOutstanding
                    if totalStockholderEquity is not None:
                        value_map["totalStockholderEquity"] = totalStockholderEquity
                    if totalAssets is not None:
                        value_map["totalAssets"]=totalAssets


           
                            

        if "Income_Statement" in fdata.keys():            
            bdata=fdata["Income_Statement"]
            if "yearly" in bdata.keys():
                ydata=bdata["yearly"]
                for date in ydata:
                    #print(f"Financials Income_Statement {date}")
                    yydata=ydata[date]
                    filing_date = yydata["filing_date"]
                    if filing_date is None:
                        filing_date = date
                    incomeBeforeTax = yydata["incomeBeforeTax"]
                    ebit = yydata["ebit"]
                    netIncome = yydata["netIncome"]
                    totalRevenue = yydata["totalRevenue"]
                    value_map=getmap(filing_date,jdata)
                    value_map["date"]=filing_date
                    if incomeBeforeTax is not None:
                        value_map["incomeBeforeTax"]=incomeBeforeTax

                    if ebit is not None:
                        value_map["incomeBeforeTax"]=ebit
                    if netIncome is not None:
                        value_map["netIncome"]=netIncome
                    if totalRevenue is not None:
                        value_map["totalRevenue"]=totalRevenue

            
        
        alldata=[]
        dates=[]
        #logging.info(jdata)
        #print(jdata)
        for key in jdata:
            #print(f"Date:{key}")
            if key >= "2010-01-01":                
                dates.append(key)
        if len(dates) > 0:
            #print(dates)
            dates.sort()
            #
            logging.info(jdata.keys())
            for key in dates:
                
                values=jdata[key]
                #print(f"Date:{key}: XX{values}XX")

                # if "totalAssets" in values.keys() and "totalRevenue" in values.keys() and "costOfRevenue" in values.keys():
                #     print("GPX") 
                #     if values["costOfRevenue"] < 1:
                #         costs=values["totalOperatingExpenses"]
                #     else:
                #         costs=values["costOfRevenue"]
                #     GP = round((values["totalRevenue"] -  costs)/values["totalAssets"],8)
                #     values["gp"]=GP

                alldata.append(values)
                #print(f"{key}: {values}")
            
            #print(f"{filepath}")
            with open(filepath,"w") as jfile:
                json.dump(alldata,jfile)

            df=_pd.read_json(filepath)

            #transform_fundamentals2df

            # logging.info(df)
           
            df=df.rename(columns={"date":"Date"})
            df.set_index("Date",inplace=True)
            df = df.fillna(method="ffill").fillna(0)

            
             
            print(df.columns)
            #Levermann Eigenkapitalrendite LJ
            df["gp"]=round(df["incomeBeforeTax"] / df["totalRevenue"],4)
            # EBIT Marge LJ
            df["ebit_margin"]=round(df["netIncome"] / df["totalStockholderEquity"],4)

            # Eigenkapitalquote LJ
            df["equity_ratio"]=round(df["netIncome"] / df["totalStockholderEquity"],4)

            logging.info(df)
            
            """we use the Income and shares to calculate eps and use this as the estimate"""
           
            if "earningsEstimateAvg" not in df.columns.values:
                df["earningsEstimateAvg"]=df["netIncome"] / df["shares"]


            logging.info(df.columns)
            df.loc[df["earningsEstimateAvg"] == 0  ,"earningsEstimateAvg"]=df["netIncome"] / df["shares"]
            logging.info(df)
            df.loc[df["earningsEstimateAvg"].isna(),"earningsEstimateAvg"]=df["netIncome"] / df["shares"]
            #logging.info("OKAY")
            

            if "earningsEstimateAvg_+1y" not in df.columns.values:
                df["earningsEstimateAvg_+1y"] = df["earningsEstimateAvg"]
            else:
                df.loc[df["earningsEstimateAvg_+1y"] == 0, "earningsEstimateAvg_+1y"]=df["earningsEstimateAvg"]
                df.loc[df["earningsEstimateAvg_+1y"].isna(), "earningsEstimateAvg_+1y"]=df["earningsEstimateAvg"]

            if "earningsEstimateAvg1" not in df.columns.values:
                df["earningsEstimateAvg1"]=df["earningsEstimateAvg"]
            else:
                df.loc[df["earningsEstimateAvg1"].isna(), "earningsEstimateAvg1"]=df["earningsEstimateAvg"]

            

            if "earningsEstimateAvg2" not in df.columns.values:
                df["earningsEstimateAvg2"]=df["earningsEstimateAvg1"]
            else:
                df.loc[df["earningsEstimateAvg2"].isna(), "earningsEstimateAvg2"]=df["earningsEstimateAvg1"]

            if "earningsEstimateAvg3" not in df.columns.values:
                df["earningsEstimateAvg3"]=df["earningsEstimateAvg2"]
            else:
                df.loc[df["earningsEstimateAvg3"].isna(), "earningsEstimateAvg3"]=df["earningsEstimateAvg2"]


            df["earningsEstimateAvg5"]=(df["earningsEstimateAvg1"]+df["earningsEstimateAvg2"]+df["earningsEstimateAvg3"]+df["earningsEstimateAvg"]+df["earningsEstimateAvg_+1y"]) / 5.0
            df["estimatedGrowth"]=(df["earningsEstimateAvg_+1y"]-df["earningsEstimateAvg"])/df["earningsEstimateAvg"]



            #logging.info(df)
            
            return df
        return None
    else:
        return None

def process(jsonstr,filepath,jpath : str = None):
    """transform the fundamentals into something usable for Levermann"""
    if jpath is not None:
        with open(jpath) as jj:
            data=json.load(jj)
    else:
        data = jsonstr #json.loads(jsonstr)

    df=fundamentals.load_fundamentals_json(data)
    """
    currency_symbol
    eps_ttm_+1
    netIncome
    netIncome_ytd
    netIncome_ttm
    roe = Levermann 1
    shares
    eps_ttm
    eps_ttm_1
    eps_ttm_2
    eps_ttm_3
    ebit_marge_lj = Levermann 2
    operatingIncome_ytd
    totalRevenue_ytd
    eigenkapitalrendit_ytd = Levermann 1
    equity_ratio = Eigenkapitalquote LJ   =  Levermann 3
    bal_qtr_totalStockholderEquity
    bal_qtr_totalAssets
    year
    date
    """
    df=df.drop(columns=["currency_symbol","year","date"])
    df = df.astype(float)

    #print("Transformation DONE")
    #for col in df.columns:
    #    print(col)
    
    #Levermann Eigenkapitalrendite LJ
    #OLDdf["gp"]=round(df["incomeBeforeTax"] / df["totalRevenue"],4)
    df["gp"]=round(df["roe"],4)
    #logging.info("L1 passed")
    # EBIT Marge LJ
    #OLD df["ebit_margin"]=round(df["netIncome"] / df["totalStockholderEquity"],4)
    df["ebit_margin"]=round(df["ebit_marge_lj"],4)
    
    #logging.info("L2 passed")
    # Eigenkapitalquote LJ
    #df["equity_ratio"]=round(df["netIncome"] / df["totalStockholderEquity"],4)

    #logging.info("L3 passed")
    
    
    df["earningsEstimateAvg"]=df["eps_ttm"]
    df["earningsEstimateAvg5"]=(df["eps_ttm"]+df["eps_ttm_1"]+df["eps_ttm_2"]+df["eps_ttm_3"]+df["eps_ttm_+1"]) / 5.0
    #logging.info("Pass 9")
    #df["estimatedGrowth"]=(df["earningsEstimateAvg_+1y"]-df["earningsEstimateAvg"])/df["earningsEstimateAvg"]
    #logging.info("Pass 10")
    #print("End of PROCESS")
    return df


def processV2(jsonstr,filepath,jpath : str = None):
    """transform the fundamentals into something usable for Levermann"""
    if jpath is not None:
        with open(jpath) as jj:
            data=json.load(jj)
    else:
        data = jsonstr #json.loads(jsonstr)

    df=transform_fundamentals2df(data)
    """
    currency_symbol
    eps_ttm_+1
    netIncome
    netIncome_ytd
    netIncome_ttm
    roe = Levermann 1
    shares
    eps_ttm
    eps_ttm_1
    eps_ttm_2
    eps_ttm_3
    ebit_marge_lj = Levermann 2
    operatingIncome_ytd
    totalRevenue_ytd
    eigenkapitalrendit_ytd = Levermann 1
    equity_ratio = Eigenkapitalquote LJ   =  Levermann 3
    bal_qtr_totalStockholderEquity
    bal_qtr_totalAssets
    year
    date
    """
    df = df.astype(float)

    #print("Transformation DONE")
    #for col in df.columns:
    #    print(col)
    
    #Levermann Eigenkapitalrendite LJ
    #OLDdf["gp"]=round(df["incomeBeforeTax"] / df["totalRevenue"],4)
    df["gp"]=round(df["roe"],4)
    #logging.info("L1 passed")
    # EBIT Marge LJ
    #OLD df["ebit_margin"]=round(df["netIncome"] / df["totalStockholderEquity"],4)
    df["ebit_margin"]=round(df["ebit_marge_lj"],4)
    
    #logging.info("L2 passed")
    # Eigenkapitalquote LJ
    #df["equity_ratio"]=round(df["netIncome"] / df["totalStockholderEquity"],4)

    #logging.info("L3 passed")
    
    """we use the Income and shares to calculate eps and use this as the estimate"""
    
    if "earningsEstimateAvg" not in df.columns.values:
        df["earningsEstimateAvg"]=df["netIncome"] / df["shares"]


    logging.info(df)

    #logging.info("Shares passed earningsEstimateAvg")
    df.loc[df["earningsEstimateAvg"] == 0  ,"earningsEstimateAvg"]=df["netIncome"] / df["shares"]
    #logging.info(df)
    df.loc[df["earningsEstimateAvg"].isna(),"earningsEstimateAvg"]=df["netIncome"] / df["shares"]
    #logging.info("OKAY")
    
    #logging.info("Pass 5")
    if "earningsEstimateAvg_+1y" not in df.columns.values:
        df["earningsEstimateAvg_+1y"] = df["earningsEstimateAvg"]
    else:
        df.loc[df["earningsEstimateAvg_+1y"] == 0, "earningsEstimateAvg_+1y"]=df["earningsEstimateAvg"]
        df.loc[df["earningsEstimateAvg_+1y"].isna(), "earningsEstimateAvg_+1y"]=df["earningsEstimateAvg"]
    #logging.info("Pass 6")
    if "earningsEstimateAvg1" not in df.columns.values:
        df["earningsEstimateAvg1"]=df["earningsEstimateAvg"]
    else:
        df.loc[df["earningsEstimateAvg1"].isna(), "earningsEstimateAvg1"]=df["earningsEstimateAvg"]

    
    #logging.info("Pass 7")
    if "earningsEstimateAvg2" not in df.columns.values:
        df["earningsEstimateAvg2"]=df["earningsEstimateAvg1"]
    else:
        df.loc[df["earningsEstimateAvg2"].isna(), "earningsEstimateAvg2"]=df["earningsEstimateAvg1"]

    if "earningsEstimateAvg3" not in df.columns.values:
        df["earningsEstimateAvg3"]=df["earningsEstimateAvg2"]
    else:
        df.loc[df["earningsEstimateAvg3"].isna(), "earningsEstimateAvg3"]=df["earningsEstimateAvg2"]
    #ogging.info("Pass 8")
    cc=["earningsEstimateAvg1","earningsEstimateAvg2","earningsEstimateAvg3","earningsEstimateAvg","earningsEstimateAvg_+1y"]
    #df = df.astype(float)
    #logging.info(df[cc].dtypes)
    df["earningsEstimateAvg5"]=(df["earningsEstimateAvg1"]+df["earningsEstimateAvg2"]+df["earningsEstimateAvg3"]+df["earningsEstimateAvg"]+df["earningsEstimateAvg_+1y"]) / 5.0
    #logging.info("Pass 9")
    df["estimatedGrowth"]=(df["earningsEstimateAvg_+1y"]-df["earningsEstimateAvg"])/df["earningsEstimateAvg"]
    #logging.info("Pass 10")
    #print("End of PROCESS")
    return df

def write_json(filepath,ticker,jsonstring):
    with open(f"{filepath}","w") as ofile:
        json.dump(jsonstring,ofile)

class FundamentalResolver(Resolver):
    def __init__(self,root="data/eod",evaluate=False):
        super().__init__(path=f"{root}/fundamental_ext",extension="parquet")
        self.evaluate=evaluate
        self.readpath=f"{root}/fundamental"

    def empty_df(self,index=[]):
        #implied_volatility          pcr  pcr_open_interest
        empty = _pd.DataFrame(index=index, data={
            'totalAssets': _np.nan, 'totalRevenue': _np.nan, 'totalOperatingExpenses': _np.nan,"costOfRevenue": _np.nan, "gp": _np.nan})
        empty.index.name = 'Date'
        return empty

    def iresolve(self,ticker,api_token,start,end,filepath) -> _pd.DataFrame:
        
        jsonfile=f"{filepath}.json"
        reload=True
        xpath=f"{self.readpath}/{ticker}.json"
        #print(f"FundamentalResolver.resolve {xpath}")

        if reload and self.evaluate and os.path.exists(xpath):
            #print(f"Loading from file only {xpath}")
            try:
                dx=process(None,jsonfile,xpath)
                ppath=f"{self.path}/{ticker}.parquet"
                dx.to_parquet(ppath)
            except MissingFieldException as ex:
                print(f"ERROR {ex}")
                return None
            except BaseException as ex:
                print(f"ERROR on {ticker} {ex}")
                return None
            # dx=_pd.read_json(filepath)
            # dx=dx.rename(columns={"date":"Date"})
            # dx.set_index("Date",inplace=True)
            return dx
        else:
            url=f"https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token={api_token}" 
            okay=False
            try:
                response=requests.get(url)
                write_json(xpath,ticker,response.json())
                okay=True
            except Exception as ex:
                print(f"{ex}")
                okay=False
            

            if okay == False or response.status_code != 200 or response.status_code >= 400:
                #(f"ERROR in {url}")
                return None
            else:
                jsonfile=f"{filepath}.json"
                try:
                    logging.debug(f"Writing {jsonfile} {filepath}")
                    dx=process(response.json(),jsonfile)
                    logging.debug("PROCESS DONE")
                    logging.debug(dx)
                    if dx is None or len(dx.index.values) == 0:
                        return None
                    dx.to_parquet(filepath)
                    return dx.fillna(method='ffill').interpolate(method='linear')
                except MissingFieldException as ex:
                    logging.info(f"ERROR ticker:{ticker} Missing Field {ex}")
                    
                    return None
                except Exception as ex:
                    print(f"ERROR other ticker:{ticker} {ex}")
                    return None 


class CoreResolver(Resolver):
    def __init__(self,root="data/eod",asset_index_map=None):
        super().__init__(path=f"{root}/core",extension="parquet")
        self.asset_index_map = asset_index_map
        self.stockResolver = StockResolver(root="data/eod")
        self.fundamentalResolver=FundamentalResolver(root="data/eod",evaluate=True)
        self.infodf=_pd.read_parquet("data/eod/universe_info.parquet")
        

    def iresolve(self,ticker,api_token,start,end,filepath) -> _pd.DataFrame:
        ddx=None
        try:
            start_dt=datetime.strptime(start,"%Y-%m-%d")
            #print(f"CoreResolver.resolve({ticker},{start},{end})")
            data_df = self.stockResolver.resolve(ticker,api_token,start,end)

            last_date=data_df.index[-1]
            fund_df = self.fundamentalResolver.resolve(ticker,api_token,start,end)
            fund_df=fund_df[fund_df.index <= last_date]
            index_symbol = self.asset_index_map[ticker]

            #print(f"found {index_symbol} for {ticker}")
            index_df = self.stockResolver.resolve(index_symbol,api_token,start,end)


            index_df=index_df[index_df.index <= last_date]
            #for Levermann we need to decide for Financial or Non-Financial
            #infodf=_pd.read_parquet("data/eod/universe_info.parquet")
            sector=self.infodf.loc[self.infodf["SYMBOL"] == ticker]["Sector"].values[0]
            financial_flag=False
            if sector == "Financials":
                financial_flag=True
            ddx=create_levermann(data_df,fund_df,index_df,start_dt,financial_flag)

            fcol=_pd.read_csv("config/fundamental_columns.csv")
            
            invalid_cols=fcol[fcol["valid"] == "N"]["column"].tolist()
            logging.debug(f"DROPPING invalid cols {invalid_cols}")
            ddx=ddx.drop(columns=invalid_cols,axis=1)
            ddx.to_parquet(filepath)
        except Exception as ex:
            print(f"Error {ex} in CORE {ticker}")
        return ddx



def download(tickers, start=None, end=None, actions=False, threads=True,
             group_by='column', auto_adjust=False, back_adjust=False,
             progress=True, period="max", interval="1d", prepost=False,
             proxy=None, rounding=False,api_token="",usecache=False,resolver : Resolver = None,**kwargs):
    """Download yahoo tickers
    :Parameters:
        tickers : str, list
            List of tickers to download
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is now
        group_by : str
            Group by 'ticker' or 'column' (default)
        prepost : bool
            Include Pre and Post market data in results?
            Default is False
        auto_adjust: bool
            Adjust all OHLC automatically? Default is False
        actions: bool
            Download dividend + stock splits data. Default is False
        threads: bool / int
            How many threads to use for mass downloading. Default is True
        proxy: str
            Optional. Proxy server URL scheme. Default is None
        rounding: bool
            Optional. Round values to 2 decimal places?
    """

    # create ticker list
    tickers = tickers if isinstance(
        tickers, (list, set, tuple)) else tickers.replace(',', ' ').split()

    tickers = list(set([ticker.upper() for ticker in tickers]))

    if progress:
        shared._PROGRESS_BAR = utils.ProgressBar(len(tickers), 'completed')

    # reset shared._DFS
    shared._DFS = {}
    shared._ERRORS = {}

    # download using threads
    if threads:
        if threads is True:
            threads = min([len(tickers), _multitasking.cpu_count() * 2])
            
        _multitasking.set_max_threads(threads)
        for i, ticker in enumerate(tickers):
            _download_one_threaded(ticker, period=period, interval=interval,
                                   start=start, end=end, prepost=prepost,
                                   actions=actions, auto_adjust=auto_adjust,
                                   back_adjust=back_adjust,
                                   progress=(progress and i > 0), proxy=proxy,
                                   rounding=rounding,api_token=api_token,usecache=usecache,resolver=resolver)
        while len(shared._DFS) < len(tickers):
            _time.sleep(0.01)

    # download synchronously
    else:
        for i, ticker in enumerate(tickers):
            data = _download_one(ticker, period=period, interval=interval,
                                 start=start, end=end, prepost=prepost,
                                 actions=actions, auto_adjust=auto_adjust,
                                 back_adjust=back_adjust, rounding=rounding,api_token=api_token)
            shared._DFS[ticker.upper()] = data
            if progress:
                shared._PROGRESS_BAR.animate()

    if progress:
        shared._PROGRESS_BAR.completed()

    if shared._ERRORS:
        logging.error('\n%.f Failed download%s:' % (
            len(shared._ERRORS), 's' if len(shared._ERRORS) > 1 else ''))
        # print(shared._ERRORS)
        logging.error("\n".join(['- %s: %s' %
                         v for v in list(shared._ERRORS.items())]))

    if len(tickers) == 1:
        return shared._DFS[tickers[0]]

    try:
        data = _pd.concat(shared._DFS.values(), axis=1,
                          keys=shared._DFS.keys())
    except Exception:
        _realign_dfs()
        data = _pd.concat(shared._DFS.values(), axis=1,
                          keys=shared._DFS.keys())

    if group_by == 'column':
        data.columns = data.columns.swaplevel(0, 1)
        data.sort_index(level=0, axis=1, inplace=True)

    return data


def _realign_dfs():
    idx_len = 0
    idx = None

    for df in shared._DFS.values():
        if len(df) > idx_len:
            idx_len = len(df)
            idx = df.index

    for key in shared._DFS.keys():
        try:
            shared._DFS[key] = _pd.DataFrame(
                index=idx, data=shared._DFS[key]).drop_duplicates()
        except Exception:
            shared._DFS[key] = _pd.concat([
                utils.empty_df(idx), shared._DFS[key].dropna()
            ], axis=0, sort=True)

        # remove duplicate index
        shared._DFS[key] = shared._DFS[key].loc[
            ~shared._DFS[key].index.duplicated(keep='last')]


@_multitasking.task
def _download_one_threaded(ticker, start=None, end=None,
                           auto_adjust=False, back_adjust=False,
                           actions=False, progress=True, period="max",
                           interval="1d", prepost=False, proxy=None,
                           rounding=False,api_token="",usecache=False,resolver : Resolver = None):

    data = _download_one(ticker, start, end, auto_adjust, back_adjust,
                         actions, period, interval, prepost, proxy, rounding,api_token,usecache,resolver)
    shared._DFS[ticker.upper()] = data

    if progress:
        shared._PROGRESS_BAR.animate()


def _download_one(ticker, start=None, end=None,
                  auto_adjust=False, back_adjust=False,
                  actions=False, period="max", interval="1d",
                  prepost=False, proxy=None, rounding=False,api_token="",usecache=False,resolver : Resolver = None):

    r = resolver
    if r is None:
        r = StockResolver()
    
    logging.info(f"Downloading {ticker} from {start} until {end}")
    
    return r.resolve(ticker,api_token,start,end)
    #return onetickerx(ticker,fromx=start,to=end,api_token=api_token,usecache=usecache)


def mcreate(paths):
    for path in paths:
        if os.path.exists(path) == False:
            os.mkdir(path)
 
def onetickerx(ticker,fromx="2019-01-01",to="2122-01-01",api_token="",usecache=False):    
    filepath=f"data/ticker/{fromx}_{to}/{ticker}.json"
    url=f"https://eodhistoricaldata.com/api/eod/{ticker}?from={fromx}&to={to}&fmt=json&period=d&api_token={api_token}"

    if os.path.exists(filepath) and usecache: 
        #print(f"Loading from cache {filepath}")
        with open(filepath) as jsonfile:      
            jx=json.load(jsonfile)
        dx=_pd.read_json(json.dumps(jx))
        if len(dx.index.values) == 0:
                #print(f"{ticker} has no data {url}")
                shared._ERRORS[ticker]="Empty"
                return utils.empty_df()
                
        if "date" not in list(dx.columns):
                #print(f"{ticker} has no data {url}")
                shared._ERRORS[ticker]="Empty"
                return utils.empty_df()
        dx=dx.rename(columns={"date":"Date","open":"Open","high":"High","low":"Low","close":"Close","adjusted_close":"Adjusted_Close","volume":"Volume"})
        dx.set_index("Date",inplace=True)
        return dx
    else:
        
        response=requests.get(url)

        if response.status_code != 200 or response.status_code >= 400:
            #print(f"Could not retrieve {ticker}")
            shared._ERRORS[ticker]="Empty"
            return utils.empty_df()
        else:
            mcreate([f"data",f"data/ticker",f"data/ticker/{fromx}_{to}"])
            with open(filepath,"w") as jsonfile:
                json.dump(response.json(),jsonfile)
            jx=json.dumps(response.json())

            dx=_pd.read_json(jx)
            if len(dx.index.values) == 0:
                #print(f"{ticker} has no data {url}")
                shared._ERRORS[ticker]="Empty"
                return utils.empty_df()

            if "date" not in list(dx.columns):
                #print(f"{ticker} has no data {url}")
                shared._ERRORS[ticker]="Empty"
                return utils.empty_df()


            dx=dx.rename(columns={"date":"Date","open":"Open","high":"High","low":"Low","close":"Close","adjusted_close":"Adjusted_Close","volume":"Volume"})
            dx.set_index("Date",inplace=True)

            return dx.fillna(method='ffill').interpolate(method='linear')

