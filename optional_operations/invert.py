def apply_invert(pixels,w,h):
        # invert operation

        # invert each channel
        for x in range(w):
            for y in range(h):
                r,g,b=pixels[y][x]
                r,g,b=255-r,255-g,255-b
                pixels[y][x]=(r,g,b)

        return pixels