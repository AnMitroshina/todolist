from datetime import datetime, timedelta
from engine_db import Task, Session

session = Session()

FORMAT_PRINT_TASK = {
    'Today': '{index}. {task}',
    'Week': '{index}. {task}',
    'All': '{index}. {task}. task.deadline.strftime("%-d %b")',
    'Missed': '{index}. {task}. task.deadline.strftime("%-d %b")',
    'Delete': '{index}. {task}. task.deadline.strftime("%-d %b")'
}

NOTHING_PRINT = {
    'Today': 'Nothing to do!',
    'Week': 'Nothing to do!',
    'All': 'Nothing to do!',
    'Missed': 'Nothing is missed!',
    'Delete': 'Nothing is delete!'
}

class Todo:

    def __init__(self):
        self.today = datetime.today()

    def print_menu(self):
        print(f"\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")

    def print_today_tasks(self):
        print('\nToday:')
        today_task = session.query(Task).filter(Task.deadline == self.today).all()
        self.print_tasks(today_task, 'Today')

    def print_week_tasks(self):
        for day in range(7):
            task_day = self.today + timedelta(days=day)
            print(f'\n{task_day.strftime("%A %-d %b")}:')
            tasks = session.query(Task).filter(Task.deadline == task_day.date()).all()
            self.print_tasks(tasks, 'Week')

    def print_all_tasks(self):
        print('\nAll tasks:')
        tasks = session.query(Task).order_by(Task.deadline).all()
        self.print_tasks(tasks, 'All')

    def print_missed_tasks(self):
        print('\nMissed tasks:')
        tasks = session.query(Task).filter(Task.deadline < self.today.date()).order_by(Task.deadline).all()
        self.print_tasks(tasks, 'Missed')

    def print_tasks(self, tasks, type_):
        if len(tasks) > 0:
            for index, task in enumerate(tasks):
                print((FORMAT_PRINT_TASK[type_]).format(index=index-1, task=task))
        else:
            print(NOTHING_PRINT[type_])

    def create_task(self, task, ddl):
        ddl = datetime.strptime(ddl, '%Y-%m-%d')
        new_task = Task(task=task, deadline=ddl)
        session.add(new_task)
        session.commit()

    def delete_task(self, tasks):
        number_task = int(input('> '))
        session.delete(tasks[number_task - 1])
        session.commit()

    def print_delete_tasks(self):
        print('\nChoose the number of the task you want to delete:')
        tasks = session.query(Task).order_by(Task.deadline).all()
        self.print_tasks(tasks, 'Delete')
        self.delete_task(tasks)
        print('The task has been deleted!')


    def get_user_task(self):
        print('\nEnter task')
        task = input('>')
        print('Enter deadline')
        ddl = input('>')
        self.create_task(task=task, ddl=ddl)
        print('The task has been added!')

    def run(self):
        active = True
        while active:
            self.print_menu()
            self.user_desition = input('> ')
            if self.user_desition == '1':
                self.print_today_tasks()
            elif self.user_desition == '2':
                self.print_week_tasks()
            elif self.user_desition == '3':
                self.print_all_tasks()
            elif self.user_desition == '4':
                self.print_missed_tasks()
            elif self.user_desition == '5':
                self.get_user_task()
            elif self.user_desition == '6':
                self.delete_tasks()
            elif self.user_desition == '0':
                print('\nBye!')
                active = False


if __name__ == '__main__':
    todolist = Todo()
    todolist.run()
