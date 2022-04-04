class DirectoryError(Exception):
    def __init__(self, message):
        self.message = f"Could Not Create Directory {message}"
        super().__init__(self.message)


class DataBaseCreationError(Exception):
    def __init__(self):
        self.message = "Unable to Create DataBase tasks.db"
        super().__init__(self.message)
        

class DataBaseReadError(Exception):
    def __init__(self, query):
        self.message = f"Unable to Read From DataBase\n{query}"
        super().__init__(self.message)
        

class DataBaseWriteError(Exception):
    def __init__(self, query):
        self.message = f"Unable to Write to DataBase\n{query}"
        super().__init__(self.message)
        

class IDNotFoundError(Exception):
    def __init__(self, id):
        self.message = f"id with {id} not found in DataBase"
        super().__init__(self.message)


class ConnectionError(Exception):
    def __init__(self):
        self.message = "Unable to establish Connection to DataBase tasks.db"
        super().__init__(self.message)