from scientist import datahandler

datahandler.SQLALCHEMY_URI = 'sqlite:///output/s2data.db'
datahandler.SQLALCHEMY_URI_USER = 'sqlite:///output/user.db'
datahandler.SQLALCHEMY_ECHO = False

from scientist.search import DataScientist, LogSettings, Record
from scientist.datahandler.dtos_S2Data import Collection

logSet = LogSettings("logger scientist", filemode="a", filepath="./output/search.log")
sc: DataScientist = DataScientist(logSet, True)
