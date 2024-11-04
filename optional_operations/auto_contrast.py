from utils import normalize

def apply_auto_contrast(pixels,w,h):
        # auto contrast operation

        # find min and max values for each channel
        r_min,g_min,b_min=255,255,255
        r_max,g_max,b_max=0,0,0

        for x in range(w):
            for y in range(h):
                r,g,b=pixels[y][x]
                r_min,g_min,b_min=min(r_min,r),min(g_min,g),min(b_min,b)
                r_max,g_max,b_max=max(r_max,r),max(g_max,g),max(b_max,b)
            
        # normalize each channel
        for x in range(w):
            for y in range(h):
                r,g,b = pixels[y][x]
                r = normalize(r,r_min,r_max)
                g = normalize(g,g_min,g_max)
                b = normalize(b,b_min,b_max)
                pixels[y][x]=(r,g,b)
        
        return pixels