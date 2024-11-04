from numpy import cumsum
from utils import normalize_cdf, acid_normalize_cdf

def apply_auto_levels(pixels,w,h,flag):
        # auto levels operation

        # initialize histograms of 0's
        red_hist=[0]*256
        green_hist=[0]*256
        blue_hist=[0]*256

        # populate histograms
        for x in range(w):
            for y in range(h):
                red_hist[pixels[y][x][0]]+=1
                green_hist[pixels[y][x][1]]+=1
                blue_hist[pixels[y][x][2]]+=1
        
        # calculate cdf
        # np.cumsum: numpy function that calculates the cumulative sum of an array
        red_cdf=cumsum(red_hist)
        green_cdf=cumsum(green_hist)
        blue_cdf=cumsum(blue_hist)

        # determine if we are normalizing or acid normalizing
        # acid normalization was just a mistake i made in the beginning but decided to keep
        if flag=="reg":
            red_cdf_normal=normalize_cdf(red_cdf)
            green_cdf_normal=normalize_cdf(green_cdf)
            blue_cdf_normal=normalize_cdf(blue_cdf)
        elif flag=="acid":
            red_cdf_normal=acid_normalize_cdf(red_cdf)
            green_cdf_normal=acid_normalize_cdf(green_cdf)
            blue_cdf_normal=acid_normalize_cdf(blue_cdf)

        for x in range(w):
            for y in range(h):
                # apply normalization to each pixel
                r,g,b=pixels[y][x]
                pixels[y][x]=(red_cdf_normal[r],green_cdf_normal[g],blue_cdf_normal[b])

        return pixels