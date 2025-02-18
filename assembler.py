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

    opcode= instructionJ['jal']
    try:
        z=sign_ext_J(int(register[1]))
    except:
        if register[1] in label_dict:
            if (list(label_dict.items())[0][0] == register[1]):
                z = sign_ext_J((label_dict[register[1]]-count+1)*4)
            else:
                z = sign_ext_J((label_dict[register[1]] - count) * 4)

    return (z[0]+z[10:20]+z[9]+z[1:9]+registers[register[0]]+opcode)

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
    if instruction == "lw":
        register[1], temp = register[1].split('(')
        z = sign_ext_RISB(int(register[1]))
        temp = temp[:-1]
        register.append(temp)
        rd, rs1 = registers[register[0]], registers[register[2]]
        imm = z
    else:
        rd, rs1 = registers[register[0]], registers[register[1]]
        imm = sign_ext_RISB(int(register[2]))
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
        imm = sign_ext_B((int(label_dict[register[2]])-count)*4)
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
def main(filename):
    output = []
    file_name = filename
    with open(f"{filename}.txt", "r") as f:
        lines = f.readlines()

    global count
    count = 1
    ct = 0
    for line in lines:
        if ':' in str(line):
            line = line.strip()
            label, instruct, reg = line.split(" ")

            for key, value in label_dict.items():
                if value == count:
                    ct+=1
            if ct!= 0:
                count += 1
            label_dict[label[:-1]] = count
        else:
            count -= ct
            ct = 0
            count += 1
    print(label_dict)
    # if label_dict:
        # print(label_dict[list(label_dict.items())[0][0]])
        # label_dict[list(label_dict.items())[0][0]] = label_dict[list(label_dict.items())[0][0]]-1
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
                registerlist = register.split(',')
            else:
                register = None
            count += 1
        if instruction == None or register == None:
            print("Error!!")
        elif instruction in instructionR:
            res = r_type(registerlist, instruction)
        elif instruction in instructionI:
            res = i_type(registerlist, instruction)
        elif instruction in instructionS:
            res = s_type(registerlist)
        elif instruction in instructionB:
            res = b_type(registerlist, instruction)
        elif instruction in instructionJ:
            res = j_type(registerlist)
        elif instruction in instructionbonus:
            res = bonustype(registerlist, instruction)

        else:
            res = "Error"
        print(res)
        output.append(res)

    with open("answer.txt", "w") as f:
        for item in output:
            f.write(item+"\n")


# 11111110100001001101000011100011 # Solution
# 11111110100001001101010011100011 # Result

# 0 0 0 0 0 0 0 0 1 0 0 0
