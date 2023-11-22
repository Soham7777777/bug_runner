import os
from shelve import open as shopen
datapath = os.path.join(os.path.dirname(__file__), './playerdata')
with shopen(datapath) as cupboard:
    cupboard['highscore'] = '0'