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

fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
fig.suptitle("BRs arranging policies")

#https://matplotlib.org/stable/gallery/color/named_colors.html
markers_arr = [["matrix", "black", "+"],
               ["asap", "dodgerblue", "s"],
               ["asapmargin", "blue", "D"],
               ["perfect_orange", "magenta", "o"],
               ["intersecting_orange", "red", "h"],
               ["flower", "orange", (5,2)],
               ["intersecting_flower (new)", "green", "*"],
               ["intersecting_flower (old)", "black", "*"]
               ]
markers = []
for m in markers_arr:
    blue_star = mlines.Line2D([], [], color=m[1], marker=m[2], linestyle='None',
                              markersize=10, label=m[0])
    markers.append(blue_star)

plt.legend(handles=markers, bbox_to_anchor=(1.05, 1), loc='upper left')

for index, size in enumerate([[200,200], [300,300], [400,400],[200,100], [300,150], [400,200]]):
    best_snr = None
    max_black = 0
    best = 0
    stop = None

    x = []
    y = []

    for policy in ["matrix", "asap", f"asapmargin_{radius/2}", "perfect_orange", "intersecting_orange", "flower","intersecting_flower_1.85", "old_flower"]:
        brs_gen = BRDisplacer(size[0], size[1], radius)
        brs_array = brs_gen.displace(policy)

        snr = SNRVisualizer(policy=policy, detail=1, brs=brs_array, power_mw=POWER_MW, path_loss=PATH_LOSS,
                            white_noise=WHITE_NOISE, rssi_sensitivity=RSSI_SENSITIVITY, length=size[0], height=size[1], snr_threshold=SNR_THRESHOLD)

        interference, coverage = snr.compute_perc()

        x.append(1 - coverage)
        y.append(interference)


    for xp, yp, m in zip(x, y, markers_arr):
        axs[math.floor(index/3), index %
            3].scatter([xp], [yp], marker=m[2], color=m[1])
    axs[math.floor(index/3), index % 3].set_title(f"Size = {size[0]}m x {size[1]}m")
plt.xlim([-0.02 , max(x)+0.02])
plt.ylim([-0.02 , max(y)+0.02])
plt.tight_layout()

# add a big axes, hide frame
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel("Non coverage %")
plt.ylabel("Interference %")

plt.show()
