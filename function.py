from typing import Tuple
import mem_access


def write_function(function: str, locals_count: str, state: dict) -> Tuple[Tuple[str, ...], dict]:
    new_state = {**state, 'function': function}
    push_local_var, _ = mem_access.write_push("constant", "0", new_state)
    asm_block = (
        f'({function})',
        f'// {locals_count} local variables'
    ) + int(locals_count) * push_local_var

    return asm_block, new_state


def write_return(state: dict) -> Tuple[Tuple[str, ...], dict]:
    prep_return_value, _ = mem_access.write_pop("argument", "0", state)
    prep_return_value_and_SP = prep_return_value + (
        'D=A+1  // A = ARG => D = ARG + 1',
        '@SP',
        'M=D    // SP = ARG + 1',
        '',
    )
    asm_block = (
        '@LCL   // endFrame',
        'D=M    // D = endFrame',
        '@5',
        'A=D-A  // A =   endFrame - 5',
        'D=M    // D = *(endFrame - 5) = retAddr',
        '@R15',
        'M=D    // R15 = retAddr',
        '',
    ) + prep_return_value_and_SP + (
        '@LCL   // endFrame',
        'AM=M-1 // A =   endFrame - 1 (storing "saved THAT"), also LCL--',
        'D=M    // D = *(endFrame - 1)',
        '@THAT',
        'M=D    // THAT = *(endFrame - 1)',
        '',
        '@LCL   // endFrame - 1',
        'AM=M-1 // A =   endFrame - 2 (storing "saved THIS"), also LCL--',
        'D=M    // D = *(endFrame - 2)',
        '@THIS',
        'M=D    // THIS = *(endFrame - 2)',
        '',
        '@LCL   // endFrame - 2',
        'AM=M-1 // A =   endFrame - 3 (storing "saved ARG"), also LCL--',
        'D=M    // D = *(endFrame - 3)',
        '@ARG',
        'M=D    // ARG = *(endFrame - 3)',
        '',
        '@LCL   // endFrame - 3',
        'A=M-1  // A =   endFrame - 4 (storing "saved LCL")',
        'D=M    // D = *(endFrame - 4)',
        '@LCL',
        'M=D    // LCL = *(endFrame - 4)',
        '',
        '@R15',
        'A=M    // A = retAddr',
        '0;JMP  // return!',
    )

    return asm_block, state


def write_call(callee: str, args_count: str, state: dict) -> Tuple[Tuple[str, ...], dict]:
    caller = state['function']
    count = state['call_count']
    return_address = f'{caller}$ret.{count}'

    asm_block = (
       f'@{return_address}',
        'D=A    // D = returnAddress',
        '@SP',
        'M=M-1  // SP-- (temporarily, will increment later)',
        'AM=M+1 // now SP will "automatically follow" wherever we write to the stack',
        'M=D    // push returnAddress',
        '',
    ) + tuple(
      (f'@{pointer}'                '\n'
       f'D=M    // D = {pointer}'   '\n'
        '@SP'                       '\n'
        'AM=M+1'                    '\n'
       f'M=D    // push {pointer}'  '\n'
      ) for pointer in ('LCL', 'ARG', 'THIS', 'THAT')
    ) + (
        '@SP',
        'MD=M+1 // D = SP, also SP++ (as promised)',
        '@LCL',
        'M=D    // LCL = SP',
       f'@{5 + int(args_count)}',
        'D=D-A  // D = SP - 5 - nArgs',
        '@ARG',
        'M=D    // ARG = SP - 5 - nArgs',
       f'@{callee}  // goto {callee}',
        '0;JMP',
       f'({return_address})'
    )

    new_state = {**state, 'call_count': count + 1}
    return asm_block, new_state