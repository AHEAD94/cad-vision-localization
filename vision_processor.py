import image_loader
import geometrics
import positioning
import positioning_test

import copy
import operator
import timeit
import cv2


def image_test(model, image_dir, hall_nodes, hall_nodes_reverse, end_nodes, img_num):
    image_file = image_dir + "/" + str(img_num) + ".jpg"
    image = image_loader.load_an_image(image_file)

    im_height, im_width, im_color = image.shape  # 4032 x 3024

    print("-image " + str(img_num) + ":")
    re_frame = cv2.resize(image, (int(im_width / 4), int(im_height / 4)))
    re_height, re_width, re_color = re_frame.shape
    # print("image resized: " + str(re_width) + " x " + str(re_height))  # 806 x 604

    # # [inference]
    # results = model(re_frame)
    #
    # # [vertical door outline]
    # coords_found = get_coords(results)
    # coords_found = geometrics.get_vert_door_lines(coords_found, re_frame)
    #
    # # [vanishing floor line]
    # vanish_lines = geometrics.get_vanishings(re_frame, re_width)
    # vanishing_pt, left_coords, right_coords = distinguish_doors(coords_found, vanish_lines)
    #
    # # [2D factor coordinates]
    # left_factor_2d, right_factor_2d = geometrics.get_2d_factors(vanish_lines, left_coords, right_coords)
    #
    # # [visualized image saving]
    # result_image = visualizing_test(coords_found, vanish_lines, vanishing_pt, left_factor_2d, right_factor_2d,
    #                               re_frame, re_width)
    # cv2.imwrite('img_results/'+str(img_num)+'.jpg', result_image)
    #
    # # [2D factor ratio]
    # left_ratio, right_ratio = geometrics.get_2d_ratio(left_coords, right_coords, vanish_lines, vanishing_pt,
    #                                                 left_factor_2d, right_factor_2d, image)

    # [temporary values] - torch not work on MPS (M1 MAC processor)
    # left_ratio = [1.93, 10.07582856316721, 3.6132788165522642]
    # right_ratio = [1, 1.8273389866507055, 0.9825519851281554, 1.8482234762617111, 1.7790402110667929]

    # [best cases] - excel reading
    left_ratio = []
    right_ratio = []
    import pandas as pd
    xlsx = pd.read_excel('IPS_cases/_best/hallway0_back.xlsx')  # ['-image 148:', 32, 45, 89.12, (4, 23, 91.833)] O
    # xlsx = pd.read_excel('IPS_cases/_best/hallway0_for.xlsx') # ['-image 409:', (13, 2, 86.889), 55, 36, 79.404] O - sliding_0108 -> ['-image 409:', (13, 2, 86.889), 53, 34, 87.899] -> 한쪽 벽면 오류, 방향 결과 오류 -> temp ['-image 452:', 15, 2, 91.201, 51, 34, 89.751] O -> 한쪽만
    # xlsx = pd.read_excel('IPS_cases/_best/hallway1_back(1).xlsx') # ['-image 264:', 9, 2, 96.632, 55, 36, 85.164] X - sliding_0108 -> ['-image 264:', 9, 2, 96.632, (53, 34, 93.491)] -> 한쪽 벽면 오류
    # xlsx = pd.read_excel('IPS_cases/_best/hallway1_back(2).xlsx') # ['-image 576:', 19, 4, 92.424, 55, 36, 82.325] X - sliding_0108 -> ['-image 600:', 9, 2, 90.859, 49, 32, 97.073] - awake -> ['-image 600:', 9, 2, 90.859, (47, 32, 97.073)] O
    # xlsx = pd.read_excel('IPS_cases/_best/hallway1_back(3).xlsx') # ['-image 858:', 9, 2, 87.594, 55, 36, 75.037] X - sliding_0108 -> ['-image 801:', 17, 4, 78.661, 45, 30, 88.179] - check_size -> ['-image 926:', 9, 2, 75.012, (43, 30, 93.263)] O
    # xlsx = pd.read_excel('IPS_cases/_best/hallway1_for(1).xlsx') # ['-image 69:', (28, 39, 92.245), 6, 25, 78.193] O
    # xlsx = pd.read_excel('IPS_cases/_best/hallway1_for(2).xlsx') # ['-image 198:', (30, 41, 97.492), 4, 23, 90.764] O
    # xlsx = pd.read_excel('IPS_cases/_best/hallway1_for(3).xlsx') # ['-image 585:', 32, 45, 95.372, 4, 21, 93.992] O -> 한쪽 벽면 오류
    indexing_column = xlsx.columns[0]
    image_now = None
    highest_value = 0
    highest_result = []
    for index, row in xlsx.iterrows():
        if "image" in str(row[indexing_column]):
            image_now = str(row[indexing_column])
            print(image_now)
        if image_now == "-image 148:":
            # if True:
            if "left ratio" in str(row[indexing_column]):
                left_ratio_str = row[indexing_column][14:-1]
                strings = left_ratio_str.split(',')
                left_ratio = []
                for i in range(len(strings)):
                    left_ratio.append(float(strings[i]))
                print("left_ratio =", left_ratio)
            if "right ratio" in str(row[indexing_column]):
                right_ratio_str = row[indexing_column][15:-1]
                strings = right_ratio_str.split(',')
                right_ratio = []
                for i in range(len(strings)):
                    right_ratio.append(float(strings[i]))
                print("right_ratio =", right_ratio)
                estimate_len_left, estimate_len_right, forward_position, backward_position = positioning_test.check_similarity(
                    hall_nodes, hall_nodes_reverse, left_ratio, right_ratio)
                forward_position_found, backward_position_found = positioning_test.get_candidates(estimate_len_left,
                                                                                                  estimate_len_right,
                                                                                                  forward_position,
                                                                                                  backward_position)
                print("\n\n" + image_now)
                print("\n========! FORWARD POSITION !========")
                print("- left_side_node:", forward_position_found[0].left_position[0][1].val)
                print("    - relative: ", forward_position_found[2])
                print("- right_side_node:", forward_position_found[0].right_position[0][1].val)
                print("    - relative: ", forward_position_found[3])
                print("==> Sim_score: ", forward_position_found[1])
                relative_forward = round((forward_position_found[2] + forward_position_found[3]) / 2 * 100, 3)
                print("--> relative_similariy: ", relative_forward, "%")
                print("\n========! BACKWARD POSITION !========")
                print("- left_side_node:", backward_position_found[0].left_position[0][1].val)
                print("    - relative: ", backward_position_found[2])
                print("- right_side_node:", backward_position_found[0].right_position[0][1].val)
                print("    - relative: ", backward_position_found[3])
                print("==> Sim_score: ", backward_position_found[1])
                relative_backward = round((backward_position_found[2] + backward_position_found[3]) / 2 * 100, 3)
                print("--> relative_similariy: ", relative_backward, "%")
                print("====================================\n")
                relative_high = max(relative_forward, relative_backward)
                if relative_high >= highest_value:
                    highest_value = relative_high
                    highest_result = [image_now, forward_position_found[0].left_position[0][1].val,
                                      forward_position_found[0].right_position[0][1].val, relative_forward,
                                      backward_position_found[0].left_position[0][1].val,
                                      backward_position_found[0].right_position[0][1].val, relative_backward]
    print(highest_result)
    print("")

    # print("left ratio: " + str(left_ratio))
    # print("right ratio: " + str(right_ratio))

    # estimate_len_right, estimate_len_left, forward_position, backward_position = positioningTest.check_similarity(
    #     hall_nodes, hall_nodes_reverse, left_ratio, right_ratio)
    #
    # forward_position_found, backward_position_found = positioningTest.get_candidates(estimate_len_right, estimate_len_left,
    #                                                                                 forward_position, backward_position)

    # print("\n\n========! FORWARD POSITION !=======")
    # print("- left_side_node:", forward_position_found[0].left_position[0][1].val)
    # print("    - relative: ", forward_position_found[2])
    # print("- right_side_node:", forward_position_found[0].right_position[0][1].val)
    # print("    - relative: ", forward_position_found[3])
    # print("==> Sim_score: ", forward_position_found[1])
    # print("--> relative_similariy: ", round((forward_position_found[2]+forward_position_found[3])/2*100, 3), "%")
    # print("\n========! BACKWARD POSITION !=======")
    # print("- left_side_node:", backward_position_found[0].left_position[0][1].val)
    # print("    - relative: ", backward_position_found[2])
    # print("- right_side_node:", backward_position_found[0].right_position[0][1].val)
    # print("    - relative: ", backward_position_found[3])
    # print("==> Sim_score: ", backward_position_found[1])
    # print("--> relative_similariy: ", round((backward_position_found[2]+backward_position_found[3])/2*100, 3), "%")


def video_test(model, capture, hall_nodes, hall_nodes_reverse, end_nodes):
    if capture.isOpened():
        fps = capture.get(cv2.CAP_PROP_FPS)
        f_count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        f_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        f_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        print('Frames per second: ', fps, 'fps')
        print('Frames count: ', f_count)
        print('Frames width: ', f_width)
        print('Frames height: ', f_height)

    while capture.isOpened():
        ret, frame = capture.read()
        if ret:
            start_t = timeit.default_timer()
            # re_frame = cv2.resize(frame, (1280,720))
            re_frame = cv2.resize(frame, (960, 540))
            im_height, im_width, im_color = re_frame.shape

            # Inference
            results = model(re_frame)

            # 1. 문 좌표 정리
            coords_found = get_coords(results)
            # print("DOOR DETECTION RESULT: [xmin, xmax ,ymin ,ymax, class_name]")
            # print(coords_found)

            # 2. 문 수직선 확보
            coords_found = geometrics.get_vert_door_lines(coords_found, re_frame)
            # print("VERTICAL DOOR LINES: [xmin, xmax ,ymin ,ymax, class_name, "
            #       "vert_line1:[d_len,x1,x2,y1,y2,degree,(x1+x2)/2], "
            #       "vert_line2:[d_len,x1,x2,y1,y2,degree,(x1+x2)/2]]")
            # print(coords_found)

            # 3. 소실선 확보
            vanish_lines = geometrics.get_vanishings(re_frame, im_width)
            # print("VANISHING LINES: [[d_len, x1, x2, y1, y2, degree], [d_len, x1, x2, y1, y2, degree]]")
            # print(vanish_lines)

            # 4. 소실점 계산 및 좌/우 문 구분
            vanishing_pt, left_coords, right_coords = distinguish_doors(coords_found, vanish_lines)

            # 5. 2D factor 계산
            left_factor_2d, right_factor_2d = geometrics.get_2d_factors(vanish_lines, left_coords, right_coords)

            # [VISUALIZING TEST]
            result_frame = visualizing_test(coords_found, vanish_lines, vanishing_pt, left_factor_2d, right_factor_2d,
                                            re_frame, im_width)

            # 6. Ratio 계산
            left_ratio, right_ratio = geometrics.get_2d_ratio(left_coords, right_coords, vanish_lines, vanishing_pt,
                                                              left_factor_2d, right_factor_2d, re_frame)
            print("left ratio: " + str(left_ratio))
            print("right ratio: " + str(right_ratio))

            # 7. similarity check
            estimate_len, estimate_len_left, right_position, left_position, right_position_reverse, left_position_reverse = positioning.check_similar(
                hall_nodes, hall_nodes_reverse, left_ratio, right_ratio)

            # 8. get candidates
            # right_position_found, left_position_found = positioning.get_candidates(estimate_len, estimate_len_left, right_position, left_position, right_position_reverse, left_position_reverse)

            # 9.

            teminate_t = timeit.default_timer()
            fps = int(1. / (teminate_t - start_t))
            cv2.imshow('result', result_frame)
            key = cv2.waitKey(10)
            print("- fps: ", fps)
            print("=====")

            if key == ord('q'):
                break
        else:
            break

    capture.release()
    cv2.destroyAllWindows()


def get_coords(model_results):
    coords_found = geometrics.get_coodinates_found(model_results.pandas().xyxy[0])

    for i in range(0, len(coords_found)):
        coords_found[i].append(coords_found[i][1] - coords_found[i][0])  # x좌표 차
    coords_found = sorted(coords_found, key=operator.itemgetter(5))  # 박스 가로길이 순

    for i in range(0, len(coords_found)):
        del coords_found[i][5]

    return coords_found


def distinguish_doors(coords_found, vanish_lines):
    # vanish_line1 = []
    # vanish_line2 = []
    vanish_line3 = []
    vanish_line4 = []
    # Vanishing line 1 and 2 are not used. (We just use floor lines not ceiling lines)
    # If you need to use ceiling lines, activate and modify all the codes related to them.

    if len(vanish_lines) > 1:
        vanish_line3 = vanish_lines[0]
        vanish_line4 = vanish_lines[1]

    # if len(vani_lines1) != 0 and len(vani_lines2) != 0:
    #     vanishing_pt = get_crosspt(vanish_line1[1], vanish_line1[3], vanish_line1[2], vanish_line1[4], vanish_line2[1],
    #                                vanish_line2[3], vanish_line2[2], vanish_line2[4])
    #     print("Vanishing Point: " + str(vanishing_pt) + '\n')
    #     cv2.line(image_np, (int(vanishing_pt[0]), int(vanishing_pt[1])), (int(vanishing_pt[0]), int(vanishing_pt[1])),
    #              (0, 0, 0), 20)
    # elif len(vani_lines3) != 0 and len(vani_lines4) != 0:
    if len(vanish_line3) != 0 and len(vanish_line4) != 0:
        vanishing_pt = geometrics.get_crosspt(vanish_line3[1], vanish_line3[3], vanish_line3[2], vanish_line3[4],
                                              vanish_line4[1],
                                              vanish_line4[3], vanish_line4[2], vanish_line4[4])
        # print("Vanishing Point: " + str(vanishing_pt) + '\n')
    else:
        # print("No vanishing point detected.")
        vanishing_pt = (0, 0)

    left_coords = []
    right_coords = []

    if vanishing_pt != (0, 0):
        for coords in coords_found:
            if coords[0] > vanishing_pt[0]:
                right_coords.append(coords)
            if coords[0] < vanishing_pt[0]:
                left_coords.append(coords)

        left_coords = sorted(left_coords, key=operator.itemgetter(0))
        right_coords = sorted(right_coords, key=operator.itemgetter(0))

        # print("left coords: "+str(left_coords))
        # print("right coords: "+str(right_coords)+'\n')

    return vanishing_pt, left_coords, right_coords


def visualizing_test(coords_found, vanish_lines, vanishing_pt, left_factor_2d, right_factor_2d, frame, im_width):
    image_np = copy.deepcopy(frame)

    for coord in coords_found:
        # vertical door lines
        vert1_coord1 = (int(coord[5][1]), int(coord[5][3]))
        vert1_coord2 = (int(coord[5][2]), int(coord[5][4]))
        vert2_coord1 = (int(coord[6][1]), int(coord[6][3]))
        vert2_coord2 = (int(coord[6][2]), int(coord[6][4]))
        cv2.line(image_np, (vert1_coord1[0], vert1_coord1[1]), (vert1_coord2[0], vert1_coord2[1]), (255, 0, 255),
                 int(im_width * 4 / 1920))
        cv2.line(image_np, (vert2_coord1[0], vert2_coord1[1]), (vert2_coord2[0], vert2_coord2[1]), (255, 0, 255),
                 int(im_width * 4 / 1920))

        # door rectangles-
        if coord[4] == 'door1':
            cv2.rectangle(image_np, (coord[0], coord[2]), (coord[1], coord[3]), (0, 255, 0), int(im_width * 2 / 1920))
        else:
            cv2.rectangle(image_np, (coord[0], coord[2]), (coord[1], coord[3]), (0, 230, 255), int(im_width * 2 / 1920))

    # vanishing lines
    for i in range(len(vanish_lines)):
        if vanishing_pt != (0, 0):
            if vanish_lines[i][1] < vanishing_pt[0]:
                starting_pt = (int(vanish_lines[i][1]), int(vanish_lines[i][3]))
                end_pt = (int(vanishing_pt[0]), int(vanishing_pt[1]))
            else:
                starting_pt = (int(vanishing_pt[0]), int(vanishing_pt[1]))
                end_pt = (int(vanish_lines[i][2]), int(vanish_lines[i][4]))
        else:
            starting_pt = (int(vanish_lines[i][1]), int(vanish_lines[i][3]))
            end_pt = (int(vanish_lines[i][2]), int(vanish_lines[i][4]))
        cv2.line(image_np, starting_pt, end_pt, (0, 0, 255), int(im_width * 4 / 1920))
        cv2.putText(image_np, str(round(vanish_lines[i][5], 2)) + "(deg)",
                    (int(vanish_lines[i][1]), int(vanish_lines[i][3])), cv2.FONT_HERSHEY_SIMPLEX, im_width * 1 / 1920,
                    (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(image_np, str(round(vanish_lines[i][0], 2)) + "(len)",
                    (int(vanish_lines[i][2]), int(vanish_lines[i][4])), cv2.FONT_HERSHEY_SIMPLEX, im_width * 1 / 1920,
                    (200, 200, 255), 1, cv2.LINE_AA)

    # vanishing points
    cv2.line(image_np, (int(vanishing_pt[0]), int(vanishing_pt[1])), (int(vanishing_pt[0]), int(vanishing_pt[1])),
             (0, 0, 0), int(im_width * 20 / 1920))

    # 2D factors
    for i in range(0, len(left_factor_2d)):
        if i % 2 == 0:
            color = (255, 65, 65)
        else:
            color = (200, 0, 0)
        cv2.putText(image_np, '2Dfactor' + str(i) + '(left)', (int(left_factor_2d[i][0]), int(left_factor_2d[i][1])),
                    cv2.FONT_HERSHEY_SIMPLEX, im_width * 1 / 1920, color, 1, cv2.LINE_AA)
        cv2.line(image_np, (int(left_factor_2d[i][0]), int(left_factor_2d[i][1])),
                 (int(left_factor_2d[i][0]), int(left_factor_2d[i][1])), color, int(im_width * 20 / 1920))
    for i in range(0, len(right_factor_2d)):
        if i % 2 == 0:
            color = (255, 65, 65)
        else:
            color = (200, 0, 0)
        cv2.putText(image_np, '2Dfactor' + str(i) + '(right)', (int(right_factor_2d[i][0]), int(right_factor_2d[i][1])),
                    cv2.FONT_HERSHEY_SIMPLEX, im_width * 1 / 1920, color, 1, cv2.LINE_AA)
        cv2.line(image_np, (int(right_factor_2d[i][0]), int(right_factor_2d[i][1])),
                 (int(right_factor_2d[i][0]), int(right_factor_2d[i][1])), color, int(im_width * 20 / 1920))

    return image_np
