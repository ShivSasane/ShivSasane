import os, mysql.connector as myc
def dbcon():
    try:
     con=myc.connect(host='Localhost',user='root',password='')
     mycursor=con.cursor()
     mycursor.execute('DROP DATABASE IF EXISTS cinemaproj')
     mycursor.execute('CREATE DATABASE cinemaproj')
     mycursor.execute('DROP TABLE IF EXISTS hall_det')
     sql='''CREATE TABLE hall_det(
             hallno INT(5)PRIMARY KEY,
             hallname VARCHAR(20) NOT NULL,
             frontseats INTEGER NOT NULL,
             midseats INTEGER NOT NULL,
             backseats INTEGER NOT NULL)'''
     mycursor.execute(sql)
     mycursor.execute('DROP TABLE IF EXISTS booking_det')
     sql='''CREATE TABLE booking_det(
            ticket no INT(5) AUTO_INCREMENT PRIMARY KEY,
            hallno INT(5) NOT NULL,
            customer VARCHAR(15) NOT NULL,
            no_of_seats INT(2) NOT NULL,
            cost_of_seat INT(4) NOT NULL,
            seattype char(1) NOT NULL,
            discount INT(3) NULL,
            CONSTRAINT FOREIGN KEY(hallno)
            REFRENCES hall_det(hallno))'''
     mycursor.execute(sql)
     #INSERTING ROWS IN TO THE CINEMA HALL TABLE
     sql='''INSERT INTO hall_det(hallno,hallname,frontseats,midseats,backseats)
     VALUES(%s,%s,%s,%s,%s)'''
     rows=((10001,'PVR-YPR',50,50,50),
           (1002,'INOX-MANTRI',50,50,50),
           (1003,'PVR-GDP',50,50,50),
           (1004,'PHEONIX',60,50,50))
     mycursor.executemany(sql,rows)
     sql='''INSERT INTO booking_det(hallno<customer,no_of_seats,cost_of_seat,seattype,discount)
     VALUES(%s,%s,%s,%s,%s)'''
     rows=((1001,'Pooja',5,500,'A',100),
           (1002,'Ankush',5,500,'B',100),
           (1003,'Krunal',5,700,'C',100),
           (1004,'Parth',5,500,'B',100))
     mycursor.executemany(sql,rows)
     con.commit()
    except myc.Error as err:
        print(err)
        print("SQLSTATE",err.sqlstate)
    finally:
        print('Databses schema created')
        con.close()
def getseats():
    try:
        import mysql.connector as myc
        con=myc.connect(host='localhost',user='root',passwd='',database='cinemaproj')
        mycursor=con.cursor()
        sql="SELECT frontseats,midseats,backseats FROM hall_det WHERE hallno='%d%(hn0)"
        mycursor.execute(sql)
        rec=mycursor.fetchone()
        con.close()
    except myc.Error as err:
        print(err)
    finally:
        return rec      

def hallnums():
    try:
        import mysql.connector as myc
        con=myc.connect(host='localhost',user='root',passwd='',database='cinemaproj')
        mycursor=con.cursor()
        sql="SELECT hallno FROM hall_det ORDER BY hallno"
        mycursor.execute(sql)
        rec=mycursor.fetchall()
        hlst=[]
        for x in rec:
            hlst.append(x[0])
    except myc.Error as err:
        print(err)
    finally:
        con.close()
        return hlst

def getticketdet():
    try:
        import mysql.connector as myc
        con=myc.connect(host='localhost',user='root',passwd='',database='cinemaproj')
        mycursor=con.cursor()
        sql="SELECT ticketno FROM booking_det"
        mycursor.execute(sql)
        rec=mycursor.fetchall()
        tlst=[]
        for x in rec:
            tlst.append(x[0])
    except myc.Error as err:
        print(err)
    finally:
        con.close()
        return rec

def updateseats(hno,stype,amt):
    try:
        import mysql.connector as myc
        con=myc.connect(host='localhost',user='root',passwd='',database='cinemaproj')
        mycursor=con.cursor()
        if stype=='A':
           sql="UPDATE hall_det set frontseats=frontseats-'%d' WHERE hallno='%d%(amt,hno)'"
        if stype=='b':
           sql="UPDATE hall_det set middleseats=middleseats-'%d' WHERE hallno='%d%(amt,hno)'"
        if stype=='C':
           sql="UPDATE hall_det set backseats=backseats-'%d' WHERE hallno='%d%(amt,hno)'"  
        mycursor.execute(sql)
        con.commit()
    except myc.Error as err:
      print(err)
    finally:
        print('Seats Updated')
        con.close()
        
def booking(hno,cname,noseat,cost,stype,disc=0):
    import mysql.connector as myc
    s1,s2,s3=getseats(hno)
    if((stype=='A'and noseat>s1) or (stype=='B'and noseat>2) (stype=='C'and noseat>3)):
        return'No seats available'
    else:
        try:
         con=myc.connect(host='localhost',user='root',passwd='',database='cinemaproj')

         mycursor=con.cursor()
         sql="INSERT INTO booking_det(hallno,customer,no_of_seats,cost_of_seat,seattype,discount)VALUES(%s,%s,%s,%s,%s)"
         rows=((hno,cname,noseat,cost,stype,disc))
         mycursor.executemany(sql,rows)
         con.commit()
         updateseats(hno,stype,noseat) 
        except myc.Error as err:
            print(err)
        finally:
            print('Record inserted')
            con.close()

def showhallbooking(hno):
    try:
       import mysql.connector as myс
       count = 0
       con =myc.connect(host='localhost', user='root', passwd='', database='cinemaproj')
       mycursor=con.cursor()
       count = "SELECT COUNT(*) FROM booking_det,hall_det WHERE b.hallno=h.hallno and b.hallno='%d%(hno)'"
       if count> 0:
        sql = "SELECT b.ticketno, b.hallno, h.hallname ,b.seattype,b.no_of_seats,b.cost_of_seat,b.discount FROM booking_det b, hall_det h WHERE b.hallno = h.hallno and b.hallno='%d" % (hno)
        mycursor.execute(sql)
        rec =mycursor.fetchall()
       else:
            print("NO RECORDS")
    except myc.Error as err:
        print(err)
        print("sqlstate",err.sqlstate)
    finally:
        print(showhallbooking(1001))
        con.close()
        return rec

def hallstat():
    try:
        import mysql.connector as myc
        con =myc.connect(host='localhost', user='root', passwd='', database='cinemaproj')
        mycursor=con.cursor()
        sql="SELECT b.ticketno, h.hallno, h.hallname, b.seattype,b.no_of_seats,b.cost_of_seat,b.discount, h.frontseats, h.midseats, h.backseats FROM booking_det b,hall_det h WHERE b.hallno=h.hallno"
        mycursor.execute(sql)
        rec = mycursor.fetchall()
    except myc.Error as err:
        print(err)
        print("SQLSTATE", err.sqlstate)
    finally:
     con.close()
     return rec
    
def allbookings():
    try:
        import mysql.connector as myc
        con =myc.connect(host='localhost', user='root', passwd='123', database='cinemaproj')
        mycursor=con.cursor()
        sql="SELECT b.ticketno, h.hallno, h.hallname, b.seattype,b.no_of_seats,b.cost_of_seat,b.discount, h.frontseats, h.midseats,h.backseats FROM booking_det b,hall_det h WHERE b.hallno=h.hallno"
        mycursor.execute(sql)
        rec = mycursor.fetchall()
    except myc. Error as err:
        print(err)
        print("SQLSTATE", err.sqlstate)
    finally:
        con.close()
        return rec

def addhall(hallno, hname, fs, ms, bs):
    try:
        import mysql.connector as myc
        con =myc.connect(host='localhost', user='root', passwd='', database='cinemaproj')
        mycursor=con.cursor()
        sql="INSERT INTO hall_det(hallno, hallname, frontseats, midseats, backesats) VALUES (%s, %s, %s, %s,%s)"
        rows=(hallno,hname, fs, ms,bs)
        mycursor.executemany(sql,rows)
        con.commit()
    except myc.Error as err:
     print(err)
     print("SQLSTATE", err.sqlstate)
    finally:
     print("Hall Added")
     con.close()

def printticket(tno):
    try:
     import mysql.connector as myc
     con =myc.connect(host='localhost', user='root', passwd='123', database='cinemaproj')
     mycursor=con.cursor()
     sql= "SELECT b.ticketno, b.hallno, h.hallname,b.customer,b.seattype, b.no_of_seats, b.cost_of_seat,b.discount FROM booking_det b,hall_det h WHERE b.hallno=h.hallno and b.ticketno='%d%(tno)'"
     mycursor.execute(sql)
     rec=mycursor.fetchall()
    except myc.Error as err:
     print(err)
     print("SQLSTATE", err.sqlstate)
    finally:
     con.close()
     return rec

def inputNumber(message):
    while True:
        try:
            userInput=int(input(message))
        except ValueError:
            print("Not an integer! Try again")
        continue
    else:
        return userinput
while True:
    print('||======================GO MY SHOW=====================')
    print('|| Type 1 To add a hall in your portal ||')
    print('|| Type 2 To view all the halls in your portal ||')
    print('|| Type 3 To book a ticket in a hall ||')
    print('|| Type 4 To see a booking status of a hall ||')
    print('|| Type 5 To see all the bookings of halls ||')
    print('|| Type 6 To generate ticket for booking ||')
    print('|| Type 7 To quit||')
    print('|| Type 0 To reset Application ||')
    print(' ||====================================================')
    choice=int(input('Enter your choice'))
    if choice==0:
        dbcon()
    if choice==1:
        hallno=input('Enter your hall number:')
        hname=input('Enter your hall name:')
        fs=int(input('Enter the maximum front seats:'))
        ms=int(input('Enter maximum middle seats'))
        bs=int(input('Enter the maximum back seats'))
        addhall(hallno,hname,fs,ms,bs)
        break
    if choice==2:
        import pandas as pd
        rec=hallstat()
        df=pd.DataFrame(rec)
        df.columns=['Hallno','Hallname','A-type','B-type','C-type']
        print(df)
        break
    if choice==3:
        import pandas as pd
        print('You have the following hall Numbers')
        print(hallnums())
        hno=int(input('Enter a valid hallno:'))
        cname=int(input('Enter Customer name:'))
        stype=input('Enter Seat Type as A,B,C:')
        noseat=int(input('Enter number of seats:'))
        cost=int(input('Enter cost of each seat:'))
        dis=0
        if noseat*cost>=2000:
            dis=100
        booking(hno,cname,noseat,cost,stype,dis)
        break
    if choice==4:
        import pandas as pd
        print('You can get details of the following hall numbers')
        print(hallnums())
        hno=int(input('Enter a valid hallno:'))
        if hno in hallnums():
            rec=showhallbooking(hno)
            df=pd.DataFrame(rec)
            df.columns=['Ticket No','Hall No','Hall Name','Seat Type','No of Seats','Rate','Discount']
            print(df)
        else:
            print('Invalid Hall Number')
        break
    if choice==5:
        import pandas as pd 
        rec=allbookings()
        df=pd.DataFrame(rec)
        df.columns=['Ticket No','Hall No','Hall Name','Seat Type','No of Seats','Cost per seat','Discount','A-type','B-type','C-type']
        print(df)
        break
    if choice==6:
        tno=int(input('Enter the ticket number:'))
        rec=getticketdet()
        if tno in rec:
            rec=printticket(tno)
            print("---------Ticket Details----------")
            print("Ticket Number is :%d" % (rec[0][0]))
            print("Hall Number is :%d" % (rec[0][1]))
            print("Hall Name is :%s" % (rec[0][2]))
            print("Customer Name is :%s" % (rec[0][3]))
            print("Seat Type  :%s" % (rec[0][4]))
            print("Number of Seats :%d" % (rec[0][5]))
            print("Cost per seat  :%d" % (rec[0][6]))
            print("Discount :%d" % (rec[0][7]))
            total=rec[0][5]*rec[0][6]-rec[0][7]
            print("Total Cost :%d"%(total))
            print(rec)
        else:
            print('Ticket Number not available')
        break
    if choice==7:
        exit(0)
        os.system('pause')
        os.system('cls')
        break
