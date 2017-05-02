import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Modules import Hashing
from EmeraldAI.Logic.ComputerVision.ModelMonitor import ModelMonitor


print Hashing.GetDirHash('/Users/maximilianporzelt/Google Drive/EmeraldAI/testing')

m = ModelMonitor()

m.Rebuild("Person", "350x350")

