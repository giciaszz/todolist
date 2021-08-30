from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


def addtask():
    print('Enter task')
    new_row = Table(task=input(), deadline=datetime.strptime(input('Podaj date Y-m-d'), '%Y-%m-%d').date())
    print('The task has been added!')
    session.add(new_row)
    session.commit()


def meni():
    print("\n")
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print('4) Missed tasks')
    print('5) Add task')
    print('6) Delete task')
    print('0) Exit')
    co = int(input())
    if co == 1:
        pokataski()
        meni()
    elif co == 2:
        weekst()
        meni()
    elif co == 3:
        alltask()
        meni()
    elif co == 4:
        mistask()
        meni()
    elif co == 5:
        addtask()
        meni()
    elif co == 6:
        deltask()
        meni()
    elif co == 0:
        print('Bye!')


def mistask():
    dejt = datetime.today().date()
    rows = session.query(Table).filter(Table.deadline < dejt).order_by(Table.deadline).all()
    print('Missed tasks:')
    if len(rows) == 0:
        print('Nothing is missed!')
    for i in range(len(rows)):
        first_row = rows[i]
        print(f"{i+1}. {first_row.task}. {first_row.deadline.strftime('%d %b')}")



def deltask():
    print('Choose the number of the task you want to delete:')
    rows = session.query(Table).order_by(Table.deadline).all()
    for i in range(len(rows)):
        first_row = rows[i]
        print(f"{i+1}. {first_row.task}. {first_row.deadline.strftime('%d %b')}")
    dowyjebania = int(input()) - 1
    specific_row = rows[dowyjebania]
    session.delete(specific_row)
    session.commit()
    print('The task has been deleted!')

def weekst():
    for i in range(7):
        dejt = datetime.today().date() + timedelta(i)
        rows = session.query(Table).filter(Table.deadline == dejt).order_by(Table.deadline).all()
        if len(rows) == 0:
            print(f"{dejt.strftime('%A %d %b')}:\nNothing to do!\n")
        else:
            print(dejt.strftime('%A %d %b'))
            for z in range(len(rows)):
                first_row = rows[z]
                print(f"{z+1}.{first_row.task} \n")

def alltask():
    rows = session.query(Table).order_by(Table.deadline).all()
    print('All tasks:')
    for i in range(len(rows)):
        first_row = rows[i]
        print(f"{i+1}. {first_row.task}. {first_row.deadline.strftime('%d %b')}")


def pokataski():
    rows = session.query(Table).all()
    if len(rows) == 0:
        print(f"Today: {datetime.today().strftime('%d %b')}")
        print('Nothing to do!')
    else:
        for i in range(len(rows)):
            first_row = rows[i]
            print(first_row.task)


Session = sessionmaker(bind=engine)
session = Session()


meni()
