from curses import wrapper
from columnar import columnar

import sys
b = []
b.append([ "Lampe 19", "310ab2d31d355ea937ef026414a70cfb", "68e8deb0cf66b7bfcef4", "37dac720-4bb2-11ed-b3ae-37777209e331", 
   "@klyqa.lighting.rgb-cw-ww.e27", "False" ])

b.append(["Lampe 4", "AES-KEY: b1b13997763c", "ss" , "ss" , "ss" , "ss" ])
b.append(["Virtueller GU10 Strahler" , "AEs", "dd", "ss" , "ss" , "ss"     ])
b.append(["Wohnzimmer Deckenleuchte G95", "AEs", "dd", "ss" , "ss" , "ss"  ])


for i in b:
    print("{: <20} {: <20} {: <20}".format(*i) + "\n")

table = columnar(b, ["Name","AES Key","Unit ID","Cloud ID","Type","Cloud Connected"], no_borders=True)
print(table)

sys.exit(0)

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(1, 11):
        v = i-10
        if (v==0): continue
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)