# vt100.py
#
# Copyright (C) 2022 Katie Rust (katie@ktpanda.org)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
vt100
=====

Constants for VT100/Xterm control sequences. Import as `from ktpanda import vt100 as vt` for convenience.
'''

def cseq(c, *t):
    return '\033[%s%s%s' %(c[1:], ';'.join(str(v) for v in t), c[0])

CR           = '\r'
RESET        = '\x1bc'
NEXTLINE     = '\x1b[0K\n'
CLEAR        = '\r\x1b[0K'
CLEARBELOW   = '\x1b[0J'
RETURNTOP    = '\x1b[f'
CURSUP       = '\x1b[A'

BLACK        = '\x1b[30m'
RED          = '\x1b[31m'
GREEN        = '\x1b[32m'
YELLOW       = '\x1b[33m'
BLUE         = '\x1b[34m'
MAGENTA      = '\x1b[35m'
CYAN         = '\x1b[36m'
WHITE        = '\x1b[37m'
DEFAULT      = '\x1b[39m'

BGBLACK      = '\x1b[40m'
BGRED        = '\x1b[41m'
BGGREEN      = '\x1b[42m'
BGYELLOW     = '\x1b[43m'
BGBLUE       = '\x1b[44m'
BGMAGENTA    = '\x1b[45m'
BGCYAN       = '\x1b[46m'
BGWHITE      = '\x1b[47m'
BGDEFAULT    = '\x1b[49m'

BRBLACK      = '\x1b[90m'
BRRED        = '\x1b[91m'
BRGREEN      = '\x1b[92m'
BRYELLOW     = '\x1b[93m'
BRBLUE       = '\x1b[94m'
BRMAGENTA    = '\x1b[95m'
BRCYAN       = '\x1b[96m'
BRWHITE      = '\x1b[97m'
BRDEFAULT    = '\x1b[99m'

BGBRBLACK    = '\x1b[100m'
BGBRRED      = '\x1b[101m'
BGBRGREEN    = '\x1b[102m'
BGBRYELLOW   = '\x1b[103m'
BGBRBLUE     = '\x1b[104m'
BGBRMAGENTA  = '\x1b[105m'
BGBRCYAN     = '\x1b[106m'
BGBRWHITE    = '\x1b[107m'
BGBRDEFAULT  = '\x1b[109m'

BOLD         = '\x1b[1m'
NOBOLD       = '\x1b[22m'

UNDERLINE    = '\x1b[4m'
NOUNDERLINE  = '\x1b[24m'

BLINK        = '\x1b[5m'
NOBLINK      = '\x1b[25m'

INVERSE      = '\x1b[7m'
NOINVERSE    = '\x1b[27m'

NORM         = '\x1b[22;39m'

WRAPON       = '\x1b[?7h'
WRAPOFF      = '\x1b[?7l'

CURSON       = '\x1b[?25h'
CURSOFF      = '\x1b[?25l'

ALTSCRON     = '\x1b[?1049h'
ALTSCROFF    = '\x1b[?1049l'

if __name__ == '__main__':
    def mkconst(name, val):
        globals()[name] = val
        print(f"{name:12} = {val!r}")

    def csconst(name, c, *val):
        mkconst(name, cseq(c, *val))

    def _init_attrs():
        colors = [(name, val) for val, name in enumerate(('BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', None, 'DEFAULT')) if name]
        attrs = [(name, val) for val, name in enumerate((None, 'BOLD', None, None, 'UNDERLINE', 'BLINK', None, 'INVERSE')) if name]

        toggles = [
            ('WRAP', 7),
            ('CURS', 25),
            ('ALTSCR', 1049),
        ]

        mkconst('CR', '\r')
        mkconst('RESET', '\033c')
        mkconst('NEXTLINE', cseq('K', 0) + '\n')
        mkconst('CLEAR', CR + cseq('K', 0))
        csconst('CLEARBELOW', 'J', 0)
        csconst('RETURNTOP', 'f')
        csconst('CURSUP', 'A')
        print()

        for pfx, base in [('', 30), ('BG', 40), ('BR', 90), ('BGBR', 100)]:
            for name, val in colors:
                csconst(pfx + name, 'm', base + val)
            print()

        for name, val in attrs:
            csconst(name, 'm', val)
            csconst('NO' + name, 'm', 20 + (2 if name == 'BOLD' else val))
            print()

        csconst('NORM', 'm', 0, 39)
        print()

        for name, code in toggles:
            csconst(name + 'ON', 'h?', code)
            csconst(name + 'OFF', 'l?', code)
            print()

    _init_attrs()
