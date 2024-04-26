.386
.model flat, stdcall
.stack 4096
ExitProcess proto, dwExitCode:dword

.data
		input BYTE 1,2,3,4,5,6,7,8
		shift BYTE 2
.code
		main proc
			; clear up the registers to make sure there is no old values inside them
			mov eax,0               ; clear up EAX                       
			mov ebx,0				; clear up EBX
			mov ecx,0               ; clear up ECX
			mov edx,0               ; clear up EDX

			; setup EAX register with 1st and 2nd values from the input array
			mov ah,[input+0]                       ; add 1st value from input into register
			add ah,shift						   ; shift the value inside the register
			mov al,[input+1]	                   ; add 2nd value from input into register
			add al,shift						   ; shift the value inside the register
				
			; setup EBX register with 3rd and 4th values from the input array
			mov bh,[input+2]                       ; add 3rd value from input into register
			add bh,shift                           ; shift the value inside the register
			mov bl,[input+3]                       ; add 4th value from input into register
			add bl,shift                           ; shift the value inside the register

			; setup ECX register with 5th and 6th values from the input array
			mov ch,[input+4]                       ; add 5th value from input into register
			add ch,shift                           ; shift the value inside the register
			mov cl,[input+5]                       ; add 6th value from input into register
			add cl,shift                           ; shift the value inside the register

			; setup EDX register with 7th and 8th values from the input array
			mov dh,[input+6]                       ; add 7th value from input into register
			add dh,shift                           ; shift the value inside the register
            mov dl,[input+7]                       ; add 8th value from input into register
			add dl,shift                           ; shift the value inside the register

			; exit the program
			invoke ExitProcess, 0
		main endp
end main