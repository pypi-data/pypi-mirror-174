from time_it import time_def

@time_def # without logger
def time_max(A):
  return max(A)

print(time_max([1,4,2,5,3,3])) # prints execution time of time_max function and returns max value


# with logger
import logging
import sys
logger = logging.getLogger("gen")
logger.setLevel(logging.DEBUG)
stdh = logging.StreamHandler(sys.stdout)
stdh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdh.setFormatter(formatter)
logger.addHandler(stdh)

@time_def(log_name="gen")
def time_with_log(A):
    return max(A)

time_with_log([1,4,2,5,3,3]) 
