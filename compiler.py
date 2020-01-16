import mem_access
import calculation as calc
import function
import branching

pointers_base = [(256, 'SP'), (300, 'LCL'), (400, 'ARG'), (3000, 'THIS'), (3010, 'THAT')]

# Hack bootstrap code
bootstrap = (
    "// bootstrap",
    '',
    *[(f"@{address}" "\n"
        "D=A"        "\n"
       f"@{pointer}" "\n"
        "M=D"        "\n") for address, pointer in pointers_base],
    #*function.write_call('Sys.init', 0, 0),
)  # TODO: enable call to Sys.init after passing SimpleFunction test & before NestedCall test

# Dispatch table for commands
compile = {
    'add': calc.write_add,
    'sub': calc.write_sub,
    'and': calc.write_and,
    'or' : calc.write_or,
    'eq' : calc.write_eq,
    'gt' : calc.write_gt,
    'lt' : calc.write_lt,
    'not': calc.write_not,
    'neg': calc.write_neg,

    'push': mem_access.write_push,
    'pop' : mem_access.write_pop,

    'if-goto': branching.write_if,
    'label'  : branching.write_label,
    'goto'   : branching.write_goto,

    'function': function.write_function,
    'call'    : function.write_call,
    'return'  : function.write_return,
}

# Groups of commands that are scoped
branching_commands = {'label', 'goto', 'if-goto'}
mem_access_commands = {'push', 'pop'}


def compile_line(command: str, args: list, scope: dict, count: dict) -> tuple:
    if command == '//':
        return ()

    elif command in count:
        return compile[command](*args, count[command])

    elif command in mem_access_commands and args[0] == 'static':
        # accessing static segment is scoped by filename
        static_label = f"{scope['filename']}.{args[1]}"
        return compile[command]('static', static_label)

    elif command in branching_commands:
        # branching is scoped by label's function
        current_function = scope['function'][-1]
        branching_label = f"{current_function}.{args[0]}"
        return compile[command](branching_label)

    else:
        return compile[command](*args)