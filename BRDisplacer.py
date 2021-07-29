import math

from SNRVisualizer import *


class BRDisplacer:
    def __init__(self, length, height, br_range):
        self.height = height
        self.length = length
        self.br_range = br_range

    def displace(self, policy):
        if policy == "matrix":
            brs = {}
            space = self.br_range * math.sqrt(2)
            X = math.floor(self.length/space + 1)
            Y = math.floor(self.height/space + 1)

            margin_x = (self.length - space * (X-1))/2
            margin_y = (self.height - space * (Y-1))/2

            for id in range(0, X*Y):

                pos_x = id % X
                pos_y = math.floor(id/X)

                brs[f"bbr_{id}"] = [margin_x + pos_x *
                                    space, margin_y + pos_y * space]

            return brs
        if policy == "asap":

            if self.length < 0.75 * 2 * self.br_range and self.height < 0.75 * 2 * self.br_range:
                return {"br_0": [self.length / 2, self.height / 2]}

            brs = {}
            r = self.br_range / math.sqrt(2)
            X = math.ceil(self.length/(2*r))
            Y = math.ceil(self.height/(2*r))

            
            for id in range(0, X*Y):

                pos_x = id % X
                pos_y = math.floor(id/X)

                if(X>1):
                    space_x = self.length / (X-1)
                    x = pos_x * space_x
                else:
                    x = self.length/2

                if(Y > 1):
                    space_y = self.height / (Y-1)
                    y = pos_y * space_y
                else:
                    y = self.height / 2

                brs[f"bbr_{id}"] = [x, y]

            return brs
        if "asapmargin_" in policy:

            if self.length < 0.75 * 2 * self.br_range and self.height < 0.75 * 2 * self.br_range:
                return {"br_0": [self.length / 2, self.height / 2]}

            margin = float(policy.split("_")[1])
            brs = {}
            r = self.br_range / math.sqrt(2)
            X = math.ceil(self.length/(2*r))
            Y = math.ceil(self.height/(2*r))

            for id in range(0, X*Y):

                pos_x = id % X
                pos_y = math.floor(id/X)

                if(X == 1):
                    x = self.length/2
                else:
                    space_x = self.length / (X-1)
                    x = pos_x * space_x
                    if x == 0:
                        x = margin
                    if x == self.length:
                        x = self.length - margin

                if(Y == 1):
                    y = self.height / 2
                else:
                    space_y = self.height / (Y-1)
                    y = pos_y * space_y
                    if y == 0:
                        y = margin
                    if y == self.height:
                        y = self.height - margin

                brs[f"bbr_{id}"] = [x, y]

            return brs

        if policy == "perfect_orange":
            brs = {}
            row_size = math.floor(self.length/(2*self.br_range)) + 1
            levels = math.floor(self.height/(math.sqrt(3)*self.br_range)) + 1

            margin_x = (self.length - 2*self.br_range*(row_size-1))/2
            margin_y = (self.length - math.sqrt(3)*self.br_range*(levels-1))/2

            id = 0
            for i in range(0, levels):
                if i % 2 == 0:
                    for j in range(0, row_size):
                        x = margin_x + j * 2 * self.br_range
                        y = margin_y + i * math.sqrt(3) * self.br_range
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1
                else:
                    for j in range(0, row_size-1):
                        x = margin_x + self.br_range + j * 2 * self.br_range
                        y = margin_y + i * math.sqrt(3) * self.br_range
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1

            return brs

        if policy == "intersecting_orange":
            brs = {}
            row_size = round(self.length/(2*self.br_range) + 1)
            levels = round(self.height/(math.sqrt(3)*self.br_range) + 1)

            if self.length/(2*self.br_range) + 1 - math.floor(self.length/(2*self.br_range) + 1) >= 0.5:
                r_x = self.length / (row_size - 1)
            else:
                r_x = 2 * self.br_range

            if self.height/(math.sqrt(3)*self.br_range) + 1 - math.floor(self.height/(math.sqrt(3)*self.br_range) + 1) >= 0.5:
                r_y = self.height / (levels - 1)
            else:
                r_y = math.sqrt(3) * self.br_range

            margin_x = (self.length - r_x*(row_size-1))/2
            margin_y = (self.height - r_y*(levels-1))/2

            id = 0
            for i in range(0, levels):
                if i % 2 == 0:
                    for j in range(0, row_size):
                        x = margin_x + j * r_x
                        y = margin_y + i * r_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1
                else:
                    for j in range(0, row_size-1):
                        x = margin_x + r_x/2 + j * r_x
                        y = margin_y + i * r_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1

            return brs

        if policy == "flower":
            brs = {}

            r_x = self.br_range*math.sqrt(3)/2
            r_y = 3*self.br_range/2

            row_size = math.floor(self.length/(2*r_x)) + 1
            levels = math.floor(self.height/(r_y)) + 1

            margin_x = (self.length - 2*r_x*(row_size-1))/2
            margin_y = (self.length - r_y*(levels-1))/2

            id = 0
            for i in range(0, levels):
                if i % 2 == 0:
                    for j in range(0, row_size):
                        x = margin_x + j * 2 * r_x
                        y = margin_y + i * r_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1
                else:
                    for j in range(0, row_size-1):
                        x = margin_x + r_x + j * 2 * r_x
                        y = margin_y + i * r_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1

            return brs

        if "intersecting_flower_" in policy:

            add_one_th = float(policy.split("_")[2])
            brs = {}

            if self.length < 0.75 * 2 * self.br_range and self.height < 0.75 * 2 * self.br_range:
                return {"br_0": [self.length / 2, self.height / 2]}

            r_x = 0
            r_y = 3*self.br_range/2

            row_size = math.ceil(self.length/(self.br_range*2)) 
            print(row_size)
            levels = math.floor(self.height/(r_y)) + 1

            if row_size == 1 and levels == 2:
                return {"br_0": [0, self.height / 2], "br_1": [self.length, self.height/2]} 
               
            if row_size > 1 and (self.length / (row_size-1)) / self.br_range >= add_one_th:
                row_size += 1
            
            r_x = self.length / (2*(row_size-1))

            margin_y = (self.height - r_y*(levels-1))/2
            
            id = 0
            for i in range(0, levels):
                if i % 2 == 0:
                    
                    for j in range(0, row_size):
                        x = j * 2 * r_x
                        y = margin_y + i * r_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1
                else:
                    for j in range(0, row_size-1):
                        x = r_x + j * 2 * r_x
                        y = margin_y + i * r_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1

            return brs

        if policy == "new":
            brs = {}
            X = math.ceil(self.length/(2*self.br_range))

            margin_x = math.sqrt(2)*self.br_range/2
            space_x = (self.length - 2*margin_x)/(X-1)
            if space_x > 2*self.br_range:
                margin_x = self.length/(2*X)
                space_x = self.length/(2*X)

            Y = math.ceil((2*(self.height - math.sqrt(2)*self.br_range))/(math.sqrt(3)*space_x))

            margin_y = self.br_range* math.sqrt(2)/2
            space_y = (self.height - 2*margin_y) /(Y-1)
            
            print(f"X = {X}, Y = {Y}")

            id = 0
            for i in range(0,Y):
                if i%2==0:
                    for j in range(0, X):
                        x = margin_x + j * space_x
                        y = margin_y + i * space_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1
                else:
                    for j in range(0, X+1):
                        x = j * self.length/X
                        y = margin_y + i * space_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1

            return brs

        if "old_flower" in policy:
            brs = {}

            if self.length < 0.75 * 2 * self.br_range and self.height < 0.75 * 2 * self.br_range:
                return {"br_0": [self.length / 2, self.height / 2]}

            r_x = 0
            r_y = 3*self.br_range/2

            row_size = math.floor(self.length/(self.br_range*math.sqrt(3))) +1
            print(row_size)
            levels = math.floor(self.height/(r_y)) + 1

            if row_size == 1 and levels == 2:
                return {"br_0": [0, self.height / 2], "br_1": [self.length, self.height/2]} 
               
            if row_size > 1 and (self.length / (row_size-1)) / self.br_range >= 1.85:
                row_size += 1
            
            r_x = self.length / (2*(row_size-1))

            margin_y = (self.height - r_y*(levels-1))/2
            
            id = 0
            for i in range(0, levels):
                if i % 2 == 0:
                    
                    for j in range(0, row_size):
                        x = j * 2 * r_x
                        y = margin_y + i * r_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1
                else:
                    for j in range(0, row_size-1):
                        x = r_x + j * 2 * r_x
                        y = margin_y + i * r_y
                        brs[f"bbr_{id}"] = [x, y]
                        id += 1

            return brs

