"""CPU functionality."""

import sys

# ALU operations

ADD = 0b10100000
MUL = 0b10100010
SUB = 0b10100001
DIV = 0b10100011
MOD = 0b10100100
CMP = 0b10100111
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101

ALU_OP = [ADD, SUB, MUL, DIV, MOD, CMP, AND, NOT, OR, XOR, SHL, SHR]


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # 8 general-purpose registers
        self.reg = [0] * 8
        # PC
        self.pc = 0
        # stack pointer (SP)
        self.sp = 256

        self.flag = self.reg[4]

        # self.mdr = 0
        # Commands
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010000: self.call,
            0b00010001: self.iret,
            0b10100111: self.cmp_function,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b10100000: self.add,
            0b10100010: self.mul,
            0b10100001: self.sub,
            0b10100011: self.div,
            0b10100100: self.mod,
            0b10100111: self.cmp_function,
            0b10101000: self.aluand,
            0b10101010: self.aluor,
            0b10101011: self.aluxor,
            0b01101001: self.alunot,
            0b10101100: self.shl,
            0b10101101: self.shr
        }

    # accepts the address in RAM and returns the value stored there
    def ram_read(self, address):
        return self.ram[address]

    # accepts a value to write, and the address to write it to.
    def ram_write(self, value, address):
        self.ram[address] = value

    # halt the CPU and exit the emulator
    def hlt(self, operand_a, operand_b):
        return (0, False)

    # load immediate, store a value in a register, or set this register to this value
    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        return (3, True)

    # prints the numeric value stored in a register
    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return (2, True)

    # STRETCH GOALS

    def add_i(self, operand_a, operand_b):
        self.reg[operand_a] += operand_b
        return (2, True)

    # ALU ops
    def mul(self, operand_a, operand_b):
        # calling alu function
        self.alu("MUL", operand_a, operand_b)
        return (3, True)

    def add(self, operand_a, operand_b):
        # calling alu function
        self.alu("ADD", operand_a, operand_b)
        return (3, True)

    def sub(self, operand_a, operand_b):
        self.alu("SUB", operand_a, operand_b)
        return (3, True)

    def div(self, operand_a, operand_b):
        self.alu("DIV", operand_a, operand_b)
        return (3, True)

    def aluand(self, operand_a, operand_b):
        self.alu("AND", operand_a, operand_b)
        return (3, True)

    def alunot(self, operand_a, operand_b):
        self.alu("NOT", operand_a, operand_b)
        return (3, True)

    def aluor(self, operand_a, operand_b):
        self.alu("OR", operand_a, operand_b)
        return (3, True)

    def aluxor(self, operand_a, operand_b):
        self.alu("XOR", operand_a, operand_b)
        return (3, True)

    def shl(self, operand_a, operand_b):
        self.alu("SHL", operand_a, operand_b)
        return (3, True)

    def shr(self, operand_a, operand_b):
        self.alu("SHR", operand_a, operand_b)
        return (3, True)

    def mod(self, operand_a, operand_b):
        self.alu("MOD", operand_a, operand_b)
        return (3, True)

    def push(self, operand_a, operand_b):
        # reg_address = self.ram[self.pc + 1]
        self.sp -= 1
        value = self.reg[operand_a]
        self.ram[self.sp] = value
        return (2, True)

    def pop(self, operand_a, operand_b):
        pop_value = self.ram[self.sp]
        reg_address = operand_a
        self.reg[reg_address] = pop_value
        self.sp += 1
        return (2, True)

    def call(self, operand_a, operand_b):
        # push the next program counter on the stack
        next_address = self.pc + 2
        self.reg[2] = next_address
        self.push(2, None)

        # move program counter to the start of first command of the function
        routine_address = self.reg[operand_a]
        # print(operand_a, routine_address)
        self.pc = routine_address

        return (0, True)

    def iret(self, *args):
        self.pop(2, None)
        next_address = self.reg[2]
        self.pc = next_address

        # next_address = self.ram[self.sp]
        # self.sp += 1
        # self.pc = next_address
        return (0, True)

    # SPRINT CHALLENGE
    def cmp_function(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        return (3, True)

    def jmp(self, operand_a, operand_b):
        self.pc = self.reg[operand_a]
        return (0, True)

    def jeq(self, operand_a, operand_b):
        if self.flag == 0b00000001:
            self.pc = self.reg[operand_a]
            return(0, True)
        return (2, True)

    def jne(self, operand_a, operand_b):
        if self.flag != 0b00000001:
            self.pc = self.reg[operand_a]
            return(0, True)
        return (2, True)

    # loading from a file

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(program) as f:
            for line in f:
                comment_split = line.split('#')
                num = comment_split[0].strip()

                if num == '':
                    continue

                try:
                    # print(num)
                    self.ram_write(int(num, 2), address)
                    address += 1
                except ValueError:
                    # print("Value error")
                    pass

        # print("Finished reading the program")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b])
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction_register = self.ram_read(self.pc)
            # print(instruction_register)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # print(instruction_register, operand_a, operand_b)

            try:
                f = self.commands[instruction_register]
                # print(f)
                operation_op = f(operand_a, operand_b)
                running = operation_op[1]
                self.pc += operation_op[0]

            except Exception as e:
                print(f"Error: Instruction {instruction_register} not found!")
                # print(e)
                sys.exit(1)
