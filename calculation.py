binary_common = [
    '@SP',
    'AM=M-1 // A = *SP-1, also (*SP)--',
    'D=M    // D = *(*SP-1)',
    'A=A-1  // A = *SP-2',
]  # D holds *(*SP-1), M holds *(*SP-2), A holds *SP-2


def write_add() -> list:
    return [
        *binary_common,
        'M=D+M  // *(*SP-2) += *(*SP-1)',
    ]


def write_sub() -> list:
    return [
        *binary_common,
        'M=M-D  // *(*SP-2) -= *(*SP-1)',
    ]


def write_and() -> list:
    return [
        *binary_common,
        'M=D&M  // *(*SP-2) &= *(*SP-1)',
    ]


def write_or() -> list:
    return [
        *binary_common,
        'M=D|M  // *(*SP-2) |= *(*SP-1)',
    ]


def write_eq(eq_count: int) -> list:
    # initialize :EQ: subroutine, when eq is called for the first time
    init = [
        '@DEF_:EQ:',
        '0;JMP  // :EQ: definition -> jump over',
        '',
        '(:EQ:)',
        '@R15',
        'M=D    // R15 = return address',

        *binary_common,
        'MD=M-D // D = *(*SP-2) = *(*SP-2) - *(*SP-1)',
        '@:EQ_FLIP:',
        'D;JEQ  // if *(*SP-2) == 0, flip all bits',
        '       // else: set *(*SP-2) = -1 first',
        '@SP    // now M = *SP-1',
        'A=M-1  // A = *SP-2',
        'M=-1   // *(*SP-2) = -1',
        '(:EQ_FLIP:)',
        '@SP    // now M = *SP-1',
        'A=M-1  // A = *SP-2',
        'M=!M   // flip all bits to correct value',
        '@R15',
        'A=M',
        '0;JMP  // return',
        '',
        '(DEF_:EQ:)',
        '',
    ]

    # call previously initialized :EQ:
    call = [
        '@RETURN_EQ_%s' % eq_count,
        'D=A',
        '@:EQ:',
        '0;JMP',
        '(RETURN_EQ_%s)' % eq_count,
    ]

    if eq_count:
        return call
    else:
        return init + call


def write_gt(gt_count: int) -> list:
    # initialize :GT: subroutine, when gt is called for the first time
    init = [
        '@DEF_:GT:',
        '0;JMP  // :GT: definition -> jump over',
        '',
        '(:GT:)',
        '@R15',
        'M=D    // R15 = return address',

        *binary_common,
        'D=M-D  // D = *(*SP-2) - *(*SP-1)',
        '@:TRUE_GT:',
        'D;JGT  // jump if D > 0',
        '       // else:',
        '@SP    // now M = *SP-1',
        'A=M-1  // A = *SP-2',
        'M=0    // false',
        '@R15',
        'A=M',
        '0;JMP  // return',
        '',
        '(:TRUE_GT:)',
        '@SP    // now M = *SP-1',
        'A=M-1  // A = *SP-2',
        'M=-1   // true',
        '@R15',
        'A=M',
        '0;JMP  // return',
        '',
        '(DEF_:GT:)',
        '',
    ]

    # call previously initialized :GT:
    call = [
        '@RETURN_GT_%s' % gt_count,
        'D=A',
        '@:GT:',
        '0;JMP',
        '(RETURN_GT_%s)' % gt_count,
    ]

    if gt_count:
        return call
    else:
        return init + call


def write_lt(lt_count: int) -> list:
    # initialize :LT: subroutine, when lt is called for the first time
    init = [
        '@DEF_:LT:',
        '0;JMP  // :LT: definition -> jump over',
        '',
        '(:LT:)',
        '@R15',
        'M=D    // R15 = return address',

        *binary_common,
        'D=M-D  // D = *(*SP-2) - *(*SP-1)',
        '@:TRUE_LT:',
        'D;JLT  // jump if D < 0',
        '       // else:',
        '@SP    // now M = *SP-1',
        'A=M-1  // A = *SP-2',
        'M=0    // false',
        '@R15',
        'A=M',
        '0;JMP  // return',
        '',
        '(:TRUE_LT:)',
        '@SP    // now M = *SP-1',
        'A=M-1  // A = *SP-2',
        'M=-1   // true',
        '@R15',
        'A=M',
        '0;JMP  // return',
        '',
        '(DEF_:LT:)',
        '',
    ]

    # call previously initialized :LT:
    call = [
        '@RETURN_LT_%s' % lt_count,
        'D=A',
        '@:LT:',
        '0;JMP',
        '(RETURN_LT_%s)' % lt_count,
    ]

    if lt_count:
        return call
    else:
        return init + call


def write_not() -> list:
    return [
        '@SP',
        'A=M-1  // A = *SP-1',
        'M=!M   // *SP-1 = !(*SP-1)',
    ]


def write_neg() -> list:
    return [
        '@SP',
        'A=M-1  // A = *SP-1',
        'M=-M   // *SP-1 = -(*SP-1)',
    ]
