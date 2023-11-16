import multiprocessing
from multiprocessing import shared_memory
import  time


def save_memory(value):
    shm = shared_memory.SharedMemory(name='test', create=False, size=4)
    print(f"in shared memory a: {type(value)}")
    i = shm.buf[0]
    # Convert bytes to memoryview before assignment
    value_memoryview = memoryview(value)
    shm.buf[i:(i + len(value_memoryview))] = value_memoryview
    print(f"Starting at [{i} : {i+len(value_memoryview)}] list is: {shm.buf.tolist()}")
    shm.buf[0] = i + len(value_memoryview)

if __name__ == '__main__':
    print("created shared memory")
    shm = shared_memory.SharedMemory(name='test', create=True, size=4)
    shm.buf[0] = 1
    p = multiprocessing.Process(target=save_memory, args=(b"a",))
    p2 = multiprocessing.Process(target=save_memory, args=(b"b",))

    p.start()
    p2.start()
    p.join()
    p2.join()
    print(shm.buf.tolist())

