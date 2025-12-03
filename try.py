#  craete the frame of the table 
import pandas as pd 
import tabulate 

#Dictionary to hold all instructions with respective formats & hexadecimal code
OPTAB = {"FIX":[1,"C4"],"FLOAT":[1,"C0"],"HIO":[1,"F4"],"NORM":[1,"C8"],"SIO":[1,"F0"],"TIO":[1,"F8"],"ADDR":[2,"90"],"CLEAR":[2,"B4"],
         "COMPR":[2,"A0"],"DIVR":[2,"9C"],"MULR":[2,"98"],"RMO":[2,"AC"],"SHIFTL":[2,"A4"],"SHIFTR":[2,"A8"],"SUBR":[2,"94"],
         "SVC":[2,"B0"],"TIXR":[2,"B8"],"ADD":[3,"18"],"ADDF":[3,"58"],"AND":[3,"40"],"COMP":[3,"28"],"DIV":[3,"24"],"DIVF":[3,"64"],
         "J":[3,"3C"],"JEQ":[3,"30"],"JGT":[3,"34"],"JLT":[3,"38"],"JSUB":[3,"48"],"LDA":[3,"00"],"LDB":[3,"68"],"LDCH":[3,"50"],
         "LDF":[3,"70"],"LDL":[3,"08"],"LDS":[3,"6C"],"LDT":[3,"74"],"LDX":[3,"04"],"LPS":[3,"D0"],"MUL":[3,"20"],"MULF":[3,"60"],
         "OR":[3,"44"],"RD":[3,"D8"],"RSUB":[3,"4C"],"SSK":[3,"EC"],"STA":[3,"0C"],"STB":[3,"78"],"STCH":[3,"54"],"STF":[3,"80"],
         "STI":[3,"D4"],"STL":[3,"14"],"STS":[3,"7C"],"STSW":[3,"E8"],"STT":[3,"84"],"STX":[3,"10"],"SUB":[3,"1C"],"SUBF":[3,"5C"],
         "TD":[3,"E0"],"TIX":[3,"2C"],"WD":[3,"DC"]}


format1 = {"FIX", "FLOAT", "HIO", "NORM", "SIO", "TIO"}
#####
format2 = {"ADDR", "CLEAR", "COMPR", "DIVR", "MULR",
           "RMO", 'SHIFTL', "SHIFTR", "SUBR", "SVC", "TIXR"}
#####
format3 = {"ADD", "ADDF", "AND", "COMP", "COMPF", "DIV", "DIVF", "J", "JEQ",
            "JGT", "JLT", "JSUB", "LDA", "LDB", "LDCH", 'LDF', "LDL", "LDS", "LDT", "LDX",
           "LPS", "MUL", "SSK", "STA", "STB", "STCH", "STF", "STI", "STL", "STS", "STSW", 
           "STT", "STX", "SUB", "SUBF", "MULF", "OR", 'RD', "RSUB", "TD", "TIX", "WD"}
#####
format4 = {"+ADD", "+ADDF", "+AND", "+COMP", "+COMPF", "+DIV", "+DIVF", "+J", "+JEQ",
            "+JGT", "+JLT", "+JSUB", "+LDA", "+LDB", "+LDCH", "+LDF", "+LDL", "+LDS", "+LDT", "+LDX",
           "+LPS", "+MUL", "+SSK", "+STA", "+STB", "+STCH", "+STF", "+STI", "+STL", "+STS", "+STSW", "+STT", "+STX",
             "+SUB", "+SUBF", "+MULF", "+OR", "+RD", "+RSUB", "+TD", "+TIX", "+WD"}
 
 # varible 
pass1_success = False
pass2_success = False
location_ctr = ""
prog_length = ""
prog_name = ""
start_adr = ""

Symbols_arr = ["A","X","L","B","S","T","F","PC","SW"]
loc_symbols_arr = ["0","1","2","3","4","5","6","8","9"]

location_ctr_arr = []
label_arr= []
instruction_arr = []
reference_arr = []
object_code_arr = []
modif_arr=[]
format_4_indices = []

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
    

     #index
def indirect_loccr(location_counter): #8 =1000 fa hnsh3l tl one 7tkon 0000 fa 7tb2a heya heya el zero 
    indirect_ref= {"0":"8","1":"9", "2":"A", "3":"B","4":"C", "5":"D", "6":"E", "7":"F"}
    x = indirect_ref[location_counter[0]]
    new_loccr = x+location_counter[1:]
    return new_loccr

     # ascl c,abc,
def str_to_ascii(string):
    # initialize an empty string 
    ascii_str = ""
    # loop 
    for char in string:
        # convert
        ascii_code = ord(char)
        # convert the ascii 
        ascii_str += str(ascii_code)
    return ascii_str

# check from symbol table 
def get_addr(Symbol):
    for i in range(len(Symbols_arr)):
        if Symbols_arr[i]==Symbol:
            return loc_symbols_arr[i]

# pass one 
def first_pass(f):
    label = ""
    instruction = ""
    reference = ""
    
    line = f.readline()

    if "START" in line:
        # n2sm el line 
        parts = line.split()
        if(len(parts)==3):
            global prog_name,prog_length, pass1_success
            prog_name = parts[0]
            label_arr.append(parts[0])
            instruction_arr.append(parts[1])
            reference_arr.append(parts[2])
            location_ctr = parts[2]
            location_ctr_arr.append(location_ctr)
            start_adr = location_ctr
            line =f.readline()
            # lwo fe line fadi stop 
        while(line.strip() != ""):
            parts = line.split()
            if(len(parts) ==3):
                label = parts[0]
                label_arr.append(label)
                instruction = parts[1]
                instruction_arr.append(instruction)
                reference = parts[2]
                reference_arr.append(reference)
                location_ctr_arr.append(location_ctr)

# error lwo have the same name 
                if label in Symbols_arr:
                    print("Error: Duplicate symbol ",label)
                    return
                else:
                    Symbols_arr.append(label)
                    loc_symbols_arr.append(location_ctr)
            elif(len(parts)==2):
                label = "----"
                label_arr.append(label)
                instruction = parts[0]
                instruction_arr.append(instruction)
                reference = parts[1]
                reference_arr.append(reference)
                if(instruction == "BASE"):
                    location_ctr_arr.append("----")
                else:
                    location_ctr_arr.append(location_ctr)
                if instruction == "END":
                    prog_length =  sub_hex(location_ctr, start_adr).zfill(6)
                    pass1_success = True
                    break
            elif(len(parts)==1): #one
                label="----"
                label_arr.append(label)
                instruction=parts[0]
                instruction_arr.append(instruction)
                reference_arr.append("----")
                location_ctr_arr.append(location_ctr)
            

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
                            location_ctr = sum_hex_int(location_ctr, round((len(reference)-3)/2.0))
                case "BASE":
                    pass

                case _:
                    found = False
                    format_ = 0
                    format_four = False
                    if "+" in instruction:
                        format_four = True
                    if(format_four):
                        found = True
                        if instruction in format4:
                            format_ = 4
                    else:
                        if instruction in OPTAB or instruction == "End":
                            found = True
                            format_ = OPTAB[instruction][0]
                    if found:
                        location_ctr = sum_hex_int(location_ctr,format_)
                    else:
                        print("Error: Invalid operation code " , instruction)
                        return
            line = f.readline()
            # instruction el 3adyA no resw or end e hakza
            # second pass 

def second_pass():
    global pass1_success,pass2_success
    if pass1_success == False:
        print("Pass 1 was unsuccessful")
        return
            
    #pass two 
    for index, ins in enumerate(instruction_arr):

        reference = reference_arr[index]
        
        if ins== "START" or ins == "END" or ins=="RESW" or ins =="RESB" or ins == "BASE":
          if ins == "BASE":
            base = get_addr(reference)
          object_code_arr.append("No object code")

        elif ins== "WORD":
            object_code_arr.append(format(int(reference), '0>6X'))
            
        elif ins =="BYTE":
            if reference[:2] == "C'":
                object_code_arr.append(str_to_ascii(reference[2:len(reference)-1]))

            elif reference[:2] == "X'":
                object_code_arr.append(reference[2:len(reference)-1])
                
        elif ins == "RSUB":
            object_code_arr.append("4F0000")

        else:
            if "+" in ins:
                opcode = OPTAB[ins[1:]][1]
            else:       
                opcode = OPTAB[ins][1]
            bin_opcode1 = bin(int(opcode, 16))[2:].zfill(8)
            binary_opcode = bin_opcode1[:len(bin_opcode1)-2]

            if ins in format1:
                object_code_arr.append(opcode)        

            elif ins in format2:
                first_reg = reference[0]
                if ins == "CLEAR" or ins == "TIXR" or ins == "SVC":
                    object_code_arr.append(opcode+get_addr(first_reg)+"0")            
                
                else:
                    last_reg = reference_arr[index][2]
                    object_code_arr.append(opcode + get_addr(first_reg) + get_addr(last_reg))

            elif ins in format3:
                e = "0"

                if reference.startswith("#"):
                    n = "0"
                    i = "1"
                    x = "0"
                    b = "0"
                    p = "0"


                    if ",X" in reference:
                        x = "1"
                        reference = reference[:len(reference)-2]
                        
                    if(reference[1:].isdigit()):
                        disp = int(reference[1:])
                    else:
                        TA1 = get_addr(reference[1:])
                        if location_ctr_arr[index+1] == "----":
                            disp = int(TA1,16) - int(location_ctr_arr[index+2],16)
                        else:
                            disp = int(TA1,16) - int(location_ctr_arr[index+1],16)
                        if(-2047 <= disp <= 2048):
                            p="1"       
                        else:
                            disp = hex(int(TA1,16) - int(base))
                            b ="1"
                    


                    if disp < 0:
                       disp = format(disp + (1 << 12), '03X')
                    TA = str(binary_opcode) + n + i + x + b + p + e
                    hex_objCode = format(int(TA, 2), '02X') + format(disp, '03X')
                    object_code_arr.append(hex_objCode)            
                
                elif reference.startswith("@"):
                    n = "1"
                    i = "0"
                    x = "0"
                    b = "0"
                    p = "0"

                    if ",X" in reference:
                        x = "1"
                        reference = reference[:len(reference)-2]
        
                    TA1 = get_addr(reference[1:])
                    if location_ctr_arr[index+1] == "----":
                        disp = str(hex(int(TA1,16) - int(location_ctr_arr[index+2],16)))
                    else:
                        disp = int(TA1,16) - int(location_ctr_arr[index+1],16)
                    if(-2047 <= disp <= 2048):
                        p="1"
                    else:
                        disp = int(TA1,16) - int(base)
                        b ="1"
                    

                    if disp < 0:
                        disp = format(disp + (1 << 12), '03X')

                    TA = str(binary_opcode) + n + i + x + b + p + e
                    hex_objCode = format(int(TA, 2), '02X') + format(disp, '03X')
                    object_code_arr.append(hex_objCode)
                else:
                    n = "1"
                    i = "1"
                    x = "0"
                    b = "0"
                    p = "0"

                    if ",X" in reference:
                        x = "1"
                        reference = reference[:len(reference)-2]

                    

            
                    TA1 = get_addr(reference)
                    if location_ctr_arr[index+1] == "----":
                        disp = int(TA1,16) - int(location_ctr_arr[index+2],16)
                    else:       
                        disp = int(TA1,16) - int(location_ctr_arr[index+1],16)
                        
                    if(-2047 <= disp <= 2048):       
                        p="1"       
                    else:       
                        disp = int(TA1,16) - int(base)
                        b ="1"

                    if disp < 0:
                        disp = format(disp + (1 << 12), '03X')

                        
                    TA = str(binary_opcode) + n + i + x + b + p + e
                    hex_objCode = str(hex(int(TA,2))[2:]) + str(disp)
                    object_code_arr.append(hex_objCode)
                
            elif ins in format4:
                e = "1"
                if reference.startswith("#"):
                    n = "0"
                    i = "1"
                    x = "0"
                    b = "0"
                    p = "0"

                    if ",X" in reference:
                        x = "1"
                        reference = reference[:len(reference)-2]
                        
                    if(reference[1:].isdigit()):
                        address = hex(int(reference[1:]))[2:].zfill(5)
                    else:
                        TA1 = get_addr(reference[1:]).zfill(5)
                    
                    TA = str(binary_opcode) + n + i + x + b + p + e
                    hex_objCode = format(int(TA, 2), '08X')
                    object_code_arr.append(hex_objCode + address)
                
                elif reference.startswith("@"):
                    n = "1"       
                    i = "0"       
                    x = "0"       
                    b = "0"       
                    p = "0"

                    if ",X" in reference:
                        x = "1"
                        reference = reference[:len(reference)-2]
                        
                    TA1 = get_addr(reference[1:]).zfill(5)
                    
                    TA = str(binary_opcode) + n + i + x + b + p + e
                    hex_objCode = format(int(TA, 2), '08X')
                    object_code_arr.append(hex_objCode + address)
                    
                else:
                    n = "1"       
                    i = "1"       
                    x = "0"       
                    b = "0"       
                    p = "0"
                    address = "" 
                    for i in modif_arr:
                        i = int(i)
                        address = "" 
                       
                        if ",X" in reference:
                          x = "1"
                          reference = reference[:len(reference)-2]
                          address = get_addr(reference)
                          


                    
                    TA = str(binary_opcode) + n + str(i) + x + b + p + e
                    hex_objCode = format(int(TA, 2), '08X')
                    object_code_arr.append(hex_objCode + address)
                    modif_arr.append(i)
                    


                    
  
    pass2_success = True 
    #for index in range (len(instruction)):
          # print(f"{location_ctr_arr[index]} {label_arr[index].ljust(6, ' ')} {instruction_arr[index].ljust(6, ' ')} {reference_arr[index].ljust(8, ' ')} {object_code_arr[index]}")

# direct 
# create table witw frame 
def create_table():  
    global pass2_success
    if pass2_success==False:
        print("pass 2 was unsuccessful")
        return
    print( len(object_code_arr))
    print(len(label_arr))
    
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

    print(df.to_markdown(index=False, tablefmt='fancy_grid'))
    print(symb.to_markdown(index=False, tablefmt='fancy_grid'))

# function to generate the HTE record from the object code list
def generate_HTE(object_code_list):
    hte_record = ""
    global prog_name, prog_length, pass2_success
    if pass2_success == False:
        return
    start_addr = reference_arr[0].zfill(6)
    if len(prog_name) < 6:
        prog_name = prog_name.zfill(6)
    header_record = f"H^{prog_name}^{start_addr}^{prog_length}"
    hte_record += header_record + "\n"
    text_record = ""
    modif_record = ""
    total_modif_record = ""
    text_record_length = 0
    text_record_start = ""
    for i in range(1, len(object_code_list) - 1):
        object_code = object_code_list[i]
        if object_code == "No object code":
            if text_record != "":
                text_record = f"T^{text_record_start}^{format(text_record_length, '0>2X')}{text_record}"
                hte_record += text_record + "\n"
            text_record = ""
            text_record_length = 0
            text_record_start = ""
        else:
            object_code_length = int(round(len(object_code) / 2.0))
            if text_record_length + object_code_length > 30:
                text_record = f"T^{text_record_start}^{format(text_record_length, '0>2X')}{text_record}"
                hte_record +=  text_record + "\n"
                text_record = ""
                text_record_length = 0
                text_record_start = ""
            if text_record == "":
                text_record_start = location_ctr_arr[i].zfill(6)
            text_record += f"^{object_code}"
            text_record_length += object_code_length
    if text_record != "":
        text_record= f"T^{text_record_start}^{format(text_record_length, '0>2X')}{text_record}"
        hte_record += text_record + "\n"
    for i in modif_arr:
        i = int(i)
        
        location_ctr_arr[i] = sum_hex_int(location_ctr_arr[i], 1)
        modif_addr = location_ctr_arr[i]
        
        modif_record = f"M^{modif_addr}^05^+{prog_name}"
        total_modif_record = modif_record + "\n" 
        
        if(total_modif_record != ""):
            hte_record += total_modif_record
    end_record = f"E^{start_addr}"
    hte_record += end_record + "\n"
    print("\nHTEM RECORD: \n")
    print(hte_record)
                       
                
def main():
    f = open("inSICXE.txt", "r")
    first_pass(f)
    second_pass()
    create_table()
    generate_HTE(object_code_arr)
            
    

main()