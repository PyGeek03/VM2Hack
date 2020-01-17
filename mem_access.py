from typing import Tuple


def _find_addr(segment: str, index: str, state: dict) -> str:
    latt_common = (
        'D=M    // D = segmentPointer'  '\n'
        f'@{index}'                     '\n'
        f'A=A+D  // addr = segmentPointer + {index}'
    )
    address = {
        'constant': f'@{index}',
        'temp'    : f'@{5 + int(index)}    // addr = 5 + {index}',
        'pointer' : f"@{'THIS' if index == '0' else 'THAT'}",
        'static'  : f"@{state['class']}.{index}",

        'local'   : f'@LCL\n{latt_common}',
        'argument': f'@ARG\n{latt_common}',
        'this'    : f'@THIS\n{latt_common}',
        'that'    : f'@THAT\n{latt_common}',
    }
    return address[segment]


def write_push(segment: str, index: str, state: dict) -> Tuple[Tuple[str, ...], dict]:
    addr = _find_addr(segment, index, state)

    if segment == 'constant':
        D = f'D=A    // D = {index}'
    else:
        D =  'D=M    // D = *addr'

    asm_block = (
        addr,
        D,
        '@SP',
        'A=M',
        'M=D    // *SP = D',
        '@SP',
        'M=M+1  // SP++',
    )

    return asm_block, state


def write_pop(segment: str, index: str, state: dict) -> Tuple[Tuple[str, ...], dict]:
    addr = _find_addr(segment, index, state)

    if segment == 'pointer':
        asm_block = (
            '@SP',
            'AM=M-1 // SP--',
            'D=M    // D = *SP',
            addr,
           f"M=D    // {'THIS' if index == '0' else 'THAT'} = *SP",
        )
    else:
        asm_block = (
            addr,
            'D=A    // D = addr',
            '@SP',
            'AM=M-1 // SP--',
            '// now M = *SP, D = addr, we have to make A = addr, D = *SP',
            'D=D-M  // addr - *SP',
            'A=M+D  // *SP + (addr - *SP) = addr!',
            'D=A-D  // addr - (addr - *SP) = *SP!',
            'M=D    // *addr = *SP!!!',
        )
    
    return asm_block, state