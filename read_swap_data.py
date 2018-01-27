#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 14:25:55 2017

@author: mattange
"""

import pandas as pd
import numpy as np


filename = '/home/mattange/Documents/Python/SwapData/RawData.xlsx'
header = 0
skiprows = [1,2,3]
sheet_name = ['US','EU','JP','GB','CA','CH','AU','NZ','SE','CB_US','CB_EU','CB_JP','CB_GB','CB_CA','CB_CH','CB_CN','FX']
sheets = pd.read_excel(filename,skiprows=skiprows,sheet_name=sheet_name,header=header,dtype=np.float)

sample_rule = 'W-FRI'

FXdata = sheets['FX']
FX = FXdata.resample(rule=sample_rule).mean()

#central bank balance sheets in log
uscbbs = sheets['CB_US']['USDm'].rename('USCBBS').resample(rule=sample_rule).last()
uscbbslog = uscbbs.apply(np.log)
uscbbs_usd = uscbbs

eucbbs = sheets['CB_EU']['EURbn'].rename('EUCBBS').resample(rule=sample_rule).last()
eucbbs_usd = eucbbs * FX['EUR'] * 1000
eucbbs_usd.name = 'EUCBBS_USD'
eucbbslog = eucbbs.apply(np.log)

jpcbbs = sheets['CB_JP']['JPYbn'].rename('JPCBBS').resample(rule=sample_rule).last()
jpcbbs_usd = jpcbbs.rename('JPCBBS_USD') / FX['JPY'] * 1000
jpcbbs_usd.name = 'JPCBBS_USD'
jpcbbslog = jpcbbs.apply(np.log)

gbcbbs = sheets['CB_GB']['GBPm'].rename('GBCBBS').fillna(method='bfill').resample(rule=sample_rule).last()
gbcbbs_usd = gbcbbs.rename('GBCBBS_USD') * FX['GBP']
gbcbbs_usd.name = 'GBCBBS_USD'
gbcbbslog = gbcbbs.apply(np.log)

cacbbs = sheets['CB_CA']['CADm'].rename('CACBBS').resample(rule=sample_rule).last()
cacbbs_usd = cacbbs.rename('CACBBS_USD') / FX['CAD']
cacbbs_usd.name = 'CACBBS_USD'
cacbbslog = cacbbs.apply(np.log)

chcbbs = sheets['CB_CH']['CHFm'].rename('CHCBBS').resample(rule=sample_rule).last().fillna(method='ffill')
chcbbs_usd = chcbbs.rename('CHCBBS_USD') / FX['CHF']
chcbbs_usd.name = 'CHCBBS_USD'
chcbbslog = chcbbs.apply(np.log)

cncbbs = sheets['CB_CN']['CNYbn'].rename('CNCBBS').resample(rule=sample_rule).last().fillna(method='ffill')
cncbbs_usd = cncbbs.rename('CNCBBS_USD') / FX['CNY'] * 1000
cncbbs_usd.name = 'CNCBBS_USD'
cncbbslog = cncbbs.apply(np.log)

allcbbs = uscbbs + eucbbs_usd + jpcbbs_usd + gbcbbs_usd + cacbbs_usd + chcbbs_usd + cncbbs_usd
allcbbs.fillna(method='ffill', inplace=True)
allcbbs.fillna(method='bfill', inplace=True)
allcbbs.name = 'ALLCBBS'
allcbbslog = allcbbs.apply(np.log)




### US
ctry = 'US'
allcbbs_ex_us = allcbbs - uscbbs_usd
allcbbs_ex_us.name = 'ALLCBBS_EX_' + ctry
allcbbs_ex_uslog = allcbbs_ex_us.apply(np.log)
cbbslogus = pd.concat([uscbbslog, allcbbs_ex_uslog], axis=1)
yieldsdata_us = sheets[ctry]
#convert the libor rates to be equivalent to 30/360 like the rest of the swap rates
yieldsdata_us[['on','3m','6m']] = yieldsdata_us[['on','3m','6m']] * 360/365  
#actually drop the 6m tenor as the first swap rate needs to be 3m for 3m, while
#the 6m has some compounding impact in there as the US is vs. 3m Libor
yieldsdata_us = yieldsdata_us[['on','3m','1y','2y','3y','4y','5y','7y','10y','15y','20y','30y']]
tenor_columns = [1/365, 0.25, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30]
data_to_work = pd.DataFrame(yieldsdata_us.values, columns=tenor_columns, index=yieldsdata_us.index)
yieldsus = data_to_work.resample(rule=sample_rule).mean()


### EU
ctry = 'EU'
allcbbs_ex_eu = allcbbs - eucbbs_usd
allcbbs_ex_eu.name = 'ALLCBBS_EX_' + ctry
allcbbs_ex_eulog = allcbbs_ex_eu.apply(np.log)
cbbslogeu = pd.concat([eucbbslog, allcbbs_ex_eulog], axis=1)
yieldsdata_eu = sheets[ctry]
#convert the libor rates to be equivalent to 30/360 like the rest of the swap rates
yieldsdata_eu[['on','3m','6m']] = yieldsdata_eu[['on','3m','6m']] * 360/365  
#actually drop the 6m tenor as the first swap rate needs to be 3m for 3m, while
#the 3m has some compounding impact in there as the eu is vs. 6m Euribor
yieldsdata_eu = yieldsdata_eu[['on','6m','1y','2y','3y','4y','5y','7y','10y','15y','20y','30y']]
tenor_columns = [1/365, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30]
data_to_work = pd.DataFrame(yieldsdata_eu.values, columns=tenor_columns, index=yieldsdata_eu.index)
yieldseu = data_to_work.resample(rule=sample_rule).mean()

### GB
ctry = 'GB'
allcbbs_ex_gb = allcbbs - gbcbbs_usd
allcbbs_ex_gb.name = 'ALLCBBS_EX_' + ctry
allcbbs_ex_gblog = allcbbs_ex_gb.apply(np.log)
cbbsloggb = pd.concat([gbcbbslog, allcbbs_ex_gblog], axis=1).loc['2005-01-10':]
yieldsdata_gb = sheets[ctry].loc['2005-01-10':]
#actually drop the 6m tenor as the first swap rate needs to be 3m for 3m, while
#the 6m has some compounding impact in there as the gb is vs. 6m GBPLibor
yieldsdata_gb = yieldsdata_gb[['on','6m','1y','2y','3y','4y','5y','7y','10y','15y','20y','30y']]
tenor_columns = [1/365, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30]
data_to_work = pd.DataFrame(yieldsdata_gb.values, columns=tenor_columns, index=yieldsdata_gb.index)
yieldsgb = data_to_work.resample(rule=sample_rule).mean()


### JP
ctry = 'JP'
allcbbs_ex_jp = allcbbs - jpcbbs_usd
allcbbs_ex_jp.name = 'ALLCBBS_EX_' + ctry
allcbbs_ex_jplog = allcbbs_ex_jp.apply(np.log)
cbbslogjp = pd.concat([jpcbbslog, allcbbs_ex_jplog], axis=1).fillna(method='bfill')
yieldsdata_jp = sheets[ctry]
#convert the libor rates to be equivalent to 30/360 like the rest of the swap rates
yieldsdata_jp[['on','3m','6m']] = yieldsdata_jp[['on','3m','6m']] * 360/365  
#actually drop the 6m tenor as the first swap rate needs to be 3m for 3m, while
#the 6m has some compounding impact in there as the jp is vs. 6m jpPLibor
yieldsdata_jp = yieldsdata_jp[['on','6m','1y','2y','3y','4y','5y','7y','10y','15y','20y','30y']]
tenor_columns = [1/365, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30]
data_to_work = pd.DataFrame(yieldsdata_jp.values, columns=tenor_columns, index=yieldsdata_jp.index)
yieldsjp = data_to_work.resample(rule=sample_rule).mean()

### CA
ctry = 'CA'
allcbbs_ex_ca = allcbbs - cacbbs_usd
allcbbs_ex_ca.name = 'ALLCBBS_EX_' + ctry
allcbbs_ex_calog = allcbbs_ex_ca.apply(np.log)
cbbslogca = pd.concat([cacbbslog, allcbbs_ex_calog], axis=1)
yieldsdata_ca = sheets[ctry]
#convert the libor rates to be equivalent to 30/360 like the rest of the swap rates
#actually drop the 6m tenor as the first swap rate needs to be 3m for 3m, while
#the 6m has some compounding impact in there as the ca is vs. 6m caPLibor
yieldsdata_ca = yieldsdata_ca[['on','6m','1y','2y','3y','4y','5y','7y','10y','15y','20y','30y']]
tenor_columns = [1/365, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30]
data_to_work = pd.DataFrame(yieldsdata_ca.values, columns=tenor_columns, index=yieldsdata_ca.index)
yieldsca = data_to_work.resample(rule=sample_rule).mean()

### AU
ctry = 'AU'
allcbbs_ex_au = allcbbs
#allcbbs_ex_au.name = 'ALLCBBS_EX_' + ctry
allcbbs_ex_aulog = allcbbs_ex_au.apply(np.log)
cbbslogau = allcbbs_ex_aulog.loc['2003-01-20':]
yieldsdata_au = sheets[ctry].loc['2003-01-20':]
#convert the libor rates to be equivalent to 30/360 like the rest of the swap rates
#actually drop the 6m tenor as the first swap rate needs to be 3m for 3m, while
#the 6m has some compounding impact in there as the au is vs. 6m AU Libor
yieldsdata_au = yieldsdata_au[['on','6m','1y','2y','3y','4y','5y','7y','10y','15y','20y','30y']]
tenor_columns = [1/365, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30]
data_to_work = pd.DataFrame(yieldsdata_au.values, columns=tenor_columns, index=yieldsdata_au.index)
yieldsau = data_to_work.resample(rule=sample_rule).mean()

