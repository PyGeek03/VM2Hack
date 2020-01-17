from typing import Tuple, List

import calculate
import branching
import function
import mem_access


pointers_base = ((256, 'SP'), (300, 'LCL'), (400, 'ARG'), (3000, 'THIS'), (3010, 'THAT'))
call_sys_init, _ = function.write_call('Sys.init', '0', {'function': 'Boot.0', 'call_count': 0})
bootstrap_dir = tuple(
    (f"@{address}" "\n"
      "D=A"        "\n"
     f"@{pointer}" "\n"
      "M=D"        "\n") for address, pointer in pointers_base
) + call_sys_init

# Commands that do not depend on or modify the state
stateless = {
    '//': lambda: (),  # comments do nothing...

    'add': calculate.write_add,
    'sub': calculate.write_sub,
    'and': calculate.write_and,
    'or' : calculate.write_or,
    'not': calculate.write_not,
    'neg': calculate.write_neg,
}

# Commands that depend on and/or modify the state
stateful = {
    'eq' : calculate.write_eq,
    'gt' : calculate.write_gt,
    'lt' : calculate.write_lt,

    'label'  : branching.write_label,
    'goto'   : branching.write_goto,
    'if-goto': branching.write_if,

    'function': function.write_function,
    'call'    : function.write_call,
    'return'  : function.write_return,

    'push': mem_access.write_push,
    'pop' : mem_access.write_pop,
}


def parse(vm_line: str) -> Tuple[str, List[str]]:
    '''Tokenize and parse the source vm line'''
    tokens = vm_line.split("//")[0].split()  # ignore comments
    try:
        command, *args = tokens
    except ValueError:              # blank line
        command, args = '//', []    # no difference from a comment
    
    return (command, args)


def compile_line(vm_line: str, state: dict) -> Tuple[Tuple[str, ...], dict]:
    # Parse
    command, args = parse(vm_line)

    # Compile!
    if command in stateless:
        asm_block = stateless[command]()
        return asm_block, state
    else:
        asm_block, new_state = stateful[command](*args, state)
        return asm_block, new_state