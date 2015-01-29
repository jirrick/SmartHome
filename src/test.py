import serial
import io
import sqlite3
import datetime

ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=3)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
sio._CHUNK_SIZE = 1
con = sqlite3.connect('test.db') # @UndefinedVariable
sio.flush()

while not sio.closed:
    try:    
        line = sio.readline()
        words = line.split(',')
        charge = int(words[1][1:])
        discharge = int(words[2][1:])
        f = int(words[3][1:])
        bilance = int(words[4][1:])
        ub = float(words[5][2:])/10
        i = float(words[6][1:])/1000
        al = int(words[7][2:])
        ah = int(words[8][2:])
        stamp = int(datetime.datetime.now().timestamp())

        cur = con.cursor()  
        cur.execute("insert into battery (charge, discharge, f, bilance, ub, i, al, ah, date) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (charge, discharge, f, bilance, ub, i, al, ah, stamp))
        con.commit()

        print('stamp: ' + str(stamp), end=", ")
        print('char: ' + str(charge), end=", ")
        print('disch: ' + str(discharge), end=", ")
        print('f: ' + str(f), end=", ")
        print('bil: ' + str(bilance), end=", ")
        print('ub: ' + str(ub), end=", ")
        print('i: ' + str(i), end=", ")
        print('al: ' + str(al), end=", ")
        print('ah: ' + str(ah), end=" ")

    except ValueError:
        print("Conversion error")

    print()
