import operator
import cv2
import math
import numpy as np
import copy


def get_coodinates_found(detection_coords):
    det_coords = []

    for i in range(len(detection_coords.index)):
        class_name = detection_coords.iloc[i]['name']

        (xmin, xmax, ymin, ymax) = (
            detection_coords.iloc[i]['xmin'], detection_coords.iloc[i]['xmax'], detection_coords.iloc[i]['ymin'],
            detection_coords.iloc[i]['ymax'])
        det_coords.append([int(xmin), int(xmax), int(ymin), int(ymax), class_name])

    coordinates = sorted(det_coords, key=operator.itemgetter(0))
    return coordinates


def get_vert_door_lines(coords_found, frame):
    image_np = copy.deepcopy(frame)

    for i in range(0, len(coords_found)):
        xmin, xmax, ymin, ymax, class_name = coords_found[i]
        crop_img = image_np[ymin:ymax, xmin:xmax]
        h_crop, w_crop, c_crop = crop_img.shape
        # cv2.imwrite('vert_test/0_crop/'+str(i)+'vert0_crop.jpg',crop_img)

        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 2)

        # print("door"+str(i)+"_height: ", h_crop)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        # cv2.imwrite('vert_test/1_morph/' + str(i) + '.jpg', opening)

        edges = cv2.Canny(opening, 100, 140, apertureSize=3)
        # cv2.imwrite('vert_test/2_canny/' + str(i) + '.jpg', edges)

        edges2 = cv2.dilate(edges, kernel, iterations=1)
        # cv2.imwrite('vert_test/3_dilate/'+str(i)+'.jpg', edges2)

        lines = cv2.HoughLinesP(edges2, rho=1, theta=1 * np.pi / 180,
                                threshold=50,  # 150
                                minLineLength=h_crop / 10,  # 50
                                maxLineGap=0)

        # hough output test
        # if lines is not None:
        #     for line in lines:
        #         for x1, y1, x2, y2 in line:
        #             cv2.line(crop_img, (x1, y1), (x2, y2), (0, 255, 0), 6)
        #     cv2.imwrite('vert_test/4_hough/'+str(i)+'.jpg', crop_img)

        if lines is not None:
            lines_coords_around_90 = []
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(crop_img, (x1, y1), (x2, y2), (0, 255, 0), 6)
                    dx = x2 - x1
                    dy = y2 - y1
                    d_len = math.sqrt((dx * dx) + (dy * dy))
                    if y1 > y2:
                        degree = abs((np.arctan2(y1 - y2, x2 - x1) * 180) / np.pi)
                    elif y1 < y2:
                        degree = 180 - abs((np.arctan2(y2 - y1, x2 - x1) * 180) / np.pi)

                    if 80 < degree < 100:  # 70 < d < 110
                        cv2.line(crop_img, (x1, y1), (x2, y2), (255, 255, 0), 6)
                        # strDegree = str(round(degree, 2))
                        # cv2.putText(crop_img, strDegree, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 4)
                        lines_coords_around_90.append([d_len, x1, x2, y1, y2, degree, (x1 + x2) / 2])

            lines_coords_around_90 = sorted(lines_coords_around_90, key=operator.itemgetter(6))

            j = 0
            k = len(lines_coords_around_90) - 1
            count = 0
            if len(lines_coords_around_90) != 0:
                degree_diff = 2
                line_vert1 = []
                line_vert2 = []

                while True:
                    if abs(lines_coords_around_90[j][5] - lines_coords_around_90[k][5]) < degree_diff and abs(
                            lines_coords_around_90[j][6] - lines_coords_around_90[k][6]) > w_crop * (1 / 2):
                        line_vert1 = lines_coords_around_90[j]
                        line_vert2 = lines_coords_around_90[k]
                        break
                    else:
                        if k - j < 2:
                            if degree_diff < 3:
                                degree_diff = degree_diff + 0.5
                                j = 0
                                k = len(lines_coords_around_90) - 1
                                continue
                            else:
                                break

                        if count % 2 == 0:
                            j = j + 1
                        else:
                            k = k - 1
                    count = count + 1

                if len(line_vert1) != 0 and len(line_vert2) != 0:
                    cv2.line(crop_img, (line_vert1[1], line_vert1[3]), (line_vert1[2], line_vert1[4]), (255, 0, 255), 6)
                    # cv2.putText(crop_img, str(line_vert1[5]), (line_vert1[1],line_vert1[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 4)
                    cv2.line(crop_img, (line_vert2[1], line_vert2[3]), (line_vert2[2], line_vert2[4]), (255, 0, 255), 6)
                    # cv2.putText(crop_img, str(line_vert2[5]), (line_vert2[1],line_vert2[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 4)

                    line_vert1[1] = line_vert1[1] + xmin
                    line_vert1[2] = line_vert1[2] + xmin
                    line_vert1[3] = line_vert1[3] + ymin
                    line_vert1[4] = line_vert1[4] + ymin
                    line_vert2[1] = line_vert2[1] + xmin
                    line_vert2[2] = line_vert2[2] + xmin
                    line_vert2[3] = line_vert2[3] + ymin
                    line_vert2[4] = line_vert2[4] + ymin

                if line_vert1 != line_vert2:
                    coords_found[i].append(line_vert1)
                    coords_found[i].append(line_vert2)
                else:
                    # print("[just one vertical line] door number:", i)
                    coords_found[i].append(
                        [None, coords_found[i][0], coords_found[i][0], coords_found[i][2], coords_found[i][3]])
                    coords_found[i].append(
                        [None, coords_found[i][1], coords_found[i][1], coords_found[i][2], coords_found[i][3]])

        if lines is None or len(lines_coords_around_90) == 0:
            # print("[no vertical lines] door number:", i)
            coords_found[i].append(
                [None, coords_found[i][0], coords_found[i][0], coords_found[i][2], coords_found[i][3]])
            coords_found[i].append(
                [None, coords_found[i][1], coords_found[i][1], coords_found[i][2], coords_found[i][3]])

    return coords_found


def get_vani_lines(frame, im_width):
    image_np = copy.deepcopy(frame)
    # 3840x2160
    # kernel = (2,2)
    # minLineHough = 100
    # 1920x1080
    # kernel = (3,3)
    # minLineHough = 50
    # 1280x720
    # kernel (3,3)
    # minLineHough = 33
    # 960x540
    # kernel (3,3), (2,2)
    # minLineHough = 25
    # => *50/1920

    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray, -100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    erode = cv2.erode(opening, kernel,
                      iterations=3)  # 8 -> 3 (hough_thresh = 100, hough_minLength = 40/1920)_(BETTER) -> 2 (hough_thresh = 100, hough_minLength = 65/1920) => both kernel =(3,3)
    canny = cv2.Canny(erode, 100, 140, apertureSize=3)
    edges = cv2.dilate(canny, kernel, iterations=1)
    lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180,
                            threshold=100,  # 20 -> 100
                            minLineLength=im_width * 40 / 1920,  # good case (denominator->length): 1->100, 3->50, 4->30
                            maxLineGap=1)

    # cv2.imwrite('vani_test/0_morph.jpg',opening)
    # cv2.imwrite('vani_test/1_erode.jpg',erode)
    # cv2.imwrite('vani_test/2_canny.jpg',canny)
    # cv2.imwrite('vani_test/3_dilate.jpg', edges)
    # for line in lines:
    #     for x1, y1, x2, y2 in line:
    #         cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 6)
    # cv2.imwrite('vani_test/4_hough.jpg', frame)

    # cv2.imwrite('results/vani_test/0_original.jpg', image_np)
    # cv2.imwrite('results/vani_test/1_morph.jpg',opening)
    # cv2.imwrite('results/vani_test/2_erode.jpg',erode)
    # cv2.imwrite('results/vani_test/3_canny.jpg',canny)
    # cv2.imwrite('results/vani_test/4_dilate.jpg', edges)
    # for line in lines:
    #     for x1, y1, x2, y2 in line:
    #         cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 6)
    # cv2.imwrite('results/vani_test/4_hough.jpg', frame)

    lines_coords_above_90 = []
    lines_coords_below_90 = []

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                dx = x2 - x1
                dy = y2 - y1
                d_len = math.sqrt((dx * dx) + (dy * dy))
                round_len = round(d_len, 2)
                str_len = str(round_len) + "(len)"
                cv2.line(image_np, (x1, y1), (x2, y2), (0, 255, 0), 6)
                # cv2.putText(image_np, str_len, (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

                # Degrees start from 3 o'clock with counter-clockwise
                if y1 > y2:
                    degree = abs((np.arctan2(y1 - y2, x2 - x1) * 180) / np.pi)
                elif y1 < y2:
                    degree = 180 - abs((np.arctan2(y2 - y1, x2 - x1) * 180) / np.pi)
                else:
                    degree = 180

                if 20 < degree < 70:  # previous test: 10 < < 80
                    cv2.line(image_np, (x1, y1), (x2, y2), (255, 255, 0), 6)
                    # strDegree = str(round(degree, 2)) + "(deg)"
                    # cv2.putText(image_np, strDegree, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 4)
                    lines_coords_below_90.append([d_len, x1, x2, y1, y2, degree])
                elif 110 < degree < 160:  # previous test: 100 < < 170
                    cv2.line(image_np, (x1, y1), (x2, y2), (255, 255, 0), 6)
                    # strDegree = str(round(degree, 2)) + "(deg)"
                    # cv2.putText(image_np, strDegree, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 4)
                    lines_coords_above_90.append([d_len, x1, x2, y1, y2, degree])

    ### integrates vanishing line ###
    # 이미지를 4분면을 나눠서 각각의 대표 소실선 지정
    # 2 1
    # 3 4

    h, w, c = image_np.shape
    center_x = w / 2
    center_y = h / 2
    # vani_lines1 = []
    # vani_lines2 = []
    vani_lines3 = []
    vani_lines4 = []

    # print("h and center_y:", h, center_y)
    # offset_y = int(im_width*33/1280)
    offset_y = int(im_width * 50 / 1920)
    # offset_x1 = int(im_width*166/1280)
    offset_x1 = int(im_width * 400 / 1920)
    offset_x2 = w - offset_x1

    for i in range(len(lines_coords_below_90)):
        # if (lines_coords_below_90[i][1] > center_x and lines_coords_below_90[i][2] > center_x
        #     and lines_coords_below_90[i][1] < offset_x2 and lines_coords_below_90[i][2] < offset_x2
        #     and lines_coords_below_90[i][3] < center_y - offset_y and lines_coords_below_90[i][4] < center_y - offset_y):
        #     vani_lines1.append(lines_coords_below_90[i])
        if (lines_coords_below_90[i][1] < center_x and lines_coords_below_90[i][2] < center_x
                and lines_coords_below_90[i][1] > offset_x1 and lines_coords_below_90[i][2] > offset_x1
                and lines_coords_below_90[i][3] > center_y + offset_y and lines_coords_below_90[i][
                    4] > center_y + offset_y):
            vani_lines3.append(lines_coords_below_90[i])
            cv2.line(image_np, (int(lines_coords_below_90[i][1]), int(lines_coords_below_90[i][3])),
                     (int(lines_coords_below_90[i][2]), int(lines_coords_below_90[i][4])), (0, 0, 255), 3)

    for i in range(len(lines_coords_above_90)):
        # if (lines_coords_above_90[i][1] < center_x and lines_coords_above_90[i][2] < center_x
        #     and lines_coords_above_90[i][1] > offset_x1 and lines_coords_above_90[i][2] > offset_x1
        #     and lines_coords_above_90[i][3] < center_y - offset_y and lines_coords_above_90[i][4] < center_y - offset_y):
        #         vani_lines2.append(lines_coords_above_90[i])
        if (lines_coords_above_90[i][1] > center_x and lines_coords_above_90[i][2] > center_x
                and lines_coords_above_90[i][1] < offset_x2 and lines_coords_above_90[i][2] < offset_x2
                and lines_coords_above_90[i][3] > center_y + offset_y and lines_coords_above_90[i][
                    4] > center_y + offset_y):
            vani_lines4.append(lines_coords_above_90[i])
            cv2.line(image_np, (int(lines_coords_above_90[i][1]), int(lines_coords_above_90[i][3])),
                     (int(lines_coords_above_90[i][2]), int(lines_coords_above_90[i][4])), (0, 0, 255), 3)

    # cv2.line(image_np, (offset_x1, 0), (offset_x1, h), (255, 255, 255), 3)
    # cv2.putText(image_np, "offset_x1", (offset_x1, int(h / 9)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)
    # cv2.line(image_np, (offset_x2, 0), (offset_x2, h), (255, 255, 255), 3)
    # cv2.putText(image_np, "offset_x2", (offset_x2, int(h / 9)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)
    # cv2.line(image_np, (0, round(center_y - offset_y)), (w, round(center_y - offset_y)), (255, 255, 255), 3)
    # cv2.putText(image_np, "offsetY1", (0, round(center_y - offset_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)
    # cv2.line(image_np, (0, round(center_y + offset_y)), (w, round(center_y + offset_y)), (255, 255, 255), 3)
    # cv2.putText(image_np, "offsetY2", (0, round(center_y + offset_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)
    # cv2.imwrite('vani_test/5_result.jpg', image_np)

    # return vani_lines1, vani_lines2, vani_lines3, vani_lines4
    return vani_lines3, vani_lines4


# 소실선 평균통합 - 검출되는 여러 소실선들의 각도와 시작점, 끝점의 평균을 구해 통합 소실선 생성
def integrate_vani_lines(vani_lines):
    vanish_line = []
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    degree = 0
    min_deg = 361
    max_deg = -1
    candi_count = 0

    for i in range(len(vani_lines)):
        cur_deg = vani_lines[i][5]
        if cur_deg < min_deg: min_deg = cur_deg
        if cur_deg > max_deg: max_deg = cur_deg
        degree = degree + vani_lines[i][5]
    deg_avg = degree / len(vani_lines)
    tolerance = (max_deg - min_deg) / 2
    # print("min_deg: ", min_deg, " max_deg: ", max_deg, "avg_deg: ", deg_avg, " toler: ", tolerance)
    deg_thresh_min = deg_avg - tolerance
    deg_thresh_max = deg_avg + tolerance

    for i in range(len(vani_lines)):
        if deg_thresh_min < vani_lines[i][5] < deg_thresh_max:
            x1 = x1 + vani_lines[i][1]
            x2 = x2 + vani_lines[i][2]
            y1 = y1 + vani_lines[i][3]
            y2 = y2 + vani_lines[i][4]
            degree = degree + vani_lines[i][5]
            candi_count = candi_count + 1
    if candi_count == 0:
        candi_count = len(vani_lines)
        for i in range(candi_count):
            x1 = x1 + vani_lines[i][1]
            x2 = x2 + vani_lines[i][2]
            y1 = y1 + vani_lines[i][3]
            y2 = y2 + vani_lines[i][4]
            degree = degree + vani_lines[i][5]

    x1 = x1 / candi_count
    x2 = x2 / candi_count
    y1 = y1 / candi_count
    y2 = y2 / candi_count
    degree = degree / candi_count
    dx = x2 - x1
    dy = y2 - y1
    d_len = math.sqrt((dx * dx) + (dy * dy))

    vanish_line = [d_len, x1, x2, y1, y2, degree]

    return vanish_line


def get_vanishings(frame, im_width):
    image_np = copy.deepcopy(frame)

    # vani_lines1, vani_lines2, vani_lines3, vani_lines4 = get_vani_lines(image_np, denominator)
    vani_lines3, vani_lines4 = get_vani_lines(image_np, im_width)
    # print("vani_lines1: ")
    # print(vani_lines1)
    # print("vani_lines2: ")
    # print(vani_lines2)
    # print("vani_lines3: ")
    # print(vani_lines3)
    # print("vani_lines4: ")
    # print(vani_lines4)

    vanish_lines = []

    # if len(vani_lines1) != 0:
    #     vanishLine1 = integrate_vani_lines(vani_lines1)
    #     vanish_lines.append(vanishLine1)
    # if len(vani_lines2) != 0:
    #     vanishLine2 = integrate_vani_lines(vani_lines2)
    #     vanish_lines.append(vanishLine2)
    if len(vani_lines3) != 0:
        vanish_line3 = integrate_vani_lines(vani_lines3)
        vanish_lines.append(vanish_line3)
    if len(vani_lines4) != 0:
        vanish_line4 = integrate_vani_lines(vani_lines4)
        vanish_lines.append(vanish_line4)

    return vanish_lines


def get_crosspt(x11, y11, x12, y12, x21, y21, x22, y22):
    if x12 == x11 or x22 == x21:
        # print('delta x = 0')
        if x12 == x11:
            cx = x12
            m2 = (y22 - y21) / (x22 - x21)
            cy = m2 * (cx - x21) + y21
            return cx, cy
        if x22 == x21:
            cx = x22
            m1 = (y12 - y11) / (x12 - x11)
            cy = m1 * (cx - x11) + y11
            return cx, cy

    m1 = (y12 - y11) / (x12 - x11)
    m2 = (y22 - y21) / (x22 - x21)
    if m1 == m2:
        # print('parallel')
        return None
    cx = (x11 * m1 - y11 - x21 * m2 + y21) / (m1 - m2)
    cy = m1 * (cx - x11) + y11

    return cx, cy


def get_euclidean_d(f1, f2):
    x1 = f1[0]
    y1 = f1[1]
    x2 = f2[0]
    y2 = f2[1]
    dx = x2 - x1
    dy = y2 - y1
    d_len = math.sqrt((dx * dx) + (dy * dy))

    if d_len == 0:
        return 1
    return d_len


def get_2d_factors(vanish_lines, left_coords, right_coords):
    right_factor_2d = []
    left_factor_2d = []

    # vanishLine1 = []
    # vanishLine2 = []
    vanish_line3 = []
    vanish_line4 = []

    if len(vanish_lines) > 1:
        vanish_line3 = vanish_lines[0]
        vanish_line4 = vanish_lines[1]

    # if len(vani_lines1) != 0 and len(vani_lines2) != 0:
    #     for i in range(0, len(right_coords)):
    #         x1, y1 = get_crosspt(vanishLine1[1], vanishLine1[3], vanishLine1[2], vanishLine1[4], right_coords[i][5][1],
    #                              right_coords[i][5][3], right_coords[i][5][2], right_coords[i][5][4])
    #         x2, y2 = get_crosspt(vanishLine1[1], vanishLine1[3], vanishLine1[2], vanishLine1[4], right_coords[i][6][1],
    #                              right_coords[i][6][3], right_coords[i][6][2], right_coords[i][6][4])
    #         right_factor_2d.append([x1, y1])
    #         right_factor_2d.append([x2, y2])
    #     for i in range(0, len(left_coords)):
    #         x1, y1 = get_crosspt(vanishLine2[1], vanishLine2[3], vanishLine2[2], vanishLine2[4], left_coords[i][5][1],
    #                              left_coords[i][5][3], left_coords[i][5][2], left_coords[i][5][4])
    #         x2, y2 = get_crosspt(vanishLine2[1], vanishLine2[3], vanishLine2[2], vanishLine2[4], left_coords[i][6][1],
    #                              left_coords[i][6][3], left_coords[i][6][2], left_coords[i][6][4])
    #         left_factor_2d.append([x1, y1])
    #         left_factor_2d.append([x2, y2])
    # elif len(vani_lines3) != 0 and len(vani_lines4) != 0:
    if len(vanish_line3) != 0 and len(vanish_line4) != 0:
        for i in range(0, len(right_coords)):
            x1, y1 = get_crosspt(vanish_line4[1], vanish_line4[3], vanish_line4[2], vanish_line4[4], right_coords[i][5][1],
                                 right_coords[i][5][3], right_coords[i][5][2], right_coords[i][5][4])
            x2, y2 = get_crosspt(vanish_line4[1], vanish_line4[3], vanish_line4[2], vanish_line4[4], right_coords[i][6][1],
                                 right_coords[i][6][3], right_coords[i][6][2], right_coords[i][6][4])
            right_factor_2d.append([x1, y1])
            right_factor_2d.append([x2, y2])
        for i in range(0, len(left_coords)):
            x1, y1 = get_crosspt(vanish_line3[1], vanish_line3[3], vanish_line3[2], vanish_line3[4], left_coords[i][5][1],
                                 left_coords[i][5][3], left_coords[i][5][2], left_coords[i][5][4])
            x2, y2 = get_crosspt(vanish_line3[1], vanish_line3[3], vanish_line3[2], vanish_line3[4], left_coords[i][6][1],
                                 left_coords[i][6][3], left_coords[i][6][2], left_coords[i][6][4])
            left_factor_2d.append([x1, y1])
            left_factor_2d.append([x2, y2])

    # if len(left_factor_2d) != 0 or len(right_factor_2d) != 0:
    #     print("left 2d factor: " + str(left_factor_2d))
    #     print("right 2d factor: " + str(right_factor_2d))

    return left_factor_2d, right_factor_2d


def get_2d_ratio(left_coords, right_coords, vanish_lines, vanishing_pt, left_factor_2d, right_factor_2d, frame):
    left_start_ratio = -1
    left_real_ratio = []
    right_start_ratio = -1
    right_real_ratio = []

    vanish_line3 = []
    vanish_line4 = []
    if len(vanish_lines) > 1:
        vanish_line3 = vanish_lines[0]
        vanish_line4 = vanish_lines[1]

    image_np = copy.deepcopy(frame)
    im_height, im_width, im_color = image_np.shape

    # if len(vani_lines1) != 0 and len(vani_lines2) != 0:
    #     b_left = vanishLine2[3] - vanishLine2[1] * (vanishLine2[4] - vanishLine2[3]) / (vanishLine2[2] - vanishLine2[1])
    #     b_right = vanishLine1[3] + (im_width - vanishLine1[1]) * (vanishLine1[4] - vanishLine1[3]) / (
    #                 vanishLine1[2] - vanishLine1[1])
    # el
    if len(vanish_line3) != 0 and len(vanish_line4) != 0:
        b_left = vanish_line3[3] - vanish_line3[1] * (vanish_line3[4] - vanish_line3[3]) / (vanish_line3[2] - vanish_line3[1])
        b_right = vanish_line4[3] + (im_width - vanish_line4[1]) * (vanish_line4[4] - vanish_line4[3]) / (
                    vanish_line4[2] - vanish_line4[1])
    # else:
    #     floor_blp = copy.deepcopy(drawing)
    #     image_np = cv2.resize(image_np, (frameWidth, frameHeight))
    #     window = attach_images(image_np, floor_blp)
    #     cv2.imshow('object detection', window)
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         cap.release()
    #         cv2.destroyAllWindows()
    #         cv2.waitKey(1)
    #         break
    #     continue

    # cv2.line(image_np, (0, int(b_left)), (0, int(b_left) + 1), (255, 0, 255), 20)
    # cv2.line(image_np, (im_width, int(b_right)), (im_width, int(b_right) + 1), (255, 0, 255), 20)

    if len(left_factor_2d) != 0:
        left_start_ratio = ((get_euclidean_d((0, int(b_left)), left_factor_2d[1]) * get_euclidean_d(left_factor_2d[0],
                                                                                                    vanishing_pt))
                            / (get_euclidean_d(left_factor_2d[0], left_factor_2d[1]) * get_euclidean_d((0, int(b_left)),
                                                                                                       vanishing_pt))) - 1

    if len(left_coords) != 0:
        if left_coords[0][4] == 'door2':
            left_real_ratio = [1.93]
        else:
            left_real_ratio = [1]

    for i in range(0, int(len(left_factor_2d)) - 2):
        # print("term2-1: ", get_euclidean_d(left_factor_2d[i + 1], left_factor_2d[i + 2]))
        # next_ratio = 1 / (((get_euclidean_d(left_factor_2d[i], left_factor_2d[i + 2]) * get_euclidean_d(left_factor_2d[i + 1],
        #                                                                                       vanishing_pt))
        #                    / (get_euclidean_d(left_factor_2d[i + 1], left_factor_2d[i + 2]) * get_euclidean_d(left_factor_2d[i],
        #                                                                                             vanishing_pt))) - 1) * \
        #              left_real_ratio[i]

        term1 = get_euclidean_d(left_factor_2d[i], left_factor_2d[i + 2]) * get_euclidean_d(left_factor_2d[i + 1], vanishing_pt)
        term2 = get_euclidean_d(left_factor_2d[i + 1], left_factor_2d[i + 2]) * get_euclidean_d(left_factor_2d[i], vanishing_pt)
        next_ratio = 1 / ((term1 / term2 * 0.99) - 1) * left_real_ratio[i]
        left_real_ratio.append(abs(next_ratio))

    right_factor_2d.reverse()

    if len(right_factor_2d) != 0:
        right_start_ratio = ((get_euclidean_d((im_width, int(b_right)), right_factor_2d[1]) * get_euclidean_d(right_factor_2d[0],
                                                                                                              vanishing_pt))
                             / (get_euclidean_d(right_factor_2d[0], right_factor_2d[1]) * get_euclidean_d(
                    (im_width, int(b_right)), vanishing_pt))) - 1

    if len(right_coords) != 0:
        if right_coords[len(right_coords) - 1][4] == 'door2':
            right_real_ratio = [1.93]
        else:
            right_real_ratio = [1]

    for i in range(0, int(len(right_factor_2d)) - 2):
        next_ratio = 1 / (((get_euclidean_d(right_factor_2d[i], right_factor_2d[i + 2]) * get_euclidean_d(right_factor_2d[i + 1],
                                                                                                          vanishing_pt))
                           / (get_euclidean_d(right_factor_2d[i + 1], right_factor_2d[i + 2]) * get_euclidean_d(
                    right_factor_2d[i], vanishing_pt))) - 1) * right_real_ratio[i]
        right_real_ratio.append(abs(next_ratio))

    # print("left start ratio: " + str(left_start_ratio))
    # print("right start ratio: " + str(right_start_ratio))
    # print("left ratio: " + str(left_real_ratio))
    # print("right ratio: " + str(right_real_ratio) + '\n')

    left_ratio = left_real_ratio
    right_ratio = right_real_ratio

    return left_ratio, right_ratio
