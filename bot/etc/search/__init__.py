import sqlite3
_database = sqlite3.connect("./output/s2data.db")
_database.execute("DELETE FROM collection")
_database.close()

from scientist import datahandler

datahandler.SQLALCHEMY_URI = 'sqlite:///output/s2data.db'
datahandler.SQLALCHEMY_URI_USER = 'sqlite:///output/user.db'
datahandler.SQLALCHEMY_ECHO = False

from ..sql import connection

from scientist.search import DataScientist, LogSettings, Record
from scientist.datahandler.dtos_S2Data import Collection

logSet = LogSettings("logger scientist", filemode="a", filepath="./output/search.log")
sc: DataScientist = DataScientist(logSet, True)
_id = 0
for x in connection.table("qaa").select("id, question, answer, tags").fetchall():
    collection = Collection(_id, x[0])
    collection.name = x[1]
    collection.extraSearch = x[2]
    collection.category = x[3].split(", ")
    sc.insertCollection(collection)
sc.recreateIndex()
