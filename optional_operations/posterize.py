def apply_posterize(pixels, w, h):
        # posterize operation
        bands=6
        factor=256//bands # 42
        # posterize factor
        # scale each channel to the nearest multiple of factor
        for x in range(w):
            for y in range(h):
                r,g,b=pixels[y][x]
                r=int(r//factor)*factor
                g=int(g//factor)*factor
                b=int(b//factor)*factor
                pixels[y][x]=(r,g,b)

        return pixels
    