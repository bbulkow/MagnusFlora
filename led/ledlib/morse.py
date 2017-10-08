# Implement functions to create pattern masks from Morse Code.
# Extend Morse code with a space and error handling

# A dot is one unit long.  A dash is three units long.
# There is one space between parts of the same letter.
# three spaces between letters; seven spaces between words

from ledlib import masking
from ledlib import colordefs

Class MorseMask(masking.Mask):
    def __init__(self, letter, faction)
        self.faction_rgb = colordefs.faction_rgb(faction)       # not needed?
        self.letter = letter
        self.faction = faction
        # TODO: this should obviously be a library call
        self.factioncode = "N"
        if self.faction = "ENL":
            self.factioncode = "E"
        if self.faction = "RES":
            self.factioncode = "R"
        # 2 options:  white letters wrapped in faction color, or just
        # have the letters be in faction color, more subtle
        # idea was one letter per petal, alternatively can do a marquee but
        # that means allowing for a pattern longer than the base it's on.
        # And to generalize further, portal under attack should
        # change the marquee to SOS in red letters
        if self.letter in __morseLetters:           # numbers are just too long
            self.morsebits = "-"
            for i in len(__morseLetters[self.letter]):
                bit = __morseLetters[self.letter][i]
                # Error handling?  We don't need no steenkin' error handling.
                if bit == ".":
                    self.morsebits = self.morsebits  + "w-"
                if bit == "-":
                    self.morsebits = self.morsebits + "www-"
        else
            self.morsebits = "-w----w----w-"
        debugprint (("Morse for ",letter, self.morsebits))
        # self.maskstring =
        self.mask = Mask(maskstring)

# The space probably needs to be pulled from the dict and handled separately.
__morseAlphabet = {
    "A" : ".-",
    "B" : "-...",
    "C" : "-.-.",
    "D" : "-..",
    "E" : ".",
    "F" : "..-.",
    "G" : "--.",
    "H" : "....",
    "I" : "..",
    "J" : ".---",
    "K" : "-.-",
    "L" : ".-..",
    "M" : "--",
    "N" : "-.",
    "O" : "---",
    "P" : ".--.",
    "Q" : "--.-",
    "R" : ".-.",
    "S" : "...",
    "T" : "-",
    "U" : "..-",
    "V" : "...-",
    "W" : ".--",
    "X" : "-..-",
    "Y" : "-.--",
    "Z" : "--..",
    " " : "/"
    "1" : ".----",
    "2" : "..---",
    "3" : "...--",
    "4" : "....-",
    "5" : ".....",
    "6" : "-....",
    "7" : "--...",
    "8" : "---..",
    "9" : "----.",
    "0" : "-----"
}
# The space probably needs to be pulled from the dict and handled separately.
__morseLetters = {
    "A" : ".-",
    "B" : "-...",
    "C" : "-.-.",
    "D" : "-..",
    "E" : ".",
    "F" : "..-.",
    "G" : "--.",
    "H" : "....",
    "I" : "..",
    "J" : ".---",
    "K" : "-.-",
    "L" : ".-..",
    "M" : "--",
    "N" : "-.",
    "O" : "---",
    "P" : ".--.",
    "Q" : "--.-",
    "R" : ".-.",
    "S" : "...",
    "T" : "-",
    "U" : "..-",
    "V" : "...-",
    "W" : ".--",
    "X" : "-..-",
    "Y" : "-.--",
    "Z" : "--.."
}

