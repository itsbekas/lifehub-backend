from pydantic import BaseModel

from lifehub.lib.api.habitica.models import DailyTask, HabitTask, TodoTask


class Habit(BaseModel):
    id: str
    text: str

    @classmethod
    def from_obj(cls, task: HabitTask):
        return cls(id=task.id, text=task.text)


class Daily(BaseModel):
    id: str
    text: str

    @classmethod
    def from_obj(cls, task: DailyTask):
        return cls(id=task.id, text=task.text)


class Todo(BaseModel):
    id: str
    text: str

    @classmethod
    def from_obj(cls, task: TodoTask):
        return cls(id=task.id, text=task.text)


class Tasks(BaseModel):
    habits: list[Habit]
    dailies: list[Daily]
    todos: list[Todo]

    @classmethod
    def from_obj(
        cls, habits: list[HabitTask], dailies: list[DailyTask], todos: list[TodoTask]
    ):
        habits = [Habit.from_obj(h) for h in habits]
        dailies = [Daily.from_obj(d) for d in dailies]
        todos = [Todo.from_obj(t) for t in todos]
        return cls(habits=habits, dailies=dailies, todos=todos)
