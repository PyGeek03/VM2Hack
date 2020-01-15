def write_push(segment, index):
    # constant and pointer are "virtual" segments
    if segment == 'constant': 
        head = (
            "@"              + str(index) + "\n"
            "D=A    // D = " + str(index) + "\n"
        )
    elif segment == 'pointer':
        head = (
            "@" + str(3+index) +    "\n" # index = 0: this, index = 1: that
            "D=A    // D = pointer" "\n"
        )
    else:
        proper_segments = {
            'local'     : "@" + str(1+index),
            'argument'  : "@" + str(2+index),
            'this'      : "@" + str(3+index),
            'that'      : "@" + str(4+index),
            'temp'      : "@" + str(5+index),
            'static'    : "@" + index,
        }
        head = (
            proper_segments[segment]  + "\n"
            "D=M  // D = memory value"  "\n"
        )

    body = (
        "@0     // A = SP"  "\n"
        "A=M    // A = *SP" "\n"
        "M=D    // *SP = D" "\n"
        "@0     // A = SP"  "\n"
        "M=M+1  // (*SP)++" "\n"
        "\n"
    )

    return head + body


def write_pop(segment, index):
    pass