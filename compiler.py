import mem_access
import calculation as calc
import function
import branching


def compile(vm_filepath):
    filepath = vm_filepath[:-3]
    filename = filepath.split("/")[-1]
    asm_filepath = filepath + '.asm'

    with open(vm_filepath) as vm_file, open(asm_filepath, 'w') as asm_file:
        # Write Hack bootstrap code
        init_asm = (
            "// Bootstrap"          "\n"
            "@256   // set SP=256"  "\n"
            "D=A"                   "\n"
            "@0"                    "\n"
            "M=D"                   "\n"
        )
        asm_file.write(init_asm)

        # Set up routing table for commands without argument
        no_arg = {
            'add': calc.write_add,
            'sub': calc.write_sub,
            'and': calc.write_and,
            'or' : calc.write_or,

            'eq' : calc.write_eq,
            'gt' : calc.write_gt,
            'lt' : calc.write_lt,

            'not': calc.write_not,
            'neg': calc.write_neg,
            'return': function.write_return,
        }

        # Set up routing table for commands with arguments
        with_args = {
            'push'     : mem_access.write_push,
            'pop'      : mem_access.write_pop,
            'label'    : branching.write_label,
            'goto'     : branching.write_goto,
            'if-goto'  : branching.write_if,
            'call'     : function.write_call,
            'function' : function.write_function,
        }

        # Go through vm file, line by line
        for vm_line in vm_file:
            # Skip blank lines
            if vm_line == "\n":
                continue

            # Document the vm source line
            asm_header = '// ' + vm_line

            # Analyze the vm source line
            tokens = vm_line.split()
            command, *args = tokens

            # Compile!
            if command == '//':
                # skip comment lines
                asm_line = ""
            elif args == []:
                # commands without argument
                asm_line = no_arg[command]()
            elif args[0] == 'static':
                # accessing static segment is quite pesky
                label = filename + "." + str(args[1])
                asm_line = with_args[command]('static', label)
            else:
                # commands with arguments
                asm_line = with_args[command](*args)

            # Finally, write to asm file
            asm_block = asm_header + asm_line
            print(asm_block, end="")
            asm_file.write(asm_block)
