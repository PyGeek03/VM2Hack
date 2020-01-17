from typing import Tuple


def write_not() -> Tuple[str, ...]:
    return (
        '@SP',
        'A=M-1  // A = SP-1',
        'M=!M   // *(SP-1) = !*(SP-1)',
    )


def write_neg() -> Tuple[str, ...]:
    return (
        '@SP',
        'A=M-1  // A = SP-1',
        'M=-M   // *(SP-1) = -*(SP-1)',
    )


# asm lines that all binary commands need
_binary_common = (
    '@SP',
    'AM=M-1 // A = SP-1, also SP--',
    'D=M    // D = *(SP-1)',
    'A=A-1  // A = SP-2',
)  # D holds *(SP-1), M holds *(SP-2), A holds SP-2


def write_add() -> Tuple[str, ...]:
    return _binary_common + ('M=D+M  // *(SP-2) += *(SP-1)',)


def write_sub() -> Tuple[str, ...]:
    return _binary_common + ('M=M-D  // *(SP-2) -= *(SP-1)',)


def write_and() -> Tuple[str, ...]:
    return _binary_common + ('M=D&M  // *(SP-2) &= *(SP-1)',)


def write_or() -> Tuple[str, ...]:
    return _binary_common + ('M=D|M  // *(SP-2) |= *(SP-1)',)


def _is_first_compare(state: dict) -> bool:
    return state["eq_count"] + state["lt_count"] + state["gt_count"] == 0


_prep_compare = (
    '// Definitions needed for comparison commands -> jump over',
    '@:CP_DEF:',
    '0;JMP',
    '',
    '(:TRUE:)',
    '@SP    // now M = SP-1',
    'A=M-1  // A = SP-2',
    'M=-1   // true',
    '@R15',
    'A=M',
    '0;JMP  // return',
    '',
    '(:FALSE:)',
    '@SP    // now M = SP-1',
    'A=M-1  // A = SP-2',
    'M=0    // false',
    '@R15',
    'A=M',
    '0;JMP  // return',
    '',
    '(:CP_DEF:)',
    '',
)


def _init_common(sub: str) -> Tuple[str, ...]:
    return (
       f'@DEF_{sub}',
       f'0;JMP  // {sub} definition -> jump over',
        '',
       f'({sub})',
        '@R15',
        'M=D    // R15 = return address',
    ) + _binary_common + (
        'D=M-D  // D = *(SP-2) - *(SP-1)',
       f'@:TRUE:',
       f'D;J{sub}',
       f'@:FALSE:',
       f'0;JMP',
        '',
       f'(DEF_{sub})',
        '',
    )


def _call_common(sub: str, count: int) -> Tuple[str, ...]:
    return (
       f'@RETURN_{sub}_{count}',
        'D=A',
       f'@{sub}',
        '0;JMP',
       f'(RETURN_{sub}_{count})',
    )


def write_eq(state: dict) -> Tuple[Tuple[str, ...], dict]:
    sub = 'EQ'
    count = state['eq_count']
    call = _call_common(sub, count)

    if _is_first_compare(state):
        asm_block = _prep_compare + _init_common(sub) + call
    elif count == 0:
        asm_block = _init_common(sub) + call
    else:
        asm_block = call

    new_state = {**state, 'eq_count': count + 1}
    return asm_block, new_state


def write_gt(state: dict) -> Tuple[Tuple[str, ...], dict]:
    sub = 'GT'
    count = state['gt_count']
    call = _call_common(sub, count)

    if _is_first_compare(state):
        asm_block = _prep_compare + _init_common(sub) + call
    elif count == 0:
        asm_block = _init_common(sub) + call
    else:
        asm_block = call

    new_state = {**state, 'gt_count': count + 1}
    return asm_block, new_state


def write_lt(state: dict) -> Tuple[Tuple[str, ...], dict]:
    sub = 'LT'
    count = state['lt_count']
    call = _call_common(sub, count)

    if _is_first_compare(state):
        asm_block = _prep_compare + _init_common(sub) + call
    elif count == 0:
        asm_block = _init_common(sub) + call
    else:
        asm_block = call

    new_state = {**state, 'lt_count': count + 1}
    return asm_block, new_state