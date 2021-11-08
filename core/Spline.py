import datetime
import time
import numpy as np
import numpy.ma as ma
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

def read_timeseries_info(input):
  """
  Read DSS pathname part info, units, and type from first seven lines
  of input. Assume pathname E-part to be 1DAY. Return information as a
  dictionary.
  
  """
  
  timeseries_info = {}
  try:
    timeseries_info["apart"] = input[0].strip().split()[1]
  except IndexError:
    timeseries_info["apart"] = " "  
  timeseries_info["bpart"] = input[1].strip().split()[1]
  timeseries_info["cpart"] = input[2].strip().split()[1]
  timeseries_info["epart"] = "1DAY"
  timeseries_info["fpart"] = input[4].strip().split()[1]
  timeseries_info["units"] = input[5].strip().split()[1]
  timeseries_info["type"] = input[6].strip().split()[1]
  return timeseries_info

def read_date(raw_date):
  """
  Read date from a string. Assume raw_date to be in the form of
  DDMMMYYYY. Return a timeseries date object. 

  """
  months = {}
  months["Jan"] = 1
  months["Feb"] = 2
  months["Mar"] = 3
  months["Apr"] = 4
  months["May"] = 5
  months["Jun"] = 6
  months["Jul"] = 7
  months["Aug"] = 8
  months["Sep"] = 9
  months["Oct"] = 10
  months["Nov"] = 11
  months["Dec"] = 12

  month = months[raw_date[2:5]]
  day = int(raw_date[0:2])
  year = int(raw_date[5:])
    
  date = pd.Period(freq='D',
    year=year,
    month=month,
    day=day)
    
  return date      

def read_faux_date(raw_date):
  """"
  Read date from raw_date string. Assumed raw_date to be in the form of
  DDMMMYYYY. Return a timeseries date object 400 years in the future in
  order to bypass limitations of timeseries module that prevent working
  with hourly data prior to 1970. Four hundred years chosen to prevent
  issues with leap days--leap years run on a 400 year cycle. 
  
  """

  months = {}
  months["Jan"] = 1
  months["Feb"] = 2
  months["Mar"] = 3
  months["Apr"] = 4
  months["May"] = 5
  months["Jun"] = 6
  months["Jul"] = 7
  months["Aug"] = 8
  months["Sep"] = 9
  months["Oct"] = 10
  months["Nov"] = 11
  months["Dec"] = 12

  month = months[raw_date[2:5]]
  day = int(raw_date[0:2])
  faux_year = int(raw_date[5:]) + 400
    
  date = pd.Period(freq='D',
    year=faux_year,
    month=month,
    day=day)
    
  return date

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

def spline(daily_flow_filename, location, peaks_file_name = False):
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
 
  start_timer = time.clock()
 
  #TODO make cleaner input filehanding logic
  daily_flow_readlines = open(daily_flow_filename, "r").readlines()
  timeseries_info = read_timeseries_info(daily_flow_readlines)
  del daily_flow_readlines[0:7]
  start_date = daily_flow_readlines[0].strip().split()[1]
  start = read_date(start_date)
  dates = []
  flows = []
  first_date = read_faux_date(start_date)
  dates.append(first_date)
  flows.append(0)

  print (f"Reading input timeseries for {location}") 

  missing_log_file_name = r"outfiles/" + location + "_missing.log"
  missing_log_file = open(missing_log_file_name, "w")


  for line in daily_flow_readlines:
    try:
      raw_date = line.strip().split()[1]
      faux_date = read_faux_date(raw_date) + 1
      dates.append(faux_date)
      a = line.strip().split()[2]
      b = float(a)
      flows.append(b)
    except IndexError:
      missing_log_file.write("Error: %s \t line: %s" % (location, line))
      flows.append(0.0)
    except ValueError:
      missing_log_file.write("Error: %s \t line: %s" % (location, line)) 
      flows.append(0.0)
      
  print ("Generating smoothed (hourly) timeseries")

  x_days = pd.PeriodIndex(dates, freq = 'D')
  y_days = np.array(flows)
  daily_hydrograph = pd.Series(y_days, index = dates)
  y_days_cumsum = np.cumsum(y_days)
  daily_accumulation = pd.Series(y_days_cumsum, index = dates)
  hourly_accumulation = daily_accumulation.asfreq('H', how='start')
  targ_idx = pd.period_range(daily_accumulation.index.min(), daily_accumulation.index.max(), freq='H')
  hourly_accumulation = hourly_accumulation.reindex(targ_idx)
  hourly_accumulation[-1] = np.max(hourly_accumulation)

  #TODO make cleaner output file handling
  peak_log_file_name = r"outfiles/" + location + "_peaks.log"
  peak_log_file = open(peak_log_file_name, "w")
  
  if peaks_file_name: 

    print ("Inserting peaks")
    peaks_readlines = open(peaks_file_name, "r").readlines()
    del peaks_readlines[0:7]
    peak_dates = []
    peak_values = []
    peak_types = []
    peak_dictionary = {}
    real_dates = {}
    for line in peaks_readlines:
      try:
        line.strip().split()[2]
        raw_date = line.strip().split()[1]
        real_date = read_date(raw_date)
        faux_date = read_faux_date(raw_date)
        peak_dates.append(faux_date)
        a = line.strip().split()[2]
        b = float(a)
        peak_values.append(b)
        peak_types.append(line.strip().split()[3])
        peak_dictionary[faux_date] = b
        real_dates[faux_date] = real_date
      except IndexError:
        peak_log_file.write("Peaksfile: %s \t line: %s, does not contain a \
          valid peak value, skipping line\n" % (peaks_file_name, line))
  
    for i in range(0, len(peak_dates)):

        if(peak_types[i] == "0"):
          hourly_accumulation = insert_peak_1am(daily_accumulation, 
            hourly_accumulation, peak_dates[i], peak_values[i])
          peak_log_file.write("Inserting peak of %.2f on %s at 1 AM\n" % (peak_values[i], peak_dates[i])) 

        if(peak_types[i] == "1"):
          hourly_accumulation = insert_peak_12am(daily_accumulation, 
            hourly_accumulation, peak_dates[i], peak_values[i])
          peak_log_file.write("Inserting peak of %.2f on %s at 12 AM\n" % (peak_values[i], peak_dates[i])) 

        if(peak_types[i] == "2"):
          hourly_accumulation = insert_peak_11am(daily_accumulation, 
            hourly_accumulation, peak_dates[i], peak_values[i])
          peak_log_file.write("Inserting peak of %.2f on %s at 11 AM\n" % (peak_values[i], peak_dates[i]))    
       
        if(peak_types[i] == "3"):
          hourly_accumulation = insert_peak_11pm(daily_accumulation, 
            hourly_accumulation, peak_dates[i], peak_values[i])
          peak_log_file.write("Inserting peak of %.2f on %s at 11 PM\n" % (peak_values[i], peak_dates[i]))    
          
        if(peak_types[i] == "4"):
          hourly_accumulation = insert_peak_10pm(daily_accumulation, 
            hourly_accumulation, peak_dates[i], peak_values[i])
          peak_log_file.write("Inserting peak of %.2f on %s at 10 PM\n" % (peak_values[i], peak_dates[i]))  

  else:
    peak_log_file.write("No peaks specified")   

  print ("Cleaning negative flows")

  hourly_hydrograph = generate_hydrograph(hourly_accumulation)
  linear_function = interp1d(hourly_accumulation.dropna().index.view('int64'), 
                             hourly_accumulation.dropna().values, kind = 'linear')
  count = 0
 
  while np.min(hourly_hydrograph) <= -0.01 and count < 15:
    hourly_accumulation.loc[(hourly_hydrograph <0) | (hourly_hydrograph.shift(1) <0)] = linear_function(hourly_accumulation.loc[(hourly_hydrograph <0) | (hourly_hydrograph.shift(1) <0)].index.view('int64'))
    hourly_hydrograph = generate_hydrograph(hourly_accumulation)

    
    count+=1
    print (f"{count} iterations completed; min flow = {np.min(hourly_hydrograph)}") 
    #print(hourly_hydrograph.loc[hourly_hydrograph<0].describe())

  print ("Checking peaks") 

  if peaks_file_name:     
    for date in peak_dates:
      peak_good = True
      for hour in range(0, 24):
        hourly_date = pd.Period(freq = "H", year = date.year, 
          month = date.month, day = date.day, hour = hour)
        hourly_ordinate = hourly_date
        if (hourly_hydrograph[hourly_date] > (peak_dictionary[date] + 1) \
          or hourly_hydrograph[hourly_date + 1] > (peak_dictionary[date] \
          + 1)) and peak_good == True:
        
          print ("Peak on Date: %s is being overestimated") % (real_dates[date])
          peak_log_file.write("Peak on Date: %s is being overestimated\n" 
            % (real_dates[date]))
          peak_good = False


  print ("Writing results to file")

  output_file_name = r"OUTFILES/" + location + ".out"
  y_hourly_hydrograph_string = []
  for y in hourly_hydrograph:
    if y >= 0:
      y_hourly_hydrograph_string.append("%.2f" % y)
    else:
      y_hourly_hydrograph_string.append("0.00")
  output_file = open(output_file_name, "w")
  
  timeseries_info["fpart"] = "SYNTHETIC"
  output_file.write("/" + timeseries_info["apart"])
  output_file.write("/" + timeseries_info["bpart"])
  output_file.write("/" + timeseries_info["cpart"])
  output_file.write("/" + "/" + "1hour")
  output_file.write("/" + timeseries_info["fpart"] + "/")
  output_file.write("\n")
  output_file.write("CFS\n")
  output_file.write("PER-AVER\n")
  output_file.write(start_date + " 0100\n")
   
  for o in range(1, np.size(hourly_accumulation)):
    output_file.write(y_hourly_hydrograph_string[o])
    output_file.write("\n")
  
  output_file.write("END")
  output_file.write("\n")
  output_file.write("FINISH")
  output_file.close()

  end_timer = time.clock()
  compute_time = (end_timer-start_timer)/60
  print( f"Compute time: {compute_time:.2f} minutes")

