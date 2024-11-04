from random import randint
from utils import scaler

def apply_grain(pixels,w,h,factor=50):
        # grain operation

        for x in range(w):
            for y in range(h):
                r,g,b=pixels[y][x]
                factor=50 # arbritary depending on how strong we want the grain to be
                r+=randint(-factor,factor)
                g+=randint(-factor,factor)
                b+=randint(-factor,factor)

                # scale values between 0 and 255
                r,g,b=scaler(r,0,255),scaler(g,0,255),scaler(b,0,255)
                pixels[y][x]=(r,g,b)

        return pixels