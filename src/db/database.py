import sqlite3
from typing import List, Optional
import datetime
from model import Task
from pathlib import Path
try:
    from exceptions import exception
except ModuleNotFoundError:
    import importlib.util       
    spec = importlib.util.spec_from_file_location(
    "exception", Path(__file__).parent.parent / "exceptions/exception.py")
    exception = importlib.util.module_from_spec(spec)       
    spec.loader.exec_module(exception)


class DataBaseHandler():
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.connection_status = False
        try:
            self.create_data_base()
            self.connect()
            self.create_table()
        except Exception as e:
            print(e)

    def create_data_base(self):
        try:
            self.database_path.parent.mkdir(exist_ok=True)
        except OSError:
            raise exception.DirectoryError("data")

        try:
            self.database_path.touch(exist_ok=True)
        except OSError:
            raise exception.DataBaseCreationError()

    def connect(self):
        try:
            self.conn = sqlite3.connect(str(self.database_path))
            self.cursor = self.conn.cursor()
            self.connection_status = True
        except Exception as e:
            raise ConnectionError()

    def create_table(self):
        try:
            if not self.connection_status:
                raise exception.ConnectionError()
            with self.conn:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title VARCHAR(100),
                                    date_added TEXT,
                                    status TINYINT,
                                    category VARCHAR(50),
                                    priority TINYINT,
                                    date_completed TEXT,
                                    desc TEXT)''')
                self.conn.commit()
        except Exception as e:
            raise exception.DataBaseWriteError(str(e))
    
    def add_task(self, task: Task):
        try:
            if not self.connection_status:
                raise exception.ConnectionError()
            with self.conn:
                self.cursor.execute('INSERT INTO tasks(title, date_added, status, category, priority, date_completed, desc) VALUES (:title, :date_added, :status, :category, :priority, :date_completed, :desc)',
                {'title': task.title, 'date_added':task.date_added,'status': task.status, 
                'category': task.category, 'priority': task.priority, 'date_completed': task.date_completed, 'desc': task.desc})
            self.conn.commit()
        except Exception as e:
            raise exception.DataBaseWriteError(str(e))

    def get_all_tasks(self) -> List[Task]:
        try:
            if not self.connection_status:
                raise exception.ConnectionError()
            with self.conn:
                self.cursor.execute('SELECT * FROM tasks')
                results = self.cursor.fetchall()
                tasks = []
                for result in results:
                    tasks.append(Task(*result))
                return tasks
        except Exception as e:
            raise exception.DataBaseReadError(str(e))
    
    def get_tasks_by_cond(self, cond, sort=[]) -> List[Task]:
        if not self.connection_status:
            raise exception.ConnectionError()
        cond_msg = ''

        for key, value in cond.items():
            cond_msg += f'{key}={value} AND'
        cond_msg = cond_msg[:-4]
        command = f'SELECT * FROM tasks WHERE {cond_msg}'
        
        if sort:
            command += f' ORDER BY {",".join(sort)}'
        print(command)
        try:
            with self.conn:
                self.cursor.execute(command)
                results = self.cursor.fetchall()
                tasks = []
                for result in results:
                    tasks.append(Task(*result))
                return tasks
        except Exception as e:
            raise exception.DataBaseReadError(str(e))
            
    def get_tasks_by_date(self, date_fmt: str, date_column='date_added') -> List[Task]:
        try:
            if not self.connection_status:
                raise exception.ConnectionError()
            with self.conn:
                self.cursor.execute(f'SELECT * FROM tasks WHERE date({date_column}) LIKE :day', {'day': date_fmt})
                results = self.cursor.fetchall()
                tasks = []
                for result in results:
                    tasks.append(Task(*result))
                return tasks

        except Exception as e:
            raise exception.DataBaseReadError(str(e))

    def remove_task(self, id:int):
        try:
            if not self.connection_status:
                raise exception.ConnectionError()
            with self.conn:
                self.cursor.execute('DELETE FROM tasks WHERE id = :id', {'id': id})
                self.conn.commit()
        except Exception as e:
            raise exception.IDNotFoundError(id)

    def remove_all_tasks(self, id:int):
        try:
            if not self.connection_status:
                raise exception.ConnectionError()
            with self.conn:
                self.cursor.execute('DELETE FROM tasks')
                self.conn.commit()
        except Exception as e:
            raise exception.IDNotFoundError(id)

    def undone_task(self, id:int):
        try:
            if not self.connection_status:
                raise exception.ConnectionError()
            with self.conn:
                self.cursor.execute('UPDATE tasks SET status = 0 AND date_completed=NULL WHERE id = :id', {'id': id})
                self.conn.commit()
        except Exception as e:
            raise exception.IDNotFoundError(id)
    
    def done_task(self, id:int):
        try:
            if not self.connection_status:
                raise exception.ConnectionError()
            with self.conn:
                self.cursor.execute('UPDATE tasks SET status = 1 AND date_completed=:date_completed WHERE id = :id', {'id': id, 'date_completed': datetime.datetime.now().isoformat()})
                self.conn.commit()
        except Exception as e:
            raise exception.IDNotFoundError(id)


if __name__ == '__main__':
    db = DataBaseHandler(Path(__file__).parent.parent.parent / 'data' / 'tasks.db')
    print(db.get_all_tasks())
