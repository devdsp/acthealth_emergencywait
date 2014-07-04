from bs4 import BeautifulSoup
import requests
import time
import sqlite3 as sql
con = sql.connect("data.sqlite")
con.execute("create table if not exists data (timestamp int, hospital text, key text, value int)")
soup = BeautifulSoup(requests.get('http://health.act.gov.au/emergency/live-emergency-data-information').text)
now = time.time()
for row in soup.find("table", { "class" : "emergencywait" }).findAll('tr'):
    cells = row.findAll('td')
    if len(cells[0].contents) == 1:
        cur = con.cursor()
        cur.executemany(
            "INSERT INTO data VALUES(?,?,?,?)",
            (
                (now,"calvery",cells[0].getText(),cells[1].getText()),
                (now,"tch",    cells[0].getText(),cells[2].getText())
            )
        )
con.commit()
