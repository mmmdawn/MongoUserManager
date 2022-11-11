def endless_function(function):
    def wrapper(self):
        while True:
            next_loop = function(self)
            if next_loop:
                continue
            else:
                return

    return wrapper
