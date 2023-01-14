import math

def type_1():
    global nP
    CPU_bits = int(input("Enter no of bits in CPU: "))
    change = int(input("Enter the new addressable memory option: "))
    while (change > 4 or change < 1 or change == memtype):
        print("Wrong Type.. :(")
        change = int(input("Enter the type of memory: "))
    if change == 1:
        nP += 3
    elif change == 2:
        nP += 1
    elif change == 4:
        nP +=  math.log2(CPU_bits / 8)
    print("Address pins saved of required are", P-nP)
    
def type_2():    
    CPU_bits = int(input("Enter no of bits in CPU: "))
    pins_count = int(input("Enter the no. of address pins: "))
    change = int(input("Enter the new addressable memory option: "))
    while (change > 4 or change < 1):
        print("Wrong Type.. :(")
        change = int(input("Enter the type of memory: "))
    answer = (2 ** pins_count)
    if change == 1:
        answer = (2 * -3)
    elif change == 2:
        answer = (2 * -1)
    elif change == 4:
        answer *=  (CPU_bits / 8)
    print("Max memory in Bytes:", (answer / (2 ** 30)), "GB")

space = float(input("Enter the space in memory(in MB): "))
print("""1. Bit Addressable Memory - Cell Size = 1 bit
2. Nibble Addressable Memory - Cell Size = 4 bit
3. Byte Addressable Memory - Cell Size = 8 bits(standard)
4. Word Addressable Memory - Cell Size = Word Size (depends on CPU)""")
memtype = int(input("Enter the type of memory: "))
while (memtype > 4 or memtype < 1):
    print("Wrong Type.. :(")
    memtype = int(input("Enter the type of memory: "))
length_instruction = int(input("Enter the length of instruction in bits: "))

"""
R -> length of register
Q -> length of opcode
P -> length of address
F -> length of Filler
"""

R = int(input("Enter the length of register in bits: "))
P = 20 + math.log2(space)
nP = P
if memtype == 1:
    P += 3
elif memtype == 2:
    P += 1
elif memtype == 4:
    P +=  math.log2(8/int(input("Enter the no. of bits for the CPU: ")))

Q = length_instruction - P - R
F = length_instruction - Q - 2 * R
print("Minimum no. of bits needed to represent an address in the given architecture: ", P)
print("No. of bits needed by opcode: ", Q)
print("Number of filler bits in the instruction: ", F)
print("Max no. of instruction: ", 2 ** Q)
print("Max no. of register: ", 2 ** R)

print("\n\nSystem enhancement related answers\n")
choice = int(input("Enter type of System enhancement related questions to be answered: "))
if choice > 2 or choice < 1:
    print("Wrong choice")
    choice = int(input("Enter type of System enhancement related questions to be answered: "))

if choice == 1:
    type_1()
elif choice == 2:
    type_2()
