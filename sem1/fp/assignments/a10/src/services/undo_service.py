class UndoException(Exception):
    pass

class FunctionCall:
    def __init__(self, function_name, *function_params):
        self._function_name = function_name
        self._function_params = function_params

    def call(self):
        self._function_name(*self._function_params)



class Operation:
    def __init__(self, undo_command: FunctionCall, redo_command: FunctionCall):
        self._undo = undo_command
        self._redo = redo_command

    def undo(self):
        self._undo.call()

    def redo(self):
        self._redo.call()


class UndoService:
    def __init__(self):
        self.__history = []
        self.__index = 0

    def undo(self):
        if self.__index <= 0:
            raise UndoException("Nothing to undo")
        self.__index -= 1
        self.__history[self.__index].undo()

    def redo(self):
        if self.__index >= len(self.__history):
            raise UndoException("Nothing to redo")
        self.__history[self.__index].redo()
        self.__index += 1

    def record(self, operation: Operation):
        if self.__index < len(self.__history):
            self.__history = self.__history[:self.__index]
        self.__history.append(operation)
        self.__index = len(self.__history)

    def can_undo(self):
        return self.__index > 0

    def can_redo(self):
        return self.__index < len(self.__history)