import threading

lock = threading.Lock()

print ('First try :' + str(lock.acquire()))
print ('Second try:' + str(lock.acquire(0)))

lock = threading.RLock()

print ('First try :' + str(lock.acquire()))
print ('Second try:' + str(lock.acquire(0)))