def find_addr(segment: str, index: str) -> str:
    try:
        temp_addr = 5 + int(index)
    except ValueError:
        # only static segment has non-numeric "index" (actually label)
        return f'@{index}'

    latt_common = (
        'D=M    // D = segmentPointer'  '\n'
        f'@{index}'                     '\n'
        f'A=A+D  // addr = segmentPointer + {index}'
    )
    numeric_segments = {
        'constant': f'@{index}',
        'temp'    : f'@{temp_addr}    // addr = 5 + {index}',
        'pointer' : f"@{'THIS' if index == '0' else 'THAT'}",

        'local'   : f'@LCL\n{latt_common}',
        'argument': f'@ARG\n{latt_common}',
        'this'    : f'@THIS\n{latt_common}',
        'that'    : f'@THAT\n{latt_common}',
    }
    return numeric_segments[segment]


def write_push(segment: str, index: str) -> tuple:
    addr = find_addr(segment, index)
    
    if segment == 'constant':
        D = f'D=A    // D = {index}'
    else:
        D =  'D=M    // D = *addr'

    return (
        addr,
        D,
        '@SP',
        'A=M',
        'M=D    // *SP = D',
        '@SP',
        'M=M+1  // SP++',
    )


def write_pop(segment: str, index: str) -> tuple:
    addr = find_addr(segment, index)

    if segment == 'pointer':
        return (
            '@SP',
            'AM=M-1 // SP--',
            'D=M    // D = *SP',
            addr,
           f"M=D    // {'THIS' if index == '0' else 'THAT'} = *SP",
        )
    else:
        return (
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