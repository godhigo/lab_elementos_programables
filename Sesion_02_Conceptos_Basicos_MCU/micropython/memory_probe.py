import time
time.sleep(0.1)  # Wait for USB to become ready

import os, gc, machine

print(os.uname())
print(machine.freq())
print()

gc.collect()
print('libre inicial:', gc.mem_free())

buffer = bytearray(10000)
print('después de reservar:', gc.mem_free())

del buffer
gc.collect()
print('después de liberar:', gc.mem_free())
