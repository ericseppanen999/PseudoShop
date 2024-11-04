def apply_sharpen(pixels, width, height):
    sharpened_pixels = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    kernel = [[ 0, -1,  0],
              [-1,  5, -1],
              [ 0, -1,  0]]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            r, g, b = 0, 0, 0
            for ky in range(-1, 2):
                for kx in range(-1, 2):
                    pr, pg, pb = pixels[y + ky][x + kx]
                    weight = kernel[ky + 1][kx + 1]
                    r += pr * weight
                    g += pg * weight
                    b += pb * weight
            sharpened_pixels[y][x] = (min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b)))

    return sharpened_pixels