import time

start = time.time()

def delay(ms):
  time.sleep(ms)

def millis():
  end = time.time()
  return end - start