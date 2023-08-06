from datetime import datetime as dt


def timeof(func):
    def wrapper(*args, **kwargs):
        start = dt.now()
        result = func(*args, **kwargs)
        time = dt.now() - start

        print(f'<TIMEOF:{func.__name__}> {time} sec')

        return result

    return wrapper
