from lifehub.lib.api import Habitica
from lifehub.lib.api.habitica.models import DailyTask, HabitTask, TodoTask


def get_habits(habitica: Habitica = None) -> list[HabitTask]:
    if habitica is None:
        habitica = Habitica()
    return habitica.get_user_habits()


def get_dailies(habitica: Habitica = None) -> list[DailyTask]:
    if habitica is None:
        habitica = Habitica()
    return habitica.get_user_dailies()


def get_todos(habitica: Habitica = None) -> list[TodoTask]:
    if habitica is None:
        habitica = Habitica()
    return habitica.get_user_todos()


def get_tasks(habitica: Habitica = None) -> dict:
    if habitica is None:
        habitica = Habitica()
    habits = get_habits(habitica)
    dailies = get_dailies(habitica)
    todos = get_todos(habitica)
    return {"habits": habits, "dailies": dailies, "todos": todos}
