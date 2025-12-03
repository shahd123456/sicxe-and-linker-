from tabulate import tabulate

def hex_to_int(hex_str):
    try:
        return int(hex_str, 16)
    except ValueError:
        return 0

def int_to_hex_str(value, width):
    return format(value, f'0{width}X')

def linker_loader(linker):
    with open(linker, 'r') as file:
        input_text = file.read()

    memory = [0] * 0x1000000  # Initialize memory with zeros
    base_address = None
    program_data = []

    lines = input_text.split('\n')

    for line in lines:
        if line.startswith('HXPROG'):
            if program_data:
                # Display the first table
                print("\nControl Section Table:")
                for entry in program_data:
                    entry[1] = int_to_hex_str(entry[1], 6)
                    entry[2] = int_to_hex_str(entry[2], 6)
                print(tabulate(program_data, headers=['Control Section', 'Address', 'Length'],
                               tablefmt='grid', showindex=False))

                # Display a separator between tables
                print("\n" + "=" * 50 + "\n")

                program_data = []  # Reset program_data for the next program

            base_address = hex_to_int(line[7:13])
            control_section = line[1:7].strip()
            program_data.append([control_section, base_address, 0])

        elif line.startswith('T') and base_address is not None:
            text_record = line[1:]
            address = base_address + hex_to_int(text_record[0:6])
            length = hex_to_int(text_record[6:8])
            data = text_record[8:]

            for i in range(0, length * 2, 2):
                value = hex_to_int(data[i:i+2]) 
#Within the loop, two characters are extracted from the data string at positions i and i+1. These two characters represent a hexadecimal byte, which is then converted to an integer
                # using the hex_to_int function. This integer value (value) is the data to be stored in memory.
                if address + i // 2 < len(memory):
                    memory[address + i // 2] = value #If the memory address is valid,
                    #the value is stored in the memory array at the calculated address.
                    if program_data:
                     program_data[-1][2] = max(program_data[-1][2], address + i // 2 - base_address + 1) # and the difference between 
                        #the current memory address and the base address, plus 1.
                        #This ensures that the length is always the maximum memory location used by the current control section.

    # Display the second table for the last program
    if program_data:
        print("\nControl Section Table:")
        for entry in program_data:
            entry[1] = int_to_hex_str(entry[1], 6)
            entry[2] = int_to_hex_str(entry[2], 6)
        print(tabulate(program_data, headers=['Control Section', 'Address', 'Length'],
                       tablefmt='grid', showindex=False))

        # Display a separator between tables
        print("\n" + "=" * 50 + "\n")

    # Display the third table
    print("\nMemory Table:")
    memory_data = [[int_to_hex_str(i, 6), int_to_hex_str(value, 2)] for i, value in enumerate(memory) if value != 0]
    print(tabulate(memory_data, headers=['Address', 'Value'], tablefmt='grid', showindex=False))

if __name__ == "__main__":
    linker_loader("linker.txt")

























