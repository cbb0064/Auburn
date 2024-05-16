# Overview
This directory is dedicated to the term project for my Secure Software Process class that focused on the exploitation and prevention of threats and vulnerabilities. In here you will find two different types of files. ELF 32-bit LSB executables (toystacks) and python scripts that exploit a buffer overflow. The goal of this project was to override return for each executable to instead point to a hidden win function which printed some flag. In order to run these files, we needed to scp them into the virtual desktop on a website designated for our project, and execute them inside a specific directory with a hidden source file. The tools used for crafting the exploit were pwntools, pwndbg, and gdb.

# Executables
## Toystack1
This was a basic 32-bit executable without PIE or ASLR. The associated python file is test1.py
## Toystack2
This was another 32-bit executable but with PIE enabled. This made it so the first two bits for each address were scrambled randomly making it so we could not hardcode to the win address using the same manner we did for toystack1
## Toystack3 
This was similar to toystack2 however even after adjusting for PIE we were not able to hardcode the win function the same and instead found the flag in an instruction further down.

# Exploits
These exploits followed a specific template. We noticed that the binary called for a user input in which we could exploit the stack through a buffer overflow. The commented out section showed one way to launch gdb however I found it more effective to launch the process and then pause, copy the PID into another window where i was running gdb and work from there. From here I used cyclic to generate some string that caused a crash at some address. Pwndbg showed me a 4 character strong that was stored in the EIP instruction which is what I needed to use to find the return address. From here, using cyclic -l "<string>" gave me the offset which was how long my buffer overflow needed to be. From here, I used dissasemble to find the address on the win function and hardcoded the file to print that address at the end of the overflow. 
## test1.py
Overflowed from user input to return and then inserted the win memory address using p32.
## test2.py
Because PIE was enabled the first two bits were always scrambmled. Instead, we used p16 to inser tonly the last 2 bytes of the win function which always remaiend the same
## test3.py
Same as test2.py however we could not call to the beginning of the function to get our flag and had to steap through each instruction to find which gave us the flag.
