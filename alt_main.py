from SNRVisualizer import *
from BRDisplacer import *

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import math

# https://www.researchgate.net/publication/256733582_Path_Loss_Exponent_Analysis_in_Wireless_Sensor_Networks_Experimental_Evaluation
PATH_LOSS = 1.7

# https://www.ti.com/lit/ds/symlink/cc2420.pdf?ts=1626269285937&ref_url=https%253A%252F%252Fwww.google.com%252F
RSSI_SENSITIVITY = -90
POWER_MW = 0.1  # -10dBm

WHITE_NOISE = 10**(-105/10)

# https://people.eecs.berkeley.edu/~pister/290Q/Papers/Radios/LanziseraMultirate15dot4.pdf
SNR_THRESHOLD = 5

radius = math.sqrt((POWER_MW/PATH_LOSS)*((0.125/(4*math.pi))
                   ** 2)*10**(-RSSI_SENSITIVITY/10))

sizes = [[x,y] for x in range(200,600,10) for y in range(200,600,10)]
print(len(sizes))
for size in sizes:
    for policy in [f"asapmargin_{radius/2}", "intersecting_flower_1.85"]:
        brs_gen = BRDisplacer(size[0], size[1], radius)
        brs_array = brs_gen.displace(policy)

        snr = SNRVisualizer(policy=policy, detail=1, brs=brs_array, power_mw=POWER_MW, path_loss=PATH_LOSS,
                            white_noise=WHITE_NOISE, rssi_sensitivity=RSSI_SENSITIVITY, length=size[0], height=size[1], snr_threshold=SNR_THRESHOLD)

        #snr.draw()
        interference, coverage = snr.compute_perc()

        with open("output.csv", "a") as file:
            file.write(f"{size[0]}x{size[1]};{policy};{interference};{coverage}\n")