import  hotelManagement
import sqlite3
import time

dbcon=sqlite3.connect('cronhoteldb.db')

def dohoteltask(taskname,parameter):
    pointer=dbcon.cursor()
    dbcon.text_factory = bytes
    temp=pointer.execute("SELECT TaskId FROM Tasks WHERE TaskName=(?) AND Parameter=(?)",[taskname,parameter],).fetchone()[0]
    myTask =pointer.execute("SELECT TaskId from TaskTimes WHERE TaskId=?",(temp,)).fetchone()
    myTask=myTask[0]
    myNumTimes=pointer.execute("SELECT NumTimes FROM TaskTimes WHERE TaskId=?",(myTask,)).fetchone()[0]
    DoEvery = pointer.execute("SELECT DoEvery FROM TaskTimes WHERE TaskId=?",(myTask,)).fetchone()[0]
    if  taskname !='clean':
        FirstName = pointer.execute("SELECT FirstName FROM Residents WHERE RoomNumber=(?)",(parameter,)).fetchone()[0]
        LastName = pointer.execute("SELECT LastName FROM Residents WHERE RoomNumber=?",(parameter,)).fetchone()[0]
        MyTime=time.time()
        if taskname == 'breakfast':
            if myNumTimes == 1:
                print('{} {} in room {} has been served breakfast at {}'.format(FirstName,LastName,parameter,MyTime))
                return -1
            else:
                print('{} {} in room {} has been served breakfast at {}'.format(FirstName,LastName,parameter,MyTime))
                return MyTime+DoEvery
        else:##wakeup
            if myNumTimes == 1:
                print('{} {} in room {} received a wakeup call at {}'.format(FirstName, LastName ,parameter, MyTime))
                return -1
            else:

                print('{} {} in room {} received a wakeup call at {}'.format(FirstName, LastName, parameter, MyTime))
                return MyTime + float(DoEvery)
    else:##cleaning
        RoomsToBeCleand=pointer.execute("SELECT RoomNumber FROM Rooms WHERE RoomNumber not in(SELECT RoomNumber FROM Residents) ").fetchall()
        RoomsToBeCleand.sort()
        currRooms=""
        for currlist in RoomsToBeCleand:
            currRooms=currRooms+","+str(currlist[0])
        currRooms=currRooms[1:]
        RoomsToBeCleand=currRooms
        MyTime= time.time()
        if myNumTimes==1:
            print('Rooms {} were cleaned at {}'.format(RoomsToBeCleand[:],MyTime))
        else:
            print('Rooms {} were cleaned at {}'.format(RoomsToBeCleand[:], MyTime))
            return MyTime + float(DoEvery)
    







