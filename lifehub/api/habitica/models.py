class Task:
    pass

class HabitTask(Task):
    def __init__(
            self,
            _id: str,
            attribute: str,
            byHabitica: bool,
            challenge: dict,
            counterDown: int,
            counterUp: int,
            createdAt: str,
            down: bool,
            frequency: str,
            group: dict,
            history: list,
            id: str,
            notes: str,
            priority: float,
            reminders: list,
            tags: str,
            text: str,
            type: str,
            up: bool,
            updatedAt: str,
            userId: str,
            value: float,
    ):
        self._id: str = _id
        self.attribute: str = attribute
        self.byHabitica: bool = byHabitica
        self.challenge: dict = challenge
        self.counterDown: int = counterDown
        self.counterUp: int = counterUp
        self.createdAt: str = createdAt #TODO: Convert to datetime
        self.down: bool = down
        self.frequency: str = frequency
        self.group: dict = group
        self.history: list = history
        self.id: str = id
        self.notes: str = notes
        self.priority: float = priority
        self.reminders: list = reminders
        self.tags: str = tags
        self.text: str = text
        self.type: str = type
        self.up: bool = up
        self.updatedAt: str = updatedAt #TODO: Convert to datetime
        self.userId: str = userId
        self.value: float = value
    
    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)
    
    def __repr__(self):
        return f"<Habitica HabitTask: {self.text}>"

class DailyTask(Task):
    def __init__(
            self,
            _id: str,
            attribute: str,
            byHabitica: bool,
            challenge: dict,
            checklist: list,
            collapseChecklist: bool,
            completed: bool,
            createdAt: str,
            daysOfMonth: list,
            everyX: int,
            frequency: str,
            group: dict,
            history: list,
            id: str,
            isDue: bool,
            nextDue: list,
            notes: str,
            priority: float,
            repeat: dict,
            reminders: list,
            startDate: str,
            streak: int,
            tags: list,
            text: str,
            type: str,
            updatedAt: str,
            userId: str,
            value: float,
            weeksOfMonth: list,
            yesterDaily: bool,
    ):
        self._id: str = _id
        self.attribute: str = attribute
        self.byHabitica: bool = byHabitica
        self.challenge: dict = challenge
        self.checklist: list = checklist
        self.collapseChecklist: bool = collapseChecklist
        self.completed: bool = completed
        self.createdAt: str = createdAt #TODO: Convert to datetime
        self.daysOfMonth: list = daysOfMonth
        self.everyX: int = everyX
        self.frequency: str = frequency
        self.group: dict = group
        self.history: list = history
        self.id: str = id
        self.isDue: bool = isDue
        self.nextDue: list = nextDue
        self.notes: str = notes
        self.priority: float = priority
        self.repeat: dict = repeat
        self.reminders: list = reminders
        self.startDate: str = startDate #TODO: Convert to datetime
        self.streak: int = streak
        self.tags: list = tags
        self.text: str = text
        self.type: str = type
        self.updatedAt: str = updatedAt #TODO: Convert to datetime
        self.userId: str = userId
        self.value: float = value
        self.weeksOfMonth: list = weeksOfMonth
        self.yesterDaily: bool = yesterDaily
    
    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return f"<Habitica DailyTask: {self.text}>"

class TodoTask(Task):
    def __init__(
        self,
        _id: str,
        attribute: str,
        byHabitica: bool,
        challenge: dict,
        checklist: list,
        collapseChecklist: bool,
        completed: bool,
        createdAt: str,
        group: dict,
        id: str,
        notes: str,
        priority: float,
        reminders: list,
        tags: list,
        text: str,
        type: str,
        updatedAt: str,
        userId: str,
        value: float,
    ):
        self._id: str = _id
        self.attribute: str = attribute
        self.byHabitica: bool = byHabitica
        self.challenge: dict = challenge
        self.checklist: list = checklist
        self.collapseChecklist: bool = collapseChecklist
        self.completed: bool = completed
        self.createdAt: str = createdAt #TODO: Convert to datetime
        self.group: dict = group
        self.id: str = id
        self.notes: str = notes
        self.priority: float = priority
        self.reminders: list = reminders
        self.tags: list = tags
        self.text: str = text
        self.type: str = type
        self.updatedAt: str = updatedAt #TODO: Convert to datetime
        self.userId: str = userId
        self.value: float = value
    
    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return f"<Habitica TodoTask: {self.text}>"
