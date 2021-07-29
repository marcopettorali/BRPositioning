import matplotlib.pyplot as plt
import numpy as np


labels = ['200x100', '200x200', '300x150', '300x300', '400x200', '400x400']
asapmargin = [2,4,6,9,8,16]
intersecting_orange = [3,5,5,8,11,14]
old_flower = [3,5,7,10,7,14]
intersecting_flower = [3,5,5,8,7,14]

dimensions = [2.00*1.00,2.00*2.00,3.00*1.50, 3.00*3.00, 4.00*2.00,4.00*4.00]

asapmargin = [x / y for (x,y) in zip(asapmargin, dimensions)]
intersecting_orange = [x / y for (x,y) in zip(intersecting_orange, dimensions)]
old_flower = [x / y for (x,y) in zip(old_flower, dimensions)]
intersecting_flower = [x / y for (x,y) in zip(intersecting_flower, dimensions)]


x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, old_flower, width, label='intersecting_flower (old)')
rects2 = ax.bar(x , intersecting_flower, width, label='intersecting_flower (new)')
rects3 = ax.bar(x + width, asapmargin, width, label='asapmargin')


# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('Number of BRs')
ax.set_title('Number of BRs per hm\xb2 for each arranging policy')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

#ax.bar_label(rects1, padding=3)
#ax.bar_label(rects2, padding=3)
#ax.bar_label(rects3, padding=3)

fig.tight_layout()

plt.show()
