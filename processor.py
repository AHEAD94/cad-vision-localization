import data_structures

INFINITY = 999999


def sort_pairs(list):  # merge sort
    if len(list) > 1:
        mid = len(list) // 2
        left = list[:mid]
        right = list[mid:]

        sort_pairs(left)
        sort_pairs(right)

        i = j = k = 0

        # Copy data to temp arrays left[] and right[]
        while i < len(left) and j < len(right):
            if left[i].slope == INFINITY:
                if left[i].center_start.x < right[j].center_start.x:
                    list[k] = left[i]
                    i += 1
                else:
                    list[k] = right[j]
                    j += 1
                k += 1
            else:
                if left[i].center_start.y < right[j].center_start.y:
                    list[k] = left[i]
                    i += 1
                else:
                    list[k] = right[j]
                    j += 1
                k += 1

        # Checking if any element was left
        while i < len(left):
            list[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            list[k] = right[j]
            j += 1
            k += 1


"""##### (2) 마주보는 벽체 탐색 단계 #####"""


### line equation calculator ###
def def_line_equation(x1, y1, x2, y2):  # 여기 문제 있음 -> 원인분석 (반올림문제인듯?) -> 해결
    slope = 0
    intercept = 0
    # print("args are not in trouble")
    # print(str(x1) + ", " + str(y1))
    # print(str(x2) + ", " + str(y2))

    if x1 != x2:
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
    else:
        slope = INFINITY
        intercept = x1

    new_equation = data_structures.LineEquation()

    try:
        new_equation.slope = round(slope, 2)
        new_equation.intercept = round(intercept, 2)
    except TypeError:
        print('coords: ' + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2))
        print('slope: ' + str(slope))
        print('intercept: ' + str(intercept))
        raise

    # new_equation.slope = round(slope, 2)
    # new_equation.intercept = round(intercept, 2)
    # new_equation.slope = slope
    # new_equation.intercept = intercept

    return new_equation


### classifying same equations ###
def classify_same_wall_lines(wall_line_list, line_equations=[]):
    search_result = 0

    for i in range(len(wall_line_list)):
        search_result = 0
        equation = def_line_equation(wall_line_list[i].start_x, wall_line_list[i].start_y,
                                     wall_line_list[i].end_x, wall_line_list[i].end_y)

        if wall_line_list[i].angle == 90.0 or wall_line_list[i].angle == 270.0:
            if wall_line_list[i].start_y > wall_line_list[i].end_y:
                temp = wall_line_list[i].start_y
                wall_line_list[i].start_y = wall_line_list[i].end_y
                wall_line_list[i].end_y = temp

        for j in range(len(line_equations)):  # 나중에 BST 등으로 탐색방법 교체
            if (line_equations[j].head.data.slope == equation.slope and
                    line_equations[j].head.data.intercept == equation.intercept):
                line_equations[j].append_node(wall_line_list[i])
                search_result = 1
                break

        if search_result == 0:
            list_head = data_structures.LinkedList(equation)
            list_head.name = "Lines"
            list_head.append_node(wall_line_list[i])
            line_equations.append(list_head)


### identifying walls ###
def identify_walls(outer_wall_thickness, line_equations, wall_pairs=[]):
    slope1 = 0
    slope2 = 0
    intercept1 = 0
    intercept2 = 0
    center_intercept = 0
    temporary_list = line_equations.copy()

    for i in range(len(temporary_list) - 1):
        if temporary_list[i] is None:
            continue

        slope1 = temporary_list[i].head.data.slope
        intercept1 = temporary_list[i].head.data.intercept

        for j in range(i + 1, len(temporary_list)):
            if temporary_list[i] is None or temporary_list[j] is None:
                continue

            slope2 = temporary_list[j].head.data.slope
            intercept2 = temporary_list[j].head.data.intercept

            if slope1 != slope2:
                continue
            else:
                thickness = abs(intercept2 - intercept1)

                if thickness <= outer_wall_thickness:
                    center_intercept = round((intercept1 + intercept2) / 2, 2)

                    # 직선들의 가장 작은 시작 좌표값, 가장 큰 끝 좌표값 선택
                    starting_point1, end_point1 = temporary_list[i].get_endpoints()
                    starting_point2, end_point2 = temporary_list[j].get_endpoints()

                    center_start = data_structures.Point()
                    center_end = data_structures.Point()

                    if slope1 == INFINITY:
                        center_start.x = center_intercept
                        center_end.x = center_intercept
                        if starting_point1.y < starting_point2.y:
                            center_start.y = starting_point1.y
                        else:
                            center_start.y = starting_point2.y
                        if end_point1.y > end_point2.y:
                            center_end.y = end_point1.y
                        else:
                            center_end.y = end_point2.y
                    else:
                        if starting_point1.x < starting_point2.x:
                            center_start.x = starting_point1.x
                        else:
                            center_start.x = starting_point2.x
                        if end_point1.x > end_point2.x:
                            center_end.x = end_point1.x
                        else:
                            center_end.x = end_point2.x
                        center_start.y = slope1 * center_start.x + center_intercept
                        center_end.y = slope1 * center_end.x + center_intercept

                    new_wall_pair = data_structures.Pair()
                    new_wall_pair.name = "wallPair"
                    new_wall_pair.intercept1 = intercept1
                    new_wall_pair.intercept2 = intercept2
                    new_wall_pair.center = center_intercept
                    new_wall_pair.slope = slope1
                    new_wall_pair.center_start = center_start
                    new_wall_pair.center_end = center_end

                    wall_pairs.append(new_wall_pair)
                    temporary_list[i] = None
                    temporary_list[j] = None


def identify_halls(min_hall_width, wall_pairs, hall_pairs=[]):  # 실제 hall만 선택하도록 수정해야 함
    wall_pair1 = None
    wall_pair2 = None
    wall_pair1 = None
    wall_pair2 = None
    min_difference = 0
    intercept1 = 0
    intercept2 = 0
    center_intercept = 0
    search_result = 0
    wall1_center_start = None
    wall1_center_end = None
    wall2_center_start = None
    wall2_center_end = None
    # temporary_list = wall_pairs.copy()

    # 복도 중앙 선택 전 정렬 -> 해야됨
    vert_wall_pairs = []
    nonvert_wall_pairs = []
    for i in range(len(wall_pairs)):
        if wall_pairs[i].slope == INFINITY:
            vert_wall_pairs.append(wall_pairs[i])
        else:
            nonvert_wall_pairs.append(wall_pairs[i])
    sort_pairs(vert_wall_pairs)
    sort_pairs(nonvert_wall_pairs)

    # print("[sorting test]")
    # for i in range(len(vert_wall_pairs)):
    #     print(vert_wall_pairs[i])
    # for i in range(len(nonvert_wall_pairs)):
    #     print(nonvert_wall_pairs[i])

    sorted_wall_pairs = vert_wall_pairs + nonvert_wall_pairs

    for i in range(len(sorted_wall_pairs) - 1):
        if sorted_wall_pairs[i] is None:
            continue

        wall_pair1 = sorted_wall_pairs[i]

        for j in range(i + 1, len(sorted_wall_pairs)):
            if sorted_wall_pairs[i] is None or sorted_wall_pairs[j] is None:
                continue

            wall_pair2 = sorted_wall_pairs[j]

            if wall_pair1.slope == wall_pair2.slope:
                center_intercept = \
                    round((wall_pair1.center + wall_pair2.center) / 2, 2)

                # wallPair 내 벽선들 중 복도 중앙과 가까운 벽선 intercept 선택
                if (abs(wall_pair1.intercept1 - center_intercept) <
                        abs(wall_pair1.intercept2 - center_intercept)):
                    intercept1 = wall_pair1.intercept1
                else:
                    intercept1 = wall_pair1.intercept2
                wall1_center_start = wall_pair1.center_start
                wall1_center_end = wall_pair1.center_end

                if (abs(wall_pair2.intercept1 - center_intercept) <
                        abs(wall_pair2.intercept2 - center_intercept)):
                    intercept2 = wall_pair2.intercept1
                else:
                    intercept2 = wall_pair2.intercept2
                wall2_center_start = wall_pair2.center_start
                wall2_center_end = wall_pair2.center_end

                hall_width = abs(intercept2 - intercept1)
                if hall_width < min_hall_width:
                    sorted_wall_pairs[i] = None
                    continue

                # hallPair 선들 좌표 지정을 위한 길이 선택
                hall_center_start = data_structures.Point()
                hall_center_end = data_structures.Point()
                hall_inner1_start = data_structures.Point()
                hall_inner1_end = data_structures.Point()
                hall_inner2_start = data_structures.Point()
                hall_inner2_end = data_structures.Point()

                if wall_pair1.slope == INFINITY:
                    # 두 벽 중앙선들 중 긴 선의 길이 선택
                    hall_center_start.x = center_intercept
                    hall_center_end.x = center_intercept
                    if wall1_center_start.y < wall2_center_start.y:
                        hall_center_start.y = wall1_center_start.y
                    else:
                        hall_center_start.y = wall2_center_start.y
                    if wall1_center_end.y > wall2_center_end.y:
                        hall_center_end.y = wall1_center_end.y
                    else:
                        hall_center_end.y = wall2_center_end.y

                    # 내측 벽선 길이 선택
                    hall_inner1_start.x = intercept1
                    hall_inner1_end.x = intercept1
                    hall_inner2_start.x = intercept2
                    hall_inner2_end.x = intercept2
                    hall_inner1_start.y = wall1_center_start.y
                    hall_inner1_end.y = wall1_center_end.y
                    hall_inner2_start.y = wall2_center_start.y
                    hall_inner2_end.y = wall2_center_end.y

                else:
                    # 두 벽 중앙선들 중 긴 선의 길이 선택
                    if wall1_center_start.x < wall2_center_start.x:
                        hall_center_start.x = wall1_center_start.x
                    else:
                        hall_center_start.x = wall2_center_start.x
                    if wall1_center_end.x > wall2_center_end.x:
                        hall_center_end.x = wall1_center_end.x
                    else:
                        hall_center_end.x = wall2_center_end.x
                    hall_center_start.y = \
                        wall_pair1.slope * hall_center_start.x + center_intercept
                    hall_center_end.y = \
                        wall_pair1.slope * hall_center_end.x + center_intercept

                    # 내측 벽선 길이 선택
                    hall_inner1_start.x = wall1_center_start.x
                    hall_inner1_end.x = wall1_center_end.x
                    hall_inner2_start.x = wall2_center_start.x
                    hall_inner2_end.x = wall2_center_end.x
                    hall_inner1_start.y = \
                        wall_pair1.slope * hall_inner1_start.x + intercept1
                    hall_inner1_end.y = \
                        wall_pair1.slope * hall_inner1_end.x + intercept1
                    hall_inner2_start.y = \
                        wall_pair1.slope * hall_inner2_start.x + intercept2
                    hall_inner2_end.y = \
                        wall_pair1.slope * hall_inner2_end.x + intercept2

                # print("hall_center")
                # print(hall_center_start, hall_center_end)
                # print("hall_inner1")
                # print(hall_inner1_start, hall_inner1_end)
                # print("hall_inner2")
                # print(hall_inner2_start, hall_inner2_end)

                new_hall_pair = data_structures.Pair()
                new_hall_pair.name = "hallPair"
                new_hall_pair.intercept1 = intercept1
                new_hall_pair.intercept2 = intercept2
                new_hall_pair.center = center_intercept
                new_hall_pair.slope = wall_pair1.slope
                new_hall_pair.center_start = hall_center_start
                new_hall_pair.center_end = hall_center_end
                new_hall_pair.intercept1_start = hall_inner1_start
                new_hall_pair.intercept1_end = hall_inner1_end
                new_hall_pair.intercept2_start = hall_inner2_start
                new_hall_pair.intercept2_end = hall_inner2_end

                hall_pairs.append(new_hall_pair)
                sorted_wall_pairs[i] = None

                """
                0 --------------
                     복도공간
                1 --------------
                2 --------------
                     복도공간
                3 --------------

                0에서 시작해 내려가면 가장 가까운게 1이니까 올바르게 페어링 됨
                1에서 시작해 내려가면 2랑 페어링되어 오류
                -> 가장 가까운 선들끼리의 연산은 어렵고, 선들 좌표순 정렬 후 스캔하는 방식으로 변경
                -> 아니면, 스캔해서 선들 짝수관계, 위치관계를 갖고 복도로 페어링
                """


"""##### (3) 벽체의 내측 벽선 선택 단계 #####"""


### inner line selector ###
def classify_inner_lines(line_equations, hall_pairs, inner_lines=[]):
    equation_slope = 0
    equation_intercept = 0
    hall_slope = 0
    hall_intercept1 = 0
    hall_intercept2 = 0

    for i in range(len(line_equations)):
        equation_slope = line_equations[i].head.data.slope
        equation_intercept = line_equations[i].head.data.intercept

        for j in range(len(hall_pairs)):
            hall_slope = hall_pairs[j].slope
            hall_intercept1 = hall_pairs[j].intercept1
            hall_intercept2 = hall_pairs[j].intercept2

            if equation_slope == hall_slope:
                if (equation_intercept == hall_intercept1 or
                        equation_intercept == hall_intercept2):
                    inner_lines.append(line_equations[i])
                else:
                    continue
            else:
                continue


"""##### (4) 복도 중앙선 생성 단계 #####"""


### finding cross point of two center lines ###
def find_cross_points(hall_pairs, inner_lines, cross_points=[]):
    hall_pair1 = None
    inner_line1 = None
    cross_x = 0
    cross_y = 0
    search_result = 0

    for i in range(len(hall_pairs)):
        hall_pair1 = hall_pairs[i]

        for j in range(len(inner_lines)):
            inner_line1 = inner_lines[j].head.data
            search_result = 0

            if hall_pair1.slope == inner_line1.slope:
                continue
            else:
                if hall_pair1.slope == INFINITY:
                    cross_x = hall_pair1.center
                    cross_y = \
                        inner_line1.slope * hall_pair1.center + inner_line1.intercept
                elif inner_line1.slope == INFINITY:
                    cross_x = inner_line1.intercept
                    cross_y = \
                        hall_pair1.slope * inner_line1.intercept + hall_pair1.center
                else:
                    numerator = inner_line1.intercept - hall_pair1.center
                    denominator = hall_pair1.slope - inner_line1.intercept
                    cross_x = numerator / denominator
                    cross_y = \
                        hall_pair1.slope * numerator / denominator + hall_pair1.center

                cross_point = data_structures.Point()
                cross_point.x = cross_x
                cross_point.y = cross_y

                for k in range(len(cross_points)):  # 나중에 BST 등으로 탐색방법 교체
                    if (cross_points[k].head.data.slope == hall_pair1.slope and
                            cross_points[k].head.data.center == hall_pair1.center and
                            cross_points[k].head.data.intercept1 ==
                            hall_pair1.intercept1):
                        cross_points[k].append_node(cross_point)
                        search_result = 1
                        break

                if search_result == 0:
                    list_head = data_structures.LinkedList(hall_pair1)
                    list_head.name = "Points"
                    list_head.append_node(cross_point)
                    cross_points.append(list_head)
