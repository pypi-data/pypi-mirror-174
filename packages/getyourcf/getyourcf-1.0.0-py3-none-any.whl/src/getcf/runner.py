"""
Module that contains the Extractor class.
"""

import os
import pathlib
import json
import numpy as np
from getcf.exception import *


class Extractor():
    """
    The class that does all the dirty work.
    """

    def __init__(self, cf=''):
        self.CF = cf

    def parse_data(self,):
        self.name = input("Nome: ").replace(' ','')
        self.surname = input("Cognome: ").replace(' ','')
        self.sex = input("Sesso (M/F): ")
        if self.sex not in ['M', 'F']:
            raise OutOfRangeError("Invalid gender!")
        self.yob = int(input("Anno di nascita: "))
        if not (1900 <= self.yob <= 2022):
            raise OutOfRangeError("Invalid year of birth!")
        self.mob = int(input("Mese di nascita (numero 1-12): "))
        if not (1 <= self.mob <= 12):
            raise OutOfRangeError("Invalid month!")
        self.dob = int(input("Giorno di nascita: "))
        if not (1 <= self.dob <= 31):
            raise OutOfRangeError("Invalid day of birth!")
        self.pob = input("Stato in cui sei nato/a: ")
        if (self.pob.lower()=="italia"):
            self.pob = input("Città di nascita: ")

    def _parse_data_txt(self, txt_path):
        with open(txt_path, 'r') as f:

            lines = [l.strip() for l in f.readlines() if l[0] != '#' and l[0] != '\n']
            assert 7<=len(lines)<=8, "Invalid file format!"

            self.name = lines[0].replace(' ','')
            self.surname = lines[1].replace(' ','')
            self.sex = lines[2]
            if self.sex not in ['M', 'F']:
                raise OutOfRangeError("Invalid gender!")
            self.yob = int(lines[3])
            if not (1900 <= self.yob <= 2022):
                raise OutOfRangeError("Invalid year of birth!")
            self.mob = int(lines[4])
            if not (1 <= self.mob <= 12):
                raise OutOfRangeError("Invalid month!")
            self.dob = int(lines[5])
            if not (1 <= self.dob <= 31):
                raise OutOfRangeError("Invalid day of birth!")
            self.pob = lines[6]
            if self.pob.lower()=="italia":
                self.pob = lines[7]


    def _parse_data_json(self, json_file):
        
        with open(json_file) as file:

            d = json.load(file)

            self.name = d["name"]
            self.surname = d["surname"]
            self.yob = d["year"]
            self.mob = d["month"]
            self.dob = d["day"]
            self.sex = d["sex"]
            self.pob = d["place"]

    
    def parse_input_file(self, input_file):
        if len(input_file)>5 and input_file[-5:]=='.json':
            self._parse_data_json(input_file)
        else:
            self._parse_data_txt(input_file)


    def get_first_name(self,):
        """
        Returns three letters of the first name, according to the
        Italian Fiscal Code rules.
        """
        if(len(self.name)<=3):
            while(len(self.name)<3):
              self.name += 'X'
            return self.name.upper()

        cons = [letter.upper() for letter in list(self.name) if letter.upper() not in vowels.upper()]

        if (len(cons)>3):
            return ''.join([cons[0],cons[2],cons[3]])
        elif(len(cons)==3):
            return ''.join(cons)
        else:
            voc = [letter.upper() for letter in list(self.name) if letter.upper() in vowels.upper()]
            cons += voc
            return ''.join(cons[:3])        
    

    def get_last_name(self,):
        """
        Returns three letters of the last name, according to the
        Italian Fiscal Code rules.
        """
        if(len(self.surname)<=3):
            while(len(self.surname)<3):
              self.surname += 'X'
            return self.surname.upper()

        cons = [letter.upper() for letter in list(self.surname) if letter.upper() not in vowels.upper()]
        if (len(cons)>=3):
            return ''.join([cons[0],cons[1],cons[2]])
        else:
            voc = [letter.upper() for letter in list(self.surname) if letter.upper() in vowels.upper()]
            cons += voc
            return ''.join(cons[:3])  


    def get_birthdate(self,):
        """
        Returns the birthdate in the 
        Italian Fiscal Code format.
        """
        date = ''.join(list(str(self.yob))[-2:]) 
        date += month_to_number[self.mob]
        if(len(str(self.dob))==1):
            self.dob = int(str(self.dob)+ '0')
            self.dob = int(str(self.dob)[::-1])
        if self.sex=='F':
            self.dob += 40
        date += str(self.dob)
        return date


    def get_birthplace(self,):
        """
        Returns the birthplace in the 
        Italian Fiscal Code format.
        """
        data_dir = os.path.join(pathlib.Path(__file__).parent.parent.parent, 'data')
        ita = np.loadtxt(os.path.join(data_dir, "Codici_ITA.csv"), delimiter=";", dtype=str)
        ext = np.loadtxt(os.path.join(data_dir, "Codici_EXT.csv"), delimiter=";", dtype=str)
        
        d = { k.upper():v for k,v in ita}
        d.update ({ k.upper():v for k,v in ext})

        if not(self.pob.upper() in d.keys()):
            err_msg = "Luogo di nascita non valido. Non posso generare il codice."
            raise PlaceNotFoundError(err_msg)
        
        return d[self.pob.upper()]


    def get_control_digit(self,):
        """
        Returns the control digit of the Fiscal Code.
        """
        evens = list(self.__sep_str__(self.CF))
        odds = list(self.__sep_str__(self.CF, get_even=False))
        score = 0

        for i in range(len(evens)):
            score += even_digit[evens[i]]
        for j in range(len(odds)):
            score += odd_digit[odds[j]]
        score = int(score)%26
        return str(remainder[score])


    @staticmethod
    def __sep_str__(word, get_even:bool=True):
        """
        Get only the odd or even digits of a string.

        :param word: string to be separated
        """
        lw=list(word)
        if get_even:
            del lw[::2]
        else:
            del lw[1::2]
        return ''.join(lw)


    def run(self,):
        """
        Get all the pieces together and return the Fiscal Code.
        """
        self.CF = self.get_last_name() + self.get_first_name()
        self.CF += self.get_birthdate() + self.get_birthplace()
        self.CF += self.get_control_digit()

        return self.CF