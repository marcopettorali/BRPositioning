from PIL import Image, ImageDraw, ImageFont
import math
import random


class SNRVisualizer:
    def __init__(self, **args):
        self.params = args

    def rssi(self, x1, y1, x2, y2):
        distance = math.sqrt((x1-x2)**2+(y1-y2)**2)
        return 10 * math.log10((self.params["power_mw"]*0.0000989464684007)/(self.params["path_loss"]*(distance**2)))

    def compute_snr_in_point(self, x, y):
        rssi_arr = []
        max_rssi = -100
        max_rssi_index = -1
        for i, br in enumerate(self.params["brs"]):
            rssi_val = self.rssi(
                x, y, self.params["brs"][br][0], self.params["brs"][br][1])
            if rssi_val > max_rssi:
                max_rssi = rssi_val
                max_rssi_index = i
            rssi_arr.append(rssi_val)
        if max_rssi < self.params["rssi_sensitivity"]:
            return 0

        noise = self.params["white_noise"]
        for i, rssi_val in enumerate(rssi_arr):
            if i == max_rssi_index:
                continue
            if rssi_val > self.params["rssi_sensitivity"]:
                noise += 10**(rssi_val/10)

        max_rssi_mw = 10**(max_rssi/10)

        return max_rssi_mw/noise

    def compute_perc(self):
        green = 0
        black = 0
        for i in range(self.params["length"]*self.params["detail"]):
            for j in range(self.params["height"]*self.params["detail"]):
                if [i/self.params["detail"], j/self.params["detail"]] not in self.params["brs"].values():
                    snr = self.compute_snr_in_point(
                        i/self.params["detail"], j/self.params["detail"])
                    if snr > self.params["snr_threshold"]:
                        green += 1
                    elif snr == 0:
                        black += 1
        return 1 - green/(self.params["length"]*self.params["detail"]*self.params["height"]*self.params["detail"]), 1 - black/(self.params["length"]*self.params["detail"]*self.params["height"]*self.params["detail"])

    def draw(self):
        img = Image.new('RGB', (self.params["length"]*self.params["detail"],
                        self.params["height"]*self.params["detail"]), "black")
        pixels = img.load()
        green = 0
        black = 0
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if [i/self.params["detail"], j/self.params["detail"]] not in self.params["brs"].values():
                    snr = self.compute_snr_in_point(
                        i/self.params["detail"], j/self.params["detail"])
                    if snr > self.params["snr_threshold"]:
                        pixels[i, j] = (0, 255, 0)
                        green += 1
                    else:
                        if snr == 0:
                            pixels[i, j] = (0, 0, 0)
                            black += 1
                        else:
                            # red = round(255 - 255*snr/5)
                            # green = 255-red
                            # pixels[i, j] = (red, green, 0)
                            pixels[i, j] = (255, 0, 0)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 10)
        print(self.params["brs"])
        text = f"""
        Policy = {self.params["policy"]}
        Covered % = {str(round(100 - 100*black/(img.size[0]*img.size[1]),2))}%
        Interference % = {str(round(100 - 100*green/(img.size[0]*img.size[1]),2))}%
        Length x height = {self.params["length"]}x{self.params["height"]}
        Border routers = {self.params["brs"]}
        Transmitting power = {self.params["power_mw"]} mW = {str(round(10*math.log10(self.params["power_mw"]),2))} dBm
        Path loss = {str(round(10*math.log10(self.params["path_loss"]),2))} dBm
        RSSI sensitivity = {self.params["rssi_sensitivity"]} dBm
        White noise = {str(round(10*math.log10(self.params["white_noise"]),2))} dBm
        SNR threshold = {self.params["snr_threshold"]}"""
        draw.text((10, 0), text, (0, 0, 0), font=font)

        for br in self.params["brs"]:
            draw.ellipse((self.params["brs"][br][0]*self.params["detail"]-math.ceil(self.params["detail"]/2), self.params["brs"][br][1]*self.params["detail"]-math.ceil(self.params["detail"]/2), self.params["brs"]
                         [br][0]*self.params["detail"]+math.ceil(self.params["detail"]/2), self.params["brs"][br][1]*self.params["detail"]+math.ceil(self.params["detail"]/2)), fill='black', outline='black')

            draw.text((self.params["brs"][br][0]*self.params["detail"], self.params["brs"]
                      [br][1]*self.params["detail"]), br, (0, 0, 0), font=font)
        #img.show()

        img.save(f"{self.params['policy']},{self.params['length']}x{self.params['height']},{self.params['power_mw']},{self.params['path_loss']},{str(round(10*math.log10(self.params['white_noise']),2))},{self.params['snr_threshold']}-{random.uniform(0,1000000000)}.png", 'PNG')

        return green/(img.size[0]*img.size[1])
