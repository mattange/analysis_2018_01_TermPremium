# -*- coding: utf-8 -*-
"""

created by Matteo


"""
import pandas as pd
import seaborn as sns
from irmodels.affine import ACMUnspanned, ACM
from irmodels.irconventions import CurveConv
from irmodels.genericirmodel import MarketDataType


b = MarketDataType.swap


tenors = [1,2,3,4,5,10,15,20,30]
iterables = [['US','EU','JP','GB','CA','AU'], tenors]
midx = pd.MultiIndex.from_product(iterables,names=['country','tenor'])
tp = pd.DataFrame(data=None, index=yieldsus.index, columns=midx)
stexp = pd.DataFrame(data=None, index=yieldsus.index, columns=midx)

freq = 52

#US
c_us = CurveConv("USD")
a_us = ACMUnspanned()
a_us.initialize(yieldsus,b,c_us,cbbslogus,freq=freq)
a_us.fit()
tp_us = a_us.term_premium()[tenors]
tp_us.name = 'US'
tp['US'] = tp_us
r_us = a_us.interpolate()[tenors]
stexp['US'] = r_us - tp_us


#EU
c_eu = CurveConv("EUR")
a_eu = ACMUnspanned()
a_eu.initialize(yieldseu,b,c_eu,cbbslogeu,freq=freq)
a_eu.fit()
tp_eu = a_eu.term_premium()[tenors]
tp_eu.name = 'EU'
tp['EU'] = tp_eu
r_eu = a_eu.interpolate()[tenors]
stexp['EU'] = r_eu - tp_eu


#GB
c_gb = CurveConv("GBP")
a_gb = ACMUnspanned()
a_gb.initialize(yieldsgb,b,c_gb,cbbsloggb,freq=freq)
a_gb.fit()
tp_gb = a_gb.term_premium()[tenors]
tp_gb.name = 'GB'
tp['GB'] = tp_gb
r_gb = a_gb.interpolate()[tenors]
stexp['GB'] = r_gb - tp_gb


#JP
c_jp = CurveConv("JPY")
a_jp = ACMUnspanned()
a_jp.initialize(yieldsjp,b,c_jp,cbbslogjp,freq=freq)
a_jp.fit()
tp_jp = a_jp.term_premium()[tenors]
tp_jp.name = 'JP'
tp['JP'] = tp_jp
r_jp = a_jp.interpolate()[tenors]
stexp['JP'] = r_jp - tp_jp


#CA
c_ca = CurveConv("CAD")
a_ca = ACMUnspanned()
a_ca.initialize(yieldsca,b,c_ca,cbbslogca,freq=freq)
a_ca.fit()
tp_ca = a_ca.term_premium()[tenors]
tp_ca.name = 'CA'
tp['CA'] = tp_ca
r_ca = a_ca.interpolate()[tenors]
stexp['CA'] = r_ca - tp_ca


#AU
c_au = CurveConv("AUD")
a_au = ACMUnspanned()
a_au.initialize(yieldsau,b,c_au,cbbslogau,freq=freq)
a_au.fit()
tp_au = a_au.term_premium()[tenors]
tp_au.name = 'AU'
tp['AU'] = tp_au
r_au = a_au.interpolate()[tenors]
stexp['AU'] = r_au - tp_au


tp10y = tp.T.xs(10,level='tenor').T
tp2y = tp.T.xs(2,level='tenor').T
stexp10y = stexp.T.xs(10,level='tenor').T
stexp2y = stexp.T.xs(2,level='tenor').T

tp10y_1yavg = tp10y.rolling(freq).mean()
tp2y_1yavg = tp2y.rolling(freq).mean()