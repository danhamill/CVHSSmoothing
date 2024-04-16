import pandas as pd
from CVHSSmoothing.Spline import spline
from CVHSSmoothing.dss_util import import_smooth_ts
import os

inputFiles = {
  'CVHS':r'USBC_1DAY\Yuba-Feather\CVHS\DEER_CR_NR_SMARTVILLE.txt',
}

outFiles = {
  'CVHS':r'OUTFILES\Yuba-Feather\CVHS_DEER_CR_NR_SMARTVILLE_wPeak.out',
}
peaksFiles = {
  'CVHS':r'USBC_PEAKS\DEER_CR_NR_SMARTVILLE.txt'
}

os.makedirs(r'OUTFILES\Yuba-Feather', exist_ok=True)

out_dss = r"OUTFILES\splineDemo.dss"

for source in inputFiles.keys():

  spline(
    inputFiles[source], 
    outFiles[source], 
    peaksFiles[source])

  import_smooth_ts(
    outFiles[source],
    out_dss,
    f'/SPLINE_TEST/DEER CREEK @ SMARTSVILLE/FLOW-RES-IN//1HOUR/regSpline_peaks/', 
    day_offset=0)
