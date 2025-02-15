# Harshul

from mapping import *
label_dict = {}

# Prabhav Singhal

# sign extension functions -->
def sign_ext_RISB(n):
    num=(n&((1<<12)-1))
    binary=bin(num)[2:]
    binary_string=binary.zfill(12)
    return binary_string

def sign_ext_J(n):
    num=(n&((1<<21)-1))
    binary=bin(num)[2:]
    binary_string=binary.zfill(21)
    return binary_string

def sign_ext_U(n):
    num=(n&((1<<20)-1))
    binary=bin(num)[2:]
    binary_string=binary.zfill(20)
    return binary_string

def sign_ext_B(n):
    num=(n&((1<<13)-1))
    binary=bin(num)[2:]
    binary_string=binary.zfill(13)
    return binary_string

# type instruction -->
def s_type(register):
    register[1],temp=register[1].split('(')
    z=sign_ext_RISB(int(register[1]))
    temp=temp[:-1]
    register.append(temp)
    funct3,opcode= instructionS['sw']
    return (z[:7]+registers[register[0]]+registers[register[2]]+funct3+z[7:12]+opcode)

def j_type(register):
    z=sign_ext_J(int(register[1]))
    opcode= instructionJ['jal']
    return (z[0]+z[10:20]+z[9]+z[1:9]+registers[register[0]+opcode])

# Darshan Bothra

def r_type(register: list[str], instruction: str)->str:
    f3 = instructionR[instruction][1]
    f7 = instructionR[instruction][0]
    opcode = instructionR[instruction][2]
    rd, rs1, rs2 = [registers[x] for x in register]
    instr_32_bit = f7+rs2+rs1+f3+rd+opcode
    return instr_32_bit

def i_type(register: list[str], instruction: str)->str:

    f3, opcode = instructionI[instruction]
    register[1], temp = register[1].split('(')
    z = sign_ext_RISB(int(register[1]))
    temp = temp[:-1]
    register.append(temp)
    rd, rs1 = registers[register[0]], registers[register[2]]
    imm = z
    instr_32_bit = imm + rs1 + f3 + rd + opcode
    return instr_32_bit

def b_type(register: list[str], instruction: str)->str:
    # beq rs1,rs2,imm
    f3, opcode = instructionB[instruction]
    rs1, rs2 = registers[register[0]], registers[register[1]]
    if register[2] not in label_dict:
        imm = sign_ext_B(int(register[2]))
        instruct_32_bit = imm[0] + imm[2:8] + rs2 + rs1 + f3 + imm[8:12] + imm[1] + opcode
    else:
        imm = sign_ext_B((count-int(label_dict[register[2]]))*4)
        instruct_32_bit = imm[0] + imm[2:8] + rs2 + rs1 + f3 + imm[8:12] + imm[1] + opcode

    return instruct_32_bit

def bonustype(register: list[str], instruction: str)->str:
    if instruction == "mul":
        rd, rs1, rs2 = [registers[x] for x in register]
        instruct_32_bit = "0"*7 + rs2 + rs1 + "0"*7 + rd + "0"*7
    elif instruction == "rvrs":
        rd, rs1 = [registers[x] for x in register]
        instruct_32_bit = "0"*12 + rs1 + "0"*3 + rd + "0"*7
    else:
        instruct_32_bit = "0"*32
    return instruct_32_bit

# Garv Ahuja
file_name = "testcase.txt"
with open("testcase.txt", "r") as f:
    lines = f.readlines()

global count
count = 0
for line in lines:
    line = line.strip()
    particular_line = line.split()

    if ":" in particular_line[0]:
        label = particular_line[0][:-1]

        if len(particular_line) > 1:
            instruction = particular_line[1]
        else:
            instruction = None

        if len(particular_line) > 2:
            register = particular_line[2]
            registerlist = register.split(",")
        else:
            register = None

        label_dict[label] = count

    else:
        instruction = particular_line[0]

        if len(particular_line) > 1:
            register = particular_line[1]
            registerlist = register.split()
        else:
            register = None
        count += 1
    if instruction == None or register == None:
        print("Error!!")

    if instruction in instructionR:
        print(r_type(registerlist, instruction))
    elif instruction in instructionI:
        print(i_type(registerlist, instruction))
    elif instruction in instructionS:
        print(s_type(registerlist))
    elif instruction in instructionB:
        print(b_type(registerlist, instruction))
    elif instruction in instructionJ:
        print(j_type(registerlist))
    elif instruction in instructionbonus:
        print(bonustype(registerlist, instruction))
    else:
        print("Error!!")