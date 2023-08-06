'''
###########################
VTOFG: Vibration Test Object Function Generator
###########################
vtofg.plotter
Author: Zack Ravetz

This file contains VTOFG's tools. These are validator commands for entry boxes
'''

def check_int(P: str) -> bool:
    '''
    checks that P is an integer

    Parameters:
    -P (str): the string to check
    '''
    if str.isdecimal(P) or str(P) == "":
        return True
    else:
        return False

def check_float(P: str) -> bool:
    '''
    checks that P is a float

    Parameters:
    -P (str): the string to check
    '''
    P = str(P).replace('.', '', 1)
    if P.isdecimal() or P == "":
        return True
    else:
        return False

def check_perc(P: str) -> bool:
    '''
    checks that P is a percentage

    Parameters:
    -P (str): the string to checkk
    '''
    if check_float(P):
        if P=="":
            return True
        elif float(P) <= 100:
            return True
        else:
            return False
    else:
        return False

def check_byte(P: str) -> bool:
    '''
    checks that P is an integer between >=1 and <=4 (the byte resolutions that pyaudio is capable of)

    Parameters:
    -P (str): the string to check
    '''
    if check_int(P):
        if P=="":
            return True
        elif int(P) <= 4 and int(P)>0:
            return True
        else:
            return False
    else:
        return False