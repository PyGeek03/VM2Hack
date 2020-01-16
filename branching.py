def write_label(label: str) -> tuple:
    return (
        f'({label})',
    )


def write_goto(label: str) -> tuple:
    return (
        f'@{label}',
        '0;JMP',
    )


def write_if(label: str) -> tuple:
    return (
        '@SP',
        'AM=M-1 // A = SP-1, also SP--',
        'D=M    // D = *(SP-1)',
        f'@{label}',
        'D;JNE  // jump if *(SP-1) != 0',
    )