# -*- coding: utf-8 -*-
"""

created by Matteo


"""

import pandas as pd
from matplotlib import pyplot as plt
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
#a_us = ACMUnspanned()
#a_us.initialize(yieldsus,b,c_us,cbbslogus,freq=freq)
a_us = ACM()
a_us.initialize(yieldsus,b,c_us,freq=freq)
a_us.fit()
tp_us = a_us.term_premium()[tenors]
tp_us.name = 'US'
tp['US'] = tp_us
r_us = a_us.interpolate()[tenors]
stexp['US'] = r_us - tp_us


#EU
c_eu = CurveConv("EUR")
a_eu = ACM()
a_eu.initialize(yieldseu,b,c_eu,freq=freq)
a_eu.fit()
tp_eu = a_eu.term_premium()[tenors]
tp_eu.name = 'EU'
tp['EU'] = tp_eu
r_eu = a_eu.interpolate()[tenors]
stexp['EU'] = r_eu - tp_eu


#GB
c_gb = CurveConv("GBP")
a_gb = ACM()
a_gb.initialize(yieldsgb,b,c_gb,freq=freq)
a_gb.fit()
tp_gb = a_gb.term_premium()[tenors]
tp_gb.name = 'GB'
tp['GB'] = tp_gb
r_gb = a_gb.interpolate()[tenors]
stexp['GB'] = r_gb - tp_gb


#JP
c_jp = CurveConv("JPY")
a_jp = ACM()
a_jp.initialize(yieldsjp,b,c_jp,freq=freq)
a_jp.fit()
tp_jp = a_jp.term_premium()[tenors]
tp_jp.name = 'JP'
tp['JP'] = tp_jp
r_jp = a_jp.interpolate()[tenors]
stexp['JP'] = r_jp - tp_jp


#CA
c_ca = CurveConv("CAD")
a_ca = ACM()
a_ca.initialize(yieldsca,b,c_ca,freq=freq)
a_ca.fit()
tp_ca = a_ca.term_premium()[tenors]
tp_ca.name = 'CA'
tp['CA'] = tp_ca
r_ca = a_ca.interpolate()[tenors]
stexp['CA'] = r_ca - tp_ca


#AU
c_au = CurveConv("AUD")
a_au = ACM()
a_au.initialize(yieldsau,b,c_au,freq=freq)
a_au.fit()
tp_au = a_au.term_premium()[tenors]
tp_au.name = 'AU'
tp['AU'] = tp_au
r_au = a_au.interpolate()[tenors]
stexp['AU'] = r_au - tp_au


#summary variables and relative pickles stored in the folder
tp10y = tp.T.xs(10,level='tenor').T
tp2y = tp.T.xs(2,level='tenor').T
stexp10y = stexp.T.xs(10,level='tenor').T
stexp2y = stexp.T.xs(2,level='tenor').T
tp10y.to_pickle('tp10y.dat')
tp2y.to_pickle('tp2y.dat')
stexp10y.to_pickle('stexp10y.dat')
stexp2y.to_pickle('stexp2y.dat')

#store the central banks balance sheets to pickles
allcbbslog.to_pickle('allcbbslog.dat')
uscbbs.to_pickle('uscbbs.dat')
eucbbs_usd.to_pickle('eucbbs_usd.dat')
jpcbbs_usd.to_pickle('jpcbbs_usd.dat')
gbcbbs_usd.to_pickle('gbcbbs_usd.dat')
cncbbs_usd.to_pickle('cncbbs_usd.dat')

tp10y_1qtr = tp10y.rolling(12).mean()
tp2y_1qtr = tp2y.rolling(12).mean()

sns.set()
sns.set_palette(sns.dark_palette('red'))
fig,ax = plt.subplots(2,1)
plt.sca(ax[0])
plt.title('3M running averages')
plt.ylabel('2y term premium (%)')
tp2y_1qtr.plot(ax=ax[0])
ax[0].legend_.remove()
plt.sca(ax[1])
plt.ylabel('10y term premium (%)')
tp10y_1qtr.plot(ax=ax[1])


fig,ax = plt.subplots(1,1)
sns.regplot(allcbbslog, tp10y['US'])
sns.regplot(allcbbslog, tp10y['EU'])
sns.regplot(allcbbslog, tp10y['JP'])
sns.regplot(allcbbslog, tp10y['GB'])
sns.regplot(allcbbslog, tp10y['CA'])
sns.regplot(allcbbslog, tp10y['AU'])
plt.ylabel('10y term premium %')
plt.xlabel('Log of Global Major Central Banks balance sheets sum in USDm')
plt.legend(['US','EU','JP','GB','CA','AU'])


fig, ax = plt.subplots(2,1)
plt.sca(ax[0])
plt.title('Major central banks balance sheets')
allcbbslog.plot(color='k',grid=True, ax=ax[0])
plt.ylabel('Log (from USDm amounts)')
plt.sca(ax[1])
(uscbbs/1e6).plot()
(eucbbs_usd/1e6).plot()
(jpcbbs_usd/1e6).plot()
(gbcbbs_usd/1e6).plot()
(cncbbs_usd/1e6).plot()
plt.ylabel('USDtrn')
plt.legend(['US','EU','JP','GB','CN'])
fig.show()