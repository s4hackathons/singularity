from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
import pandas
import numpy
import random
import matplotlib.pylab as plt
from statsmodels.tsa.stattools import adfuller

l = []
for _ in range(150):
    x = random.randint( 0, 50 )
    l.append( x )

orig_data = l
#Perform Dickey-Fuller test:
def dickey_test( timeseries ):
    dfresult = adfuller( timeseries, maxlag = 1, autolag='AIC' )
    #print dftest[4]['1%']
    dfoutput = pandas.Series( dfresult[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'] )
    for key,value in dfresult[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print dfoutput
    
    return dfresult

d = 0
while True:
    result = dickey_test( l )
    critical_val_1pc = result[4]['1%']
    test_stat = result[0]
    if test_stat < critical_val_1pc:
        break
    l_data_frame = pandas.DataFrame( l )
    l_diff = l_data_frame - l_data_frame.shift()
    l_diff.dropna( inplace=True )
    l = l_diff
    l = list(l.values.flatten())
    d = d + 1
    
#Forecasting model
def ARIMA_fun( data ):
    lag_pacf = pacf( data, nlags=20, method='ols' )
    lag_acf, ci2, Q  = acf( data, nlags=20 , qstat=True, unbiased=True)

    model = ARIMA(orig_data, order=(1, 1, int(ci2[0]) ) )  
    results_ARIMA = model.fit(disp=-1)
    plt.subplot(121)
    plt.plot( data )
    plt.plot(results_ARIMA.fittedvalues)
    #plt.show()
    return results_ARIMA.fittedvalues

def forecast( arimaResults, l ):
    predictions_ARIMA_diff = pandas.Series( arimaResults, copy=True )
    ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    #print ARIMA_diff_cumsum
    l_data_frame = pandas.DataFrame( l )
    l_series = pandas.Series(l_data_frame.ix[1], index=l_data_frame.index)
    new_series = l_series.add( ARIMA_diff_cumsum,fill_value=0 )
#    list(l.values.flatten())
    print new_series.values.flatten()

print l    
arimaResults = ARIMA_fun( l )
forecast( arimaResults, l )
