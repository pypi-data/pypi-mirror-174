import os
import sys

from pyintegrity.common.ymlInput import ymlInput
from pyintegrity.common.update_deep import AttributeDict
from pyintegrity.common.ApplicationManager import ConfigureApplicationInputs
from pyintegrity.API579 import API579

ymlfile = 'src/pyffs/tests/test_data/16in_gas_b318.yml'
sys.argv.append(ymlfile)
print(os.path.isfile(ymlfile))
cfg = ymlInput(ymlfile, updateYml=None)
cfg = AttributeDict(cfg)

basename = 'API579'
application_manager = ConfigureApplicationInputs(basename)
application_manager.configure(run_dict=None)

cfg_base = API579(application_manager.cfg)
