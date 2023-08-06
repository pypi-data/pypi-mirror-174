# Time It!

`pip install time-it` to install

- Python Decorator for timing functions. Its fast, and fun!

```python
from time_it import time_def

@time_def
def time_max(A):
  return max(A)
  
time_max([1,4,2,5,3,3]) # prints execution time of time_max function and returns max value
```

# With a logger

```python
# setup logger
logger = logging.getLogger("gen")
logger.setLevel(logging.DEBUG)
stdh = logging.StreamHandler(sys.stdout)
stdh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdh.setFormatter(formatter)
logger.addHandler(stdh)

# add decorator to function
@time_def(log_name="gen")
def time_with_log(A):
    return max(A)

time_with_log([1,4,2,5,3,3]) 
```
