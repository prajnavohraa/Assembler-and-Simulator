import string
import sys
from glob import glob
import opcode
from matplotlib.axis import YAxis
import matplotlib.pyplot as plt
import numpy as np


def binary_to_float(s):
    t = s.split('.')
    return int(t[0], 2) + int(t[1], 2) / 2.**len(t[1])

def floating_to_binary(x):
    integer=int(x.split(".")[0])
    floating=int(x.split(".")[1])
    binary=str(bin(integer)[2:])+"."
    decimal="0."+str(floating)
    decimal=float(decimal)
    result=""
    for i in range(5):
        decimal=decimal*2
        result+=str(decimal).split(".")[0]
        decimal=float("."+(str(decimal).split(".")[1]))
    return binary+result


def binary_to_cse(x):
    ans=""
    exponent=len((x.split(".")[0]))-1
    ans=str(bin(exponent)[2:].zfill(3))+(x.split(".")[0][1:]+(x.split(".")[1]))[:5]
    return ans

def cse_to_binary(x):
    exponent=int(x[:3],2)
    return "1"+x[3:][:exponent]+"."+x[3:][exponent:]
    

regs_val=[]
for i in range(7):
    regs_val.append(0)
flag=[0,0,0,0]
regs_val.append(flag)

halt=False
def print_regs(y):
    print(bin(y)[2:].zfill(8), end=" ")
    for i in regs_val[0:7]:
        if type(i)!=int:
            print(8*"0"+binary_to_cse(floating_to_binary(str(i))),end=" ")
        else:
            print (bin(i)[2:].zfill(16), end=" ")
    x=""
    for i in regs_val[7]:
        x+=str(i)
    print(12*"0"+x)
memory=[]
for i in range(256):
  memory.append(0)
def memory_dump():
    global memory
    for i in memory:
        if(type(i)==str):
            print(i)
        if(type(i)==float):
            print(8*"0"+binary_to_cse(floating_to_binary(str(i))))
        if (type(i)==int):
            print(bin(i)[2:].zfill(16))


def addf(x,y):
    if (type(x)==int):
        x= binary_to_float(cse_to_binary((8-len(bin(x)[2:]))*"0" + bin(x)[2:]))
    if (type(y)==int):
        y= binary_to_float(cse_to_binary((8-len(bin(y)[2:]))*"0" + bin(y)[2:]))
    return overflow_f(x+y)

def subf(x,y):
    if (type(x)==int):
        x= binary_to_float(cse_to_binary((8-len(bin(x)[2:]))*"0" + bin(x)[2:]))
    if (type(y)==int):
        y= binary_to_float(cse_to_binary((8-len(bin(y)[2:]))*"0" + bin(y)[2:]))
    return overflow_f(y-x)

def add(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return overflow(x+y)

def sub(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return overflow(y-x)
  
def div(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    global regs_val
    regs_val[0]=(x//y)
    regs_val[1]=x%y

def cmp(x,y):
    global regs_val
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    if(x<y):
        regs_val[7][1]=1
    elif (x>y):
        regs_val[7][2]=1
    elif(x==y):
        regs_val[7][3]=1

def mul(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return overflow(x*y)

def Xor(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return x^y

def OR(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return x|y

def AND(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    return x&y

def NOT(x,y):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    if(type(y)==float):
        y=int(binary_to_cse(floating_to_binary((str(y)))),2)
    x=[i for i in bin(x)[2:].zfill(16)]
    z=""
    for i in range(len(x)):
        if(x[i]=="1"):
            x[i]="0"
        else:
            x[i]="1"
        z+=x[i]
    return int(z,2)
def rs(x,imm):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    return x>>imm
def ls(x,imm):
    if(type(x)==float):
        x=int(binary_to_cse(floating_to_binary((str(x)))),2)
    return x<<imm
def mov(y,x):
    return x

def movf(y,x):
    return x


def ld(x,mem):
    global regs_val
    regs_val[x]=memory[mem]

def st(x,mem):
    memory[mem]=regs_val[x]
    

def jgt(address):
  if(regs_val[7][2]==1):
    return(address)
  else:
    return -1
def jet(address):
  if(regs_val[7][3]==1):
    return address
  else:
    return -1
def jlt(address):
  if(regs_val[7][1]==1):
    return address
  else:
    return -1
def jmp(address):
  return address

def hlt():
  global halt
  halt=True
  return halt

op_code={
    "00000":[addf,"A",False],
    "00001":[subf,"A",False],
    "10000":[add,"A",False],
    "10001":[sub,"A",False],
    "10110":[mul,"A",False],
    "11010":[Xor,"A",False],
    "11011":[OR,"A",False],
    "11100":[AND,"A",False],
    "00010":[movf,"B",False],
    "10010":[mov,"B",False],
    "11000":[rs,"B",False],
    "11001":[ls,"B",False],
    "10011":[mov,"C",False],
    "10111":["div","C",False],
    "11101":[NOT,"C",False],
    "11110":["cmp","C",True],
    "10100":[ld,"D",False],
    "10101":[st,"D",False],
    "11111":[jmp,"E",False],
    "01100":[jlt,"E",False],
    "01101":[jgt,"E",False],
    "01111":[jet,"E",False],
    "01010":[hlt,"F",False],
    
}
reg_code={
    "000":0,
    "001":1,
    "010":2,
    "011":3,
    "100":4,
    "101":5,
    "110":6,
    "111":7
}

def overflow(x):
    if(x<0):
        regs_val[7][0]=1
        return 0
    if(x>65535):
        regs_val[7][0]=1
        return x%65536
    return x%65536

def overflow_f(x):
    if(x<1):
        regs_val[7][0]=1
        return 0
    if(x>int("11111100",2)):
        return (int("11111100",2))
    return x


def typea(op):
    global op_code
    if type(regs_val[reg_code[op[13:]]])==float and (op_code[op[0:5]][0]!=addf and op_code[op[0:5]][0]!=subf):
        regs_val[reg_code[op[13:]]]=binary_to_float(cse_to_binary((8-len(bin(op_code[op[0:5]][0](regs_val[reg_code[op[10:13]]],regs_val[reg_code[op[7:10]]]))[2:]))*"0"+bin(op_code[op[0:5]][0](regs_val[reg_code[op[10:13]]],regs_val[reg_code[op[7:10]]]))[2:]))
    else:
        regs_val[reg_code[op[13:]]]=op_code[op[0:5]][0](regs_val[reg_code[op[10:13]]],regs_val[reg_code[op[7:10]]])

def typeb(op):
    if (op_code[op[0:5]][0])==movf:
        regs_val[reg_code[op[5:8]]]=op_code[op[0:5]][0](regs_val[reg_code[op[5:8]]],binary_to_float(cse_to_binary(op[8:])))
    else:
        regs_val[reg_code[op[5:8]]]=op_code[op[0:5]][0](regs_val[reg_code[op[5:8]]],int(op[8:],2))

def typec(op):
    if(op_code[op[0:5]][0])=="div":
        div(regs_val[reg_code[op[10:13]]],regs_val[reg_code[op[13:]]])
    elif (op_code[op[0:5]][0])=="cmp":
        cmp(regs_val[reg_code[op[10:13]]],regs_val[reg_code[op[13:]]])
    elif (op_code[op[0:5]][0])==mov and reg_code[op[10:13]]==7:
        x=""
        for i in regs_val[7]:
            x+=str(i)
        regs_val[reg_code[op[13:]]]=int(x,2)
    else:
        regs_val[reg_code[op[13:]]]=op_code[op[0:5]][0](regs_val[reg_code[op[10:13]]],regs_val[reg_code[op[10:13]]])

def typed(op):
        op_code[op[0:5]][0](reg_code[op[5:8]], int(op[8:],2))

def typee(op):
        return op_code[op[0:5]][0](int(op[8:],2))

def typef(op):
    op_code[op[0:5]][0]()

ops=sys.stdin.readlines()
op = []
for i in ops:
    i = i.strip()
    if i!="":
        op.append(i)
for i in range(len(op)):
    memory[i]=op[i]

cycle=[]
yaxis=[]
cycle_counter=0 
k=0
#while(not halt):
x=k
while(k<len(op)and halt!=True):
    x=-1
    if(op_code[op[k][0:5]][1]=="A"):
        for j in range(len(regs_val[7])):
            regs_val[7][j]=0
        typea(op[k])            
    elif(op_code[op[k][0:5]][1]=="B"):
        for j in range(len(regs_val[7])):
                regs_val[7][j]=0
        typeb(op[k])
    elif(op_code[op[k][0:5]][1]=="C"):
        typec(op[k])
        if (op_code[op[k][0:5]][2])==False:
            for j in range(len(regs_val[7])):
                regs_val[7][j]=0
        else:
            regs_val[7][0]=0
    elif(op_code[op[k][0:5]][1]=="D"):
        cycle.append(cycle_counter)
        yaxis.append(int(op[k][8:],2))
        typed(op[k])
        for j in range(len(regs_val[7])):
                regs_val[7][j]=0
    elif(op_code[op[k][0:5]][1]=="E"):
        x=typee(op[k])
        for j in range(len(regs_val[7])):
                regs_val[7][j]=0
    elif(op_code[op[k][0:5]][1]=="F"):
        typef(op[k])
        for j in range(len(regs_val[7])):
                regs_val[7][j]=0 
    print_regs(k)
    #print(regs_val[2])
    if(x!=-1):
        k=x
    else:
        k+=1
    yaxis.append(k)
    cycle_counter+=1
    cycle.append(cycle_counter)

memory_dump()
x=np.array(cycle)
y=np.array(yaxis)
plt.scatter(x,y)
plt.xlabel("Cycle counter")
plt.ylabel("Memory accessed")
plt.show()
