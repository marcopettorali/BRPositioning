from PIL import Image, ImageDraw, ImageFont
import math

LENGTH = 50
HEIGTH = 20

#https://www.researchgate.net/publication/256733582_Path_Loss_Exponent_Analysis_in_Wireless_Sensor_Networks_Experimental_Evaluation
PATH_LOSS = 1.7

# https://www.ti.com/lit/ds/symlink/cc2420.pdf?ts=1626269285937&ref_url=https%253A%252F%252Fwww.google.com%252F
RSSI_SENSITIVITY = -95 
POWER_MW = 0.1 # -10dBm

WHITE_NOISE = 10**(-105/10) 

# https://people.eecs.berkeley.edu/~pister/290Q/Papers/Radios/LanziseraMultirate15dot4.pdf
SNR_THRESHOLD = 5 

BRS = {
   "BR 1":[16.7,10],
   "BR 2":[33.3,10]
}

def rssi(x1, y1, x2, y2):
    distance = math.sqrt((x1-x2)**2+(y1-y2)**2)
    return 10 * math.log10((POWER_MW*0.0000989464684007)/(PATH_LOSS*(distance**2)))


def compute_snr_in_point(x, y):
    rssi_arr = []
    max_rssi = -100
    max_rssi_index = -1
    for i, br in enumerate(BRS):
        rssi_val = rssi(x, y, BRS[br][0], BRS[br][1])
        if rssi_val > max_rssi:
            max_rssi = rssi_val
            max_rssi_index = i
        rssi_arr.append(rssi_val)

    noise = WHITE_NOISE
    for i, rssi_val in enumerate(rssi_arr):
        if i == max_rssi_index:
            continue
        if rssi_val > RSSI_SENSITIVITY:
            noise += 10**(rssi_val/10)

    max_rssi_mw = 10**(max_rssi/10)

    return max_rssi_mw/noise

def draw():
    img = Image.new('RGB', (LENGTH*10, HEIGTH*10), "black")
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if [i/10,j/10] not in BRS.values():
                snr = compute_snr_in_point(i/10, j/10)
                if snr > SNR_THRESHOLD:
                    pixels[i, j] = (0, 255, 0) 
                else:
                    # red = round(255 - 255*snr/5)
                    # green = 255-red
                    # pixels[i, j] = (red, green, 0)
                    pixels[i, j] = (255, 0, 0)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 10)
    text = f"""
    Length x height = {LENGTH}x{HEIGTH}
    Border routers = {BRS}
    Transmitting power = {POWER_MW} mW = {str(round(10*math.log10(POWER_MW),2))} dBm
    Path loss = {str(round(10*math.log10(PATH_LOSS),2))} dBm
    RSSI sensitivity = {RSSI_SENSITIVITY} dBm
    White noise = {str(round(10*math.log10(WHITE_NOISE),2))} dBm
    SNR threshold = {SNR_THRESHOLD}"""
    draw.text((10, 0),text,(0,0,0),font=font)

    for br in BRS:
        draw.text((BRS[br][0]*10, BRS[br][1]*10),br,(0,0,0),font=font)
    img.show()

    img.save(f"{LENGTH}x{HEIGTH},{POWER_MW},{PATH_LOSS},{str(round(10*math.log10(WHITE_NOISE),2))},{SNR_THRESHOLD}.png", "PNG")

if __name__ == "__main__":
    draw()