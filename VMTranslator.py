import sys, os, fnmatch
from compiler import compile


def main():
    '''Main function of the program'''
    input = sys.argv[1]

    if input[-3:] == ".vm":
        asm_filepath = input[:-3] + ".asm"
        compile(asm_filepath, [input])
    elif os.path.isdir(input):
        # translated .asm file will be inside the directory
        asm_filepath = os.path.join(input, os.path.basename(input) + ".asm")
        for root, _, files in os.walk(input):
            vm_files = [os.path.join(root, vm_file) for vm_file in fnmatch.filter(files, '*.vm')]
        if vm_files:
            compile(asm_filepath, vm_files)
        else:
            raise ValueError("Directory does not contain .vm file. Please try again")
    else:
        raise ValueError("Not a .vm file nor a directory. Please try again")

    # print the translated .asm file
    with open(asm_filepath) as asm_file:
        print(asm_file.read(), end="")


if __name__ == "__main__":
    main()
