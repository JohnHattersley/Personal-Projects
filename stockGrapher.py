import pandas as pd
import pandas.io.data as web #Package and modules
import datetime

#starting at January 1st 2016
start = datetime.datetime(2016,1,1)
end = datetime.datetime(2016,9,25)

apple = web.DataReader("AAPL", "yahoo", start, end)
type(apple)
apple.head()

import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import pylab

%matplotlib inline

%pylab inline
pylab.rcParams['figure.figsize'] = (15,9) #Change size of plots

#Adjusted closing price of AAPL
apple["Adj Close"].plot(grid = True)



from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib import finance 
from matplotlib.finance import candlestick_ohlc

def pandas_candlestick_ohcl(dat,stick ="day", otherseries = None):
    """
    :param dat:pandas DataFrame object with datetime64 index, and float columns "Open","Hign","Low", and "Close", likely created via DataReader from "yahoo"
    :param stick: A string or number indicating the period of time covered by a single candlestick. Valid inputs are "Day","Week","Month","Year"  ("Day" = default) and any numerical input dictates the number of trading days in a period 
    :param otherseries: An iterable that will be coerced in to a list containing the columns of data that hold other series to be plotted as lines.
    
    """

    mondays = WeekdayLocator(MONDAY)     #for all the major ticks on mondays
    alldays = DayLocator()               #and minor ticks for every other day
    dayFormatter = DateFormatter('%d')   
    
    
    #Create a new DataFrame which includes OHLC data for each data period specified by the stick input 
    transdat = dat.loc[:,["Open","High","Low","Close"]]
    if(type(stick)==str):
            if stick =="day":
                plotdat = transdat
                stick = 1 
            elif stick in["week","month","year"]:
                if stick == "week":
                    transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) 
            elif stick =="month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month()[1]) 
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) 
            grouped = transdat.groupby(list(set(["year",stick]))) 
            plotdat = pd.DataFrame({"Open":[],"High":[],"Low":[],"Close":[]}) #Creates empty data frame
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open":group.iloc[0,0],
                                        "High":max(group.High),
                                        "Low":min(group.Low),
                                        "Close":group.iloc[-1,3]},
                                        index = [group.index[0]]))
            if stick =="week":stick = 5
            elif stick =="month":stick = 30
            elif stick =="year":stick = 365
        
    elif(type(stick) == int and stick >= 1):
        transdat["stick"]=[np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open":[],"High":[],"Low":[],"Close":[]})
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open":group.iloc[0,0],
                                        "High":max(group.High),
                                        "Low":min(group.Low),
                                        "Close":group.iloc[-1,3]},
                                       index=[group.index[0]]))
    else:
        raise ValueError("Valid arguments to include 'stick' include the strings 'day','month','year' or a valid integer")
        
        
    
    #Set plot parameters, including the axis object ax which is used for plotting
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom = 0.2)
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b','%d') # for example January 5th
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b','%d','%Y')
    ax.xaxis.set_major_formatter(weekFormatter)
    
    ax.grid(True)
    
    
    #Create the candlestick chart
    candlestick_ohlc(ax, list(zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
        plotdat["Low"].tolist(), plotdat["Close"].tolist())),
        colorup = "black", colordown = "red", width = stick*.4)
        
    #Plot other series(ex.Moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.log[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)
        
        
    ax.axis_date()
    ax.autoscale_view()
    plt.setp(plt.gcal().getxticklabels(), rotation=45, horizontalalignment = 'right')
    
    plt.show()
    
pandas_candlestick_ohcl(apple)
    
    
    
    
    
    
