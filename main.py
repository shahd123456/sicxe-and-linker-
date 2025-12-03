# fh = open('C:\\Users\\BluRay\\Downloads\\inSICXE.txt', 'r')
# # fh = open('inSICXE.txt')
#
# #array for lines in code
# lines = fh.readlines()
#
# for i in lines:
#     print(i)
# fh.close()
# read file
with open("input.txt") as input_file:
    lines = input_file.readlines()

print(lines)
#lists of data in SIC/XE
labels=[]
instr=[]
ref=[]
locctr=[]
objectCode=[]

#splitting strings of line by space
for i in range(len(lines)):
    # data = lines[i].split(" ")
    # print(data)

    if len(lines[i].split(" ")) == 3:
        data = lines[i].split(" ")
        labels.append(data[0].strip())
        instr.append(data[1].strip())
        ref.append(data[2].strip())
    elif len(lines[i].split(" ")) == 2:
        data = lines[i].split(" ")
        labels.append("&")
        instr.append(data[0].strip())
        ref.append(data[1].strip())
    elif len(lines[i].split(" ")) == 1:
        data = lines[i].split(" ")
        labels.append("&")
        instr.append(data[0].strip())
        ref.append("&")

#printing all labels , intsructions and References


# print("labels:", labels)
# print("Instructions:", instr)
# print("References:", ref)


#PASS1
#lOCCTR

hex_string = ref[0]

an_integer = int(hex_string, 16)
# print("First Locctr INT:", an_integer)
locctr.append(ref[0])
locctr.append(ref[0])
# print(locctr)
for i in range (len(locctr)):
    locctr[i] =int(locctr[i])



print("Lenght of lines of program:" ,len(lines))

format2=["ADDR", "CLEAR", "COMPR", "DIVR", "MULR", "RMO", "SHIFTR", "SHIFTL", "SUBR", "SVC", "TIXR"]

#get locctr in decimal
for i in range(1, len(lines)-1):
    if instr[i] == "WORD":
        num = locctr[i] + 3
        locctr.append(int(num))
    elif instr[i] == "BYTE":
        if ref[i][0] == "X":
            num = locctr[i] +(len(ref[i])-3) / 2
            locctr.append(int(num))
        elif ref[i][0] == "C":
            num = locctr[i] + (len(ref[i]) - 3)
            locctr.append(int(num))
    elif instr[i] == "RESW":
        num = locctr[i] + (int(ref[i])*3)
        locctr.append(int(num))
    elif instr[i] == "RESB":
        num = locctr[i] + int(ref[i])
        locctr.append(int(num))
    elif instr[i] == "RSUB":
        num = locctr[i] + 3
        locctr.append(int(num))
    elif instr[i] in format2:
        num = locctr[i] + 2
        locctr.append(int(num))
    elif instr[i][0] == "+":
        num = locctr[i] + 4
        locctr.append(int(num))
    elif instr[i] =="BASE":
        num = locctr[i]
        locctr.append(num)
    else:
        num= locctr[i] +3
        locctr.append(int(num))

# print("Lenght of Locctr:" , len(locctr))
# print("LOCCTR in decimal " ,locctr)


#change decimal locctrs to hexa
locctrHex=[]
for j in locctr:
    numHex=hex(j).lstrip("0x").zfill(4)
    locctrHex.append(numHex)
print("LOCCTR in Hex",locctrHex)

#print pass1
print("THE WHOLE PROGRAM WITH LOCCTR:")

for m in range (len(lines)):
    print(f"{locctrHex[m]}:{labels[m]}:{instr[m]}:{ref[m]}\n")

#get length of whole program= end - start

lenghtOfProgram = locctr[len(lines)-1] - locctr[0]
print("Lenght of whole program =", hex(lenghtOfProgram).lstrip("0x").zfill(4))

sym_Symbol = []
sym_locctr = []
#Symbol Table
print("SYMBOL TABLE:")
for n in range  (len(labels)-1):
    if labels[n] != "&":
        sym_Symbol.append(labels[n])
        sym_locctr.append(locctrHex[n])
        print(f"{labels[n]}: {locctrHex[n]}")

#Dict of opcodes: "instr" :["format","opcode"]

opcodeDict = {
        "FIX": [1, "C4"],
        "FLOAT": [1, "C0"],
        "HIO":[1, "F4"],
        "NORM":[1, "C8"],
        "SIO": [1, "F0"],
        "TIO":[1, "F8"],
        "ADDR": [2, "90"],
        "CLEAR": [2, "B4"],
        "COMPR":[2, "A0"],
        "DIVR": [2, "9C"],
        "MULR": [2, "98"],
        "RMO":[2, "AC"],
        "SHIFTL": [2, "A4"],
        "SHIFTR":[2, "A8"],
        "SUBR": [2, "94"],
        "SVC": [2, "B0"],
        "TIXR": [2, "B8"],
        "ADD": [3, "18"],
        "ADDF": [3, "58"],
        "AND": [3, "40"],
        "COMP": [3, "28"],
        "COMPF":[3, "88"],
        "DIV": [3, "24"],
        "DIVF": [3, "64"],
        "J": [3, "3C"],
        "JEQ":[3, "30"],
        "JGT": [3, "34"],
        "JLT": [3, "38"],
        "JSUB": [3, "48"],
        "LDA": [3, "00"],
        "LDB": [3, "68"],
        "LDCH": [3, "50"],
        "LDF": [3, "70"],
        "LDL": [3, "08"],
        "LDS": [3, "6C"],
        "LDT":[3, "74"],
        "LDX": [3, "04"],
        "LPS":[3, "D0"],
        "MUL": [3, "20"],
        "MULF":[3, "60"],
        "OR": [3, "44"],
        "RD": [3, "D8"],
        "RSUB": [3, "4C"],
        "SSK": [3, "EC"],
        "STA": [3, "0C"],
        "STB": [3, "78"],
        "STCH": [3, "54"],
        "STF": [3, "80"],
        "STI":[3, "D4"],
        "STL": [3, "14"],
        "STS":[3, "7C"],
        "STSW": [3, "E8"],
        "STT": [3, "84"],
        "STX": [3, "10"],
        "SUB": [3, "1C"],
        "SUBF":[3, "5C"],
        "TD": [3, "E0"],
        "TIX":[3, "2C"],
        "WD":[3, "DC"],
}

#Dict of registers:

registerDict = {
    "A": 0,
    "X": 1,
    "L": 2,
    "B": 3,
    "S": 4,
    "T": 5,
    "F": 6,
    "PC": 8,
    "SW": 9,
}


#PASS2

#instructions with no object code
none = ["BASE", "START", "END", "RESW", "RESB"]

#instructions with no object code
for j in range(len(lines)):
    if instr[j] in none:
        objectCode.append("NoObjCode")

#byte object code
    elif instr[j] == "BYTE":
        if ref[j][0] == "C":
            objectCode.append("ASCII CODE")
        else:
            objectCode.append(ref[j][2:-1])
#format 4
    elif instr[j][0] == "+":
        obj = ""
        op = opcodeDict[instr[j][1:]][1]
        op1 = op[0]
        op2 = op[1]
        op1_bin = bin(int(op1, 16)).lstrip("0b").zfill(4)
        op2_bin = bin(int(op2, 16)).lstrip("0b").zfill(4)[:2]
        obj += op1_bin
        obj += op2_bin
        # objectCode.append(obj)
        if ref[j][0] == "#":
            n = "0"
            i = "1"
            x = "0"
            b = "0"
            p = "0"
            e = "1"
            flags = n + i + x + b + p + e
            obj += flags
            # objectCode.append(obj)

# #number ex: #4096
            if ref[j][1:] not in labels:
                num = bin(int(ref[j][1:])).lstrip("0b").zfill(20)
                obj +=num
                # objectCode.append(obj)
                objectCode.append(hex(int(obj, 2)).lstrip("0x"))

# #ref ex: #table
            else:
                for n in range(len(labels)):
                    if ref[j][1:] == labels[n]:
                        num = bin(locctr[n]).lstrip("0b").zfill(20)
                        obj += num
                        # objectCode.append(obj)
                        objectCode.append(hex(int(obj, 2)).lstrip("0x"))
#direct addressing
        else:
            n = "1"
            i = "1"
            x = "0"
            b = "0"
            p = "0"
            e = "1"
            flags = n + i + x + b + p + e
            obj += flags
            # objectCode.append(obj)
            for n in range(len(labels)):
                if ref[j] == labels[n]:
                    num = bin(locctr[n]).lstrip("0b").zfill(20)
                    obj += num
                    # objectCode.append(obj)
                    objectCode.append(hex(int(obj, 2)).lstrip("0x"))
# format 1 (RSUB)
    elif instr[j] == "RSUB":
        objectCode.append("4f0000")
# format 3
    elif opcodeDict[instr[j]][0] == 3:
        e = "0"
        obj = ""
        op = opcodeDict[instr[j]][1]
        op1 = op[0]
        op2 = op[1]
        op1_bin = bin(int(op1, 16)).lstrip("0b").zfill(4)
        op2_bin = bin(int(op2, 16)).lstrip("0b").zfill(4)[:2]
        obj += op1_bin
        obj += op2_bin
        # objectCode.append(obj)

#  immediate addressing
        if ref[j][0] == "#":
            # #value ex:#3
            if ref[j][1:] not in sym_Symbol:
                n = "0"
                i = "1"
                x = "0"
                b = "0"
                p = "0"
                # e = "0"
                flags = n + i + x + b + p + e
                obj += flags
                # objectCode.append(obj)
                disp = bin(int(ref[j][1:])).lstrip("0b").zfill(12)
                obj += disp
            # #ref ex: #table
            else:
                n = "0"
                i = "1"
                if ref[j][-1] == "X":
                    x = "1"
                    # for m in range(len(sym_Symbol)):
                    #     if ref[j][:-2] == sym_Symbol[m]:
                    #         indexOfAdd = sym_Symbol.index(sym_Symbol[m])
                    #         TargetAddr = int(sym_locctr[indexOfAdd], 16)
                    #         # pc = locctr[j + 1]
                    #         # disp = TargetAddr - pc
                    indexOfAdd = sym_Symbol.index(ref[j][1:-2])
                    TargetAddr = int(sym_locctr[indexOfAdd], 16)
                else:
                    x = "0"
                    # for m in range(len(sym_Symbol)):
                    #     if ref[j][:-2] == sym_Symbol[m]:
                    #         indexOfAdd = sym_Symbol.index(sym_Symbol[m])
                    #         TargetAddr = int(sym_locctr[indexOfAdd], 16)
                    indexOfAdd = sym_Symbol.index(ref[j][1:])
                    TargetAddr = int(sym_locctr[indexOfAdd], 16)

                pc = locctr[j + 1]
                disp = TargetAddr - pc
                if -2048 <= disp <= 2047:
                    b = "0"
                    p = "1"
                    # dispInBin = bin(disp)
                    if str(disp)[0] == "-":
                        disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                        dispInBin = bin(int(disp_hex, 16)).lstrip("0b").zfill(12)
                    else:
                        dispInBin = bin(disp).lstrip("0b").zfill(12)
                    flags = n + i + x + b + p + e
                    obj += flags
                    obj += dispInBin

        # indirect addressing
        elif ref[j][0] == "@":
            n = "1"
            i = "0"
            if ref[j][-1] == "X":
                x = "1"
                # for m in range(len(sym_Symbol)):
                #     if ref[j][:-2] == sym_Symbol[m]:
                #         indexOfAdd = sym_Symbol.index(sym_Symbol[m])
                #         TargetAddr = int(sym_locctr[indexOfAdd], 16)
                #         # pc = locctr[j + 1]
                #         # disp = TargetAddr - pc
                indexOfAdd = sym_Symbol.index(ref[j][1:-2])
                TargetAddr = int(sym_locctr[indexOfAdd], 16)
            else:
                x = "0"
                # for m in range(len(sym_Symbol)):
                #     if ref[j][:-2] == sym_Symbol[m]:
                #         indexOfAdd = sym_Symbol.index(sym_Symbol[m])
                #         TargetAddr = int(sym_locctr[indexOfAdd], 16)
                indexOfAdd = sym_Symbol.index(ref[j][1:])
                TargetAddr = int(sym_locctr[indexOfAdd], 16)

            pc = locctr[j + 1]
            disp = TargetAddr - pc
            if -2048 <= disp <= 2047:
                b = "0"
                p = "1"
                # dispInBin = bin(disp)
                if str(disp)[0] == "-":
                    disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                    dispInBin = bin(int(disp_hex, 16)).lstrip("0b").zfill(12)
                else:
                    dispInBin = bin(disp).lstrip("0b").zfill(12)
                flags = n + i + x + b + p + e
                obj += flags
                obj += dispInBin
            else:
                b = "1"
                p = "0"
                base = "0033"
                disp = TargetAddr - int(base, 16)
                # dispInBin = bin(disp)
                if str(disp)[0] == "-":
                    disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                    dispInBin = bin(int(disp_hex, 16)).lstrip("0b").zfill(12)
                else:
                    dispInBin = bin(disp).lstrip("0b").zfill(12)
                flags = n + i + x + b + p + e
                obj += flags
                obj += dispInBin

        # direct addressing
        else:
            n = "1"
            i = "1"
            if ref[j][-1] == "X":
                x = "1"
                # for m in range(len(sym_Symbol)):
                #     if ref[j][:-2] == sym_Symbol[m]:
                #         indexOfAdd = sym_Symbol.index(sym_Symbol[m])
                #         TargetAddr = int(sym_locctr[indexOfAdd], 16)
                #         # pc = locctr[j + 1]
                #         # disp = TargetAddr - pc
                indexOfAdd = sym_Symbol.index(ref[j][:-2])
                TargetAddr = int(sym_locctr[indexOfAdd], 16)
            else:
                x = "0"
                # for m in range(len(sym_Symbol)):
                #     if ref[j][:-2] == sym_Symbol[m]:
                #         indexOfAdd = sym_Symbol.index(sym_Symbol[m])
                #         TargetAddr = int(sym_locctr[indexOfAdd], 16)
                indexOfAdd = sym_Symbol.index(ref[j])
                TargetAddr = int(sym_locctr[indexOfAdd], 16)

            pc = locctr[j+1]
            disp = TargetAddr - pc
            if -2048 <= disp <= 2047:
                b = "0"
                p = "1"
                # dispInBin = bin(disp)
                if str(disp)[0] == "-":
                    disp_hex = hex(disp & (2**32-1)).lstrip("0x")[-3:]
                    dispInBin = bin(int(disp_hex, 16)).lstrip("0b").zfill(12)
                else:
                    dispInBin = bin(disp).lstrip("0b").zfill(12)
                flags = n + i + x + b + p + e
                obj += flags
                obj += dispInBin
            else:
                b = "1"
                p = "0"
                base = "0033"
                disp = TargetAddr - int(base, 16)
                    # dispInBin = bin(disp)
                if str(disp)[0] == "-":
                    disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                    dispInBin = bin(int(disp_hex, 16)).lstrip("0b").zfill(12)
                else:
                    dispInBin = bin(disp).lstrip("0b").zfill(12)
                flags = n + i + x + b + p + e
                obj += flags
                obj += dispInBin

        objectCode.append(hex(int(obj, 2)).lstrip("0x").zfill(6))


 #format 2
    elif ref[j][0] !="#" and ref[j][0] != "@" and instr[j] not in none and instr[j] !="RSUB":
        code = ""
        if opcodeDict[instr[j]][0] == 2:
#get opcode of instruction
            op = opcodeDict[instr[j]][1]
            op1 = op[0]
            op2 = op[1]
            op1_bin = bin(int(op1, 16)).lstrip("0b").zfill(4)
            op2_bin = bin(int(op2, 16)).lstrip("0b").zfill(4)
            code += op1_bin
            code += op2_bin
            # objectCode.append(c)
# 2 registers
            if len(ref[j]) == 3:
                first = ref[j][0]
                second = ref[j][-1]

                register_1 = registerDict[first]
                register_2 = registerDict[second]

                register_1_bin = bin(register_1).lstrip("0b").zfill(4)
                register_2_bin = bin(register_2).lstrip("0b").zfill(4)

                code += register_1_bin
                code += register_2_bin
                objectCode.append(hex(int(code, 2)).lstrip("0x"))

 # if one register
            else:
                first = ref[j][0]
                second = "0000"
                register_1 = registerDict[first]
                register_1_bin = bin(register_1).lstrip("0b").zfill(4)
                register_2_bin = bin(int(second,16)).lstrip("0b").zfill(4)
                code += register_1_bin
                code += register_2_bin

                objectCode.append(hex(int(code, 2)).lstrip("0x"))

    else:
        objectCode.append("_")

# print whole program

for m in range(len(lines)):
    print(f"{locctrHex[m]}:{labels[m]}:{instr[m]}:{ref[m]}:{objectCode[m]} \n")

# HTE RECORD

end =hex(int(ref[0], 16)).lstrip("0x").zfill(6)
lenght =hex(lenghtOfProgram).lstrip("0x").zfill(6)

print("H ^ " + instr[0]+ " ^ " + end + "^" + lenght)
print("E " + " ^ " + end)
