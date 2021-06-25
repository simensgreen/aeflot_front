class Command:
    def do(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

    def __str__(self):
        return f"""{self.__class__.__name__}({", ".join(f'{key}: {value}' for key, value in vars(self).items())})"""
