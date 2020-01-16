import sys
import os
import fnmatch
from compiler import bootstrap, compile_line


def translate(asm_filepath: str, vm_files: list) -> None:
    '''Main translator'''
    # Bootstrap asm file (will overwrite if it already exists)
    with open(asm_filepath, 'w') as asm_file:
        for line in bootstrap:
            asm_file.write(f"{line}\n")
    
    # Keep count of "stateful" commands
    count = {
        'eq': 0,
        'lt': 0,
        'gt': 0,
        'call': 0,
    }

    # Translate all vm file in the list into the asm file
    for vm_filepath in vm_files:
        # accessing static segment & branching is scoped, but differently
        vm_filename = os.path.basename(vm_filepath)[:-3]
        scope = {
            'filename': vm_filename,           # static segment's scope
            'function': [f"{vm_filename}.0"],  # branching's scope
        }

        with open(vm_filepath) as vm_file, open(asm_filepath, 'a') as asm_file:
            # Compile line by line
            for vm_line in vm_file:
                # Document the vm source line
                asm_doc = f"// {vm_line}"

                # Tokenize and parse the vm source line
                tokens = vm_line.split("//")[0].split()  # ignore comments
                try:
                    command, *args = tokens
                except ValueError:  # blank line
                    asm_block = ()
                else:
                    # Compile!
                    asm_block = compile_line(command, args, scope, count)
                    # (if needed) update scope & count
                    if command == 'function':
                        function_name = args[1]
                        scope['function'].append(function_name)
                    elif command == 'return':
                        scope['function'].pop()
                    elif command in count:
                        count[command] += 1

                # Finally, write to asm file
                asm_file.write(asm_doc)
                for line in asm_block:
                    asm_file.write(f"{line}\n")
                if asm_block:
                    asm_file.write('\n')  # separate the blocks


def main():
    '''The program's main interface'''
    input = sys.argv[1]

    if input[-3:] == ".vm":
        asm_filepath = input[:-3] + ".asm"
        translate(asm_filepath, [input])
    elif os.path.isdir(input):
        # translated .asm file will be inside the directory
        asm_filepath = os.path.join(input, os.path.basename(input) + ".asm")
        for root, _, files in os.walk(input):
            vm_files = [os.path.join(root, vm_file)
                        for vm_file in fnmatch.filter(files, '*.vm')]
        if vm_files:
            translate(asm_filepath, vm_files)
        else:
            raise ValueError("Directory does not contain any .vm file")
    else:
        raise ValueError("Not a .vm file nor a directory")

    # print the translated .asm file
    with open(asm_filepath) as asm_file:
        print(asm_file.read(), end="")


if __name__ == "__main__":
    main()
