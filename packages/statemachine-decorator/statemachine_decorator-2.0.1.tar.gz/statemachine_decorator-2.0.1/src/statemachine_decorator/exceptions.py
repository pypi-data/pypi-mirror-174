class ReadonlyStatesException(Exception):
    """
    This exception will be raised when you try to write any state's value on a stateDefined class
    """
    def __init__(self, cls=None, state=''):
        """
        :param cls: the stateful class
        :param state: the state try to write
        """
        self.cls = cls
        self.state = state
    def __str__(self):
        return f'State {repr(self.state)} on {self.cls.__name__ if self.cls else "the class"} is only readable! All states: {self.cls.states}'

class UnswitchableStateException(ValueError):
    def __init__(self, cls, state='', current=None, allowed={''}):
        self.cls = cls
        self.current = current
        self.state = state
        self.allowed = allowed

    def __str__(self):
        return f'State {repr(self.state)} on {self.cls.__name__ if self.cls else "the class"} is not switchable! {f"Current state is {repr(self.current)}"  if self.current is not None else "No current state yet"}. You can switch to: {self.allowed}'

class EntryStateException(ValueError):
    def __init__(self, cls, err_entry_state=''):
        self.cls = cls
        self.err_entry_state = err_entry_state

    def __str__(self):
        return f'No such state {repr(self.err_entry_state)} to entry on {repr(cls.__name__)}! Allow states allowed is {cls.states}'

class NoStateException(Exception):
    def __init__(self, instance):
        self.instance = instance
    def __str__(self):
        return f"Please switch to any state in {self.instance.states} first, and then you can get {self.instance}'s state."

__all__ = ['ReadonlyStatesException', 'UnswitchableStateException', "EntryStateException", "NoStateException"]