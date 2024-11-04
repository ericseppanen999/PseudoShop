def apply_mirror(pixels,w,h):
        # mirror operation
        for y in range(h):
            # reverse each row
            pixels[y]=pixels[y][::-1]
        return pixels