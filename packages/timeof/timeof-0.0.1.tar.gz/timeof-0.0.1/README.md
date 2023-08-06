# TIMEOF
**timeof** - is a decorator, that helps you to measure time of function execution in a simple way.

## Usage

```
from timeof import timeof
from time import sleep


@timeof
def some_function():
    sleep(5)


if __name__ == "__main__":
    some_function()
```
output:
```
<TIMEOF:some_function> 0:00:05.007668 sec
```
