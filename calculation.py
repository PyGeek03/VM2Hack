binary_common = (
    '@SP',
    'AM=M-1 // A = SP-1, also SP--',
    'D=M    // D = *(SP-1)',
    'A=A-1  // A = SP-2',
)  # D holds *(SP-1), M holds *(SP-2), A holds SP-2


def write_add() -> tuple:
    return (
        *binary_common,
        'M=D+M  // *(SP-2) += *(SP-1)',
    )


def write_sub() -> tuple:
    return (
        *binary_common,
        'M=M-D  // *(SP-2) -= *(SP-1)',
    )


def write_and() -> tuple:
    return (
        *binary_common,
        'M=D&M  // *(SP-2) &= *(SP-1)',
    )


def write_or() -> tuple:
    return (
        *binary_common,
        'M=D|M  // *(SP-2) |= *(SP-1)',
    )


def _init_common(sub: str) -> tuple:
    return (
       f'@DEF_{sub}',
       f'0;JMP  // {sub} definition -> jump over',
        '',
       f'({sub})',
        '@R15',
        'M=D    // R15 = return address',

        *binary_common,
        'D=M-D  // D = *(SP-2) - *(SP-1)',
       f'@:TRUE_{sub}:',
       f'D;J{sub}  // jump if true',
        '       // else:',
        '@SP    // now M = SP-1',
        'A=M-1  // A = SP-2',
        'M=0    // false',
        '@R15',
        'A=M',
        '0;JMP  // return',
        '',
       f'(:TRUE_{sub}:)',
        '@SP    // now M = SP-1',
        'A=M-1  // A = SP-2',
        'M=-1   // true',
        '@R15',
        'A=M',
        '0;JMP  // return',
        '',
       f'(DEF_{sub})',
        '',
    )


def _call_common(sub: str, count: int) -> tuple:
    return (
       f'@RETURN_{sub}_{count}',
        'D=A',
       f'@{sub}',
        '0;JMP',
       f'(RETURN_{sub}_{count})',
    )


def write_eq(eq_count: int) -> tuple:
    # initialize EQ subroutine, when eq is called for the first time
    init = _init_common('EQ')

    # call previously initialized EQ
    call = _call_common('EQ', eq_count)

    if eq_count:
        return call
    else:
        return init + call


def write_gt(gt_count: int) -> tuple:
    # initialize GT subroutine, when gt is called for the first time
    init = _init_common('GT')

    # call previously initialized GT
    call = _call_common('GT', gt_count)

    if gt_count:
        return call
    else:
        return init + call


def write_lt(lt_count: int) -> tuple:
    # initialize LT subroutine, when lt is called for the first time
    init = _init_common('LT')

    # call previously initialized LT
    call = _call_common('LT', lt_count)

    if lt_count:
        return call
    else:
        return init + call


def write_not() -> tuple:
    return (
        '@SP',
        'A=M-1  // A = SP-1',
        'M=!M   // *(SP-1) = !*(SP-1)',
    )


def write_neg() -> tuple:
    return (
        '@SP',
        'A=M-1  // A = SP-1',
        'M=-M   // *(SP-1) = -*(SP-1)',
    )