import os


def child():
    print('Hello from child', os.getpid(), flush=True)


def parent():
    for i in range(3):
        print(i, flush=True)
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            print('Hello from parent', os.getpid(), newpid, flush=True)


parent()
