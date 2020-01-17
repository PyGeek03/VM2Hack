import sys
from pathlib import Path
from typing import List

from compiler import bootstrap_dir, compile_line

def translate(asm_filepath: Path, vm_files: List[Path]) -> None:
    '''Main translator'''
    # Initialize the translation state
    state = {
        "class"     : "",
        "function"  : "",
        "eq_count"  : 0,
        "lt_count"  : 0,
        "gt_count"  : 0,
        "call_count": 0,
    }

    # Bootstrap asm file, overwrite if exists
    with asm_filepath.open('w') as asm_file:
        if len(vm_files) > 1:
            # translating a directory with more than 1 vm file
            asm_file.writelines(f"{line}\n" for line in bootstrap_dir)
        else:
            # simply clean old asm file, if exists
            asm_file.write('')

    # Translate all vm file in the list into the asm file
    for vm_filepath in vm_files:
        # each file is a new class
        class_name = vm_filepath.stem
        state = {**state, "class": class_name, "function": f"{class_name}.0"}

        with vm_filepath.open() as vm_file, asm_filepath.open('a') as asm_file:
            # Compile line by line
            for vm_line in vm_file:
                # Document the vm source line
                asm_doc = f"// {vm_line}"

                # Compile & update state
                asm_block, state = compile_line(vm_line, state)

                # Finally, write to asm file
                asm_file.write(asm_doc)
                if asm_block:
                    asm_file.writelines(f"{line}\n" for line in asm_block)
                    asm_file.write('\n')  # separate the blocks


def main():
    '''The program's main interface'''
    input = Path(sys.argv[1])

    if input.match("*.vm"):
        asm_filepath = input.with_suffix('.asm')
        translate(asm_filepath, [input])

    elif input.is_dir():
        # translated .asm file will be inside this directory
        vm_files = list(input.glob("*.vm"))
        if vm_files:
            asm_filepath = input / f"{input.name}.asm"
            translate(asm_filepath, vm_files)
        else:
            raise ValueError("Directory does not contain any .vm file")
    else:
        raise ValueError("Not a .vm file nor a directory")


if __name__ == "__main__":
    main()
