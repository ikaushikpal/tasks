import datetime


class Task:
    def __init__(self,
                id,
                title, 
                date_added=None,
                status=0,
                category="General",
                priority=0,
                date_completed = None,
                desc=None):
        self.id = id
        self.title = title
        self.date_added = date_added if date_added else datetime.datetime.now().isoformat()
        self.status = status
        self.category = category
        self.priority = priority
        self.date_completed = date_completed
        self.desc = desc

    def __str__(self):
        return f"{self.id} {self.title} {self.desc} {self.status}"
    
    def __repr__(self) -> str:
        return self.__str__()