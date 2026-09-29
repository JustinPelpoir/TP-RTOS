from time import sleep, time


relative_time = 0.0

def thread1():
    sleep(2)  # Simulate some work being done
    return "Thread 1 is running"

def thread2():
    sleep(3)  # Simulate some work being done
    return "Thread 2 is running"

def thread3():
    
    sleep(5)  # Simulate some work being done
    return "Thread 3 is running"


def checkup():



def main():
    originel_time = time()
    print(thread1())
    print(thread2())
    print(thread3())

main()
