"""
from utils.unsplash import *
from utils.wall import *
from utils.extra import *
from utils.logo import *
from utils.nyaa import *
"""

mod_paths = glob.glob(dirname(__file__) + "/*.py")

for f in mod_paths:
  if isfile(f) and f.endswith(".py"):
    pr = basename(f)[:-3]
    from pr import *
