# Smoothing
Cubic Spline Hydrograph Interpolation


This utility is designed to upsample a daily hydrogrph to hourly using cubic spline interpolation. 

The utility is designed to work with the following sturcture

```
Smoothing
├───core - utility codes
├───OUTFILES - directory for data processing outputs
├───USBC_1DAY - directory for input daily time series
└───USBC_PEAKS - directory for input peak flow time series
```

The input text files are structured as text files saved from MS excel.  

```
A		KERN
B		ISABELLA
C	GMT-08:00	FLOW-RES IN
E		
F		POR
Units		CFS
Type		PER-AVER
1	01Oct1952	403
2	02Oct1952	395
3	03Oct1952	385
4	04Oct1952	384
```

## Basic Usage
```python
import pandas as pd
from core.Spline import spline
from core.dss_util import import_smooth_ts

locations = (
"ISB_POR",
)

inputfile = {}
outfile = {}
peaksfile = {} 

for i in locations:
  inputfile[i] = r"USBC_1DAY/%s.txt" %(i)
  outfile[i] = r"%s_UNREG_SMTHD" %(i)
  peaksfile[i] = False

out_dss = r"OUTFILES\isabella_smooth.dss"

for location in locations:
  spline(inputfile[location], outfile[location], peaksfile[location])
  import_smooth_ts(outfile[location],out_dss,'/ISABELLA/ISABELLA LAKE/FLOW-RES-IN//1HOUR/SYNTHETIC/', day_offset=1)
```