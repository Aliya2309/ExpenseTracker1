import sqlite3 as db
from datetime import datetime
import matplotlib.pyplot as plt


def init():
    '''
    Initialize a new database to store the
    expenditures
    '''
    conn = db.connect("spent.db")
    cur = conn.cursor()
    sql = '''
    create table if not exists expenses (
        amount number,
        category string,
        message string,
        date string
        )
    '''
    cur.execute(sql)
    conn.commit()

def log(amount, category, message=""):
    '''
    logs the expenditure in the database.
    amount: number
    category: string
    message: (optional) string
    '''
    date = str(datetime.now())
    data = (amount, category, message, date)
    conn = db.connect("spent.db")
    cur = conn.cursor()
    sql = 'INSERT INTO expenses VALUES (?, ?, ?, ?)'
    cur.execute(sql, data)
    conn.commit()

def view(t, category=None):
    '''
    Returns a list of all expenditure incurred, and the total expense.
    If a category is specified, it only returns info from that
    category
    '''
    conn = db.connect("spent.db")
    cur = conn.cursor()
    if category:
        sql = '''
        select amount from expenses where category = '{}'
        '''.format(category)
        sql3 = '''
        select category from expenses where category = '{}'
        '''.format(category)
        sql4 = '''
        select message from expenses where category = '{}'
        '''.format(category)
        sql5 = '''
        select date from expenses where category = '{}'
        '''.format(category)
        sql6='''
        select * from expenses where category='{}'
        '''.format(category)
        sql2 = '''
        select sum(amount) from expenses where category = '{}'
        '''.format(category)
    else:
        sql = '''
        select amount from expenses
        '''.format(category)
        sql3 = '''
                select category from expenses
                '''.format(category)
        sql4 = '''
                select message from expenses
                '''.format(category)
        sql5 = '''
                select date from expenses
                '''.format(category)
        sql2 = '''
        select sum(amount) from expenses
        '''.format(category)
        sql6 = '''
                select * from expenses
                '''.format(category)
    cur.execute(sql)
    amounts = [item[0] for item in cur.fetchall()]
    cur.execute(sql3)
    cats = [item[0] for item in cur.fetchall()]
    cur.execute(sql4)
    msgs = [item[0] for item in cur.fetchall()]
    cur.execute(sql5)
    dates = [item[0] for item in cur.fetchall()]
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    cur.execute(sql6)
    all=cur.fetchall()
    if t==1:
        return [amounts, cats, msgs, dates, total_amount]
    elif t==2:
        return all


def data_list():
    data1=view(2)
    print("Amount\tCategory\tMessage\t\tDate and Time")
    for l in data1:
        for i in l:
            print(i, end="\t\t")
        print()

def data_chart():
    data2=view(1)
    print(data2)
    labels=["Food", "Travel", "Bills", "Charity", "Clothing/Toiletries", "Others", "Savings"]
    sizes=[0, 0, 0, 0, 0, 0, 10000-data2[4]]
    print(len(data2[1]))
    for i in range(len(data2[1])):
        if data2[1][i]=="Food":
            sizes[0]=sizes[0]+data2[0][i]
            continue
        if data2[1][i]=="Travel":
            sizes[1]=sizes[1]+data2[0][i]
            continue
        if data2[1][i]=="Bills":
            sizes[2]=sizes[2]+data2[0][i]
            continue
        if data2[1][i]=="Charity":
            sizes[3]=sizes[3]+data2[0][i]
            continue
        if data2[1][i]=="Clothing" or data2[1][i]=="Toiletries":
            sizes[4]=sizes[4]+data2[0][i]
            continue
        else:
            print("here", data2[0][i])
            sizes[5]=sizes[5]+data2[0][i]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()





init()
ch=int(input("Enter 1 for entering data. 2 for viewing data. 3 to exit"))
while(ch<3):
    if ch==1:
        amt=int(input("Enter the amount spent"))
        cat=input("Enter type of expense")
        m=input("Enter optional message")
        log(amt, cat, m)
    else:
        ch2=int(input("Enter 1 to view in list form. Enter 2 to view in pie chart form"))
        if ch2==1:
            data_list()
        else:
            data_chart()

    ch = int(input("Enter 1 for entering data. 2 for viewing data. 3 to exit"))
