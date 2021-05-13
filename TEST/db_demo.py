# -*- coding: utf-8 -*-
import sqlite3

connection = sqlite3.connect("/home/mobyrktr/Python/users_test.db")

cursor = connection.execute("select * from users")

for row in cursor:
    print(row)

connection.close()

