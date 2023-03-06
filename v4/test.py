
# SuperFastPython.com
# example of returning a value from a thread
import time
from time import sleep
from threading import Thread
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Manager
from numba import njit

@njit(fastmath=True)
def accelerate_factorial(nb):
    res = 1
    # while (nb > 0):
    #     res *= nb
    #     nb -= 1
    i = 10000
    while (i > 0):
        i -= 1
    return res


def factorial(nb):
    res = 1
    # while (nb > 0):
    #     res *= nb
    #     nb -= 1
    i = 10000
    while (i > 0):
        i -= 1
    return res

# custom thread
class CustomThread(Thread):
    # constructor
    def __init__(self, start_nb, range_nb):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.start_nb = start_nb
        self.range_nb = range_nb
        self.res = []
        for i in range(self.range_nb):
            self.res.append(0)

    def run(self):
        for i in range(self.range_nb):
            self.res[i] = factorial(i + self.start_nb)


class CustomThread_accelerate(Thread):
    # constructor
    def __init__(self, start_nb, range_nb):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.start_nb = start_nb
        self.range_nb = range_nb
        self.res = []
        for i in range(self.range_nb):
            self.res.append(0)

    def run(self):
        for i in range(self.range_nb):
            self.res[i] = accelerate_factorial(i + self.start_nb)


def vProcessFunction(lst_result, start_nb, nb_value, i):
    """Function to do CPU-bound work.
    Args:
    Returns:
    """
    rep = []
    for i in range(nb_value):
        rep.append((i, factorial(i + start_nb)))

    lst_result.append(rep)


def vProcessFunction_accelerate(lst_result, start_nb, nb_value, i):
    """Function to do CPU-bound work.
    Args:
    Returns:
    """
    rep = []
    for i in range(nb_value):
        rep.append((i, accelerate_factorial(i + start_nb)))

    lst_result.append(rep)


max_value = 5000

fTimePrefCountStart = time.perf_counter()
for i in range(max_value):
    res = factorial(i)
fTimePrefCountEnd = time.perf_counter()
print(f"Single threading time ", fTimePrefCountEnd - fTimePrefCountStart)


fTimePrefCountStart = time.perf_counter()
for i in range(max_value):
    res = accelerate_factorial(i)
fTimePrefCountEnd = time.perf_counter()
print(f"Single threading compiling time ", fTimePrefCountEnd - fTimePrefCountStart)
print()




fTimePrefCountStart = time.perf_counter()

nb_thread = 8
value_per_thread = max_value // nb_thread
threads = []

for i in range(nb_thread):
    thread = CustomThread(i, value_per_thread)
    threads.append(thread)
    threads[i].start()

for i in range(nb_thread):
    threads[i].join()
    res = threads[i].res

fTimePrefCountEnd = time.perf_counter()
print(f"Multi threading time ", fTimePrefCountEnd - fTimePrefCountStart)



fTimePrefCountStart = time.perf_counter()

nb_thread = 8
value_per_thread = max_value // nb_thread
threads = []

for i in range(nb_thread):
    thread = CustomThread_accelerate(i, value_per_thread)
    threads.append(thread)
    threads[i].start()

for i in range(nb_thread):
    threads[i].join()
    res = threads[i].res

fTimePrefCountEnd = time.perf_counter()
print(f"Multi threading compiling time ", fTimePrefCountEnd - fTimePrefCountStart)
print()





fTimePrefCountStart = time.perf_counter()

executor = ProcessPoolExecutor(max_workers=8)
nbs = range(max_value)

for result in executor.map(factorial, nbs):
    # print(result)
    pass

fTimePrefCountEnd = time.perf_counter()
print(f"Pool process time ", fTimePrefCountEnd - fTimePrefCountStart)



fTimePrefCountStart = time.perf_counter()

executor = ProcessPoolExecutor(max_workers=8)
nbs = range(max_value)

for result in executor.map(accelerate_factorial, nbs):
    # print(result)
    pass

fTimePrefCountEnd = time.perf_counter()
print(f"Pool process compiling time ", fTimePrefCountEnd - fTimePrefCountStart)
print()





fTimePrefCountStart = time.perf_counter()

manager = Manager()

lstProcesses = []
lst_result = manager.list()

nb_process = 8
value_per_process = max_value // nb_process

for i in range(nb_process):
    lstProcesses.append(Process(target=vProcessFunction, args=(lst_result, i * value_per_process, value_per_process, i)))

# Start all the processes
for objProcess in lstProcesses:
    objProcess.start()

# # Wait for all processes to complete
for objProcess in lstProcesses:
    objProcess.join()

fTimePrefCountEnd = time.perf_counter()
print(f"Multi process time ", fTimePrefCountEnd - fTimePrefCountStart)



fTimePrefCountStart = time.perf_counter()

manager = Manager()

lstProcesses = []
lst_result = manager.list()

nb_process = 8
value_per_process = max_value // nb_process

for i in range(nb_process):
    lstProcesses.append(Process(target=vProcessFunction_accelerate, args=(lst_result, i * value_per_process, value_per_process, i)))

# Start all the processes
for objProcess in lstProcesses:
    objProcess.start()

# # Wait for all processes to complete
for objProcess in lstProcesses:
    objProcess.join()

fTimePrefCountEnd = time.perf_counter()
print(f"Multi process compiling time ", fTimePrefCountEnd - fTimePrefCountStart)
