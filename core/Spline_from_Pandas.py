import datetime
import time
import numpy as np
import numpy.ma as ma
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

def insert_peak_11am(daily_accumulation, hourly_accumulation, date, value):  
  """
  Accept daily_accumulation, hourly_accumulation, date and value. Insert 
  hourly peak flow of magnitude value at noon of date. Remaining daily
  volume proportionally divided between preceeding and following portions of
  remaining day. Return new hourly_accumulation.
  
  
  """
  
  start_hour = pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 11)
  end_hour =  pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 12)
  beginning_daily_sum = daily_accumulation[date]
  ending_daily_sum = daily_accumulation[date+1]
  daily_flow = ending_daily_sum - beginning_daily_sum
  beginning_peak_sum = beginning_daily_sum + (daily_flow - value/24.)*11/23
  ending_peak_sum = beginning_peak_sum + value/24.
  hourly_accumulation[start_hour] = beginning_peak_sum
  hourly_accumulation[end_hour] = ending_peak_sum
  
  return hourly_accumulation
  
def insert_peak_10pm(daily_accumulation, hourly_accumulation, date, value):  
  """
  Accept daily_accumulation, hourly_accumulation, date and value. Insert 
  hourly peak flow of magnitude value at midnight of date. Remaining daily
  volume applied to first 23 hours of day. Return new hourly_accumulation.
  
  
  """
  
  start_hour = pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 22)
  end_hour =  pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 23)
  beginning_daily_sum = daily_accumulation[date]
  ending_daily_sum = daily_accumulation[date+1]
  daily_flow = ending_daily_sum - beginning_daily_sum
  beginning_peak_sum = beginning_daily_sum + (daily_flow - value/24. - value/24.*0.9)
  ending_peak_sum = beginning_peak_sum + value/24.
  hourly_accumulation[start_hour] = beginning_peak_sum
  hourly_accumulation[end_hour] = ending_peak_sum

  return hourly_accumulation
  
def insert_peak_11pm(daily_accumulation, hourly_accumulation, date, value):  
  """
  Accept daily_accumulation, hourly_accumulation, date and value. Insert 
  hourly peak flow of magnitude value at midnight of date. Remaining daily
  volume applied to first 23 hours of day. Return new hourly_accumulation.
  
  
  """
  
  start_hour = pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 23)
  end_hour =  pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 24)
  beginning_daily_sum = daily_accumulation[date]
  ending_daily_sum = daily_accumulation[date+1]
  daily_flow = ending_daily_sum - beginning_daily_sum
  beginning_peak_sum = beginning_daily_sum + (daily_flow - value/24. - value/24)
  ending_peak_sum = beginning_peak_sum + value/24.
  hourly_accumulation[start_hour] = beginning_peak_sum
  hourly_accumulation[end_hour] = ending_peak_sum

  return hourly_accumulation
  
def insert_peak_12am(daily_accumulation, hourly_accumulation, date, value):  
  """
  Accept daily_accumulation, hourly_accumulation, date and value. Insert 
  hourly peak flow of magnitude value at 0000 of date. Remaining daily
  volume applied to remaining 23 hours of day. Return new hourly_accumulation.
  
  
  """
  
  start_hour = pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 0)
  end_hour =  pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 1)
  beginning_daily_sum = daily_accumulation[date]
  ending_daily_sum = daily_accumulation[date+1]
  daily_flow = ending_daily_sum - beginning_daily_sum
  beginning_peak_sum = beginning_daily_sum  # + (daily_flow - value/24.)
  ending_peak_sum = beginning_peak_sum + value/24.
  hourly_accumulation[start_hour] = beginning_peak_sum
  hourly_accumulation[end_hour] = ending_peak_sum

  return hourly_accumulation
  
def insert_peak_1am(daily_accumulation, hourly_accumulation, date, value):  
  """
  Accept daily_accumulation, hourly_accumulation, date and value. Insert 
  hourly peak flow of magnitude value at 0100 of date. Remaining daily
  volume applied to remaining 23 hours of day. Return new hourly_accumulation.
  
  
  """
  
  start_hour = pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 1)
  end_hour =  pd.Period(freq = 'H', year = date.year,
    month = date.month, day = date.day, hour = 2)
  beginning_daily_sum = daily_accumulation[date]
  ending_daily_sum = daily_accumulation[date+1]
  daily_flow = ending_daily_sum - beginning_daily_sum
  beginning_peak_sum = beginning_daily_sum  + value/24.*0.9# + (daily_flow - value/24.)
  ending_peak_sum = beginning_peak_sum + value/24.
  hourly_accumulation[start_hour] = beginning_peak_sum
  hourly_accumulation[end_hour] = ending_peak_sum

  return hourly_accumulation

def generate_hydrograph(hourly_accumulation):
  """
  Accept hourly_accumulation. Generate a cubic spline interpolation 
  function, constrained by the specified (unmasked) values. Interpolate
  on an hourly basis, differentiate using the  numpy diff function, and
  multiply by 24 (to convert from cfs-days to cfs-hours) in order to 
  generate a "smoothed" hydrologic timeseries. Return hydrologic_timeseries. 
  
  """

  masked_dates = ma.array(hourly_accumulation.index.view('int64'),
    mask = hourly_accumulation.isna()) 
  masked_flows = ma.array(hourly_accumulation.values,
    mask = hourly_accumulation.isna) 
  spline_function = interpolate.splrep(masked_dates.compressed(),
    hourly_accumulation.dropna().values, s=0)
  y_spline = interpolate.splev(hourly_accumulation.index.view('int64'),
    spline_function, der=0)      
  y_hourly_hydrograph_temp = np.diff(y_spline)*24
  y_hourly_hydrograph = np.zeros(np.size(hourly_accumulation))
  for i in range(1, np.size(hourly_accumulation)):
    y_hourly_hydrograph[i] =  y_hourly_hydrograph_temp[i-1]
  hydrologic_timeseries = pd.Series(y_hourly_hydrograph, 
    index = hourly_accumulation.index)  

  return hydrologic_timeseries

def spline(df):
  """ 
  Accept daily timeseries input filename, gage location name, and 
  (optional) filename for irregular time series of peaks. Create a 
  summation time series from daily average flows. Insert additional 
  points to reflect peak flow information, if known. Develop a spline
  function to "smoothly" interpolate between points on accumulation 
  curve. Differentiate spline function on an hourly basis to generate a
  "smoothed" hourly flow timeseries. Check for negative flows and add 
  additional points to the accumulation curve (based on a linear 
  interpolation of daily plus peak accumulation curve) to further 
  constrain the spline interpolation. Recompute spline and check for 
  negative flows; repeat up to 15 iterations or until minimum flow is 
  greater than -0.01 cfs. Write resulting hourly hydrograph to a text 
  file in dssts compatible format. 
  
  """
 
  start_timer = time.time()
 
  #TODO need to compe up with way to standardize the 'Local_Flow' column name
  # Maybe pass each as a series to the colname becomes an attribute
  df.columns.name = ''


  df.columns = ['date','Local_Flow']
  x_days = pd.PeriodIndex(df['date'], freq = 'D')

  daily_hydrograph = df.set_index('date').squeeze()
  daily_hydrograph.index = pd.PeriodIndex(daily_hydrograph.index, freq='H')
  daily_accumulation = daily_hydrograph.cumsum()
  daily_accumulation = daily_accumulation.asfreq('H', how='start')


  targ_idx = pd.period_range(df.date.min(), df.date.max(), freq = 'H')
  hourly_accumulation = daily_accumulation.reindex(targ_idx)
  

  hourly_hydrograph = generate_hydrograph(hourly_accumulation)
  linear_function = interp1d(hourly_accumulation.dropna().index.view('int64'), 
                             hourly_accumulation.dropna().values, kind = 'linear')
  count = 0
 
  while np.min(hourly_hydrograph) <= -0.01 and count < 15:
    hourly_accumulation.loc[(hourly_hydrograph <0) | (hourly_hydrograph.shift(1) <0)] = linear_function(hourly_accumulation.loc[(hourly_hydrograph <0) | (hourly_hydrograph.shift(1) <0)].index.view('int64'))
    
    
    hourly_hydrograph = generate_hydrograph(hourly_accumulation)

    #get rid of floating point errors close to zero
    hourly_hydrograph[(hourly_hydrograph>-0.0005) & (hourly_hydrograph<0)] = 0
    hourly_hydrograph[(hourly_hydrograph<0.0005) & (hourly_hydrograph>0)] = 0

    count+=1
    print (f"{count} iterations completed; min flow = {np.min(hourly_hydrograph)}") 

  return hourly_hydrograph
    #print(hourly_hydrograph.loc[hourly_hydrograph<0].describe())


