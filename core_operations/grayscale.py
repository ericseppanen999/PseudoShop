def apply_grayscale(w,h,pixels):
    for x in range(w):
        for y in range(h):
            r, g, b = pixels[y][x]
            Y = int(0.299 * r + 0.587 * g + 0.114 * b)  # Grayscale formula
            pixels[y][x] = (Y, Y, Y)
    return pixels