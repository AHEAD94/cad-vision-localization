import numpy as np


# Architectural drawing class definition
class Line:
    def __init__(self, start_x=None, end_x=None, start_y=None, end_y=None, length=None, angle=None, layer=None):
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y
        self.length = length
        self.angle = angle
        self.layer = layer

    def __lt__(self, other):
        if self.start_y == other.start_y:
            return self.start_x < other.start_x
        else:
            return self.start_y < other.start_y

    def get_start_x(self):
        return self.start_x

    def get_end_x(self):
        return self.end_x

    def get_start_y(self):
        return self.start_y

    def get_end_y(self):
        return self.end_y

    def get_length(self):
        return self.length

    def get_angle(self):
        return self.angle

    def get_layer(self):
        return self.layer


class Arc:
    def __init__(self, center_x=None, center_y=None, rad=None, start_angle=None, total_angle=None, layer=None):
        self.center_x = center_x
        self.center_y = center_y
        self.rad = rad
        self.start_angle = start_angle
        self.total_angle = total_angle
        self.layer = layer

    def get_center_x(self):
        return self.center_x

    def get_center_y(self):
        return self.center_y

    def get_rad(self):
        return self.rad

    def get_start_angle(self):
        return self.start_angle

    def get_total_angle(self):
        return self.total_angle

    def get_layer(self):
        return self.layer


class LineList:
    list_lines = []
    list_arcs = []
    list_cen = []
    list_isle_horizontal = []
    list_isle_vertical = []

    def add_line(self, line):
        self.list_lines.append(line)

    def add_arc(self, arc):
        self.list_arcs.append(arc)

    def get_line(self, index):
        return self.list_lines[index]

    def get_arc(self, index):
        return self.list_arcs[index]

    def add_cen(self, line):
        self.list_cen.append(line)

    def get_cen(self, index):
        return self.list_cen[index]

    def add_isle_horizontal(self, line):
        self.list_isle_horizontal.append(line)

    def get_isle_horizontal(self, index):
        return self.list_isle_horizontal[index]

    def add_isle_vertical(self, line):
        self.list_isle_vertical.append(line)

    def get_isle_vertical(self, index):
        return self.list_isle_vertical[index]


def load_drawing(drawing_file):
    # Load drawing CSV
    line_list = LineList()
    max_x = -1
    max_y = -1
    min_x = 99999
    min_y = 99999

    ############################################### LOAD CSV ###############################################
    line_count = 0
    arc_count = 0

    csv_data = np.genfromtxt(drawing_file, delimiter=',', dtype=None, encoding='UTF-8')

    for i in range(len(csv_data)):
        if csv_data[i][1] == "선":
            line_count += 1
            for j in range(len(csv_data[0])):
                if csv_data[0][j] == "도면층":
                    layer = csv_data[i][j]
                if csv_data[0][j] == "각도":
                    angle = float(csv_data[i][j])
                if csv_data[0][j] == "길이":
                    length = float(csv_data[i][j])
                if csv_data[0][j] == "끝 X":
                    end_x = float(csv_data[i][j])
                if csv_data[0][j] == "끝 Y":
                    end_y = float(csv_data[i][j])
                if csv_data[0][j] == "시작 X":
                    start_x = float(csv_data[i][j])
                if csv_data[0][j] == "시작 Y":
                    start_y = float(csv_data[i][j])

            # 선의 시작방향, 끝방향 통일
            if start_x > end_x:
                temp = start_x
                start_x = end_x
                end_x = temp
            if start_y > end_y:
                temp = start_y
                start_y = end_y
                end_y = temp

            line = Line(start_x, end_x, start_y, end_y, length, angle, layer)
            line_list.add_line(line)

            if layer == "CEN":
                line_list.add_cen(line)

            max_x = max(max_x, end_x, start_x)
            max_y = max(max_y, end_y, start_y)
            min_x = min(min_x, end_x, start_x)
            min_y = min(min_y, end_y, start_y)

            # #################################################
            # print(str(line_count)
            #       +", layer: "+line.get_layer()
            #       +", angle: "+str(line.get_angle())
            #       +", length: "+str(line.get_length())
            #       +", end_x: "+str(line.get_end_x())
            #       +", end_y: "+str(line.get_end_y())
            #       +", start_x: "+str(line.get_start_x())
            #       +", start_y: "+str(line.get_start_y()))
            # #################################################

        if csv_data[i][1] == "호":
            arc_count += 1
            for j in range(len(csv_data[0])):
                if csv_data[0][j] == "도면층":
                    layer = csv_data[i][j]
                if csv_data[0][j] == "반지름":
                    rad = float(csv_data[i][j])
                if csv_data[0][j] == "시작 각도":
                    start_angle = float(csv_data[i][j])
                if csv_data[0][j] == "전체 각도":
                    total_angle = float(csv_data[i][j])
                if csv_data[0][j] == "중심점 X":
                    center_x = float(csv_data[i][j])
                if csv_data[0][j] == "중심점 Y":
                    center_y = float(csv_data[i][j])

            arc = Arc(center_x, center_y, rad, start_angle, total_angle, layer)
            line_list.add_arc(arc)

            # #################################################
            # print(str(arc_count)
            #       +", layer: "+arc.get_layer()
            #       +", rad: "+str(arc.get_rad())
            #       +", center_x: "+str(arc.get_center_x())
            #       +", center_y: "+str(arc.get_center_y())
            #       +", start_angle: "+str(arc.get_start_angle())
            #       +", total_angle: "+str(arc.get_total_angle()))
            # #################################################

    constraints = [min_x, min_y, max_x, max_y]

    print("[Drawing load result]")
    print("-file: " + drawing_file)
    print("-lines: " + str(len(line_list.list_lines)))
    print("-arcs: " + str(len(line_list.list_arcs)))

    return line_list, constraints
