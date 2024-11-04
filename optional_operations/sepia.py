from utils import scaler

def apply_sepia(pixels,w,h):
        # sepia operation

        # apply sepia filter to each pixel and scale between 0 and 255
        for x in range(w):
            for y in range(h):
                r,g,b = pixels[y][x]
                # these values are from microsoft
                new_r=int(r*0.393+g*0.769+b*0.189)
                new_g=int(r*0.349+g*0.686+b*0.168)
                new_b=int(r*0.272+g*0.534+b*0.131)

                new_r=scaler(new_r,0,255)
                new_g=scaler(new_g,0,255)
                new_b=scaler(new_b,0,255)

                pixels[y][x]=(new_r,new_g,new_b)
        
        return pixels
    