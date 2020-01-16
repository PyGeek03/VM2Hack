def find_addr(segment: str, index: str) -> str:
    try:
        temp_addr = 5 + int(index)
    except ValueError:  # only static segment has non-numeric "index" (actually label)
        return '@%s' % index

    latt_common = (
        'D=M    // D = segmentPointer'          '\n'
        '@%s\n' % index
        'A=A+D  // addr = segmentPointer + i'   '\n'
    )
    numeric_segments = {
        'constant': '@%s' % index,
        'temp'    : '@%s    // addr = 5 + i' % temp_addr,
        'pointer' : '@%s' % ('THIS' if index == '0' else 'THAT'),

        'local'   : '@LCL\n%s'  % latt_common,
        'argument': '@ARG\n%s'  % latt_common,
        'this'    : '@THIS\n%s' % latt_common,
        'that'    : '@THAT\n%s' % latt_common,
    }
    return numeric_segments[segment]


def write_push(segment: str, index: str) -> list:
    addr = find_addr(segment, index)
    return [
        addr,
        'D=M    // D = *addr' if segment != 'constant' else 'D=A    // D = %s' % index,
        '@SP',
        'A=M',
        'M=D    // *SP = D',
        '@SP',
        'M=M+1  // SP++',
    ]


def write_pop(segment: str, index: str) -> list:
    addr = find_addr(segment, index)
    if segment == 'pointer':
        return [
            '@SP',
            'AM=M-1 // SP--',
            'D=M    // D = *SP',
            addr,
            'M=D    // %s = *SP' % ('THIS' if index == '0' else 'THAT'),
        ]
    return [
        addr,
        'D=A    // D = addr',
        '@SP',
        'AM=M-1 // SP--',
        '// now M = *SP, D = addr, we have to make A = addr, D = *SP',
        'D=D-M  // addr - *SP',
        'A=M+D  // *SP + (addr - *SP) = addr!',
        'D=A-D  // addr - (addr - *SP) = *SP!',
        'M=D    // *addr = *SP!!!',
    ]