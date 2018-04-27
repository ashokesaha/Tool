import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')
from nssrc.com.citrix.netscaler.nitro.resource.stat.ns.nsmemory_stats  import *
from test_util import *


sess = Login('10.102.28.201')
stats = nsmemory_stats.get(sess)
type(stats)
