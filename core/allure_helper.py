def print_args(function):
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper
