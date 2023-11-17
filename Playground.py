import multiprocessing
from multiprocessing import shared_memory

def save_memory(value):
    shm = shared_memory.SharedMemory(name='test', create=False, size=100)
    i = shm.buf[0]
    value_memoryview = memoryview(value)
    separator = memoryview(b'#')
    shm.buf[i:i + len(value_memoryview)] = value_memoryview
    i += len(value_memoryview)
    shm.buf[i:i + len(separator)] = separator
    i += len(separator)
    shm.buf[0] = i

if __name__ == '__main__':
    print("created shared memory")
    shm = shared_memory.SharedMemory(name='test', create=True, size=100)
    shm.buf[0] = 1
    p = multiprocessing.Process(target=save_memory, args=(b"ONE",))
    p2 = multiprocessing.Process(target=save_memory, args=(b"TWO",))

    p.start()
    p2.start()
    p.join()
    p2.join()
    filtered_list = [x for x in shm.buf.tolist() if x != 0]
    decoded_string = ''.join(chr(code) for code in filtered_list[1::])

    print(filtered_list)
    print(decoded_string)

