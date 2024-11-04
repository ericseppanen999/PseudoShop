def apply_brightness(pixels, width, height, factor=1.2):
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[y][x]
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            pixels[y][x] = (r, g, b)
    return pixels