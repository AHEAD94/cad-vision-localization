import copy
import math

import data_structures
import processor

INFINITY = 999999
INNER_WALL_THICKNESS = 0.2
OUTER_WALL_THICKNESS = 0.5


def check_contain(line, point):
    equation = processor.def_line_equation(line.start_x, line.start_y, line.end_x, line.end_y)

    if line.start_y <= point.y <= line.end_y or line.end_y <= point.y <= line.start_y:
        # if line.start_y <= point.y <= line.end_y:
        if equation.slope == INFINITY:
            # print("[infinity]")
            if point.x == line.start_x and point.x == line.end_x:
                # if line.start_x-0.1 <= point.x <= line.start_x+0.1:
                return 1
            else:
                return 0
        elif equation.slope == 0:
            if line.start_x <= point.x <= line.end_x:
                return 1
            else:
                return 0
        else:
            # print("[non-infinity]")
            # print("1. " + str(point.y) + " == " + str(round(equation.slope * point.x + equation.intercept, 2)))
            # print("eq.slope:", equation.slope)
            # print("eq.inter:", equation.intercept)
            y_cal = round(equation.slope * point.x + equation.intercept, 2)
            # print("\ncur_line:", line)
            # print("point:", point)
            # print("비교 (point.y and y_cal, diff):", point.y, y_cal, abs(point.y - y_cal))
            if abs(point.y - y_cal) <= 0.15 and line.length < 2:  # y에 허용치 둬야함 (y 1.5)
                return 1
            else:
                return 0
    else:
        return 0


def get_center_point(line, equation):  # 선 중심점 리턴
    if equation.slope == INFINITY:
        center_x = line.start_x
        center_y = round((line.start_y + line.end_y) / 2, 2)
    elif equation.slope == 0:
        center_x = round((line.start_x + line.end_x) / 2, 2)
        center_y = line.start_y
    else:
        # center_y = round((line.start_y + line.end_y)/2, 2)
        # center_x = round((center_y-equation.intercept)/equation.slope, 2) # 왜 이렇게 했지
        center_x = round((line.start_x + line.end_x) / 2, 2)
        center_y = round((line.start_y + line.end_y) / 2, 2)
    return center_x, center_y


def add_sill_line(adj_center_x, adj_center_y, equation_adj, block, line_equations):
    if block.name == "doorBlock":
        sill_length = 1
    elif block.name == "doorBlockBoth":
        sill_length = 1.93
    elif block.name == "doorBlockSmall":
        sill_length = 0.93

    sill_start_x = adj_center_x
    sill_start_y = adj_center_y
    print("sill_start_x:", sill_start_x)
    print("sill_start_y:", sill_start_y)

    if equation_adj.slope != 0:
        print("equation_adj.slope:", equation_adj.slope)
        sill_slope = -1 / equation_adj.slope
        print("sill_slope:", sill_slope)

        # point_1 = data_structures.Point()
        # point_1.x = round(sill_start_x + (sill_length * math.cos(sill_slope)), 2)
        # point_1.y = round(sill_start_y + (sill_length * math.sin(sill_slope)), 2)
        # point_2 = data_structures.Point()
        # point_2.x = round(sill_start_x - (sill_length * math.cos(sill_slope)), 2)
        # point_2.y = round(sill_start_y - (sill_length * math.sin(sill_slope)), 2)

        point_1 = data_structures.Point()
        point_1.x = round(sill_start_x + sill_length / math.sqrt(1 + sill_slope * sill_slope), 2)
        point_1.y = round(sill_start_y + sill_length * sill_slope / math.sqrt(1 + sill_slope * sill_slope), 2)
        point_2 = data_structures.Point()
        point_2.x = round(sill_start_x - sill_length / math.sqrt(1 + sill_slope * sill_slope), 2)
        point_2.y = round(sill_start_y - sill_length * sill_slope / math.sqrt(1 + sill_slope * sill_slope), 2)

        print("end_point_1:", point_1)
        print("end_point_2:", point_2)

    for i in range(len(line_equations)):
        cur = line_equations[i].head.next
        while cur is not None:
            cur_line = cur.data

            # 방향 구분하는 알고리즘 필요 -> 길이만큼의 거리에 닿는 벽 있는지 확인
            if equation_adj.slope == 0:
                sill_end_x = sill_start_x

                point_1 = data_structures.Point()
                point_1.x = sill_end_x
                point_1.y = round(sill_start_y + sill_length, 2)
                point_2 = data_structures.Point()
                point_2.x = sill_end_x
                point_2.y = round(sill_start_y - sill_length, 2)

                if check_contain(cur_line, point_1):
                    sill_end_y = point_1.y
                    break
                elif check_contain(cur_line, point_2):
                    sill_end_y = point_2.y
                    break
            else:
                # print("check_contain ?")
                if check_contain(cur_line, point_1):
                    sill_end_x = point_1.x
                    sill_end_y = point_1.y
                    break
                elif check_contain(cur_line, point_2):
                    sill_end_x = point_2.x
                    sill_end_y = point_2.y
                    break
                # else:
                #     pass
                # print(point_1, point_2)
            cur = cur.next

    sill_line = data_structures.Line()
    sill_line.layer = "SILL"
    sill_line.length = sill_length
    sill_line.start_x = sill_start_x
    sill_line.start_y = sill_start_y
    sill_line.end_x = sill_end_x
    sill_line.end_y = sill_end_y
    print("-- new sill_line:", sill_line)

    return sill_line


def setup_door_sill(door_block_list, line_equations, door_sills=[]):
    line_now = data_structures.Line()

    print("[ len of door block list:", len(door_block_list), "]")
    for b in range(len(door_block_list)):
        block = door_block_list[b]
        start_x = block.location_x
        start_y = block.location_y

        # print("=====================================================================================================")
        # print("[block No. " + str(b) + "]")
        for i in range(len(line_equations)):
            cur = line_equations[i].head.next
            while cur is not None:
                cur_line = cur.data
                point = data_structures.Point(x=start_x, y=start_y)

                # 대각선의 경우, 다른 선들도 검출될 수 있음
                # -> 1. 스캔 후 가장 차이가 작은 선 선택하거나
                # -> 2. 조건 추가해서 블럭 기준점, 호 중심점과 연관시키기
                if check_contain(cur_line, point):
                    # print("\n--")
                    # print("cur_line:", cur_line)
                    # print("point:", point)
                    # print("!contain!")
                    list_head = data_structures.LinkedList(block)
                    list_head.name = "Enclosings"
                    list_head.append_node(cur_line)
                    door_sills.append(list_head)
                    line_now = cur_line
                cur = cur.next
        # print("=====================================================================================================")

        # door sill line
        # print("__Adding door sill line__\n")

        equation_adj = processor.def_line_equation(line_now.start_x, line_now.start_y, line_now.end_x, line_now.end_y)
        center_x, center_y = get_center_point(line_now, equation_adj)  # center of what?
        # print("-- line_now:", line_now)
        # print("-- line_eq:", equation_adj)
        # print("-- block No." + str(b) + ":", block)
        # print("-- center point:", center_x, center_y)

        door_sill = add_sill_line(center_x, center_y, equation_adj, block, line_equations)
        door_sills[b].append_node(door_sill)


def is_adjacent(line_now, target_line):
    now_start_x = line_now.start_x
    now_start_y = line_now.start_y
    now_end_x = line_now.end_x
    now_end_y = line_now.end_y
    target_start_x = target_line.start_x
    target_start_y = target_line.start_y
    target_end_x = target_line.end_x
    target_end_y = target_line.end_y

    if now_start_x == target_start_x and now_start_y == target_start_y:
        return 1
    elif now_start_x == target_end_x and now_start_y == target_end_y:
        return 1
    elif now_end_x == target_start_x and now_end_y == target_start_y:
        return 1
    elif now_end_x == target_end_x and now_end_y == target_end_y:
        return 1
    else:
        return 0


def harvest_lines(line_equations, door_sills):
    inner_lines = []
    wall_lines_copy = copy.deepcopy(line_equations)
    sill_lines_copy = copy.deepcopy(door_sills)

    roop = 0
    line_now = None
    fork_stack = []
    prev_wall_line = None
    pass_value = 0
    is_closed = 0

    cur_enclose = sill_lines_copy[0].head.next  # doorBlock 기준점을 포함하는 벽선, 문틀선 포함
    if cur_enclose is not None:
        line_start = cur_enclose.data

    while line_now != line_start:
        print("[roop: " + str(roop) + "]")
        candidates = 0
        contain_block = 0
        successor_found = 0

        if line_now is None:
            line_now = line_start
            for i in range(len(wall_lines_copy)):
                wall_lines_copy[i].remove_node(line_now)
        print(line_now)

        if line_now.layer == 'W':
            # 1. door block 기준점을 포함하는지 확인
            for i in range(len(sill_lines_copy)):
                block_point = data_structures.Point()
                block_point.x = sill_lines_copy[i].head.data.location_x
                block_point.y = sill_lines_copy[i].head.data.location_y
                if check_contain(line_now, block_point):
                    contain_block = 1
                    if sill_lines_copy[i].head.next.next is not None:
                        sill_line = sill_lines_copy[i].head.next.next.data
                        sill_lines_copy[i].remove_node(sill_line)
            # 1. sill line의 끝점을 포함하는지 확인
            if contain_block == 0:
                for i in range(len(sill_lines_copy)):
                    cur = sill_lines_copy[i].head.next
                    while cur is not None:
                        if cur.data.layer == 'SILL':
                            target_line = cur.data
                            target_end_point = data_structures.Point()
                            target_end_point.x = target_line.end_x
                            target_end_point.y = target_line.end_y
                            if check_contain(line_now, target_end_point):
                                contain_block = 1
                                sill_line = target_line
                                sill_lines_copy[i].remove_node(sill_line)
                        cur = cur.next
            # 1. door block 기준점 or sill line 끝점을 포함하는 벽일 경우
            if contain_block:
                successor_found = 1
                inner_lines.append(line_now)
                line_now = sill_line

            # 2. 그냥 벽인 경우
            else:
                for i in range(len(wall_lines_copy)):
                    cur = wall_lines_copy[i].head.next
                    while cur is not None:
                        target_line = cur.data

                        if is_adjacent(line_now, target_line) and target_line != line_now:

                            if prev_wall_line is not None:
                                # print("prev_wall_line", prev_wall_line)
                                prev_start_x = prev_wall_line.start_x
                                prev_start_y = prev_wall_line.start_y
                                prev_end_x = prev_wall_line.end_x
                                prev_end_y = prev_wall_line.end_y
                                tar_start_x = target_line.start_x
                                tar_start_y = target_line.start_y
                                tar_end_x = target_line.end_x
                                tar_end_y = target_line.end_y

                                prev_wall_eq = processor.def_line_equation(prev_start_x, prev_start_y, prev_end_x,
                                                                           prev_end_y)
                                target_line_eq = processor.def_line_equation(tar_start_x, tar_start_y, tar_end_x,
                                                                             tar_end_y)

                                # sill line 이후 새로 선택하는 그냥 벽이 이전의 그냥 벽과 기울기 같고 절편이 다른 경우 pass
                                if prev_wall_eq.slope == target_line_eq.slope:
                                    if prev_wall_eq.intercept != target_line_eq.intercept:
                                        pass_value = 1
                                        # pass

                                #####################################################
                                # print("prev_wall_line:", prev_wall_line)
                                # print("prev_slope:", prev_wall_eq.slope)
                                # print("prev_intercept:", prev_wall_eq.intercept)
                                # print("target_line:", target_line)
                                # print("target_slope:", target_line_eq.slope)
                                # print("target_intercept:", target_line_eq.intercept)
                                # print("pass_value:", pass_value)
                                # print("----")
                                #####################################################

                            if pass_value != 1:
                                successor_found = 1
                                candidates += 1
                                # print("_candidate: ", target_line)
                                wall_lines_copy[i].remove_node(cur.data)
                                # fork_stack.append(target_line)

                                # ===================================
                                wall_lines_backup = copy.deepcopy(wall_lines_copy)
                                sill_lines_backup = copy.deepcopy(sill_lines_copy)
                                inner_lines_backup = copy.deepcopy(inner_lines)
                                stack_box = [target_line, wall_lines_backup, sill_lines_backup, inner_lines_backup]
                                fork_stack.append(stack_box)
                                # ===================================
                        cur = cur.next
                        pass_value = 0

                if successor_found == 1 and len(fork_stack) != 0:
                    # ===================================
                    popped = fork_stack.pop()
                    candi_line = popped[0]
                    wall_lines_copy = popped[1]
                    sill_lines_copy = popped[2]
                    inner_lines = popped[3]

                    inner_lines.append(line_now)
                    line_now = candi_line
                    # ===================================
                    # candi_line = fork_stack.pop()
                    # inner_lines.append(line_now)
                    # line_now = candi_line

                # prev_wall_line 선택할 때, inner_wall_thickness 보다 긴 선만 선택하도록
                if line_now.length > INNER_WALL_THICKNESS:
                    prev_wall_line = line_now

        elif line_now.layer == 'SILL':
            for i in range(len(wall_lines_copy)):
                cur = wall_lines_copy[i].head.next
                while cur is not None:
                    cur_line = cur.data

                    sill_end_point = data_structures.Point()
                    sill_end_point.x = line_now.end_x
                    sill_end_point.y = line_now.end_y
                    if check_contain(cur_line, sill_end_point) and successor_found == 0:
                        successor_found = 1
                        # print("++",line_now)
                        inner_lines.append(line_now)
                        line_now = cur_line
                        # print("--",cur_line)
                        wall_lines_copy[i].remove_node(cur_line)

                    sill_start_point = data_structures.Point()
                    sill_start_point.x = line_now.start_x
                    sill_start_point.y = line_now.start_y
                    if check_contain(cur_line, sill_start_point) and successor_found == 0:
                        successor_found = 1
                        inner_lines.append(line_now)
                        line_now = cur_line
                        # print("--",cur_line)
                        wall_lines_copy[i].remove_node(cur_line)

                        for j in range(len(sill_lines_copy)):
                            block_point = data_structures.Point()
                            block_point.x = sill_lines_copy[j].head.data.location_x
                            block_point.y = sill_lines_copy[j].head.data.location_y

                            if block_point.x == sill_start_point.x and block_point.y == sill_start_point.y:
                                victim = j
                        sill_lines_copy.remove(sill_lines_copy[victim])

                    cur = cur.next

        if roop > 0 and is_adjacent(line_now, line_start):
            inner_lines.append(line_now)
            is_closed = 1

        if successor_found == 0 and len(fork_stack) != 0 and is_closed == 0:
            # ===================================
            print("!retry!")
            roop = -1
            popped = fork_stack.pop()
            candi_line = popped[0]
            wall_lines_copy = popped[1]
            sill_lines_copy = popped[2]
            inner_lines = popped[3]
            line_now = candi_line
            # ===================================

        if successor_found == 0 and len(fork_stack) == 0 or is_closed == 1:
            break
        roop += 1

        # print("after", line_now)

    if is_closed:
        print("\n__Enclosing Success__\n")
    else:
        print("\n__Enclosing Failed__\n")

    return inner_lines


def get_enclosings(line_equations, door_block_list):
    print("\n__Enclosing Line Harvesting__\n")
    door_sills = []
    enclosing_lines = []

    setup_door_sill(door_block_list, line_equations, door_sills)
    print("\n_sill line setup done_")
    print("sill lines: " + str(len(door_sills)))

    print("\n_line harvesting start_\n")
    inner_lines = harvest_lines(line_equations, door_sills)
    processor.classify_same_wall_lines(inner_lines, enclosing_lines)

    return enclosing_lines, door_sills


def get_hall_end_lines(line_equations):
    left_outline = None
    right_outline = None
    top_outline = None
    bottom_outline = None

    vert_min = 999999
    vert_max = -1
    hori_min = 999999
    hori_max = -1

    # print("OUTLINES!")

    for i in range(len(line_equations)):
        # print(line_equations[i].head.data)
        if line_equations[i].head.data.slope == 0:
            if line_equations[i].head.data.intercept > hori_max:
                bottom_outline = line_equations[i].head.data
                hori_max = line_equations[i].head.data.intercept
            elif line_equations[i].head.data.intercept < hori_min:
                top_outline = line_equations[i].head.data
                hori_min = line_equations[i].head.data.intercept

        if line_equations[i].head.data.slope == INFINITY:
            if line_equations[i].head.data.intercept > vert_max:
                right_outline = line_equations[i].head.data
                vert_max = line_equations[i].head.data.intercept
            elif line_equations[i].head.data.intercept < vert_min:
                left_outline = line_equations[i].head.data
                vert_min = line_equations[i].head.data.intercept

    outlines = [top_outline, bottom_outline, right_outline, left_outline]
    indoor_outlines = []

    for i in range(len(outlines)):
        for j in range(len(line_equations)):
            target_equation = line_equations[j].head.data
            if target_equation.slope == outlines[i].slope:
                if abs(outlines[i].intercept - target_equation.intercept) == OUTER_WALL_THICKNESS:
                    indoor_outlines.append(target_equation)

    return indoor_outlines


def get_inner_lines(line_equations, enclosings, door_sills):
    victim_list = []
    enclosings_copy = copy.deepcopy(enclosings)
    sill_lines_copy = copy.deepcopy(door_sills)

    indoor_outlines = get_hall_end_lines(line_equations)

    for i in range(len(enclosings_copy)):
        if enclosings_copy[i].head.next.data.layer == 'SILL':
            victim_list.append(enclosings_copy[i])

        # elif enclosings_copy[i].head.next.next is None: # 직선 방정식에 속하는 선이 하나만 있는 경우
        #     victim_list.append(enclosings_copy[i])

        else:  # 문 block point나 sill line end point를 포함하는 선은 victim으로 간주
            for j in range(len(sill_lines_copy)):
                block_point = data_structures.Point()
                block_point.x = sill_lines_copy[j].head.data.location_x
                block_point.y = sill_lines_copy[j].head.data.location_y

                cur = enclosings_copy[i].head.next
                while cur is not None:
                    if check_contain(cur.data, block_point):
                        victim_list.append(enclosings_copy[i])
                        break
                    cur = cur.next

            out_cur = enclosings_copy[i].head.next
            while out_cur is not None:
                line_now = out_cur.data
                for k in range(len(sill_lines_copy)):
                    cur = sill_lines_copy[k].head.next
                    while cur is not None:
                        if cur.data.layer == 'SILL':
                            target_line = cur.data
                            target_end_point = data_structures.Point()
                            target_end_point.x = target_line.end_x
                            target_end_point.y = target_line.end_y
                            if check_contain(line_now, target_end_point):
                                victim_list.append(enclosings_copy[i])
                        cur = cur.next
                out_cur = out_cur.next

            # 외벽의 내측 벽면은 복도의 끝 벽선으로 간주하여 추방
            for k in range(len(indoor_outlines)):
                if enclosings_copy[i].head.data.intercept == indoor_outlines[k].intercept:
                    victim_list.append(enclosings_copy[i])

    for i in range(len(victim_list)):
        # print(victim_list[i].head.next.data)
        if victim_list[i] in enclosings_copy:
            enclosings_copy.remove(victim_list[i])

    inner_lines = enclosings_copy

    return inner_lines
