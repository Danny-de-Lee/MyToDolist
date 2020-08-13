from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


def get_date():
    input_date = [int(i) for i in input("Enter deadline\n>").split("-")]
    return input_date


def print_deadline(date, today=False):
    day_tasks = get_tasks(date.date())
    if today:
        print("Today", date.strftime("%d %b") + ":")
    else:
        print(date.strftime('%A %d %b') + ":")
    if len(day_tasks) == 0:
        print("Nothing to do!")
    else:
        count_task = 0
        for task in day_tasks:
            count_task += 1
            print(f"{count_task}. {task.task}")
    print()


def get_tasks(date):
    return session.query(Table).filter(Table.deadline == date).all()


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

while True:
    user_input = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n> ")
    print()
    if user_input == "1":  # today's tasks request
        print_deadline(datetime.today(), today=True)
    elif user_input == "2":  # week's tasks request
        date = datetime.today()
        for _ in range(7):
            print_deadline(date)
            date += timedelta(days=1)
    elif user_input == "3":
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        if len(all_tasks) == 0:
            print("Nothing to do!")
        else:
            print("All tasks:")
            count_task = 0
            for task in all_tasks:
                count_task += 1
                print(f"{count_task}. {task.task}. {task.deadline.strftime('%d %b')}")
        print()
    elif user_input == "4":
        mis_tasks = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print("Missed tasks:")
        if len(mis_tasks) == 0:
            print("Nothing is missed!")
        else:
            count_task = 0
            for task in mis_tasks:
                count_task += 1
                print(f"{count_task}. {task.task}. {task.deadline.strftime('%d %b')}")
        print()
    elif user_input == "5":
        new_row = Table(task=input("Enter task\n>"),
                        deadline=datetime(*get_date()))
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif user_input == "6":
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        if len(all_tasks) == 0:
            print("Nothing to delete")
        else:
            print("Choose the number of the task you want to delete:")
            count_task = 0
            for task in all_tasks:
                count_task += 1
                print(f"{count_task}. {task.task}. {task.deadline.strftime('%d %b')}")
            input_delete_number = int(input("> "))
            row_to_delete = all_tasks[input_delete_number - 1]
            session.delete(row_to_delete)
            session.commit()
            print("The task has been deleted!")
        print()
    elif user_input == "0":
        print("Bye!")
        break
    else:
        print("Wrong code, try else!")

session.close()
