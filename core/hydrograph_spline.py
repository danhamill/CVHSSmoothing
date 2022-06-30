import pandas as pd
from scipy.interpolate import , splev
import numpy as np
import numpy.ma as ma
from scipy import interpolate

class HydroSpline(object):

    def __init__(self, daily_dates, daily_flows, peaks_dates = None, peak_values =None, method = 'pchip'):
        """_summary_

        Args:
            daily_dates (_type_): _description_
            daily_flows (_type_): _description_
            peaks (_type_, optional): _description_. Defaults to None.
        """
        self.daily_dates = daily_dates
        self.daily_flows = daily_flows
        self.peak_dates = peaks_dates
        self.peak_values = peak_values
        if not self.peak_values is None and self.peak_dates is None:

            assert len(self.peak_dates) == len(self.peak_values), 'Peak Dates and Peak Values are of different length'
            self.peak_df = pd.DataFame(index = pd.Index(self.peak_dates, name = 'date'), data = {'flow':self.peak_values})
        self.df = pd.DataFame(index = pd.Index(self.daily_dates, name = 'date'), data = {'flow':self.daily_flows})

        self.method = method

    def spline(self):

        self.daily_hydrograph = self.df.set_index('date').squeeze()
        self.daily_hydrograph.index = pd.PeriodIndex(self.daily_hydrograph.index, freq='H')
        self.daily_accumulation = self.daily_hydrograph.cumsum()
        self.daily_accumulation = self.daily_accumulation.asfreq('H', how='start')


        targ_idx = pd.period_range(self.df.date.min(), self.df.date.max(), freq = 'H')
        hourly_accumulation = self.daily_accumulation.reindex(targ_idx)
        

        hourly_hydrograph = self.generate_hydrograph(hourly_accumulation)

    def generate_hydrograph(self):
        self.masked_dates = ma.array(self.hourly_accumulation.index.view('int64'),
                            mask = self.hourly_accumulation.isna()) 
        self.masked_flows = ma.array(self.hourly_accumulation.values,
                                mask = self.hourly_accumulation.isna) 

        if self.method == 'pchip':

            spline_function = interpolate.PchipInterpolator(self.masked_dates.compressed(),
                                                self.hourly_accumulation.dropna().values, s=0)
        else: 
            spline_function = interpolate.PchipInterpolator(self.masked_dates.compressed(),
                                                self.hourly_accumulation.dropna().values, s=0)

        y_spline = interpolate.splev(self.hourly_accumulation.index.view('int64'),
                                    spline_function, der=0)      
        self.y_hourly_hydrograph_temp = np.diff(y_spline)*24
        self.y_hourly_hydrograph = np.zeros(np.size(self.hourly_accumulation))
        for i in range(1, np.size(self.hourly_accumulation)):
            self.y_hourly_hydrograph[i] =  self.y_hourly_hydrograph_temp[i-1]
        hydrologic_timeseries = pd.Series(self.y_hourly_hydrograph, 
        index = self.hourly_accumulation.index)  





        

