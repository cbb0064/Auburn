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
