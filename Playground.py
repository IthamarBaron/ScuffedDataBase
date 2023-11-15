import multiprocessing

# Create shared memory for data and a counter
data_memory = multiprocessing.Array('c', b'\x00' * 100)
counter_memory = multiprocessing.Value('i', 0)
print("a")
def test(key):
    # Read the current counter value and update it
    with counter_memory.get_lock():
        counter = counter_memory.value
        counter_memory.value += 1

    # Calculate the start position for the new data
    start_position = counter * len(key)
    # Write the key to the shared memory
    data_memory[start_position:start_position + len(key)] = key.encode('utf-8')
    data = bytearray(data_memory[:]).decode('utf-8').rstrip('\x00')
    print("1Data in shared memory:", repr(data))  # Print the repr to see non-printable characters
if __name__ == "__main__":
    # Start two processes with the test function and different arguments
    p1 = multiprocessing.Process(target=test, args=("one",))
    p2 = multiprocessing.Process(target=test, args=("two",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # Read the data from the shared memory
    data = bytearray(data_memory[:]).decode('utf-8').rstrip('\x00')

    print("2Data in shared memory:", repr(data))  # Print the repr to see non-printable characters
