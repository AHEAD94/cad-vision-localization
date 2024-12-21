import operator
import math
import copy


def check_similar(hall_nodes, hall_nodes_reverse, left_ratio, right_ratio):
    right_hall_nodes = []
    left_hall_nodes = []
    right_hall_nodes_reverse = []
    left_hall_nodes_reverse = []

    for i in range(len(hall_nodes)):
        if hall_nodes[i][0].side == 'forward-right':
            right_hall_nodes.append(hall_nodes[i])
        elif hall_nodes[i][0].side == 'forward-left':
            left_hall_nodes.append(hall_nodes[i])
    print("(FORWARD)")
    print("right_nodes:", len(right_hall_nodes), " left_nodes:", len(left_hall_nodes))
    # for i in range(len(right_hall_nodes)):
    #     print("_right_")
    #     for j in range(len(right_hall_nodes[i])):
    #         print(right_hall_nodes[i][j].val)
    # for i in range(len(left_hall_nodes)):
    #     print("_left_")
    #     for j in range(len(left_hall_nodes[i])):
    #         print(left_hall_nodes[i][j].val)

    for i in range(len(hall_nodes_reverse)):
        if hall_nodes_reverse[i][0].side == 'forward-right':
            right_hall_nodes_reverse.append(hall_nodes_reverse[i])
        elif hall_nodes_reverse[i][0].side == 'forward-left':
            left_hall_nodes_reverse.append(hall_nodes_reverse[i])
    print("(BACKWARD)")
    print("right_nodes:", len(right_hall_nodes_reverse), " left_nodes:", len(left_hall_nodes_reverse))
    # for i in range(len(right_hall_nodes_reverse)):
    #     print("_right_reverse_")
    #     for j in range(len(right_hall_nodes_reverse[i])):
    #         print(right_hall_nodes_reverse[i][j].val)
    # for i in range(len(left_hall_nodes_reverse)):
    #     print("_left_reverse_")
    #     for j in range(len(left_hall_nodes_reverse[i])):
    #         print(left_hall_nodes_reverse[i][j].val)

    # right_side
    estimate_len = len(right_ratio)
    print("-length of right ratio: ", estimate_len)
    if estimate_len > 1:
        avail = True
    else:
        avail = False
    right_position = []
    right_position_reverse = []

    if avail:
        for i in range(0, len(right_hall_nodes)):
            ###########################################
            # print("len(right_hall_nodes)")
            # print(len(right_hall_nodes))
            ###########################################
            if len(right_hall_nodes[i]) >= estimate_len:
                for j in range(0, len(right_hall_nodes[i]) - len(
                        right_ratio) + 1):  # right_ratio1 왜 빼지? -> 인덱스 맞추려고 (window size)
                    if right_hall_nodes[i][j].name == 'door':
                        ###########################################
                        print("right_hall_nodes[i][j].val")
                        print("node: ", right_hall_nodes[i][j].val)
                        ###########################################

                        # wall test_forward
                        real_sum = 0
                        for k in range(0, len(right_ratio)):
                            s = min(right_hall_nodes[i][j + k].length, right_ratio[k]) / max(
                                right_hall_nodes[i][j + k].length, right_ratio[k])
                            print("s: ", s)  # short/long -> 값 1에 가까울수록 유사함
                            real_sum = real_sum + s  # 값이 클 수록 유사함

                        print("[real_sum]: ", real_sum)
                        right_position.append([real_sum, right_hall_nodes[i][j], 'forward'])
                        print("------------------")

        for i in range(0, len(left_hall_nodes_reverse)):
            ###########################################
            # print("len(left_hall_nodes_reverse)")
            # print(len(left_hall_nodes_reverse))
            ###########################################
            if len(left_hall_nodes_reverse[i]) >= estimate_len:
                for j in range(0, len(left_hall_nodes_reverse[i]) - len(right_ratio) + 1):
                    if left_hall_nodes_reverse[i][j].name == 'door':
                        ###########################################
                        print("left_hall_nodes_reverse[i][j].val")
                        print("node: ", left_hall_nodes_reverse[i][j].val)
                        ###########################################

                        # wall test_backward
                        real_sum = 0
                        for k in range(0, len(right_ratio)):
                            s = min(left_hall_nodes_reverse[i][j + k].length, right_ratio[k]) / max(
                                left_hall_nodes_reverse[i][j + k].length, right_ratio[k])
                            print("s: ", s)  # short/long -> 값 1에 가까울수록 유사함
                            real_sum = real_sum + s  # 값이 클 수록 유사함

                        print("[real_sum]: ", real_sum)
                        right_position_reverse.append([real_sum, left_hall_nodes_reverse[i][j], 'backward'])
                        print("------------------")

    # left_side
    estimate_len_left = len(left_ratio)
    print("estimate_len_left:", estimate_len_left)
    if estimate_len_left > 1:
        avail = True
    else:
        avail = False
    left_position = []
    left_position_reverse = []

    if avail:
        for i in range(0, len(left_hall_nodes)):
            ###########################################
            # print("len(left_hall_nodes)")
            # print(len(left_hall_nodes))
            ###########################################
            if len(left_hall_nodes[i]) >= estimate_len_left:
                for j in range(0, len(left_hall_nodes[i]) - len(left_ratio) + 1):
                    if left_hall_nodes[i][j].name == 'door':
                        ###########################################
                        print("left_hall_nodes[i][j].val")
                        print("node: ", left_hall_nodes[i][j].val)
                        ###########################################

                        # wall test_forward
                        real_sum = 0
                        for k in range(0, len(left_ratio)):
                            s = min(left_hall_nodes[i][j + k].length, left_ratio[k]) / max(
                                left_hall_nodes[i][j + k].length, left_ratio[k])
                            print("s: ", s)  # short/long -> 값 1에 가까울수록 유사함
                            real_sum = real_sum + s  # 값이 클 수록 유사함

                        print("[real_sum]: ", real_sum)
                        left_position.append([real_sum, left_hall_nodes[i][j], 'forward'])
                        print("------------------")

        for i in range(0, len(right_hall_nodes_reverse)):
            ###########################################
            # print("len(right_hall_nodes_reverse)")
            # print(len(right_hall_nodes_reverse))
            ###########################################
            if len(right_hall_nodes_reverse[i]) >= estimate_len_left:
                for j in range(0, len(right_hall_nodes_reverse[i]) - len(left_ratio) + 1):
                    if right_hall_nodes_reverse[i][j].name == 'door':
                        ###########################################
                        print("right_hall_nodes_reverse[i][j].val")
                        print("node: ", right_hall_nodes_reverse[i][j].val)
                        ###########################################

                        # wall test_backward
                        real_sum = 0
                        for k in range(0, len(left_ratio)):
                            s = min(right_hall_nodes_reverse[i][j + k].length, left_ratio[k]) / max(
                                right_hall_nodes_reverse[i][j + k].length, left_ratio[k])
                            print("s: ", s)  # short/long -> 값 1에 가까울수록 유사함
                            real_sum = real_sum + s  # 값이 클 수록 유사함

                        print("[real_sum]: ", real_sum)
                        left_position_reverse.append([real_sum, right_hall_nodes_reverse[i][j], 'backward'])
                        print("------------------")

    return estimate_len, estimate_len_left, right_position, left_position, right_position_reverse, left_position_reverse


def get_candidates(estimate_len, estimate_len_left, right_position, left_position, right_position_reverse,
                   left_position_reverse):
    right_position_found = []
    left_position_found = []

    i, j, k, l = 0, 0, 0, 0  # 가장 높은 score의 결과가 잘못된 경우(왼쪽, 오른쪽 결과 좌표가 서로 먼 경우)를 위해 가장 높은 score 결과를 낮추면서 비교 => ??
    while True:
        flag = i + j + k + l
        print("[roop no." + str(flag) + "]")
        # -----right_candiates-----
        print("[right graph]")
        # if right_position[0] is not None:
        if len(right_position) != 0:
            right_position_found1 = sorted(right_position, key=operator.itemgetter(0), reverse=True)
            right_position_found2 = sorted(right_position_reverse, key=operator.itemgetter(0), reverse=True)
            if i < len(right_position_found1) and j < len(right_position_found2):
                print("forward_candidate[i = " + str(i) + "]: (node)", right_position_found1[i][1].val, "(real sum)",
                      right_position_found1[i][0], "(average)", right_position_found1[i][0] / estimate_len)
                #         print("forward_candidate[i+1]: ", right_position_found1[i+1][1].val, right_position_found1[i+1][0], right_position_found1[i+1][0]/estimate_len)
                print("backward_candidate[j = " + str(j) + "]: (node)", right_position_found2[j][1].val, "(real sum)",
                      right_position_found2[j][0], "(average)", right_position_found2[j][0] / estimate_len)
                #         print("backward_candidate[j+1]: ", right_position_found2[j+1][1].val, right_position_found2[j+1][0], right_position_found2[j+1][0]/estimate_len)

                # -----right_ori_selection-----
                if right_position_found1[i][0] / estimate_len > right_position_found2[j][0] / estimate_len:
                    right_position_found, ori_right = right_position_found1[i][1], right_position_found1[i][2]
                    relative_score_right = right_position_found1[i][0] / estimate_len
                # elif right_position_found1[i][0] / estimate_len < right_position_found2[j][0] / estimate_len:
                else:
                    right_position_found, ori_right = right_position_found2[j][1], right_position_found2[j][2]
                    relative_score_right = right_position_found2[j][0] / estimate_len
        else:
            ori_right = None
            relative_score_right = 0

        # if left_position[0] is not None:
        if len(left_position) != 0:
            # -----left_candiates-----
            print("\n[left graph]")
            left_position_found1 = sorted(left_position, key=operator.itemgetter(0), reverse=True)
            left_position_found2 = sorted(left_position_reverse, key=operator.itemgetter(0), reverse=True)
            if k < len(left_position_found1) and l < len(left_position_found2):
                print("forward_candidate[k = " + str(k) + "]: (node)", str(left_position_found1[k][1].val),
                      "(real sum)", left_position_found1[k][0], "(average)",
                      left_position_found1[k][0] / estimate_len_left)
                #         print("forward_candidate[k+1]: ", left_position_found1[k+1][1].val, left_position_found1[k+1][0], left_position_found1[k+1][0]/estimate_len_left)
                print("backward_candidate[l = " + str(l) + "] (node):", left_position_found2[l][1].val, "(real sum)",
                      left_position_found2[l][0], "(average)",
                      left_position_found2[l][0] / estimate_len_left)
                #         print("backward_candidate[l+1]: ", left_position_found2[l+1][1].val, left_position_found2[l+1][0], left_position_found2[l+1][0]/estimate_len_left)

                # -----left_ori_selection-----
                if left_position_found1[k][0] / estimate_len_left > left_position_found2[l][0] / estimate_len_left:
                    left_position_found, ori_left = left_position_found1[k][1], left_position_found1[k][2]
                    relative_score_left = left_position_found1[k][0] / estimate_len_left
                # elif left_position_found1[k][0] / estimate_len_left < left_position_found2[l][0] / estimate_len_left: # ? 왜 같을땐 어떻게 처리??
                else:
                    left_position_found, ori_left = left_position_found2[l][1], left_position_found2[l][2]
                    relative_score_left = left_position_found2[l][0] / estimate_len_left
        else:
            ori_left = None
            relative_score_left = 0

        # -----selection-----
        if relative_score_right < relative_score_left:
            # if right_position[0] is not None:
            if len(right_position) != 0:
                if ori_right == 'forward':
                    i = i + 1
                    left_position_found, ori_left = left_position_found1[k][1], left_position_found1[k][2]
                    relative_score_left = left_position_found1[k][0] / estimate_len_left
                elif ori_right == 'backward':
                    # else:
                    j = j + 1
                    left_position_found, ori_left = left_position_found2[l][1], left_position_found2[l][2]
                    relative_score_left = left_position_found2[l][0] / estimate_len_left
            else:
                ori_left = None

        elif relative_score_right > relative_score_left:
            # else:
            # if left_position[0] is not None:
            if len(left_position) != 0:
                if ori_left == 'forward':
                    k = k + 1
                    right_position_found, ori_right = right_position_found1[i][1], right_position_found1[i][2]
                    relative_score_right = right_position_found1[i][0] / estimate_len
                elif ori_left == 'backward':
                    # else:
                    l = l + 1
                    right_position_found, ori_right = right_position_found2[j][1], right_position_found2[j][2]
                    relative_score_right = right_position_found2[j][0] / estimate_len
            else:
                ori_right = None

        # if right_position[0] is not None and left_position[0] is not None:
        if len(right_position) != 0 and len(left_position) != 0:
            print("max(relative_score_right, relative_score_left):", max(relative_score_right, relative_score_left))
            x_diff = right_position_found.pixel[0] - left_position_found.pixel[0]
            y_diff = right_position_found.pixel[1] - left_position_found.pixel[1]
            dist = math.sqrt((x_diff * x_diff) + (y_diff * y_diff))
            print("distance of two points:", dist)
            print("--------------------------------------------------------------------")
        else:
            dist = 0

        if dist < 5:
            # if right_position[0] is not None and left_position[0] is not None:
            if len(right_position) != 0 and len(left_position) != 0:
                if max(relative_score_right, relative_score_left) > 0.5:
                    break
            else:
                break

    return right_position_found, left_position_found

# def getCoordinates(drawing_img, right_position_found, left_position_found):
#     floor_blp = copy.deepcopy(drawing_img)
#     if right_position[0] is not None:
#         right_found_x = m2p(right_position_found.pixel[0])
#         right_found_y = flip(m2p(right_position_found.pixel[1]))
#         #                     cv2.circle(floor_blp, (right_found_x, right_found_y), 30, (255,0,0), 6)
#         print("\n---right_position---")
#         print(right_position_found.val, right_position_found.pixel,
#               ori_right)  # 여기 문제 있음 -> 벽 먼저 시작하면 오류 -> 벽 노드도 (0, 0 말고) 좌표 지정(해결)
#         print("relative score:", relative_score_right)
#     if left_position[0] is not None:
#         left_found_x = m2p(left_position_found.pixel[0])
#         left_found_y = flip(m2p(left_position_found.pixel[1]))
#         #                     cv2.circle(floor_blp, (left_found_x, left_found_y), 30, (0,0,255), 6)
#         print("\n---left_position---")
#         print(left_position_found.val, left_position_found.pixel,
#               ori_left)  # 여기 문제 있음 -> 벽 먼저 시작하면 오류 -> 벽 노드도 (0, 0 말고) 좌표 지정(해결)
#         print("relative score:", relative_score_left)
