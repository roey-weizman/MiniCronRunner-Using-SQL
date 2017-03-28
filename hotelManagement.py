import sqlite3
import sys
import os


def main(args):
    databaseexisted = os.path.isfile('cronhoteldb.db')
    if(databaseexisted):
        return
    dbcon = sqlite3.connect('cronhoteldb.db')
    with dbcon:
        cursor = dbcon.cursor()
        dbcon.text_factory = bytes
        cursor.execute(
            "CREATE TABLE TaskTimes(TaskId INTEGER PRIMARY KEY NOT NULL,DoEvery INTEGER NOT NULL,NumTimes INTEGER NOT NULL)")
        cursor.execute(
            "CREATE TABLE Tasks(TaskId INTEGER NOT NULL REFERENCES TaskTimes(TaskId),TaskName text NOT NULL,Parameter INTEGER)")
        cursor.execute("CREATE TABLE Rooms(RoomNumber INTEGER PRIMARY KEY NOT NULL)")
        cursor.execute(
            "CREATE TABLE Residents(RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber),FirstName text NOT NULL,LastName text NOT NULL) ")

        id = 0
        inputfilename = args[1]
        with open(inputfilename) as inputfile:
            for line in inputfile:
                theLineIgot = line.rstrip('\n').split(',')
                if len(theLineIgot) == 2:
                    cursor.execute("INSERT INTO Rooms VALUES(?)", (theLineIgot[1],))

                elif len(theLineIgot) == 3:
                    cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (id, theLineIgot[1], theLineIgot[2]))
                    cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (id, theLineIgot[0], 0))
                    id += 1
                elif len(theLineIgot) == 4:
                    if theLineIgot[0] == 'room':
                        cursor.execute("INSERT INTO Residents VALUES(?,?,?)",
                                       (theLineIgot[1], theLineIgot[2], theLineIgot[3]))
                        cursor.execute("INSERT OR  IGNORE INTO Rooms VALUES(?)", (theLineIgot[1],))  # check
                    else:
                        cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (id, theLineIgot[1], theLineIgot[3]))
                        cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (id, theLineIgot[0], theLineIgot[2]))
                        id += 1


if __name__ == '__main__':
    main(sys.argv)
