;Cameron Beck
;cbb0064
;Beck_Cameron.asm

; This program add and subtracts 32-bit Integers

.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD


.data
    shift DWORD 2
    input BYTE 1,2,3,4,5,6,7,8 
    output BYTE lengthof input dup(?)	
.code
    main proc
									;Place non-shifted values
	mov ECX, lengthof input			;This loop will iterate length - shift times. 
	sub ECX, shift

	mov EBX, 0						;Start reading from 0
	mov EDX, shift					;Start writing from input at shifts
	
    l1:	
		mov AL, [input+EBX]			;Move the value from input into al
		mov [output+EDX], AL		;Move the value from al into output

		inc EBX						;Increment the input index
		inc EDX						;Increment the output index
					
    	loop l1


									;Place shifted values

	mov ECX, shift					;This loop will iterate shift times

	mov EBX, lengthof input
	sub EBX, shift					;Start reading at index length - shift
	mov EDX, 0						;Start writing at index 0.  
				
    l2:	
		mov AL, [input+EBX]			;Move the value from input into al
		mov [output+EDX], AL		;Move the value from al into output

		inc EBX						;Increment the input index
		inc EDX						;Increment the output index

	loop l2

INVOKE ExitProcess,0
main ENDP
END main
