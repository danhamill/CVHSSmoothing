from pydsstools.heclib.dss import HecDss
import pandas as pd
from pydsstools.core import TimeSeriesContainer


def import_smooth_ts(outfile, out_dss, out_dss_path=None, day_offset = None):
    """
    DSS import helper function.  Imports smoothed time series as regular time series.

    Args:
        outfile ([str]): [file path to output file from spline interpolation]
        out_dss ([type]): [dss output file path.  Can exist or be a new file]
        out_dss_path ([str], optional): [dss path name for output record]. Defaults to line 1 of output file.
        day_offset ([int], optional): [day shift for output time series]. Defaults to None.
    """

    #TODO make cleaner input output path handling
    df = pd.read_csv(outfile)

    if day_offset is None:
        start_date = df.iloc[2][0]
    else:
        start_date = (pd.to_datetime(df.iloc[2][0], format = '%d%b%Y %H%M') + pd.DateOffset(days=day_offset)).strftime('%d%b%Y %H:00')

    if out_dss_path is None:
        out_dss_path = df.columns[0]
    else:
        pass

    data = df.iloc[3:-2]

    data.columns = ['flow']
    data.flow = data.flow.astype(float)



    tsc = TimeSeriesContainer()
    tsc.pathname = out_dss_path
    tsc.startDateTime = start_date
    tsc.numberValues = data.shape[0]
    tsc.units = "cfs"
    tsc.type = "PER-AVER"
    tsc.interval = 1
    tsc.values = data[data.columns[0]].values


    with HecDss.Open(out_dss) as fid:
        fid.put_ts(tsc)
        fid.close()