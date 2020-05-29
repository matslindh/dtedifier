def degrees_string_to_float(degrees):
    hemispheres = ('S', 'N', 'W', 'E')

    hemisphere_multiplier = 1
    if degrees[-1] in hemispheres:
        if degrees[-1] in ('S', 'W'):
            hemisphere_multiplier = -1

        degrees = degrees[:-1]

    # if the seconds part is a decimal, use the two digits before the decimal
    seconds_offset = -2

    if '.' in degrees:
        seconds_offset = degrees.index('.') - 2

    seconds = degrees[seconds_offset:]
    minutes = degrees[seconds_offset - 2:seconds_offset]
    return (int(degrees[:seconds_offset - 2]) + float(minutes) / 60 + float(seconds) / 3600) * hemisphere_multiplier


def na_or_int(s):
    if s.strip() == 'NA':
        return None

    return int(s)


def empty_or_int(s):
    if isinstance(s, bytes):
        s = s.decode('ascii')

    if not s.strip():
        return None

    return int(s)


def four_digit_single_decimal(s):
    return float(s[:3] + '.' + s[3:])


def convert_signed_16bfixed(x):
    v = x & 0xffff

    if v == 0xffff:
        return None

    if v < 0x8000:
        return x

    return 0x8000 - v
