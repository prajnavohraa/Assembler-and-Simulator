import sys


var = {}
labels = {}

def floating_to_binary(x):
    global error_list
    global j
    integer=int(x.split(".")[0])
    floating=int(x.split(".")[1])
    binary=str(bin(integer)[2:])+"."
    decimal="0."+str(floating)
    decimal=float(decimal)
    result=""
    i=0;
    checker=True
    while decimal!=0.0:
        decimal=decimal*2
        result+=str(decimal).split(".")[0]
        decimal=float("."+(str(decimal).split(".")[1]))
        i+=1
        if(i>4):
            checker=False
            break
    if(checker==False):
        error_list.append("Error at line "+str(j+1)+": "+"Overflow detected\n")    
    return binary+result+(5-len(result))*"0"

def binary_to_cse(x):
    ans=""
    exponent=len((x.split(".")[0]))-1
    ans=str(bin(exponent)[2:].zfill(3))+(x.split(".")[0][1:]+(x.split(".")[1]))[:5]
    return ans


def decimalbinary(x):
    if (str(x).count(".") == 0):
        return bin(int(x))[2:]
    else:
        ans=""
        exponent=len((x.split(".")[0]))-1
        ans=str(bin(exponent)[2:].zfill(3))+(x.split(".")[0][1:]+(x.split(".")[1]))[:5]
        return ans

############# binary encoding #############
def A(op, reg1, reg2, reg3):
    return op + '00' + '0' * (3 - len(reg1)) + reg1 + reg2 + reg3


def B(op, reg1, Imd):
    return op + reg1 + '0' * (8 - len(Imd)) + Imd


def C(op, reg1, reg2):
    return op + '00000' + reg1 + reg2


def D(op, reg1, mem):
    return op + reg1 + '0' * (8 - len(mem)) + mem


def E(op, mem):
    return op + '000' + '0' * (8 - len(mem)) + mem


def F():
    return '0101000000000000'

############# declaring dictionaries #############
dict_ISA = {"addf": "00000", "subf": "00001", "movf": "00010" ,"add": "10000", "sub": '10001', 'movi': '10010', 'movr': '10011', 'ld': '10100', 'st': '10101', 'mul': '10110', 'div': '10111', 'rs': '11000', 'ls': '11001', 'xor': '11010', 'or': '11011', 'and': '11100', 'not': '11101', 'cmp': '11110', 'jmp': '11111', 'jlt': '01100', 'jgt': '01101', 'je': '01111', 'hlt': '01010'}
Reg = {"R0": '000', "R1": '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}
type_ISA = {"addf": "A", "subf": "A", "movf": "B" ,"add": 'A', "sub": 'A', 'movi': 'B', 'movr': 'C', 'ld': 'D', 'st': 'D', 'mul': 'A', 'div': 'C', 'rs': 'B', 'ls': 'B', 'xor': 'A', 'or': 'A', 'and': 'A', 'not': 'C', 'cmp': 'C', 'jmp': 'E', 'jlt': 'E', 'jgt': 'E', 'je': 'E', 'hlt': 'F', 'var': None}
############# storing output #############
# For storing error lines
error_list = []
# For storing correct lines
lista = []


############# inputting #############
commands = sys.stdin.readlines()
# f = open(
#     "../automatedTesting/tests/assembly/hardBin/{}".format(sys.argv[1]), "r")
# commands = f.readlines()
# f.close()


def convert(j):
    global flag
    global _CommandResults
    global lista, error_list
    global Reg
    global var
    try:
    # for mov imm
    # print(commands[j][0])
    # print((list(commands[j][2][1::])).remove("."))
    #print(commands[j][2][0])

        if (commands[j][0] == 'movf'):
            a = list(commands[j][2][1::])
            a.remove(".")
            a = "".join(a)
        if (commands[j][0] == 'mov' or commands[j][0] == 'movf') and (commands[j][2][1::].isnumeric() == True or (a).isnumeric() == True) and commands[j][2][0] == "$":
            try:
                Reg[commands[j][1]]
            except:
                error_list.append(
                    "Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                flag = 1
            if Reg[commands[j][1]] == "111":
                error_list.append(
                    "Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                flag = 1
            if commands[j][0]!="movf" and flag == 0 and (int(commands[j][2][1::]) > 256 or int(commands[j][2][1::]) < 0):
                error_list.append(
                    "Error at line "+str(j+1)+": Illegal immediate values (more than 8 bits)\n")
                flag = 1
            if(commands[j][0]=="movf"):
                if(flag==0 and float((commands[j][2][1::]))>int('11111100',2) or float((commands[j][2][1::]))<1.0):
                    error_list.append("Error at line "+str(j+1)+": Illegal immediate value for floating integer\n")
                    flag=1
                if flag!=1:
                    lista.append(B(dict_ISA[commands[j][0]], Reg[commands[j][1]], binary_to_cse(floating_to_binary((commands[j][2][1:len(commands[j][2])])))) + "\n")
            if commands[j][0] != "movf" and flag != 1:
                lista.append(B(dict_ISA['movi'], Reg[commands[j][1]], decimalbinary(
                    commands[j][2][1::])) + "\n")
        # For mov reg
        elif commands[j][0] == 'mov':
            try:
                Reg[commands[j][1]]
                Reg[commands[j][2]]
            except:
                error_list.append(
                    "Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                flag = 1
            if Reg[commands[j][2]] == "111":
                error_list.append(
                    "Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                flag = 1
            if flag != 1:
                lista.append(
                    C(dict_ISA["movr"], Reg[commands[j][1]], Reg[commands[j][2]]) + "\n")

        else:
            if commands[j][0] != 'mov' and commands[j][0] != 'hlt' and commands[j][0] != 'var':
                try:
                    dict_ISA[commands[j][0]]
                except:
                    error_list.append(
                        "Error at line "+str(j+1)+": Instruction name error\n")
                    flag = 1

            ######## Type A ########
            if type_ISA[commands[j][0]] == 'A':
                try:
                    Reg[commands[j][1]]
                    Reg[commands[j][2]]
                    Reg[commands[j][3]]
                except:
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                    flag = 1
                if Reg[commands[j][1]] == "111" or Reg[commands[j][2]] == "111" or Reg[commands[j][3]] == "111":
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                    flag = 1
                if flag != 1:
                    lista.append(A(dict_ISA[commands[j][0]], Reg[commands[j][1]],
                                    Reg[commands[j][2]], Reg[commands[j][3]]) + "\n")
            ######## Type B ########
            if type_ISA[commands[j][0]] == 'B':
                try:
                    Reg[commands[j][1]]
                except:
                    error_list.append(
                        "Error at line "+str(j+1)+": Instruction name or register name error\n")
                    flag = 1

                if flag == 0 and (int(commands[j][2][1::]) > 256 or int(commands[j][2][1::]) < 0):
                    error_list.append(
                        "Error at line "+str(j+1)+": Illegal immediate values (more than 8 bits)\n")
                    flag = 1
                if Reg[commands[j][1]] == "111":
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                    flag = 1
                if flag != 1:
                    lista.append(B(dict_ISA[commands[j][0]], Reg[commands[j][1]], decimalbinary(
                        commands[j][2][1:len(commands[j][2])])) + "\n")
            ######## Type C ########
            elif type_ISA[commands[j][0]] == 'C':
                try:
                    Reg[commands[j][1]]
                    Reg[commands[j][2]]
                except:
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                    flag = 1
                if Reg[commands[j][1]] == "111" or Reg[commands[j][2]] == "111":
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Illeagal use of Flags register\n")
                    flag = 1
                if flag != 1:
                    lista.append(
                        C(dict_ISA[commands[j][0]], Reg[commands[j][1]], Reg[commands[j][2]]) + "\n")
            ######## Type D ########
            elif type_ISA[commands[j][0]] == 'D':
                try:
                    Reg[commands[j][1]]
                except:
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Instruction name or register name error\n")
                    flag = 1
                if Reg[commands[j][1]] == "111":
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Illegal use of Flags register\n")
                    flag = 1
                choice = False
                for i in range(len(commands)-1):
                    if commands[i][1] == commands[j][2]:
                        choice = True
                        break
                    elif commands[i][0][:-1] == commands[j][2]:
                        choice = "labelused"
                        break
                if choice == False:
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Use of undefined variable(s)\n")
                elif choice == "labelused":
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Misuse of label as variable\n")
                if i >= var_start:
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Variable not declared at the beginning\n")
                    flag = 1
                if flag != 1 and choice == True:
                    lista.append(D(dict_ISA[commands[j][0]], Reg[commands[j][1]], decimalbinary(
                        len(commands) + var[commands[j][2]] - len(var))) + "\n")

            ######## Type E ########
            elif type_ISA[commands[j][0]] == 'E':
                choice = False
                if commands[j][1] in labels:
                    choice = True
                elif commands[j][1] in var:
                    choice = "variableused"
                if choice == False:
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Use of undefined label(s)\n")
                    flag = 1
                elif choice == "variableused":
                    error_list.append(
                        "Error at line "+str(j+1)+": "+"Misuse of variable as label\n")
                    flag = 1
                if flag != 1 and choice == True:
                    # if i == 0:
                    lista.append(E(dict_ISA[commands[j][0]], decimalbinary(labels[commands[j][1]] - len(var))) + "\n")
                    # else:
                    #     lista.append(
                    #         E(dict_ISA[commands[j][0]], decimalbinary(str(i) - 1)) + "\n")

            ######## Type F ########
            elif type_ISA[commands[j][0]] == 'F':
                lista.append(F() + "\n")
            
            elif type_ISA[commands[j][0]] == None:
                if commands[j][1] in Reg.keys():
                    error_list.append("Register used instead of variable name at " + str(j + 1) + "\n")

    # For Non-standard error handling
    except:
        if flag == 0:
            error_list.append("Syntax error in line " + str(j + 1) + "\n")


# ERROR HANDLING
# with open("Testcase.txt") as text:

# with open("test.txt", "r") as f:
# commands = f.readlines()

# commands = []
# while True:
#     inp = sys.stdin.readlines()
#     commands.append(inp)
#     if inp == 'hlt':
#         break

# hlt print prob
commands[-1] = commands[-1] + "\n"

number = 0
for i in range(len(commands)):
    commands[i] = commands[i][0:(len(commands[i]) - 1)].split()
    try:
        if commands[i][0] == 'var':
            number += 1
    except:
        pass
try:
    # removing empty lines
    while True:
        commands.remove([])
except:
    pass

# finding where the last variable ends
for k in range(len(commands)):
    if commands[k][0] != "var":
        break
var_start = k + 1
newlist = commands.copy()       # For comparing labels

# adding variables to dict
for i in range(len(commands)):
    try:
        if commands[i][0] == 'var':
            var[commands[i][1]] = i
        elif(commands[i][0][-1] == ":"):
            labels[commands[i][0][0:-1]] = i
    except:
        error_list.append('variable not declared')


########################## Main Code ##########################
for j in range(len(commands)):
    commands = newlist.copy()
    flag = 0

    # if label in not present in the line
    if(commands[j][0].find(':') != len(commands[j][0])-1):
        convert(j)

    # if label is present in the code
    else:
        commands[j] = commands[j][1:]

        convert(j)


######### Printing and missing hlt #########
check = False
for k in range(len(commands)):
    if len(commands[k]) > 0 and commands[k][0] == 'hlt':
        check = True
        break
if check == False:
    error_list.append("Missing Halt instruction\n")
if commands[-1][0] != 'hlt' or k != (len(commands) - 1):
    error_list.append("Halt not being used as last instruction\n")

for i in commands:
    if (i[0][-1] == ":"):
        i = i[1:]
hlt_no = 0
for i in commands:
    if i[0] == "hlt":
        hlt_no += 1
if (len(error_list) == 0 or error_list[-1] != "Missing Halt instruction\n") and hlt_no > 1:
    error_list.append("Missing Halt instruction\n")
f = open("out.txt", "w")
lista[-1] = lista[-1][0:len(lista[-1]) - 1]
if (len(error_list) == 0):
    for i in lista:
        f.write(i)
        print(i, end="")
else:
    for i in error_list:
        f.write(i)
        print(i, end="")
