def apply_blur(pixels, width, height):
    blurred_pixels = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            r, g, b = 0, 0, 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nr, ng, nb = pixels[y + dy][x + dx]
                    r += nr
                    g += ng
                    b += nb
            blurred_pixels[y][x] = (r // 9, g // 9, b // 9)
    
    return blurred_pixels