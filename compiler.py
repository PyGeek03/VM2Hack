import contextlib, os
import mem_access
import calculation as calc
import function
import branching

# Routing table for functions without argument
no_arg = {
    'add': calc.write_add,
    'sub': calc.write_sub,
    'and': calc.write_and,
    'or' : calc.write_or,

    'not': calc.write_not,
    'neg': calc.write_neg,

    'return': function.write_return,
}

# Routing table for functions with arguments
with_args = {
    'eq' : calc.write_eq,
    'gt' : calc.write_gt,
    'lt' : calc.write_lt,

    'push'     : mem_access.write_push,
    'pop'      : mem_access.write_pop,

    'label'    : branching.write_label,
    'goto'     : branching.write_goto,
    'if-goto'  : branching.write_if,

    'call'     : function.write_call,
    'function' : function.write_function,
}


def bootstrap(asm_filepath: str) -> None:
    '''Write Hack bootstrap code'''

    init_asm = [
        "// bootstrap",
        '',
        "@256",
        "D=A",
        "@SP",
        "M=D",
        '',
        "@300",
        "D=A",
        "@LCL",
        "M=D",
        '',
        "@400",
        "D=A",
        "@ARG",
        "M=D",
        '',
        "@3000",
        "D=A",
        "@THIS",
        "M=D",
        '',
        "@3010",
        "D=A",
        "@THAT",
        "M=D",
        '',
    ]  # TODO: add call to Sys.init

    with open(asm_filepath, 'w') as asm_file:  # overwrite current .asm file, if exists
        for line in init_asm: 
            asm_file.write('%s\n' % line)


def compile(asm_filepath: str, vm_files: list) -> None:
    '''Main compiler'''

    # Keep count of "stateful" commands
    count = {
        'eq': 0,
        'lt': 0,
        'gt': 0,
        'call': 0,
    }

    # Bootstrap asm file
    bootstrap(asm_filepath)

    # Compile all vm file in the list into the asm file
    for vm_filepath in vm_files:
        filename = os.path.basename(asm_filepath)[:-4]  # for static segment & function command
        with open(vm_filepath) as vm_file, open(asm_filepath, 'a') as asm_file:
            for vm_line in vm_file:
                # Document the vm source line
                asm_comment = '// ' + vm_line
                asm_file.write(asm_comment)

                # Tokenize and analyze the vm source line
                tokens = vm_line.split("//")[0].split()  # ignore comments
                try:
                    command, *args = tokens
                except ValueError:  # blank line or comment line
                    continue

                # Compile!
                if command in no_arg:
                    # commands without argument
                    asm_block = no_arg[command]()
                elif command in count:
                    # "stateful" commands
                    asm_block = with_args[command](*args, count[command])
                    count[command] += 1
                elif args[0] == 'static':
                    # accessing static segment is quite pesky
                    label = filename + "." + str(args[1])
                    asm_block = with_args[command]('static', label)
                else:
                    # other commands with arguments
                    asm_block = with_args[command](*args)

                # Finally, write to asm file
                for line in asm_block:
                    asm_file.write('%s\n' % line)
                asm_file.write('\n')  # separate blocks