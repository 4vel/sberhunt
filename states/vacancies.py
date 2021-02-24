from aiogram.dispatcher.filters.state import StatesGroup, State


def previous_current_next(iterable):
    """Создает итератор который выдает таплы (предыдущий, текущий, следующий)

    Если нет значения, то значения предыдущего или следующего, то возвращает None

    """
    iterable = iter(iterable)
    prv = None
    cur = next(iterable)
    try:
        while True:
            nxt = next(iterable)
            yield prv, cur, nxt
            prv = cur
            cur = nxt
    except StopIteration:
        yield prv, cur, None

class Vacancies(StatesGroup):

    def __init__(self):
        self.lvacs = None

    def get_list_of_tups(self, iterable):
        if iterable:
            self.lvacs = previous_current_next(iterable)

    Q1paginfo = State()
    Q2paginfo = State()


class VacNavigator:

    def __init__(self, vactuple):
        self.current_id = vactuple[1]
        self.previous_id = vactuple[0]
        self.next_id = vactuple[2]
