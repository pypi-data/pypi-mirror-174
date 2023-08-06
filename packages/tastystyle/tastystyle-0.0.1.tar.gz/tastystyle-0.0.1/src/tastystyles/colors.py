def FG(*col):
    r = 255
    g = 255
    b = 255
    if len(col) == 1:
        if col[0][0] == '#':
            hex = col[0].lstrip('#')
            rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
        else:
            if col[0] == 'RED':
                r = 214
                g = 62
                b = 62
            elif col[0] == 'ORANGE':
                r = 214
                g = 143
                b = 62
            elif col[0] == 'YELLOW':
                r = 211
                g = 214
                b = 62
            elif col[0] == 'L_GREEN':
                r = 98
                g = 214
                b = 96
            elif col[0] == 'GREEN':
                r = 65
                g = 214
                b = 62
            elif col[0] == 'CYAN':
                r = 62
                g = 214
                b = 199
            elif col[0] == 'L_BLUE':
                r = 62
                g = 161
                b = 214
            elif col[0] == 'BLUE':
                r = 62
                g = 65
                b = 214
            elif col[0] == 'PURPLE':
                r = 181
                g = 62
                b = 214
            elif col[0] == 'VIOLET':
                r = 214
                g = 62
                b = 209
    else:
        r = col[0]
        g = col[1]
        b = col[2]

    return f'\033[38;2;{r};{g};{b}m'

def BG(*col):

    r = 255
    g = 255
    b = 255
    if len(col) == 1:
        if col[0][0] == '#':
            hex = col[0].lstrip('#')
            rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
        else:
            if col[0] == 'RED':
                r = 214
                g = 62
                b = 62
            elif col[0] == 'ORANGE':
                r = 214
                g = 143
                b = 62
            elif col[0] == 'YELLOW':
                r = 211
                g = 214
                b = 62
            elif col[0] == 'L_GREEN':
                r = 98
                g = 214
                b = 96
            elif col[0] == 'GREEN':
                r = 65
                g = 214
                b = 62
            elif col[0] == 'CYAN':
                r = 62
                g = 214
                b = 199
            elif col[0] == 'L_BLUE':
                r = 62
                g = 161
                b = 214
            elif col[0] == 'BLUE':
                r = 62
                g = 65
                b = 214
            elif col[0] == 'PURPLE':
                r = 181
                g = 62
                b = 214
            elif col[0] == 'VIOLET':
                r = 214
                g = 62
                b = 209
    else:
        r = col[0]
        g = col[1]
        b = col[2]

    return f'\033[48;2;{r};{g};{b}m'