import operator
import math
import copy
from dataclasses import dataclass


@dataclass
class Hallway:
    branch_num: int = None
    left_wall: [] = None
    right_wall: [] = None


@dataclass
class Position:
    left_position: [] = None
    right_position: [] = None


def get_candidates(estimate_len_left, estimate_len_right, forward_position, backward_position):
    forward_position_found = []
    backward_position_found = []
    forward_highest = 0
    backward_highest = 0

    print("")
    for i in range(len(forward_position)):
        left_relative = 0
        right_relative = 0
        result_len_left = len(forward_position[i].left_position)
        result_len_right = len(forward_position[i].right_position)

        print("[FORWARD SET " + str(i) + "]")
        for j in range(result_len_left):
            print("- ", forward_position[i].left_position[j][0], "[",
                  forward_position[i].left_position[j][1].val, "]", forward_position[i].left_position[j][2])
            left_relative = forward_position[i].left_position[j][0] / estimate_len_left
            print("\t\t- relative: ", left_relative)
        for k in range(result_len_right):
            print("- ", forward_position[i].right_position[k][0], "[",
                  forward_position[i].right_position[k][1].val, "]", forward_position[i].right_position[k][2])
            right_relative = forward_position[i].right_position[j][0] / estimate_len_right
            print("\t\t- relative: ", right_relative)
        sim_score = forward_position[i].left_position[j][0] + forward_position[i].right_position[k][0]
        print("=> score:", sim_score)

        if sim_score >= forward_highest:
            forward_highest = sim_score
            forward_position_found = [forward_position[i], sim_score, left_relative, right_relative]

    for i in range(len(backward_position)):
        left_relative = 0
        right_relative = 0
        result_len_left = len(backward_position[i].left_position)
        result_len_right = len(backward_position[i].right_position)

        print("[BACKWARD SET " + str(i) + "]")
        for j in range(result_len_left):
            print("- ", backward_position[i].left_position[j][0], "[",
                  backward_position[i].left_position[j][1].val, "]", backward_position[i].left_position[j][2])
            left_relative = backward_position[i].left_position[j][0] / estimate_len_left
            print("\t\t- relative: ", left_relative)
        for k in range(result_len_right):
            print("- ", backward_position[i].right_position[k][0], "[",
                  backward_position[i].right_position[k][1].val, "]", backward_position[i].right_position[k][2])
            right_relative = backward_position[i].right_position[j][0] / estimate_len_right
            print("\t\t- relative: ", right_relative)
        sim_score = backward_position[i].left_position[j][0] + backward_position[i].right_position[k][0]
        print("=> score:", sim_score)

        if sim_score >= backward_highest:
            backward_highest = sim_score
            backward_position_found = [backward_position[i], sim_score, left_relative, right_relative]

    return forward_position_found, backward_position_found


def slide(direction, side, hallways, hallway_index, index, check_size, passed_len_this, passed_len_other, this_waiting,
          ratio, estimate_len, position_list):
    passed_len_thresh = 3
    # future_len_thresh = 3 # not used

    diff_of_passed = round(abs(passed_len_this - passed_len_other), 2)
    if side == 'left':
        hallway = hallways[hallway_index].left_wall.copy()
        node_now = hallway[index]
    else:
        hallway = hallways[hallway_index].right_wall.copy()
        node_now = hallway[index]

    print("==================== diff of passed ====================", diff_of_passed)
    print("index:", index, "/", check_size - 1, ", check size: " + str(check_size) + " (start from 0)")

    print("waiting condition (diff/thresh): ", str(diff_of_passed) + "/" + str(passed_len_thresh))
    if (diff_of_passed <= passed_len_thresh and passed_len_other > passed_len_this) or passed_len_other > passed_len_this:
        this_waiting = False
    print("(hallway " + str(hallway_index) + ")_node: [ " + str(node_now.val) + " ]")

    print("node_index_now: " + str(index) + " / " + str(len(hallway) - 1))
    if index < len(hallway):
        # 6미터 이내부터는 슬라이딩은 안하고 유사도 계산만 수행하도록
        # 자신이 한 번 wating에 빠졌으면 다른쪽이 자신을 n미터 이상 지날때까지 wating 유지
        # 각 노드들에 대한 계산 결과는 해당 복도에서 계산이 끝날 때까지 저장해두고, 7미터 이내 결과들은 모두 조합해서 전달
        # 윈도우의 맨 앞까지의 길이도 고려 대상 -> 아니면 처음 만난 문부터 passed_len 계산
        # wating, 유사도 계산은 현재 노드가 문일때만 수행

        future_len_this = passed_len_this + node_now.length - passed_len_other  # future가 너무 커도 wait 상태로 진입하도록 수정
        print("[future] passed_len_this (" + str(passed_len_this) + ") + node_now.length (" + str(node_now.length) +
              ") - passed_len_other (" + str(passed_len_other) + ") = " + str(round(future_len_this, 2)))

        # if future_len_this >= future_len_thresh:
        #     this_waiting = True
        #     print("__" + str(node_now.val) + " wait__ case 2: future length is longer than "+str(future_len_thresh))
        #     if side == 'left':
        #         print("<< total_left_passed: ", passed_len_this)
        #     else:
        #         print(">> total right_passed: ", passed_len_this)

        if (passed_len_this > passed_len_other and abs(future_len_this) > passed_len_thresh) or this_waiting is True:
            this_waiting = True
            if index < check_size - 1:
                print("---------------------------node_" + str(node_now.val))
                ###
                real_sum = 0
                for k in range(estimate_len):
                    s = min(hallway[index + k].length, ratio[k]) / max(
                        hallway[index + k].length, ratio[k])
                    print("s: ", s)  # short/long -> 값 1에 가까울수록 유사함
                    real_sum = real_sum + s  # 값이 클 수록 유사함
                print("[real_sum]: ", real_sum)
                position_list.append([real_sum, hallway[index], direction])
                print("---------------------------------")
                ###
            print("  __" + str(node_now.val) + " wait__   * case 1: passed length is longer than other & the length is "
                                               "longer than " + str(passed_len_thresh))
            if side == 'left':
                print("<< total_left_passed: ", passed_len_this)
            else:
                print(">> total right_passed: ", passed_len_this)

    if this_waiting is False:
        if index < check_size - 1:
            print("---------------------------node_" + str(node_now.val))
            ###
            real_sum = 0
            for k in range(estimate_len):
                s = min(hallway[index + k].length, ratio[k]) / max(
                    hallway[index + k].length, ratio[k])
                print("s: ", s)  # short/long -> 값 1에 가까울수록 유사함
                real_sum = real_sum + s  # 값이 클 수록 유사함
            print("[real_sum]: ", real_sum)
            position_list.append([real_sum, hallway[index], direction])
            print("---------------------------------")
            ###
            if index == check_size - 1:
                if node_now.name == 'wall':
                    position_list = []
                return index, this_waiting, passed_len_this, passed_len_other, diff_of_passed, position_list
            passed_len_this += node_now.length
            index += 1
            print("!" + str(node_now.val) + " moved!")
            print(">> this_total_passed: ", passed_len_this)
    # else:
    #     if index < check_size - 1:
    #         passed_len_this += node_now.length
    #         index += 1

    if node_now.name == 'wall':
        position_list = []

    return index, this_waiting, passed_len_this, passed_len_other, diff_of_passed, position_list


def check_similarity(hall_nodes, hall_nodes_reverse, left_ratio, right_ratio):
    hallways = []
    hallways_reverse = []
    for i in range(int(len(hall_nodes) / 2)):
        hallway = Hallway()
        hallway_reverse = Hallway()
        hallways.append(hallway)
        hallways_reverse.append(hallway_reverse)

    for i in range(len(hall_nodes)):
        branch_num = hall_nodes[i][0].branch_num
        if branch_num is not None:
            hallways[branch_num].branch_num = branch_num
            if hall_nodes[i][0].side == 'forward-left':
                hallways[branch_num].left_wall = hall_nodes[i].copy()
            else:
                hallways[branch_num].right_wall = hall_nodes[i].copy()
    # print("(forward)")
    # for i in range(len(hallways)):
    #     print("[HALL "+str(hallways[i].branch_num)+"]")
    #     print("-left wall: ", hallways[i].left_wall[0].val)
    #     print("-right wall: ", hallways[i].right_wall[0].val)
    # print("---")

    for i in range(len(hall_nodes_reverse)):
        branch_num = hall_nodes_reverse[i][0].branch_num
        if branch_num is not None:
            hallways_reverse[branch_num].branch_num = branch_num
            if hall_nodes_reverse[i][0].side == 'forward-left':
                hallways_reverse[branch_num].left_wall = hall_nodes_reverse[i].copy()
            else:
                hallways_reverse[branch_num].right_wall = hall_nodes_reverse[i].copy()
    # print("(backward)")
    # for i in range(len(hallways_reverse)):
    #     print("[HALL " + str(hallways_reverse[i].branch_num) + "]")
    #     print("-left wall: ", hallways_reverse[i].left_wall[0].val)
    #     print("-right wall: ", hallways_reverse[i].right_wall[0].val)
    # print("---")

    estimate_len_left = len(left_ratio)
    estimate_len_right = len(right_ratio)
    print("estimate_len_left:", estimate_len_left)
    print("estimate_len_right:", estimate_len_right)

    if estimate_len_left > 1 and estimate_len_right > 1:
        avail = True
    else:
        avail = False

    forward_position = []
    backward_position = []
    if avail:
        # forward check
        direction = 'forward'
        print("\n***** IN " + direction + " TEST *****")
        for i in range(len(hallways)):
            print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
            print("len(hallways[" + str(i) + "].left_wall):", len(hallways[i].left_wall))
            print("len(hallways[" + str(i) + "].right_wall):", len(hallways[i].right_wall))

            if len(hallways[i].left_wall) >= estimate_len_left and len(hallways[i].right_wall) >= estimate_len_right:
                left_check_size = len(hallways[i].left_wall) - estimate_len_left + 1
                right_check_size = len(hallways[i].right_wall) - estimate_len_right + 1
                max_check_size = max(left_check_size, right_check_size)
                print("\nleft_check_size: ", left_check_size)
                print("right_check_size:", right_check_size)

                # ratio_len_left = 0
                # ratio_len_right = 0
                # for l in range(estimate_len_left):
                #     ratio_len_left += left_ratio[l]
                # for r in range(estimate_len_right):
                #     ratio_len_right += right_ratio[r]
                # print("ratio_len_left: ", ratio_len_left)
                # print("ratio_len_right: ", ratio_len_right)

                left_index = 0
                right_index = 0
                passed_len_left = 0
                passed_len_right = 0
                diff_of_passed = 0
                left_waiting = False
                right_waiting = False
                for j in range(max_check_size):
                    left_position = []
                    right_position = []
                    print("\n\n[ SET: " + str(
                        j) + " ] ===============================================================================")

                    # break condition
                    if left_index >= left_check_size - 1 and right_waiting is True:
                        print("end 1: left side is done & right side is waiting")
                        break
                    if right_index >= right_check_size - 1 and left_waiting is True:
                        print("end 2: right side is done & left side is waiting")
                        break
                    if left_waiting is True and right_waiting is True:
                        print("end 3: both side is waiting each other")
                        break

                    # left side sliding
                    left_index, left_waiting, passed_len_left, passed_len_right, diff_of_passed, left_position = \
                        slide(direction, 'left', hallways, i, left_index, left_check_size,
                              passed_len_left, passed_len_right, left_waiting, left_ratio,
                              estimate_len_left, left_position)
                    # right side sliding
                    right_index, right_waiting, passed_len_right, passed_len_left, diff_of_passed, right_position = \
                        slide(direction, 'right', hallways, i, right_index, right_check_size,
                              passed_len_right, passed_len_left, right_waiting, right_ratio,
                              estimate_len_right, right_position)

                    if len(left_position) != 0 and len(right_position) != 0:
                        position = Position()
                        position.left_position = left_position.copy()
                        position.right_position = right_position.copy()
                        forward_position.append(position)

        # backward check => 방향은 맞는데 왼쪽, 오른쪽 비율을 오른쪽 왼쪽 벽면과 비교하고있음
        direction = 'backward'
        print("\n***** IN " + direction + " TEST *****")
        for i in range(len(hallways_reverse)):
            print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
            print("len(hallways_reverse[i].left_wall):", len(hallways_reverse[i].left_wall))
            print("len(hallways_reverse[i].right_wall):", len(hallways_reverse[i].right_wall))

            if len(hallways_reverse[i].left_wall) >= estimate_len_left and \
                    len(hallways_reverse[i].right_wall) >= estimate_len_right:
                left_check_size = len(hallways_reverse[i].right_wall) - estimate_len_left + 1  # right * reverse = left
                right_check_size = len(hallways_reverse[i].left_wall) - estimate_len_right + 1  # left * reverse = right
                max_check_size = max(left_check_size, right_check_size)
                print("\nleft_check_size: ", left_check_size)
                print("right_check_size:", right_check_size)

                left_index = 0
                right_index = 0
                passed_len_left = 0
                passed_len_right = 0
                diff_of_passed = 0
                left_waiting = False
                right_waiting = False
                for j in range(max_check_size):
                    left_position = []
                    right_position = []

                    print("\n\n[ SET: " + str(
                        j) + " ] ===============================================================================")
                    if left_index >= left_check_size - 1 and right_waiting is True:
                        print("end 1: left side is done & right side is waiting")
                        break
                    if right_index >= right_check_size - 1 and left_waiting is True:
                        print("end 2: right side is done & left side is waiting")
                        break
                    if left_waiting is True and right_waiting is True:
                        print("end 3: both side is waiting each other")
                        break

                    # left side sliding
                    left_index, left_waiting, passed_len_left, passed_len_right, diff_of_passed, left_position = \
                        slide(direction, 'right', hallways_reverse, i, left_index, left_check_size,
                              passed_len_left, passed_len_right, left_waiting, left_ratio,
                              estimate_len_left, left_position)

                    # right side sliding
                    right_index, right_waiting, passed_len_right, passed_len_left, diff_of_passed, right_position = \
                        slide(direction, 'left', hallways_reverse, i, right_index, right_check_size,
                              passed_len_right, passed_len_left, right_waiting, right_ratio,
                              estimate_len_right, right_position)

                    if len(left_position) != 0 and len(right_position) != 0:
                        position = Position()
                        position.left_position = left_position.copy()
                        position.right_position = right_position.copy()
                        backward_position.append(position)

    return estimate_len_left, estimate_len_right, forward_position, backward_position
