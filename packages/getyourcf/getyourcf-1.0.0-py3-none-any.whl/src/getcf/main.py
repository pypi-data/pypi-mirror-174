from sympy import arg
from getcf.runner import Extractor
from getcf.reverse import is_valid
import argparse

def print_intro():
    print("#########################################")
    print("#                                       #")
    print("#         FISCAL CODE GENERATOR         #")
    print("#                                       #")
    print("#########################################\n")

def main():
    print_intro()

    parser = argparse.ArgumentParser('getcf', description="Get your Italian Fiscal Code")
    parser.add_argument("-i", "--input-file", type=str, dest="inp",
        required=False, help="Pass an input file with data")

    args = parser.parse_args()

    ex = Extractor()

    if args.inp:
        ex.parse_input_file(args.inp)
    else:
        ex.parse_data()
    CF = ex.run()

    print("Il codice fiscale è: {}".format(CF))

def reverse():

    parser = argparse.ArgumentParser('getcf-reverse', description='Validate a Fiscal Code')
    parser.add_argument('fiscal_code', type=str,  help='Potential Fiscal Code to validate')

    args = parser.parse_args()
    ans = is_valid(args.fiscal_code)

    if ans==True:
        print("Codice Fiscale valido!")

    else:
        print("Codice Fiscale non valido")
        print(f"[ Suspected error: {ans[1]} ]")


if __name__ == '__main__':

    main()

    