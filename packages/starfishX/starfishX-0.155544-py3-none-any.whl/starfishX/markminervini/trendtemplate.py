import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import text

def trendMA_YMF(symbol,start,engine,plot=True):
  df = engine.getPrice(symbol,start=start)
  df['MA50'] = df[[symbol]].rolling(window=50).mean() 
  df['MA150'] = df[[symbol]].rolling(window=150).mean() 
  df['MA200'] = df[[symbol]].rolling(window=200).mean() 
  
  if(plot):
    df.plot(figsize=(15,6))
    plt.show()

  k = df[(df[symbol]>df['MA50']) & (df['MA50']>df['MA150']) & (df['MA150']>df['MA200'])]
    
  if(len(k)==0):
    return False,'fail condition (1),(2),(4) และ (8)'

  if(df.index[-1] == k.index[-1]):
    return True ,'pass condition (1),(2),(4) และ (8) : close > MA50 , MA50 > MA150 , MA150 > MA200'
  else:
   return False,'fail condition (1),(2),(4) และ (8)'

def trendMA_Year(symbol,start,engine,month=3,plot=True):
  
  df = engine.getPrice(symbol,start=start)
  df['MA200'] = df[[symbol]].rolling(window=200).mean()
  
  lastDay = df.index[-1]
  
  timeofmonth = month*22

  k = df[['MA200']].tail(timeofmonth).dropna()
  slope, intercept = np.polyfit(np.arange(0,len(k)), k['MA200'], 1)
  abline_values = [((slope * i) + intercept) for i in range(len(k['MA200']))]

  abline_values = np.array(abline_values)

  dt = df[['MA200']].tail(timeofmonth).dropna()
  #plt.plot(dt.index, dt['SMA200'], '--')
  LastDaySL = (lastDay + pd.Timedelta('20 day'))
  
  
  if(plot):
    plt.rcParams["figure.figsize"] = (15,6)
    
    df[[symbol,'MA200']].plot(figsize=(15,6))    
    plt.plot(dt.index, abline_values*0.95, 'w--',linewidth=2,label='Slope MA200 ('+str(month)+'Months)')
    text(LastDaySL,abline_values[-1]*0.95, 'Slope MA200 ('+str(month)+'Months)', 
         rotation=0,horizontalalignment='left')
    plt.legend()
    plt.show()

 
  if(slope>0):
    return True,'pass slope(+) pass condition (3)' + 'slope :'+str(slope)
  else:
    return False,'fail slope(-) fail condition (3)'+ 'slope :'+str(slope)  


def check52WeekHighLow(symbol,start,engine,plot=True):
    df = engine.getPrice(symbol,start=start)
    
    if(len(df)<252):
        return False,'log : not enough information'
    df['52W High'] = df[[symbol]].rolling(window=252).max() 
    df['52W Low'] = df[[symbol]].rolling(window=252).min() 
    
    price52WeekH = df.iloc[-1]['52W High']
    LastPrice = df.iloc[-1][symbol]
    lastDay = df.index[-1]
    
    price52WeekL = df.iloc[-1]['52W Low']
    
    pctD_From_week52H = (LastPrice - price52WeekH )/price52WeekH
    pctD_From_week52H = round(pctD_From_week52H*100,2)
    
    pctD_From_week52L = (LastPrice - price52WeekL)/price52WeekL
    pctD_From_week52L = round(pctD_From_week52L*100,2)
    #print('x',LastPrice,price52WeekL,pctD_From_week52L)

    if(plot):
      #บวกวันเพิ่ม เพื่อให้การแสดงผลไม่ติดเกินไปเท่านั้น
      lastDay_PD = lastDay+pd.Timedelta('5 day')
      lastDay_PD2 = lastDay+pd.Timedelta('20 day')
    
      df.plot(figsize=(15,6),title=symbol+' 52Week High & Low')
      
      plt.vlines(x=lastDay_PD,linestyle='--', ymin=LastPrice, 
               ymax=price52WeekH, color='green', zorder=2)

      text(lastDay_PD,LastPrice, 'Gap '+str(pctD_From_week52H)+'% / w52H', 
             rotation=90,horizontalalignment='left')
      
        
      plt.vlines(x=lastDay_PD,linestyle='--', ymin=price52WeekL, 
               ymax=LastPrice, color='red', zorder=2)
    
      text(lastDay_PD2,price52WeekL, 'Gap '+str(pctD_From_week52L)+'% / w52L', 
         rotation=90,horizontalalignment='left')
        
      
      dayX1 = lastDay_PD-pd.Timedelta('5 day')
      dayX2 = lastDay_PD+pd.Timedelta('5 day')
      plt.hlines(y=LastPrice,xmin=dayX1,xmax=dayX2, color='r', linestyle='--')
    
    c5 = False
    if(pctD_From_week52H > -20): #อย่าลงมาต่ำกว่าจุดสูงสุดเกิน 20%
        c5 = True
        logC5 = 'pass condition (5) ,last price '+ str(pctD_From_week52H)+'%'
    else:
        logC5 = 'fail condition (5) ,last price ' + str(pctD_From_week52H)+'%'
    
    c6 = False
    if(pctD_From_week52L > 20): #ราคาปัจจุบันอยู่เหนือกว่าราคา 52W Log เยอะๆ %
        c6 = True
        logC6 = 'pass condition (6) ,last price '+ str(pctD_From_week52L)+'%'
    else:
        logC6 = 'fail condition (6) ,last price ' + str(pctD_From_week52L)+'%'
        
    if(c5==True and c6==True):
       return True,logC5+' and '+logC6
    else:
       return False,logC5+' and '+logC6

def ROC_Basket(basket,start,engine):
  pct_change = []
  close_price = []
  close_start = []
  for i in basket:
    df = engine.getPrice(i,start)
    k = (df.tail(1)[i].values[0]/df.head(1)[i].values[0])-1
    pct_change.append(round(k*100,2))
    close_price.append(round(df.tail(1)[i].values[0],2))
    close_start.append(round(df.head(1)[i].values[0],2))  
    print('.',end='')
  print('done')

  df = pd.DataFrame({'symbol':basket,'close_start':close_start,'close_end':close_price,'pct_chg':pct_change})
  df = df.set_index('symbol')
  df.sort_values('pct_chg',ascending=False)

  plt.figure(figsize=(20,6))

  df = df.sort_values('pct_chg')
  color = np.where(df.index == 'SET','gold',  
                np.where(df.pct_chg>df[df.index=='SET']['pct_chg'].values[0],'green','red') 
                )
  ax = plt.bar(x=df.index,height=df['pct_chg'],color=color)

  df['no'] = np.arange(0,len(df))
  k = df[df.index=='SET'].no[0]

  plt.title('Rate of Change')
  plt.annotate("SET INDEX", 
            xy=(k, 10), xytext=(k, 50), arrowprops={"arrowstyle":"->", "color":"gray"})
  plt.xticks(rotation=90)
  plt.show
  return df