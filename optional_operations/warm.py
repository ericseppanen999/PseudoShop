def apply_warm_tone(pixels, width, height):
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[y][x]
            r = min(255, int(r * 1.1))
            g = min(255, int(g * 1.05))
            pixels[y][x] = (r, g, b)
    return pixels
