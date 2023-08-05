"""Module to implement the command to chekc if a FC is valid"""

from getcf.runner import Extractor as Extractor
import getcf.exception as exception

import os
import pathlib
import numpy as np


def is_valid(code: str):
    if not len(code)==16:
        return (False, "len")

    month, date = code[8], code[9:11]

    if not month in exception.month_to_number.values():
        return (False, "month", month)
    
    rlim = 30
    if month in ['A', 'C', 'E', 'L', 'M', 'R', 'T']:
        rlim = 31
    elif month == 'B':
        rlim = 28


    if not (1<=int(date)<=rlim or 41<=int(date)<=40+rlim):
        return (False, "day", date)

    data_dir = os.path.join(pathlib.Path(__file__).parent.parent.parent, 'data')
    ita = np.loadtxt(os.path.join(data_dir, "Codici_ITA.csv"), delimiter=";", dtype=str)
    ext = np.loadtxt(os.path.join(data_dir, "Codici_EXT.csv"), delimiter=";", dtype=str)
    
    d = { k.upper():v for k,v in ita}
    d.update ({ k.upper():v for k,v in ext})


    if not code[-5:-1] in d.values():
        return (False, "city", code[-5:-1])

    extractor = Extractor(code[:-1])
    ctrl = extractor.get_control_digit()
    if not ctrl==code[-1]:
        return (False, "control", ctrl)

    return True


if __name__=='__main__':

    print(is_valid("SLANDR98M14L682B"))
    print(is_valid("MRYWLM80A01H501H"))

    print(is_valid("MRYWLM80A51H541H"))
    print(is_valid("MRYWLM80A91H541H"))
