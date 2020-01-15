import sys, os, fnmatch
from compiler import compile


def main():
    input = sys.argv[1]
    if input[-3:] == ".vm":
        compile(input)
    else:
        for root, _, files in os.walk(input):
            for vm_filename in fnmatch.filter(files, '*.vm'):
                vm_filepath = os.path.join(root, vm_filename)
                compile(vm_filepath)


if __name__ == "__main__":
    main()
