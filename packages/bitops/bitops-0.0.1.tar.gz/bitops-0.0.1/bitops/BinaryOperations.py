import aenum


class ENDIANNESS(aenum.AutoNumberEnum):
    UNKLNOWN = (),
    BIG      = (),
    LITTLE   = (),


def get_bit(value, n, endiannes = ENDIANNESS.BIG):
    if endiannes == ENDIANNESS.BIG:
        return ((value >> n & 1) != 0)
    elif endiannes == ENDIANNESS.LITTLE:
        return ((value << n & 1) != 0)
    else:
        raise ValueError("Endianness is not properly set - not able to decite which bit to return")


def set_bit(value, n, endiannes = ENDIANNESS.BIG):
    if endiannes == ENDIANNESS.BIG:
        return value | (1 << n)
    elif endiannes == ENDIANNESS.LITTLE:
        return value | (1 >> n)
    else:
        raise ValueError("Endianness is not properly set - not able to decite which bit to return")


def clear_bit(value, n, endiannes = ENDIANNESS.BIG):
    if endiannes == ENDIANNESS.BIG:
        return value & ~(1 << n)
    elif endiannes == ENDIANNESS.LITTLE:
        return value & ~(1 >> n)
    else:
        raise ValueError("Endianness is not properly set - not able to decite which bit to return")


def get_bit_range_as_int(value, start, end, endiannes = ENDIANNESS.BIG):
    # print(f"Byte to be analysed: {value:02X} = {value:b}")

    if start >= end:
        AssertionError(f"'end' sall be bigger than 'start', condition {start} >= {end} is not satisfied")

    value_byte = value.to_bytes(length = 1, byteorder = "big")

    mask = 0x00
    if endiannes == ENDIANNESS.BIG:
        for num in range(start, end):
            mask = mask | (1 << num)
    else:
        for num in range(8-end, 8-start):
            mask = mask | (1 << num)

    if endiannes == ENDIANNESS.BIG:
        return (int.from_bytes(value_byte, byteorder = "big") & mask) >> start
    else:
        return (int.from_bytes(value_byte, byteorder = "little") & mask) >> 8-start


if __name__ == "__main__":
    print(get_bit_range_as_int(0x6F, 5, 6))
