from sys import platform

from mariadb_sqlbuilder import Connect

if platform == "win32":
    _host = "192.168.2.230"
    _password = "superpassword"
else:
    _host = "localhost"
    _password = "superstrongpassword"

connection = Connect(
    host=_host,
    user="root",
    password=_password,
    database="nori"
)
