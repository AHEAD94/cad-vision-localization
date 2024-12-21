import data_structures

"""##### (1) 도면파일의 데이터 추출 단계 #####"""


def classify_data(csv_data, wall_line_list=[], door_line_list=[], arc_list=[], door_block_list=[]):
    line_count = 0
    arc_count = 0
    block_count = 0
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    center_x_ = 0
    center_y_ = 0

    layer = ""
    angle = 0
    length = 0
    end_x = 0
    end_y = 0
    start_x = 0
    start_y = 0
    radius = 0
    start_angle = 0
    total_angle = 0
    center_x = 0
    center_y = 0

    for i in range(len(csv_data)):
        if csv_data[i][1] == "선":

            # extracting line information
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

            # unifying starting point and end point (시작, 끝 x좌표는 같은데, y좌표가 뒤바뀜)
            if angle == 0 or angle == 90 or angle == 180 or angle == 360:
                if start_x > end_x:  # must be (start_x < end_x)
                    temp = start_x
                    start_x = end_x
                    end_x = temp
                if start_y > end_y:  # must be (start_y < end_y)
                    temp = start_y
                    start_y = end_y
                    end_y = temp
            # else: -> lineEquation 확인해보고 안되면 돌아오기
            #     if start_y > end_y:  # must be (start_y < end_y)
            #         temp = start_y
            #         start_y = end_y
            #         end_y = temp
            #         temp = start_x
            #         start_x = end_x
            #         end_x = temp

            # line structure
            new_line = data_structures.Line()
            line_count += 1

            new_line.layer = layer
            new_line.angle = angle
            new_line.length = length
            new_line.end_x = end_x
            new_line.end_y = end_y
            new_line.start_x = start_x
            new_line.start_y = start_y

            if layer == "W":
                wall_line_list.append(new_line)
            if layer == "DR":
                door_line_list.append(new_line)

            ### 안쓰는 기능들 #############
            # if layer == "CEN":
            #     line_list.add_cen(line)

            max_x = max(max_x, end_x, start_x)
            max_y = max(max_y, end_y, start_y)
            min_x = min(min_x, end_x, start_x)
            min_y = min(min_y, end_y, start_y)

        if csv_data[i][1] == "호":

            for j in range(len(csv_data[0])):
                if csv_data[0][j] == "도면층":
                    layer = csv_data[i][j]
                if csv_data[0][j] == "반지름":
                    radius = float(csv_data[i][j])
                if csv_data[0][j] == "시작 각도":
                    start_angle = float(csv_data[i][j])
                if csv_data[0][j] == "전체 각도":
                    total_angle = float(csv_data[i][j])
                if csv_data[0][j] == "중심점 X":
                    center_x = float(csv_data[i][j])
                if csv_data[0][j] == "중심점 Y":
                    center_y = float(csv_data[i][j])

            # arc structure
            new_arc = data_structures.Arc()
            arc_count += 1

            new_arc.layer = layer
            new_arc.radius = radius
            new_arc.startAngle = start_angle
            new_arc.totalAngle = total_angle
            new_arc.center_x = center_x
            new_arc.center_y = center_y

            arc_list.append(new_arc)

            max_x = max(max_x, center_x_)
            max_y = max(max_y, center_y_)

        if "doorBlock" in csv_data[i][1]:

            for j in range(len(csv_data[0])):
                if csv_data[0][j] == "도면층":
                    layer = csv_data[i][j]
                if csv_data[0][j] == "이름":
                    name = csv_data[i][j]
                if csv_data[0][j] == "위치 X":
                    location_x = float(csv_data[i][j])
                if csv_data[0][j] == "위치 Y":
                    location_y = float(csv_data[i][j])
                if csv_data[0][j] == "회전":
                    rotation = float(csv_data[i][j])

            # door block structure
            new_block = data_structures.Block()
            block_count += 1

            new_block.layer = layer
            new_block.name = name
            new_block.location_x = location_x
            new_block.location_y = location_y
            new_block.rotation = rotation

            door_block_list.append(new_block)

    return min_x, min_y, max_x, max_y
