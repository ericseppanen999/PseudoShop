def apply_night_vision(pixels,w,h):
        # night vision operation

        # we need to take the gray pixel, brighten a bit, and then set the green channel to be higher
        for x in range(w):
            for y in range(h):
                pixel=pixels[y][x][0]
                brightened_pixel=min(int(pixel*1.3),255)
                (r,g,b)=((int(brightened_pixel*0.25)),min(int(brightened_pixel*1.5),255),int(brightened_pixel*0.25))
                pixels[y][x]=(r,g,b)
    
        return pixels