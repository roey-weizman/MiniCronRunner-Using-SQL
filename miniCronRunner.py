import sys
import sqlite3
import os
import hotelWorker
import time

def main():
    databaseexisted = os.path.isfile('cronhoteldb.db')
    dbcon=sqlite3.connect('cronhoteldb.db')
    dbcon.text_factory = bytes
    c=dbcon.cursor()
    ListOfThree=list()
    sum=0
    index=0
    firstRound=False
    c.execute('SELECT * FROM TaskTimes')
    for row in c:
        InnerList=list()
        InnerList.insert(0,0)
        InnerList.insert(0,row[2])
        InnerList.insert(0,row[0])
        sum+=row[2]
        ListOfThree.insert(0,InnerList)
    ListOfThree.sort(key=lambda x: x[2])
    #print(ListOfThree)
    while(databaseexisted and sum>0 and index is not len(ListOfThree)):
        if firstRound==False:##first initialization
            for inner in ListOfThree:
                myId=inner[0]
                myTaskName=c.execute("SELECT TaskName FROM Tasks WHERE  TaskId=?",(myId,)).fetchone()[0]
                myRoom=c.execute("SELECT Parameter FROM Tasks WHERE  TaskId=?",(myId,)).fetchone()[0]
                inner[2]=hotelWorker.dohoteltask(myTaskName,myRoom)
                inner[1]-=1
                c.execute("UPDATE TaskTimes SET NumTimes=(?) WHERE TaskId=(?)", (inner[1],myId))
                sum-=1

            ListOfThree.sort(key=lambda x: x[2])
            firstRound=True
        else:
            if ListOfThree.__getitem__(index)[1]==0:
                index+=1
            else:
                currTaskId=ListOfThree.__getitem__(index)[0]
                currTimeToExecute=ListOfThree.__getitem__(index)[2]
                if currTimeToExecute>=time.time():
                    time.sleep(currTimeToExecute-time.time())
                name=c.execute("SELECT TaskName FROM Tasks WHERE  TaskId=?",(currTaskId,)).fetchone()[0]
                currRoom = c.execute("SELECT Parameter FROM Tasks WHERE  TaskId=?",(currTaskId,)).fetchone()[0]
                ListOfThree.__getitem__(index)[2]=hotelWorker.dohoteltask(name,currRoom)
                ListOfThree.__getitem__(index)[1]-=1
                c.execute("UPDATE TaskTimes SET NumTimes=(?) WHERE TaskId=(?)", (ListOfThree.__getitem__(index)[1],currTaskId))
                sum -= 1
                ListOfThree.sort(key=lambda x: x[2])

if __name__ == '__main__':
        main()

