from typing import Tuple


def write_label(label: str, state: dict) -> Tuple[Tuple[str, ...], dict]:
    current_func = state['function']
    asm_block = (
        f"({current_func}.{label})",
    )
    return asm_block, state


def write_goto(label: str, state: dict) -> Tuple[Tuple[str, ...], dict]:
    current_func = state['function']
    asm_block = (
        f"@{current_func}.{label}",
        '0;JMP',
    )
    return asm_block, state


def write_if(label: str, state: dict) -> Tuple[Tuple[str, ...], dict]:
    current_func = state['function']
    asm_block = (
        '@SP',
        'AM=M-1 // A = SP-1, also SP--',
        'D=M    // D = *(SP-1)',
        f"@{current_func}.{label}",
        'D;JNE  // jump if *(SP-1) != 0',
    )
    return asm_block, state