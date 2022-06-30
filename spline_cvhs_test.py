import pandas as pd
from core.Spline import spline
from core.dss_util import import_smooth_ts


inputFiles = {'CVHS':r'USBC_1DAY\Yuba-Feather\CVHS\DEER_CR_NR_SMARTVILLE.txt',
            #  'WCM_UPDATE': r'USBC_1DAY\Yuba-Feather\WCM_Update\DEER.txt'
             }
outFiles = {'CVHS':r'OUTFILES\Yuba-Feather\CVHS_DEER_CR_NR_SMARTVILLE.out',
            #  'WCM_UPDATE': r'OUTFILES\Yuba-Feather\WCM_Update_DEER.out'
             }
peaksFiles = {'CVHS':r'USBC_PEAKS\DEER_CR_NR_SMARTVILLE.txt',
            #  'WCM_UPDATE': False
             }



out_dss = r"OUTFILES\YF_CVHS_TEST.dss"

for source in inputFiles.keys():
  spline(inputFiles[source], outFiles[source], peaksFiles[source])
#   import_smooth_ts(outFiles[source],out_dss,f'/SPLINE_TEST/DEER CREEK @ SMARTSVILLE/FLOW-RES-IN//1HOUR/{source}_peaks/', day_offset=0)




