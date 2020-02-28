"""CPU functionality."""

import sys

print(sys.argv)

# `HLT` instruction handler
HLT = 1
# `LDI` instruction handler
LDI = 130
# `PRN` instruction handler
PRN = 71
# MUL
MUL = 162
# PUSH
PUSH = 69
# POP
POP = 70
# SP
SP = 7
# CALL
CALL = 80
# RET
RET = 17
# ADD
ADD = 160
# CMP
CMP = 167
# JMP
JMP = 84
# JEQ
JEQ = 85
# JNE
JNE = 86

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add list properties to the `CPU` class to hold 256 bytes of memory and 8
        # general-purpose registers.

        # > Hint: you can make a list of a certain number of zeros with this syntax:
        # >
        # > ```python
        # > x = [0] * 25  # x is a list of 25 zeroes
        # > ```

        # Also add properties for any internal registers you need, e.g. `PC`.

        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.less = 0
        self.greater = 0
        self.equal = 0


    # Un-hardcode the machine code
    def load(self):
        """Load a program into memory."""
        # Implement the `load()` function to load an `.ls8` file given the filename passed in as an argument
        try:
            filename = sys.argv[1]
            address = 0
            # Use those command line arguments to open a file
            with open(filename) as f:
                # Read in its contents line by line
                for line in f:
                    # Remove any comments
                    line = line.split("#")[0]
                    # Remove whitespace
                    line = line.strip()
                    # Skip empty lines
                    if line == "":
                        continue

                    value = int(line, 2)
                    
                    # Set the instruction to memory
                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

        # for instruction in filename:
        #     self.ram[address] = instruction
        #     address += 1

    # Add RAM functions `ram_read()` and `ram_write()`

    # > Inside the CPU, there are two internal registers used for memory operations:
    # > the _Memory Address Register_ (MAR) and the _Memory Data Register_ (MDR). The
    # > MAR contains the address that is being read or written to. The MDR contains
    # > the data that was read or the data to write. You don't need to add the MAR or
    # > MDR to your `CPU` class, but they would make handy paramter names for
    # > `ram_read()` and `ram_write()`

    # `ram_read()` should accept the address to read and return the value stored
    # there.
    def ram_read(self, MAR):
        return self.ram[MAR]

    # `ram_write()` should accept a value to write, and the address to write it to.
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL": # Multiply
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP": # Compare
            if self.reg[reg_a] < self.reg[reg_b]:
                self.less = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.greater = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.equal = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Implement the core of `CPU`'s `run()` method
        self.load()
        # Needs to read the memory address that's stored in register `PC`, and store
        # that result in `IR`, the _Instruction Register_.
        # `IR`, contains a copy of the currently executing instruction
        while True:
            IR = self.ram[self.pc]
            operand_c = IR >> 6
            sets_pc = IR >> 4 & 0b0001
            # LDI
            if IR == LDI:
                # Read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and `operand_b`
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                # store the data
                self.reg[operand_a] = operand_b
                # increment the PC by 3 to skip the arguments
                # self.pc += 3
            # PRN
            elif IR == PRN:
                data = self.ram[self.pc + 1]
                # print
                print(self.reg[data])
                # increment the PC by 2 to skip the argument
                # self.pc += 2
            # MUL
            elif IR == MUL:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.reg[reg_a] *= self.reg[reg_b]
            # ADD
            elif IR == ADD:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.reg[reg_a] += self.reg[reg_b]  
            # PUSH
            elif IR == PUSH:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = val
                # self.pc += 2
            # POP
            elif IR == POP:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[SP]]
                self.reg[reg] = val
                self.reg[SP] += 1
                # self.pc += 2
            # CALL
            elif IR == CALL:
                # register is self.reg
                self.reg[SP] -= 1
                # memory is self.ram
                self.ram[self.reg[SP]] = self.pc + 2
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[reg]
            # RET 
            elif IR == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1
            # HLT
            elif IR == HLT:
                sys.exit(0)
            # else, print did not understand
            else:
                print(f"Error, I did not understand that command: {IR}")
                sys.exit(1)
            if sets_pc == 0:
                self.pc += operand_c + 1
