import time
import random

def get_filename():
    try:
        filename = "result_{}_{}.png".format(int(time.time()), random.randint(1,100))
        return filename
    except Exception as ex:
        print('ex: ', ex)

#print(get_filename())