# All the code needed to implement pattern masking
# only a subset of the clearest colors are used

from ledlib.helpers import debugprint, verboseprint
from ledlib import colordefs

# A mask is a list of colors and transparencies
# Simple Colors:
# kw                =   black, white
# roygbiv       =   basic colors  # might even simplfy this to wcmyk
# X                 = Portal Faction
# R                 =   RES
#   E                   =   ENL
#   N                   =   NEUTRAL
# -                 =   completely transparent (i.e. non-masked)
# 0                 = Passed color 0
# 1                 =   Passed color 1 [...]

maskcolortable = {
    "R" :   colordefs.colortable["RES"],
    "E" :   colordefs.colortable["ENL"],
    "w" :   colordefs.colortable["WHITISH"],
    "k" :   colordefs.colortable["BLACKISH"],
    "-" :   colordefs.colortable["NOTACOLOR"]
}

class MaskPos(object):
    def __init__(self, maskchar, opacity=1.00, rgb=(0,0,0)):
        self.opacity=opacity
        self.rgb = rgb
        if maskchar == "-":
            self.opacity = 0.00
            self.rgb = (0,0,0)
        elif maskchar == 0:
            pass
        elif maskchar == "N":
            self.rgb = colordefs.colortable["NEUTRAL"]
        elif maskchar in maskcolortable:
            self.rgb = maskcolortable[maskchar]
        else:
            self.opacity = 0.00
            self.rgb = (0,0,0)
            log.info (" bad or unimplemented mask  %s, using transparent", maskchar)
    def apply_single(self, rgb_triplet):
        # not sure what kind of compositing to use. Let's at least do the right thing
        # for 0 and 1 opacity
        if self.opacity <= 0.001:
            return self.rgb
        elif self.opacity == 1.00:
            return rgb_triplet
        # not sure what to do. Try multiplying.
        # print ( "apply single: rgb {0} maskrgb {1} opacity {2}".format(rgb_triplet,self.rgb,self.opacity))
        r = ( self.rgb[0] * self.opacity ) + rgb_triplet[0]
        if r > 255:
            r = 255
        g = ( self.rgb[1] * self.opacity ) + rgb_triplet[1]
        if g > 255:
            g = 255
        b = ( self.rgb[2] * self.opacity ) + rgb_triplet[2]
        if b > 255:
            b = 255
        return ( r, g, b )

defaultmaskpos = MaskPos("-")

    

class Mask (object):
    def __init__(self,string,opacity=[1.00],
            rgbtable=[colordefs.colortable["NOTACOLOR"]]):
        # TODO: implement passed color(s)
        self.name = string
        self.size = len(string)
        self.opacity = [1.00] * self.size
        # TODO: implement variable (or even passed static) opacity
        debugprint (("Creating a mask from ", self.name))
        self.pos = [defaultmaskpos] * self.size
        for i in range(self.size):
            self.pos[i] = MaskPos(self.name[i], self.opacity[i])

    def apply(self, rgb_list):
        rgb_list_size = len(rgb_list)
        scope = min(rgb_list_size, self.size)
        #print( "apply mask: rgb_list_size {0} selfsize {1} scope {2} rgb_list {3}".format(rgb_list_size,self.size,scope,rgb_list))
        result = [(150,150,150)] * scope            # dimension result list
        for i in range(rgb_list_size):
            mp = self.pos[i].apply_single(rgb_list[i])
        # print ("mask apply result ", result, "size = ", rgb_list_size)
        return result

