from utils.unsplash import *
from utils.wall import *
from utils.extra import *
from utils.logo import *
from utils.nyaa import *


import glob
from os.path import basename, dirname, isfile

mod_paths = glob.glob(dirname(__file__) + "/*.py")
for f in mod_paths if isfile(f) and f.endswith(".py"):
  from f import *
