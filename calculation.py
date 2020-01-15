binary_common = (
    "@0     // A = SP"              "\n"
    "AM=M-1 // A = *SP = *SP-1"     "\n"  # also move stack pointer up
    "D=M    // D = *(*SP-1)"        "\n"
    "A=A-1  // A = *SP-2"           "\n"
)  # D holds *(*SP-1), M holds *(*SP-2), A holds *SP-2


def write_add():
    return (
        binary_common +
        "M=D+M  // *(*SP-2) += *(*SP-1)"  "\n"
        "\n"
    )


def write_sub():
    pass


def write_and():
    pass


def write_or():
    pass


def write_eq():
    return (
        binary_common +
        "MD=M-D // D = *(*SP-2) = *(*SP-2) - *(*SP-1)"  "\n"
        "@FLIP"                                         "\n"
        "D;JEQ  // if *(*SP-2) == 0, flip all bits"     "\n"
        "       // else: set *(*SP-2) = -1 first"       "\n"
        "@0     // A = SP (M = *SP-1)"                  "\n"
        "A=M-1  // A = *SP-2"                           "\n"
        "M=-1   // *(*SP-2) = -1"                       "\n"
        "(FLIP)"                                        "\n"
        "@0     // A = SP (M = *SP-1)"                  "\n"
        "A=M-1  // A = *SP-2"                           "\n"
        "M=!M   // flip all bits to correct value"      "\n"
        "\n"
    )


def write_gt():
    pass


def write_lt():
    pass


def write_not():
    pass


def write_neg():
    pass
