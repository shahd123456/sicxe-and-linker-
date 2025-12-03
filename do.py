import pandas as pd
from tabulate import tabulate

#Dictionary to hold all instructions with respective formats & hexadecimal code
OPTAB = {
    "FIX":[1,"C4"],
    "FLOAT":[1,"C0"],
    "HIO":[1,"F4"],
    "NORM":[1,"C8"],
    "SIO":[1,"F0"],
    "TIO":[1,"F8"],
    "ADDR":[2,"90"],
    "CLEAR":[2,"B4"],
    "COMPR":[2,"A0"],
    "DIVR":[2,"9C"],
    "MULR":[2,"98"],
    "RMO":[2,"AC"],
    "SHIFTL":[2,"A4"],
    "SHIFTR":[2,"A8"],
    "SUBR":[2,"94"],
    "SVC":[2,"B0"],
    "TIXR":[2,"B8"],
    "ADD":[3,"18"],
    "ADDF":[3,"58"],
    "AND":[3,"40"],
    "COMP":[3,"28"],
    "DIV":[3,"24"],
    "DIVF":[3,"64"],
    "J":[3,"3C"],
    "JEQ":[3,"30"],
    "JGT":[3,"34"],
    "JLT":[3,"38"],
    "JSUB":[3,"48"],
    "LDA":[3,"00"],
    "LDB":[3,"68"],
    "LDCH":[3,"50"],
    "LDF":[3,"70"],
    "LDL":[3,"08"],
    "LDS":[3,"6C"],
    "LDT":[3,"74"],
    "LDX":[3,"04"],
    "LPS":[3,"D0"],
    "MUL":[3,"20"],
    "MULF":[3,"60"],
    "OR":[3,"44"],
    "RD":[3,"D8"],
    "RSUB":[3,"4C"],
    "SSK":[3,"EC"],
    "STA":[3,"0C"],
    "STB":[3,"78"],
    "STCH":[3,"54"],
    "STF":[3,"80"],
    "STI":[3,"D4"],
    "STL":[3,"14"],
    "STS":[3,"7C"],
    "STSW":[3,"E8"],
    "STT":[3,"84"],
    "STX":[3,"10"],
    "SUB":[3,"1C"],
    "SUBF":[3,"5C"],
    "TD":[3,"E0"],
    "TIX":[3,"2C"],
    "WD":[3,"DC"]}


#Directory list that holds all directories
Directory = ["START", "END", "RESW", "RESB", "BASE", "EQU", "LTORG"]

#global variables to keep track of assembly process and components

pass1_success = False
pass2_success = False
location_ctr = ""
prog_length = ""
prog_name = ""
start_adr = ""

location_ctr_arr = []
label_arr= []
instruction_arr = []
reference_arr = []
object_code_arr = []
lit_pool = {}
lit_table = {}
modif_index_arr = []


#Preloaded Symtab
Symbols_arr = ["A","X","L","B","S","T","F","PC","SW"]
loc_symbols_arr = ["0","1","2","3","4","5","6","8","9"]

#function to round numbers
def round_float(num):
    # get the fractional part of the number
    frac = num - int(num)
    # if the fractional part is 0.5 or more, round up
    if frac >= 0.5:
        return int(num) + 1
    # otherwise, round down
    else:
        return int(num)

#function to check if a symbol is in the symbol table
def check_SYMTAB(Symbol):
    for i in range(len(Symbols_arr)): #loops through the symbols arr
        if Symbols_arr[i]==Symbol: # if there is a match then returns true, otherwise returns false
            return True
    return False

#function to check if an instruction is in the OPTAB
def check_OPTAB(instruction):
    if(instruction in OPTAB):
        return True
    else:
        return False
    
#function to add a decimal to a hexadecimal number, returns hexadecimal
def sum_hex_int(a,b):
    x = int(a, 16)
    sum1 = x + b
    return format(sum1, '0>4X')

#function to subtract two hexadecimal numbers
def sub_hex(a,b):
    x= int(a,16)
    y = int(b,16)
    sub1 = x-y
    if sub1 >0:
        return format(sub1, '0>3X')
    else:
        return(dec_to_hex(sub1,12))

def dec_to_hex(n, bits):
    # create a conversion table
    conversion_table = "0123456789ABCDEF"
    # initialize an empty string for the hexadecimal result
    hexadecimal = ""
    # if the number is negative, add 2**bits to it
    if n < 0:
        n += 2**bits
    # loop until the number is zero
    while n > 0:
        # get the remainder of dividing the number by 16
        remainder = n % 16
        # get the corresponding hexadecimal digit from the table
        hexadecimal = conversion_table[remainder] + hexadecimal
        # divide the number by 16
        n = n // 16
    # return the hexadecimal string with 0x prefix
    return hexadecimal


def str_to_ascii(string):
    # initialize an empty string to store the concatenated ascii codes
    ascii_str = ""
    # loop through each character in the input string
    for char in string:
        # convert the character to its ascii code using the ord function
        ascii_code = ord(char)
        # convert the ascii code to a string using the str function
        ascii_str += str(ascii_code)
    # return the concatenated ascii codes as a string
    return ascii_str


#function to get the address of a symbol from the symbol table or literal table
def get_addr(Symbol):
    if Symbol.startswith("="):
        return lit_table[Symbol][1]
    else:
        for i in range(len(Symbols_arr)):
            if Symbols_arr[i]==Symbol:
                return loc_symbols_arr[i]


#function that discards the last two bits of a hexadecimal number       
def drop_two_bits(a):
    x = bin(int(a,16))[2:].zfill(8)
    x = x[:len(x)-2]
    return x


def first_pass(f):
    #temporary values, used to parse the file 
    label = ""
    instruction = ""
    reference = ""

    #reads first line
    line = f.readline()

    if "START" in line: #checks if START is in the first line read
        parts = line.split() #splits line into elements in parts arr based on spaces
        
        #checks if line consists of 3 parts as START directive line must have 3 parts
        if(len(parts)==3):
            
            global prog_name,prog_length, pass1_success
            
            prog_name = parts[0] #first part of the first line contains program name
            label_arr.append(parts[0]) #first part is also a label
            instruction_arr.append(parts[1]) #second part is an instruction or in this case the START directive
            reference_arr.append(parts[2]) #third part contains the reference, or in this case the start address
            location_ctr = parts[2] #location ctr is set to the value of the reference which is = start address
            location_ctr_arr.append("----") #START directive has no loc ctr so a placeholder gets appended
            start_adr = location_ctr #start address is set to the value of the location ctr
            
            line =f.readline() #reads next line
            
        while(line): #loops until there is no line

            parts = line.split() #splits line into parts

            #check if line consists of only one part
            #this means that it contains only an instruction or a directive
            if(len(parts)==1):
                label = "----" #no label
                label_arr.append(label)
                instruction = parts[0] 
                instruction_arr.append(instruction)
                reference = "----"
                reference_arr.append(reference)
                if instruction == "LTORG":
                    location_ctr_arr.append("----")
                else:
                    location_ctr_arr.append(location_ctr)
            elif(len(parts) ==3):
                label = parts[0]
                label_arr.append(label)
                instruction = parts[1]
                instruction_arr.append(instruction)
                reference = parts[2]
                reference_arr.append(reference)
                if instruction != "EQU":
                    location_ctr_arr.append(location_ctr)
                else:
                    if reference.isdigit():
                        hexa =hex(int(reference))[2:]
                        location_ctr_arr.append(hexa)
                    elif reference == "*":
                        location_ctr_arr.append(current_loc_ctr)
                   
                    else:
                        equ_address = get_addr(reference)
                        if equ_address is None:
                            print("Error: invalid value for EQU: "+ reference)
                            return
                        else:
                            location_ctr_arr.append(equ_address)
                    

                if label in Symbols_arr:
                    print("Error: Duplicate symbol ",label)
                    return
                else:
                    Symbols_arr.append(label)
                    if instruction == "EQU":
                        if reference.isdigit():
                            loc_symbols_arr.append(hexa)
                        elif reference == "*":
                            loc_symbols_arr.append(current_loc_ctr)
                        else:
                            loc_symbols_arr.append(equ_address)
                    else:
                        loc_symbols_arr.append(location_ctr)
            elif(len(parts)==2):
                instruction = parts[0]
                reference = parts[1]
                if instruction != "END":
                    label = "----"
                    label_arr.append(label)
                    instruction_arr.append(instruction)
                    reference_arr.append(reference)
                    if(instruction == "BASE"):
                        location_ctr_arr.append("----")
                    else:
                        location_ctr_arr.append(location_ctr)
                else:
                    for key in lit_pool:
                        lit_addr = location_ctr
                        length = lit_pool[key]
                        label_arr.append(key)
                        instruction_arr.append("BYTE")
                        reference_arr.append(key[1:])
                        location_ctr_arr.append(lit_addr)    
                        lit_table[key][1] = lit_addr
                        location_ctr = sum_hex_int(location_ctr, length)
                    lit_pool.clear()
                    label_arr.append("----")
                    instruction_arr.append(instruction)
                    reference_arr.append(reference)
                    location_ctr_arr.append(location_ctr)
                    prog_length =  sub_hex(location_ctr, start_adr).zfill(6)
                    pass1_success = True
                    break

            if reference.startswith("=") and reference != "=*":
                if reference not in lit_table:
                    if reference.startswith("=C'"):
                        length = len(reference)-4
                    elif reference.startswith("=X'"):
                        length = round_float((len(reference)-4)/2.0)
                    else:
                        print("Error: invalid literal used: " + reference)
                        return

                lit_pool[reference] = length
                lit_table[reference] = [0,""]
                lit_table[reference][0] = length


            if instruction != "EQU" and location_ctr != "----":
                current_loc_ctr = location_ctr
            match instruction:
                
                case "RESW":
                    location_ctr = sum_hex_int(location_ctr, int(reference)*3)
                case "RESB":
                    location_ctr = sum_hex_int(location_ctr, int(reference))
                case "WORD":
                    location_ctr = sum_hex_int(location_ctr, 3)
                case "BYTE":
                    match reference[:2]:
                        case "C'":
                            location_ctr = sum_hex_int(location_ctr, len(reference)-3)
                        case "X'":
                            location_ctr = sum_hex_int(location_ctr, round_float((len(reference)-3)/2.0))

                case "LTORG":
                    for key in lit_pool:
                        lit_addr = location_ctr
                        length = lit_pool[key]
                        label_arr.append(key)
                        instruction_arr.append("BYTE")
                        reference_arr.append(key[1:])
                        location_ctr_arr.append(lit_addr)    
                        lit_table[key][1] = lit_addr
                        location_ctr = sum_hex_int(location_ctr, length)
                    lit_pool.clear()
                case "BASE":
                    pass

                case "EQU":
                    pass
                case _:
                    found = False
                    format4 = False
                    if "+" in instruction:
                        instruction = instruction[1:]
                        format4 = True
                    if instruction in OPTAB:
                        found = True
                        if(format4):
                            format_ = 4
                        else:
                            format_ = OPTAB[instruction][0]
                    if found:
                        location_ctr = sum_hex_int(location_ctr,format_)
                    else:
                        print("Error: Invalid operation code " , instruction)
                        return
                            
            line = f.readline()
            
def second_pass():
    global pass1_success,pass2_success
    if pass1_success == False:
        print("Pass 1 was unsuccessful")
        return
    base = ""
    for j in range(len(reference_arr)):
        n = i= x= b= p= e= "0"
        disp = ""
        address = ""
        instruction = instruction_arr[j]
        reference = reference_arr[j]
        if instruction != "END" and instruction != "EQU":
            k =1
            if location_ctr_arr[j+k] == "----":
                while(location_ctr_arr[j+k] == "----" or instruction_arr[j+k] == "EQU"):
                    k += 1
            pc = location_ctr_arr[j+k]
                
            
        if instruction in Directory:
            if instruction == "BASE":
                if reference == "*":
                    base = location_ctr_arr[j-1]
                else:
                    base = get_addr(reference)


            object_code_arr.append("No object code")
            

            
        elif instruction== "WORD":
            object_code_arr.append(format(int(reference), '0>6X'))
            
            
        elif instruction =="BYTE":
            if reference[:2] == "C'":
                object_code_arr.append(str_to_ascii(reference[2:len(reference)-1]))
                

                

            elif reference[:2] == "X'":
                object_code_arr.append(reference[2:len(reference)-1])
                
        else:
            instruction_ = instruction
            if"+" in instruction:
                e= "1"
                instruction_ = instruction[1:]
            format_ = OPTAB[instruction_][0]
            op_code = OPTAB[instruction_][1]
            if format_ == 1:
                object_code_arr.append(op_code)
            elif format_ == 2:
                if instruction == "CLEAR" or instruction == "SVC" or instruction == "TIXR":
                    object_code_arr.append(op_code + get_addr(reference)+ "0")
                    
                else:
                    register = reference.split(",")
                    if(check_SYMTAB(register[0]) and check_SYMTAB(register[1])):
                       object_code_arr.append(op_code+get_addr(register[0])+get_addr(register[1]))
                       
                    else:
                        print("Invalid registers used")
                        return
            else:
                if instruction.startswith("+"):
                    if ",X" in reference:
                        x = "1"
                        reference = reference[:len(reference)-2]
                    if "@" in reference:
                        n = "1"
                        reference = reference[1:]
                    elif "#" in reference:
                        i = "1"
                        reference = reference[1:]
                    else:
                        n = "1"
                        i = "1"
                    if(i == "1" and reference.isdigit()):
                        hex_value = format(int(reference), '0>5X')
                        binary= drop_two_bits(op_code)+n+i+x+b+p+e
                        object_code_arr.append(format(int(binary,2), '0>3X')+hex_value)
                    elif(reference == "=*"):
                        binary= drop_two_bits(op_code)+n+i+x+b+p+e
                        object_code_arr.append(format(int(binary,2), '0>3X')+location_ctr_arr[j].zfill[5])
                    else:
                        address = get_addr(reference).zfill(5)
                        binary= drop_two_bits(op_code)+n+i+x+b+p+e
                        object_code_arr.append(format(int(binary,2), '0>3X')+address)
                        modif_index_arr.append(j)
                        
                                      
                else:
                    if ",X" in reference:
                        x = "1"
                        reference = reference[:len(reference)-2]
                    if "@" in reference:
                        n = "1"
                        reference = reference[1:]
                        
                    elif "#" in reference:
                        i = "1"
                        reference = reference[1:]
                    else:
                        n = "1"
                        i = "1"
                    if(i =="1" and reference.isdigit()):
                        disp = hex(int(reference))[2:]
                        if len(disp)<4:
                            binary= drop_two_bits(op_code)+n+i+x+b+p+e
                            object_code_arr.append(format(int(binary,2), '0>3X')+disp.zfill(4-len(disp)))
                        else:
                            print("Error: immediate value too big for format 3: " + instruction)
                            return
                    else:
                        if(instruction == "RSUB"):
                            binary= drop_two_bits(op_code)+n+i+x+b+p+e
                            object_code_arr.append(format(int(binary,2), '0>3X')+ "000")
                        else:
                            pc_dec =int(get_addr(reference),16) -int(pc,16)
                            pc_disp = sub_hex(get_addr(reference),pc).zfill(3)
                            base_dec = 0
                            if base != "":
                                base_dec = int(get_addr(reference),16) - int(base,16)
                                base_disp = sub_hex(get_addr(reference),base).zfill(3)
                            if(pc_dec >= -2047 and pc_dec<=2048):
                                p="1"
                                binary= drop_two_bits(op_code)+n+i+x+b+p+e
                                object_code_arr.append(format(int(binary,2), '0>3X')+pc_disp)
                              
                            elif(base_dec>=0 and base_dec <=4095):
                                if base == "":
                                    print("Error: BASE directive not defined")
                                    return
                                b = "1"
                                binary= drop_two_bits(op_code)+n+i+x+b+p+e
                                object_code_arr.append(format(int(binary,2), '0>3X')+base_disp)
                                
                            else:
                                print("Error: Unsuitable format used for instruction: " + instruction)
                                return        
            
    pass2_success = True

                
def create_table():
    df = pd.DataFrame({
   'LOCCR': location_ctr_arr,
    'Label': label_arr,
   'Instruction': instruction_arr,
   'Reference': reference_arr,
   'Object Code': object_code_arr
   })

    symb = pd.DataFrame({
        'Symbol': Symbols_arr,
        'Address':loc_symbols_arr})


    lit = pd.DataFrame.from_dict(lit_table, orient='index', columns=['Length', 'Address'])

    lit.index.name = 'Literal Name'

    print(df.to_markdown(index=False, tablefmt='fancy_grid'))
    print(symb.to_markdown(index=False, tablefmt='fancy_grid'))
    print(tabulate(lit, headers='keys', tablefmt='fancy_grid'))

# function to generate the HTE record from the object code list
def generate_HTE(object_code_list):
    # initialize an empty string to store the HTE record
    hte_record = ""
    # get the program name, start address, and program length from the first line
    global prog_name, prog_length, pass2_success
    if pass2_success == False:
        return
    start_addr = reference_arr[0].zfill(6)
    # pad the program name with zeroes if it is less than 6 characters
    if len(prog_name) < 6:
        prog_name_ = prog_name.zfill(6)
    # create the header record with the format H^prog_name^start_addr^prog_length
    header_record = f"H^{prog_name_}^{start_addr}^{prog_length}"
    # append the header record to the HTE record
    hte_record += header_record + "\n"
    # initialize a variable to store the current text record
    text_record = ""
    modif_record = ""
    total_modif_record = ""
    # initialize a variable to store the current text record length in bytes
    text_record_length = 0
    # initialize a variable to store the current text record start address
    text_record_start = ""
    # loop through each object code in the object code list
    for i in range(1, len(object_code_list) - 1):
        # get the current object code
        object_code = object_code_list[i]
        # if the object code is "No object code", then start a new text record
        if instruction_arr[i] == "RESW" or instruction_arr[i] == "RESB":
            # if the current text record is not empty, then append it to the HTE record
            if text_record != "":
                # create the text record header with the format T^text_record_start^text_record_length^text_record
                text_record = f"T^{text_record_start}^{format(text_record_length, '0>2X')}{text_record}"
                hte_record += text_record + "\n"
            # reset the current text record, length, and start address
            text_record = ""
            text_record_length = 0
            text_record_start = ""
        elif instruction_arr[i] in Directory:
            pass
        else:
            # get the current object code length in bytes by dividing by 2
            object_code_length = int(round(len(object_code) / 2.0))
            # if the current text record length plus the current object code length exceeds 30 bytes, then start a new text record
            if text_record_length + object_code_length > 30:
                # append the current text record to the HTE record
                text_record = f"T^{text_record_start}^{format(text_record_length, '0>2X')}{text_record}"
                hte_record +=  text_record + "\n"
                # reset the current text record, length, and start address
                text_record = ""
                text_record_length = 0
                text_record_start = ""
            # if the current text record is empty, then set the start address to the location counter of the current line
            if text_record == "":
                text_record_start = location_ctr_arr[i].zfill(6)
            # append the current object code to the current text record with a ^ separator
            text_record += f"^{object_code}"
            # update the current text record length by adding the current object code length
            text_record_length += object_code_length
            
    # if the current text record is not empty, then append it to the HTE record
    if text_record != "":
        text_record= f"T^{text_record_start}^{format(text_record_length, '0>2X')}{text_record}"
        hte_record += text_record + "\n"

    for i in modif_index_arr:
        modif_addr = sum_hex_int(location_ctr_arr[i],1)
        modif_record = f"M^{modif_addr}^05^+{prog_name}"
        total_modif_record += modif_record + "\n"

    if(total_modif_record != ""):
        hte_record += total_modif_record
    # create the end record with the format E^start_addr
    end_record = f"E^{start_addr}"
    # append the end record to the HTE record
    hte_record += end_record + "\n"
    print("\n---------------\nHTE RECORD: \n")
    # return the HTE record as a string
    print(hte_record)
                       
                
def main():
    # Open the file in read mode
    f = open("inSICXE.txt", "r")
    first_pass(f)
    second_pass()
    create_table()
    generate_HTE(object_code_arr)

main()