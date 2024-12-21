import copy
import math

import data_structures
import inner_line_harvester

INFINITY = 999999


def set_door_nodes(list_head):
    head_copy = copy.deepcopy(list_head)

    cur = list_head.head.next
    while cur is not None:
        if cur.next is not None:
            cur_end = data_structures.Point(cur.data.end_x, cur.data.end_y)
            next_start = data_structures.Point(cur.next.data.start_x, cur.next.data.start_y)
            dist = get_euclid_dist(cur_end, next_start)

            door_line = data_structures.Line()
            door_line.layer = 'DR'
            door_line.angle = cur.data.angle
            door_line.length = round(dist, 2)
            door_line.start_x = cur_end.x
            door_line.start_y = cur_end.y
            door_line.end_x = next_start.x
            door_line.end_y = next_start.y

            head_copy.append_node(door_line)

        cur = cur.next

    # print("Door setting test")
    # head_copy.print_all()

    return head_copy


def set_hall_lines(inner_lines, hallways, cross_points):
    # @#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
    # 1. inner_lines 형식을 각 halwlay에 맞추어 나누기
    # 2. 벽 사이에 문 추가
    # 3. 노드들 hallway에 추가
    # @#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#

    inter1_link_head = None
    inter2_link_head = None

    for i in range(len(hallways)):
        for j in range(len(inner_lines)):
            inner_line_equation = inner_lines[j].head.data
            if hallways[i].slope == inner_line_equation.slope:

                if hallways[i].intercept1 == inner_line_equation.intercept:
                    inter1_link_head = data_structures.LinkedList(inner_line_equation)
                    inter1_link_head.name = "Lines"

                    cur = inner_lines[j].head.next
                    while cur is not None:
                        cur_line = cur.data
                        line_start_point = data_structures.Point()
                        line_start_point.x = cur_line.start_x
                        line_start_point.y = cur_line.start_y
                        line_end_point = data_structures.Point()
                        line_end_point.x = cur_line.end_x
                        line_end_point.y = cur_line.end_y

                        intercept1_line = data_structures.Line()
                        intercept1_line.start_x = hallways[i].intercept1_start.x
                        intercept1_line.start_y = hallways[i].intercept1_start.y
                        intercept1_line.end_x = hallways[i].intercept1_end.x
                        intercept1_line.end_y = hallways[i].intercept1_end.y

                        contain_start_point = inner_line_harvester.check_contain(intercept1_line, line_start_point)
                        contain_end_point = inner_line_harvester.check_contain(intercept1_line, line_end_point)

                        if contain_start_point == 1 and contain_end_point == 1:
                            inter1_link_head.append_node(cur_line)

                        elif contain_start_point == 1 and contain_end_point == 0:
                            for p in range(len(cross_points)):
                                if inner_line_harvester.check_contain(cur_line, cross_points[p]):
                                    subline = copy.deepcopy(cur_line)
                                    subline.length = round(get_euclid_dist(line_start_point, cross_points[p]), 2)
                                    subline.end_x = cross_points[p].x
                                    subline.end_y = cross_points[p].y
                            inter1_link_head.append_node(subline)

                        elif contain_start_point == 0 and contain_end_point == 1:
                            for p in range(len(cross_points)):
                                if inner_line_harvester.check_contain(cur_line, cross_points[p]):
                                    subline = copy.deepcopy(cur_line)
                                    subline.length = round(get_euclid_dist(line_end_point, cross_points[p]), 2)
                                    subline.start_x = cross_points[p].x
                                    subline.start_y = cross_points[p].y
                            inter1_link_head.append_node(subline)

                        cur = cur.next

                if hallways[i].intercept2 == inner_line_equation.intercept:
                    inter2_link_head = data_structures.LinkedList(inner_line_equation)
                    inter2_link_head.name = "Lines"

                    cur = inner_lines[j].head.next
                    while cur is not None:
                        cur_line = cur.data
                        line_start_point = data_structures.Point()
                        line_start_point.x = cur_line.start_x
                        line_start_point.y = cur_line.start_y
                        line_end_point = data_structures.Point()
                        line_end_point.x = cur_line.end_x
                        line_end_point.y = cur_line.end_y

                        intercept2_line = data_structures.Line()
                        intercept2_line.start_x = hallways[i].intercept2_start.x
                        intercept2_line.start_y = hallways[i].intercept2_start.y
                        intercept2_line.end_x = hallways[i].intercept2_end.x
                        intercept2_line.end_y = hallways[i].intercept2_end.y

                        contain_start_point = inner_line_harvester.check_contain(intercept2_line, line_start_point)
                        contain_end_point = inner_line_harvester.check_contain(intercept2_line, line_end_point)

                        if contain_start_point == 1 and contain_end_point == 1:
                            inter2_link_head.append_node(cur_line)

                        elif contain_start_point == 1 and contain_end_point == 0:
                            for p in range(len(cross_points)):
                                if inner_line_harvester.check_contain(cur_line, cross_points[p]):
                                    subline = copy.deepcopy(cur_line)
                                    subline.length = round(get_euclid_dist(line_start_point, cross_points[p]), 2)
                                    subline.end_x = cross_points[p].x
                                    subline.end_y = cross_points[p].y
                            inter2_link_head.append_node(subline)

                        elif contain_start_point == 0 and contain_end_point == 1:
                            for p in range(len(cross_points)):
                                if inner_line_harvester.check_contain(cur_line, cross_points[p]):
                                    subline = copy.deepcopy(cur_line)
                                    subline.length = round(get_euclid_dist(line_end_point, cross_points[p]), 2)
                                    subline.start_x = cross_points[p].x
                                    subline.start_y = cross_points[p].y
                            inter2_link_head.append_node(subline)

                        cur = cur.next

        # print("\n( intercept1_lines )")
        # inter1_link_head.print_all()
        # print("( intercept2_lines )")
        # inter2_link_head.print_all()

        inter1_link_head = set_door_nodes(inter1_link_head)
        inter2_link_head = set_door_nodes(inter2_link_head)
        hallways[i].inter1_link = inter1_link_head
        hallways[i].inter2_link = inter2_link_head

    return hallways


def intersection_of(line_eq1, line_eq2):
    cross_x = 0
    cross_y = 0

    if line_eq1.slope != line_eq2.slope:
        if line_eq1.slope == INFINITY:
            cross_x = line_eq1.intercept
            cross_y = line_eq2.slope * line_eq1.intercept + line_eq2.intercept
        elif line_eq2.slope == INFINITY:
            cross_x = line_eq2.intercept
            cross_y = line_eq1.slope * line_eq2.intercept + line_eq1.intercept
        else:
            numerator = line_eq2.intercept - line_eq1.intercept
            denominator = line_eq1.slope - line_eq2.intercept
            cross_x = numerator / denominator
            cross_y = line_eq1.slope * numerator / denominator + line_eq1.center

        intersection = data_structures.Point()
        intersection.x = round(cross_x, 2)
        intersection.y = round(cross_y, 2)

    return intersection


def get_euclid_dist(p1, p2):
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt((dx * dx) + (dy * dy))
    return dist


def hall_end_check(hall_start_point, hall_end_point, root_point, cross_points):
    hall_end_found = 0

    dist_start_root = get_euclid_dist(hall_start_point, root_point)
    dist_end_root = get_euclid_dist(hall_end_point, root_point)
    if dist_start_root > dist_end_root:
        small_end = hall_end_point
    else:
        small_end = hall_start_point

    for i in range(len(cross_points)):
        cross_x = cross_points[i].x
        cross_y = cross_points[i].y
        if small_end.x == cross_x and small_end.y == cross_y:
            hall_end_found = 1

    return hall_end_found, small_end


def separate_halls(inner_lines, hall_tree):
    hallways = []

    inner_lines_copy = copy.deepcopy(inner_lines)
    hall_pairs = [hall_tree[2], hall_tree[3]]
    hall_pairs_copy = copy.deepcopy(hall_pairs)

    root_point = hall_tree[0]
    cross_points = hall_tree[1]

    # 1. inner_line과 수직이면서 root를 포함하는 직선 생성
    #   - inner_line과 해당 수직선간의 교점을 포함하는지 판단하여 다른각도의 복도를 포함하는지 확인
    # 2. inner_line과 해당 직선 사이의 교점 탐색
    # 3. inner_line이 교점을 포함하는지 확인
    # 4.    if 포함하면:
    #           교점을 기준으로 나누어 intercept의 시작, 끝 지정
    #       else:
    #           선의 시작점, 끝점에서 해당 점을 포함하는 수직선 생성
    #           if root를 포함하는 수직선의 intercept > 생성한 수직선의 intercept:
    #               hall A에 선 추가
    #           else:
    #               hall B에 선 추가

    for i in range(len(hall_pairs_copy)):
        hall_pair_now = copy.deepcopy(hall_pairs_copy[i])
        # print("\n[ HALL PAIR NOW ]\n", hall_pair_now)
        # print("\n===")
        hall_start_point = hall_pair_now.center_start
        hall_end_point = hall_pair_now.center_end

        # hall_end_found가 1이면 root 기준 단일방향 복도, 0이면 root 기준 양방향 복도
        hall_end_found, small_end = hall_end_check(hall_start_point, hall_end_point, root_point, cross_points)
        # print("hall end found?", hall_end_found)

        if hall_end_found == 1:  # root 기준 단일방향 복도인 경우
            # print("\n< One-direction hallway >")
            new_hallway = copy.deepcopy(hall_pair_now)
            if small_end == hall_end_point:
                new_hallway.center_start = hall_pair_now.center_start
                new_hallway.center_end = root_point
            if small_end == hall_start_point:
                new_hallway.center_start = root_point
                new_hallway.center_end = hall_pair_now.center_end
            hallways.append(new_hallway)
            # print("new_hallway:"+str(new_hallway))

        else:  # root 기준 양방향 복도인 경우
            # print("\n< Two-direction hallway >\n", hall_pair_now)
            # print("\n---")
            new_branch1 = copy.deepcopy(hall_pair_now)
            new_branch1.center_end = root_point
            new_branch2 = copy.deepcopy(hall_pair_now)
            new_branch2.center_start = root_point

            for j in range(len(inner_lines_copy)):
                if inner_lines_copy[j].head.data.slope == hall_pair_now.slope:  # 여기에 짧은 hall 끝점 포함하는 조건 추가
                    # print("\n{ inner_line Now }")
                    # print(inner_lines_copy[j].head.data)

                    # 1. inner_line과 수직이면서 root를 포함하는 직선 생성
                    # - inner_line과 해당 수직선간의 교점을 포함하는지 판단하여 다른각도의 복도를 포함하는지 확인
                    line_eq = inner_lines_copy[j].head.data
                    if line_eq.slope == 0:
                        vert_slope = INFINITY
                        vert_intercept = root_point.x
                    else:
                        vert_slope = round(-1 / line_eq.slope, 2)
                        vert_intercept = round(root_point.y - vert_slope * root_point.x, 2)
                    vert_root_eq = data_structures.LineEquation(vert_slope, vert_intercept)

                    # 2. inner_line과 해당 직선 사이의 교점 탐색
                    intersection = intersection_of(line_eq, vert_root_eq)
                    # print("\n( vert_root Intersection )")
                    # print("line_eq:"+str(line_eq) +" & vert:"+ str(vert_root_eq))
                    # print(intersection)

                    wall_equation = data_structures.Line()
                    # print("line_eq.slope:", line_eq.slope)
                    # print("line_eq.intercept:", line_eq.intercept)
                    # print("hall_pair_now.slope:", hall_pair_now.slope)
                    # print("hall_pair_now.intercept1:", hall_pair_now.intercept1)
                    # print("hall_pair_now.intercept2:", hall_pair_now.intercept2)
                    if line_eq.slope == hall_pair_now.slope:
                        if line_eq.intercept == hall_pair_now.intercept1:  # 해당 없음
                            wall_equation.start_x = hall_pair_now.intercept1_start.x
                            wall_equation.start_y = hall_pair_now.intercept1_start.y
                            wall_equation.end_x = hall_pair_now.intercept1_end.x
                            wall_equation.end_y = hall_pair_now.intercept1_end.y
                        elif line_eq.intercept == hall_pair_now.intercept2:
                            wall_equation.start_x = hall_pair_now.intercept2_start.x
                            wall_equation.start_y = hall_pair_now.intercept2_start.y
                            wall_equation.end_x = hall_pair_now.intercept2_end.x
                            wall_equation.end_y = hall_pair_now.intercept2_end.y
                        else:
                            continue

                    is_equation_contain = inner_line_harvester.check_contain(wall_equation, intersection)
                    if is_equation_contain == 1:
                        is_segment_contain = 0
                        segment = None  # not used

                        cur = inner_lines_copy[j].head.next
                        while cur is not None:
                            is_segment_contain = inner_line_harvester.check_contain(cur.data, intersection)
                            if is_segment_contain:
                                segment = cur.data
                                break
                            cur = cur.next

                        # print("is_segment_contain: ", is_segment_contain)
                        if is_segment_contain == 0:
                            for k in range(len(hall_pairs_copy)):
                                hall_pair_other = copy.deepcopy(hall_pairs_copy[k])

                                if hall_pair_other.slope == line_eq.slope:
                                    continue

                                # print("\n---hall_pair_other---")
                                # print(hall_pair_other)

                                # two wall lines of another hall
                                hall_other_wall1 = data_structures.LineEquation()
                                hall_other_wall1.slope = hall_pair_other.slope
                                hall_other_wall1.intercept = hall_pair_other.intercept1
                                hall_other_wall2 = data_structures.LineEquation()
                                hall_other_wall2.slope = hall_pair_other.slope
                                hall_other_wall2.intercept = hall_pair_other.intercept2

                                intersection_1 = intersection_of(line_eq, hall_other_wall1)
                                intersection_2 = intersection_of(line_eq, hall_other_wall2)
                                # print("\n- INTERSECTIONS -")
                                # print("-EQ:", line_eq, hall_other_wall1, hall_other_wall2)
                                # print(intersection_1, intersection_2)

                            if line_eq.slope == 0:
                                vert1_intercept = intersection_1.x
                                vert2_intercept = intersection_2.x
                            else:
                                vert1_intercept = round(intersection_1.y - vert_slope * intersection_1.x, 2)
                                vert2_intercept = round(intersection_2.y - vert_slope * intersection_2.x, 2)

                            # print(vert1_intercept)
                            # print(vert_root_eq.intercept)
                            # print(vert2_intercept)
                            if vert1_intercept > vert_root_eq.intercept > vert2_intercept:
                                new_branch1.intercept1_start = hall_pair_now.intercept1_start
                                new_branch1.intercept1_end = intersection_2
                                new_branch2.intercept1_start = intersection_1
                                new_branch2.intercept1_end = hall_pair_now.intercept1_end
                            elif vert1_intercept < vert_root_eq.intercept < vert2_intercept:
                                new_branch1.intercept1_start = hall_pair_now.intercept1_start
                                new_branch1.intercept1_end = intersection_1
                                new_branch2.intercept1_start = intersection_2
                                new_branch2.intercept1_end = hall_pair_now.intercept1_end

                        else:
                            new_branch1.intercept2_end = intersection
                            new_branch2.intercept2_start = intersection

            hallways.append(new_branch1)
            hallways.append(new_branch2)
            # print("newHallway1: " + str(newHallway1))
            # print("newHallway2: " + str(newHallway2))

    # 1. hall_pairs 쪼개기
    #     root point를 기준으로 나뉘는 두 선들 중 짧은 선 선택
    #         center line의 반대쪽 끝이 두 threshold point 중 하나와 같은 경우
    #             하나의 hall pair 생성
    #         그렇지 않으면
    #             root point를 기준으로 center line  이후 부분 버리고 root를 끝점으로 지정
    # 2. counter-clock wise 알고리즘을 통해 왼쪽 벽면인지 오른쪽 벽면인지 구분하여 저장
    # 3. 그래프 생성

    return hallways


def break_pairs(crossed_halls, inner_lines):
    hall_trees = []

    for i in range(len(crossed_halls)):
        hallways_separated = separate_halls(inner_lines, crossed_halls[i])
        print("\n[hallways_separated]")
        for j in range(len(hallways_separated)):
            print(str(j) + ": " + str(hallways_separated[j]))

        # 각 hallway의 벽면에 포함되는 선들 덧붙임
        hallways = set_hall_lines(inner_lines, hallways_separated, crossed_halls[i][1])
        # print("\n[hallways_node_attached]")
        # for j in range(len(hallways)):
        #     print(str(j) + ": " + str(hallways[j]))
        #     print("{_inter1_}")
        #     hallways[j].inter1_link.print_all()
        #     print("{_inter2_}")
        #     hallways[j].inter2_link.print_all()
        #     print("")

        list_head = data_structures.LinkedList("Branches")
        list_head.name = "Branches"
        for j in range(len(hallways)):
            list_head.append_node(hallways[j])
        new_hall_tree = [crossed_halls[i][0], crossed_halls[i][1], list_head]
        hall_trees.append(new_hall_tree)

    print("\n__Hallway Separation Done__\n")

    return hall_trees


def get_crossed_hall(hall_pairs):
    crossed_halls = []

    for i in range(len(hall_pairs) - 1):
        hall_pair1 = hall_pairs[i]

        for j in range(i + 1, len(hall_pairs)):
            hall_pair2 = hall_pairs[j]

            if hall_pair1.slope == hall_pair2.slope:
                continue
            else:
                cross_points = []
                # 계산식 출처: https://gaussian37.github.io/math-algorithm-intersection_point/
                if hall_pair1.slope == INFINITY:
                    root_x = hall_pair1.center
                    root_y = hall_pair2.slope * hall_pair1.center + hall_pair2.center
                    cross1_x = hall_pair1.center
                    cross1_y = hall_pair2.slope * hall_pair1.center + hall_pair2.intercept1
                    cross2_x = hall_pair1.center
                    cross2_y = hall_pair2.slope * hall_pair1.center + hall_pair2.intercept2
                    cross3_x = hall_pair1.intercept1
                    cross3_y = hall_pair2.slope * hall_pair1.intercept1 + hall_pair2.center
                    cross4_x = hall_pair1.intercept2
                    cross4_y = hall_pair2.slope * hall_pair1.intercept2 + hall_pair2.center
                elif hall_pair2.slope == INFINITY:
                    root_x = hall_pair2.center
                    root_y = hall_pair1.slope * hall_pair2.center + hall_pair1.center
                    cross1_x = hall_pair2.intercept1
                    cross1_y = hall_pair1.slope * hall_pair2.intercept1 + hall_pair1.center
                    cross2_x = hall_pair2.intercept2
                    cross2_y = hall_pair1.slope * hall_pair2.intercept2 + hall_pair1.center
                    cross3_x = hall_pair2.center
                    cross3_y = hall_pair1.slope * hall_pair2.center + hall_pair1.intercept1
                    cross4_x = hall_pair2.center
                    cross4_y = hall_pair1.slope * hall_pair2.center + hall_pair1.intercept2
                else:
                    numerator = hall_pair2.center - hall_pair1.center
                    denominator = hall_pair1.slope - hall_pair2.slope  # hall_pair1.slope - hall_pair2.center 로 되어있었음
                    root_x = numerator / denominator
                    root_y = hall_pair1.slope * (numerator / denominator) + hall_pair1.center

                    numerator = hall_pair2.intercept1 - hall_pair1.center
                    denominator = hall_pair1.slope - hall_pair2.intercept1
                    cross1_x = numerator / denominator
                    cross1_y = hall_pair1.slope * numerator / denominator + hall_pair1.center

                    numerator = hall_pair2.intercept2 - hall_pair1.center
                    denominator = hall_pair1.slope - hall_pair2.intercept2
                    cross2_x = numerator / denominator
                    cross2_y = hall_pair1.slope * numerator / denominator + hall_pair1.center

                    numerator = hall_pair1.intercept1 - hall_pair2.center
                    denominator = hall_pair2.slope - hall_pair1.intercept1
                    cross3_x = numerator / denominator
                    cross3_y = hall_pair2.slope * numerator / denominator + hall_pair2.center

                    numerator = hall_pair1.intercept2 - hall_pair2.center
                    denominator = hall_pair2.slope - hall_pair1.intercept2
                    cross4_x = numerator / denominator
                    cross4_y = hall_pair2.slope * numerator / denominator + hall_pair2.center

                # 기준점
                root_point = data_structures.Point()
                root_point.x = root_x
                root_point.y = root_y

                # 소교차점
                cross_point = data_structures.Point(cross1_x, cross1_y)
                cross_points.append(cross_point)
                cross_point = data_structures.Point(cross2_x, cross2_y)
                cross_points.append(cross_point)
                cross_point = data_structures.Point(cross3_x, cross3_y)
                cross_points.append(cross_point)
                cross_point = data_structures.Point(cross4_x, cross4_y)
                cross_points.append(cross_point)

                crossed_hall = [root_point, cross_points, hall_pair1, hall_pair2]
                crossed_halls.append(crossed_hall)

    return crossed_halls


def get_hall_pairs(inner_lines):
    hall_pairs = []

    slope1 = 0
    slope2 = 0
    intercept1 = 0
    intercept2 = 0
    center_intercept = 0
    inner_lines_copy = copy.deepcopy(inner_lines)

    for i in range(len(inner_lines_copy) - 1):
        if inner_lines_copy[i] is None:
            continue

        slope1 = inner_lines_copy[i].head.data.slope
        intercept1 = inner_lines_copy[i].head.data.intercept

        for j in range(i + 1, len(inner_lines_copy)):
            if inner_lines_copy[i] is None or inner_lines_copy[j] is None:
                continue

            slope2 = inner_lines_copy[j].head.data.slope
            intercept2 = inner_lines_copy[j].head.data.intercept

            if slope1 != slope2:
                continue
            else:
                # print("slope1", slope1)
                # print("slope2", slope2)
                center_intercept = round((intercept1 + intercept2) / 2, 2)

                # 직선들의 가장 작은 시작 좌표값, 가장 큰 끝 좌표값 선택
                starting_point1, end_point1 = inner_lines_copy[i].get_endpoints()
                # print("side1")
                # print(starting_point1, end_point1)
                starting_point2, end_point2 = inner_lines_copy[j].get_endpoints()
                # print("side2")
                # print(starting_point2, end_point2)

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

                new_hall_pair = data_structures.Pair()
                new_hall_pair.name = "hallPair"
                new_hall_pair.intercept1 = intercept1
                new_hall_pair.intercept2 = intercept2
                new_hall_pair.center = center_intercept
                new_hall_pair.slope = slope1
                new_hall_pair.center_start = center_start
                new_hall_pair.center_end = center_end
                new_hall_pair.intercept1_start = starting_point1
                new_hall_pair.intercept1_end = end_point1
                new_hall_pair.intercept2_start = starting_point2
                new_hall_pair.intercept2_end = end_point2

                hall_pairs.append(new_hall_pair)
                inner_lines_copy[i] = None
                inner_lines_copy[j] = None

    return hall_pairs
