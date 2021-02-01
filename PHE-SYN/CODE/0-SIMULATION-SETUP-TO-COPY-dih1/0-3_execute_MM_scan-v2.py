import os
import time

os.system('./6_MultiWrite_NAMD_MP2geom_OPT_conf_noBCs')

time.sleep(5)

os.system('./7_MultiExec_NAMD_OPTcalcs')
