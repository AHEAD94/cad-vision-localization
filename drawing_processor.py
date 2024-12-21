import copy

import drawing_loader

import cv2
import numpy as np


def m2p(meter=None):  # meter to pixel
    mag = 50  # 50 배율(좌표가 미터단위로 나와있어 픽셀단위로 바꿔줄 필요)
    return round(meter * mag)


def flip(limit_y, y):  # OpenCV의 y축을 CAD의 y축에 맞추어 반전
    return limit_y - y


def draw_base(line_list, limit_x, limit_y):
    BRIGHTNESS = 255
    COLOR_CHANNEL = 3
    drawing_img = np.zeros((limit_y, limit_x, COLOR_CHANNEL), np.uint8) + BRIGHTNESS

    for i in range(len(line_list.list_lines)):
        x1 = m2p(line_list.list_lines[i].get_start_x())
        y1 = flip(limit_y, m2p(line_list.list_lines[i].get_start_y()))
        x2 = m2p(line_list.list_lines[i].get_end_x())
        y2 = flip(limit_y, m2p(line_list.list_lines[i].get_end_y()))

        if line_list.list_lines[i].get_layer() == "CEN":
            cv2.line(drawing_img,
                     pt1=(x1, y1),
                     pt2=(x2, y2),
                     color=(255, 255, 255),
                     thickness=1,
                     lineType=cv2.LINE_AA)
        elif line_list.list_lines[i].get_layer() == "W":
            cv2.line(drawing_img,
                     pt1=(x1, y1),
                     pt2=(x2, y2),
                     color=(0, 0, 0),
                     thickness=2,
                     lineType=cv2.LINE_AA)
        elif line_list.list_lines[i].get_layer() == "DR":
            cv2.line(drawing_img,
                     pt1=(x1, y1),
                     pt2=(x2, y2),
                     color=(255, 0, 255),
                     thickness=2,
                     lineType=cv2.LINE_AA)
    return drawing_img


def draw_root(drawing_img, line_list, cross_x, cross_y, limit_y):
    root_x = m2p(cross_x)
    root_y = flip(limit_y, m2p(cross_y))

    cv2.line(drawing_img,
             pt1=(root_x, root_y),
             pt2=(root_x, root_y),
             color=(0, 0, 0),
             thickness=25,
             lineType=cv2.LINE_AA)
    cv2.line(drawing_img,
             pt1=(root_x, root_y),
             pt2=(root_x, root_y),
             color=(255, 255, 255),
             thickness=21,
             lineType=cv2.LINE_AA)
    cv2.putText(drawing_img,
                text="(" + str(cross_x) + ", " + str(cross_y) + ")",
                org=(root_x, root_y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(255, 0, 0),
                thickness=2,
                lineType=cv2.LINE_AA)


def draw_center_line(drawing_img, cross_x, cross_y, constraints, limit_y):
    min_x, min_y, max_x, max_y = constraints[0], constraints[1], constraints[2], constraints[3]

    isle_line_vertical = drawing_loader.Line(cross_x, cross_x, min_y, max_y, max_y - min_y)
    isle_line_horizontal = drawing_loader.Line(min_x, max_x, cross_y, cross_y, max_x - min_x)
    yx1 = m2p(isle_line_vertical.get_start_x())  # 수직인 선의 시작 x좌표
    yy1 = flip(limit_y, m2p(isle_line_vertical.get_start_y()))
    yx2 = m2p(isle_line_vertical.get_end_x())  # 수직인 선의 끝 x좌표
    yy2 = flip(limit_y, m2p(isle_line_vertical.get_end_y()))
    xx1 = m2p(isle_line_horizontal.get_start_x())
    xy1 = flip(limit_y, m2p(isle_line_horizontal.get_start_y()))
    xx2 = m2p(isle_line_horizontal.get_end_x())
    xy2 = flip(limit_y, m2p(isle_line_horizontal.get_end_y()))

    cv2.line(drawing_img,
             pt1=(yx1, yy1),
             pt2=(yx2, yy2),
             color=(160, 160, 255),
             thickness=1,
             lineType=cv2.LINE_AA)
    cv2.line(drawing_img,
             pt1=(xx1, xy1),
             pt2=(xx2, xy2),
             color=(160, 160, 255),
             thickness=1,
             lineType=cv2.LINE_AA)

    # 복도 중심선 끝점
    top_end_x = yx2
    top_end_y = yy2
    bottom_end_x = yx1
    bottom_end_y = yy1
    left_end_x = xx1
    left_end_y = xy1
    right_end_x = xx2
    right_end_y = xy2

    cv2.line(drawing_img,
             pt1=(top_end_x, top_end_y),
             pt2=(top_end_x, top_end_y),
             color=(160, 160, 255),
             thickness=10,
             lineType=cv2.LINE_AA)
    cv2.line(drawing_img,
             pt1=(bottom_end_x, bottom_end_y),
             pt2=(bottom_end_x, bottom_end_y),
             color=(160, 160, 255),
             thickness=10,
             lineType=cv2.LINE_AA)
    cv2.line(drawing_img,
             pt1=(left_end_x, left_end_y),
             pt2=(left_end_x, left_end_y),
             color=(160, 160, 255),
             thickness=10,
             lineType=cv2.LINE_AA)
    cv2.line(drawing_img,
             pt1=(right_end_x, right_end_y),
             pt2=(right_end_x, right_end_y),
             color=(160, 160, 255),
             thickness=10,
             lineType=cv2.LINE_AA)


def draw_wall_lenght_x(drawing_img, limit_y, list_hall):
    for i in range(len(list_hall)):
        if list_hall[i].get_layer() == "W":
            x = m2p((list_hall[i].get_start_x() + list_hall[i].get_end_x()) / 2)
            y = flip(limit_y, m2p(list_hall[i].get_start_y()))
            cv2.putText(drawing_img,
                        text=str(list_hall[i].get_length()),
                        org=(x, y),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(255, 255, 0),
                        thickness=1,
                        lineType=cv2.LINE_AA)


def draw_wall_lenght_y(drawing_img, limit_y, list_hall):
    for i in range(len(list_hall)):
        if list_hall[i].get_layer() == "W":
            x = m2p(list_hall[i].get_start_x())
            y = flip(limit_y, m2p((list_hall[i].get_start_y() + list_hall[i].get_end_y()) / 2))
            cv2.putText(drawing_img,
                        text=str(list_hall[i].get_length()),
                        org=(x, y),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(255, 255, 0),
                        thickness=1,
                        lineType=cv2.LINE_AA)


def redraw(drawing, cross_x, cross_y, constraints):
    line_list = copy.deepcopy(drawing)
    min_x, min_y, max_x, max_y = constraints[0], constraints[1], constraints[2], constraints[3]
    CENTER_ARRANGEMENT = 150
    limit_x = m2p(round(max_x)) + CENTER_ARRANGEMENT
    limit_y = m2p(round(max_y)) + CENTER_ARRANGEMENT

    drawing_img = draw_base(line_list, limit_x, limit_y)
    draw_root(drawing_img, line_list, cross_x, cross_y, limit_y)
    draw_center_line(drawing_img, cross_x, cross_y, constraints, limit_y)

    right_hall_l, right_hall_r, left_hall_l, left_hall_r, upper_hall_l, upper_hall_r, down_hall_l, down_hall_r = get_halls(
        line_list, cross_x, cross_y)

    draw_wall_lenght_x(drawing_img, limit_y, right_hall_l)
    draw_wall_lenght_x(drawing_img, limit_y, right_hall_r)
    draw_wall_lenght_x(drawing_img, limit_y, left_hall_l)
    draw_wall_lenght_x(drawing_img, limit_y, left_hall_r)
    draw_wall_lenght_y(drawing_img, limit_y, upper_hall_l)
    draw_wall_lenght_y(drawing_img, limit_y, upper_hall_r)
    draw_wall_lenght_y(drawing_img, limit_y, down_hall_l)
    draw_wall_lenght_y(drawing_img, limit_y, down_hall_r)

    return drawing_img


def find_root(line_list):
    # 벽 사이 가상의 선 그어 선들 간의 교점 찾기 or [호 중심을 포함하는 중심선 찾기]
    for i in range(len(line_list.list_cen)):
        if line_list.list_cen[i].get_start_x() == line_list.list_cen[i].get_end_x():  # 수직인 중심선
            for j in range(len(line_list.list_arcs)):
                if line_list.list_cen[i].get_start_x() == line_list.list_arcs[j].get_center_x():  # 호 중심 포함
                    line_list.add_isle_vertical(line_list.list_cen[i])
                    break

        elif line_list.list_cen[i].get_start_y() == line_list.list_cen[i].get_end_y():  # 수평인 중심선
            for j in range(len(line_list.list_arcs)):
                if line_list.list_cen[i].get_start_y() == line_list.list_arcs[j].get_center_y():
                    line_list.add_isle_horizontal(line_list.list_cen[i])
                    break
    cross_x = (line_list.list_isle_vertical[0].get_start_x() + line_list.list_isle_vertical[1].get_start_x()) / 2
    cross_y = (line_list.list_isle_horizontal[0].get_start_y() + line_list.list_isle_horizontal[1].get_start_y()) / 2

    return cross_x, cross_y


def get_halls(line_list, cross_x, cross_y):
    right_hall_l = []
    right_hall_r = []
    left_hall_l = []
    left_hall_r = []
    upper_hall_l = []
    upper_hall_r = []
    down_hall_l = []
    down_hall_r = []

    # right hall
    # 복도 중심선과 벽 중심선 사이의 수평선 선택
    for i in range(len(line_list.list_isle_horizontal)):
        if line_list.list_isle_horizontal[i].get_start_y() > cross_y:  # 복도 중심선보다 위에 위치한 벽 중심선 선택
            for j in range(len(line_list.list_lines)):
                if (line_list.list_lines[j].get_start_y() == line_list.list_lines[j].get_end_y()  # 수평인 선
                        and line_list.list_lines[j].get_start_y() > cross_y
                        and line_list.list_lines[j].get_start_y() < line_list.list_isle_horizontal[i].get_start_y()):
                    if (line_list.list_lines[j].get_start_x() < cross_x
                            and line_list.list_lines[j].get_end_x() > cross_x  # root의 x좌표에 걸리는 선
                            and line_list.list_lines[j].get_length() > 0.2):  # 벽, 문 두께 제외
                        # root에 걸리는 선의 길이를 root의 x좌표 기준으로 잘라서 지정해야 함
                        line_cut = drawing_loader.Line(cross_x, line_list.list_lines[j].get_end_x(),
                                                       line_list.list_lines[j].get_start_y(),
                                                       line_list.list_lines[j].get_end_y(),
                                                       round(line_list.list_lines[j].get_start_x() - cross_x, 2),
                                                       line_list.list_lines[j].get_angle(),
                                                       line_list.list_lines[j].get_layer())
                        right_hall_l.append(line_cut)
                    elif (line_list.list_lines[j].get_start_x() > cross_x  # root의 x좌표보다 큰 선
                          and line_list.list_lines[j].get_length() > 0.2):
                        right_hall_l.append(line_list.list_lines[j])

        if line_list.list_isle_horizontal[i].get_start_y() < cross_y:  # 복도 중심선보다 아래에 위치한 벽 중심선 선택
            for j in range(len(line_list.list_lines)):
                if (line_list.list_lines[j].get_start_y() == line_list.list_lines[j].get_end_y()  # 수평인 선
                        and line_list.list_lines[j].get_start_y() < cross_y
                        and line_list.list_lines[j].get_start_y() > line_list.list_isle_horizontal[i].get_start_y()):
                    if (line_list.list_lines[j].get_start_x() < cross_x
                            and line_list.list_lines[j].get_end_x() > cross_x  # root의 x좌표에 걸리는 선
                            and line_list.list_lines[j].get_length() > 0.2):  # 벽, 문 두께 제외
                        # root에 걸리는 선의 길이를 root의 x좌표 기준으로 잘라서 지정해야 함
                        line_cut = drawing_loader.Line(cross_x, line_list.list_lines[j].get_end_x(),
                                                       line_list.list_lines[j].get_start_y(),
                                                       line_list.list_lines[j].get_end_y(),
                                                       round(line_list.list_lines[j].get_end_x() - cross_x, 2),
                                                       line_list.list_lines[j].get_angle(),
                                                       line_list.list_lines[j].get_layer())
                        right_hall_r.append(line_cut)
                    elif (line_list.list_lines[j].get_start_x() > cross_x  # root의 x좌표보다 큰 선
                          and line_list.list_lines[j].get_length() > 0.2):
                        right_hall_r.append(line_list.list_lines[j])

    right_hall_l = sorted(right_hall_l)
    right_hall_r = sorted(right_hall_r)

    # list에 문 추가
    temp = []
    for i in range(len(right_hall_l)):
        temp.append(right_hall_l[i])
        if i < len(right_hall_l) - 1:
            door_line = drawing_loader.Line(right_hall_l[i].get_end_x(), right_hall_l[i + 1].get_start_x(),
                                            right_hall_l[i].get_start_y(), right_hall_l[i].get_end_y(),
                                            round(right_hall_l[i + 1].get_start_x()
                                                  - right_hall_l[i].get_end_x(), 2),
                                            right_hall_l[i].get_angle(),
                                            "DR")
            temp.append(door_line)
    right_hall_l = temp

    temp = []
    for i in range(len(right_hall_r)):
        temp.append(right_hall_r[i])
        if i < len(right_hall_r) - 1:
            door_line = drawing_loader.Line(right_hall_r[i].get_end_x(), right_hall_r[i + 1].get_start_x(),
                                            right_hall_r[i].get_start_y(), right_hall_r[i].get_end_y(),
                                            round(right_hall_r[i + 1].get_start_x()
                                                  - right_hall_r[i].get_end_x(), 2),
                                            right_hall_r[i].get_angle(),
                                            "DR")
            temp.append(door_line)
    right_hall_r = temp

    ###########################################################
    # print("\n[right_hall]")
    # print("-right_hall_l:")
    # for i in range(len(right_hall_l)):
    #     print(format(right_hall_l[i].get_length(), "0.2f")
    #           + " (x: " + str(right_hall_l[i].get_start_x()) + ") "
    #           + right_hall_l[i].get_layer())
    # print("-right_hall_r:")
    # for i in range(len(right_hall_r)):
    #     print(format(right_hall_r[i].get_length(), "0.2f")
    #           + " (x: " + str(right_hall_r[i].get_start_x()) + ") "
    #           + right_hall_r[i].get_layer())
    ###########################################################

    # left hall
    # 복도 중심선과 벽 중심선 사이의 수평선 선택
    for i in range(len(line_list.list_isle_horizontal)):
        if line_list.list_isle_horizontal[i].get_start_y() < cross_y:  # 복도 중심선보다 아래에 위치한 벽 중심선 선택
            for j in range(len(line_list.list_lines)):
                if (line_list.list_lines[j].get_start_y() == line_list.list_lines[j].get_end_y()  # 수평인 선
                        and line_list.list_lines[j].get_start_y() < cross_y
                        and line_list.list_lines[j].get_start_y() > line_list.list_isle_horizontal[i].get_start_y()):

                    if (line_list.list_lines[j].get_start_x() < cross_x
                            and line_list.list_lines[j].get_end_x() > cross_x  # root의 x좌표에 걸리는 선
                            and line_list.list_lines[j].get_length() > 0.2):  # 벽, 문 두께 제외
                        # root에 걸리는 선의 길이를 root의 x좌표 기준으로 잘라서 지정해야 함
                        line_cut = drawing_loader.Line(line_list.list_lines[j].get_start_x(), cross_x,
                                                       line_list.list_lines[j].get_start_y(),
                                                       line_list.list_lines[j].get_end_y(),
                                                       round(cross_x - line_list.list_lines[j].get_start_x(), 2),
                                                       line_list.list_lines[j].get_angle(),
                                                       line_list.list_lines[j].get_layer())
                        left_hall_l.append(line_cut)
                    elif (line_list.list_lines[j].get_end_x() < cross_x  # root의 x좌표보다 작은 선
                          and line_list.list_lines[j].get_length() > 0.2):
                        left_hall_l.append(line_list.list_lines[j])

        if line_list.list_isle_horizontal[i].get_start_y() > cross_y:  # 복도 중심선보다 위에 위치한 벽 중심선 선택
            for j in range(len(line_list.list_lines)):
                if (line_list.list_lines[j].get_start_y() == line_list.list_lines[j].get_end_y()  # 수평인 선
                        and line_list.list_lines[j].get_start_y() > cross_y
                        and line_list.list_lines[j].get_start_y() < line_list.list_isle_horizontal[i].get_start_y()):
                    if (line_list.list_lines[j].get_start_x() < cross_x
                            and line_list.list_lines[j].get_end_x() > cross_x  # root의 x좌표에 걸리는 선
                            and line_list.list_lines[j].get_length() > 0.2):  # 벽, 문 두께 제외
                        # root에 걸리는 선의 길이를 root의 x좌표 기준으로 잘라서 지정해야 함
                        line_cut = drawing_loader.Line(line_list.list_lines[j].get_start_x(), cross_x,
                                                       line_list.list_lines[j].get_start_y(),
                                                       line_list.list_lines[j].get_end_y(),
                                                       round(cross_x - line_list.list_lines[j].get_end_x(), 2),
                                                       line_list.list_lines[j].get_angle(),
                                                       line_list.list_lines[j].get_layer())
                        left_hall_r.append(line_cut)
                    elif (line_list.list_lines[j].get_end_x() < cross_x  # root의 x좌표보다 작은 선
                          and line_list.list_lines[j].get_length() > 0.2):
                        left_hall_r.append(line_list.list_lines[j])

    left_hall_l = sorted(left_hall_l)
    left_hall_l.reverse()
    left_hall_r = sorted(left_hall_r)
    left_hall_r.reverse()

    # list에 문 추가
    temp = []
    for i in range(len(left_hall_l)):
        temp.append(left_hall_l[i])
        if i < len(left_hall_l) - 1:
            door_line = drawing_loader.Line(left_hall_l[i + 1].get_end_x(), left_hall_l[i].get_start_x(),
                                            left_hall_l[i].get_start_y(), left_hall_l[i].get_end_y(),
                                            round(left_hall_l[i].get_start_x()
                                                  - left_hall_l[i + 1].get_end_x(), 2),
                                            left_hall_l[i].get_angle(),
                                            "DR")
            temp.append(door_line)
    left_hall_l = temp

    temp = []
    for i in range(len(left_hall_r)):
        temp.append(left_hall_r[i])
        if i < len(left_hall_r) - 1:
            door_line = drawing_loader.Line(left_hall_r[i + 1].get_end_x(), left_hall_r[i].get_start_x(),
                                            left_hall_r[i].get_start_y(), left_hall_r[i].get_end_y(),
                                            round(left_hall_r[i].get_start_x()
                                                  - left_hall_r[i + 1].get_end_x(), 2),
                                            left_hall_r[i].get_angle(),
                                            "DR")
            temp.append(door_line)
    left_hall_r = temp

    ###########################################################
    # print("\n[left_hall]")
    # print("-left_hall_l:")
    # for i in range(len(left_hall_l)):
    #     print(format(left_hall_l[i].get_length(), "0.2f")
    #           + " (x: " + str(left_hall_l[i].get_start_x()) + ") "
    #           + left_hall_l[i].get_layer())
    # print("-left_hall_r:")
    # for i in range(len(left_hall_r)):
    #     print(format(left_hall_r[i].get_length(), "0.2f")
    #           + " (x: " + str(left_hall_r[i].get_start_x()) + ") "
    #           + left_hall_r[i].get_layer())
    ###########################################################

    # upper hall
    # 복도 중심선과 벽 중심선 사이의 수직선 선택
    for i in range(len(line_list.list_isle_vertical)):
        if line_list.list_isle_vertical[i].get_start_x() < cross_x:  # 복도 중심선보다 왼쪽에 위치한 벽 중심선 선택
            for j in range(len(line_list.list_lines)):
                if (line_list.list_lines[j].get_start_x() == line_list.list_lines[j].get_end_x()  # 수직인 선
                        and line_list.list_lines[j].get_start_x() < cross_x
                        and line_list.list_lines[j].get_start_x() > line_list.list_isle_vertical[i].get_start_x()):

                    if (line_list.list_lines[j].get_start_y() < cross_y
                            and line_list.list_lines[j].get_end_y() > cross_y  # root의 y좌표에 걸리는 선
                            and line_list.list_lines[j].get_length() > 0.2):  # 벽, 문 두께 제외
                        # root에 걸리는 선의 길이를 root의 y좌표 기준으로 잘라서 지정해야 함
                        line_cut = drawing_loader.Line(line_list.list_lines[j].get_start_x(),
                                                       line_list.list_lines[j].get_end_x(),
                                                       cross_y, line_list.list_lines[j].get_end_y(),
                                                       round(line_list.list_lines[j].get_end_y() - cross_y, 2),
                                                       line_list.list_lines[j].get_angle(),
                                                       line_list.list_lines[j].get_layer())
                        upper_hall_l.append(line_cut)
                    elif (line_list.list_lines[j].get_start_y() > cross_y  # root의 y좌표보다 큰 선
                          and line_list.list_lines[j].get_length() > 0.2):
                        upper_hall_l.append(line_list.list_lines[j])

        if line_list.list_isle_vertical[i].get_start_x() > cross_x:  # 복도 중심선보다 오른쪽에 위치한 벽 중심선 선택
            for j in range(len(line_list.list_lines)):
                if (line_list.list_lines[j].get_start_x() == line_list.list_lines[j].get_end_x()  # 수직인 선
                        and line_list.list_lines[j].get_start_x() > cross_x
                        and line_list.list_lines[j].get_start_x() < line_list.list_isle_vertical[i].get_start_x()):
                    if (line_list.list_lines[j].get_start_y() < cross_y
                            and line_list.list_lines[j].get_end_y() > cross_y  # root의 y좌표에 걸리는 선
                            and line_list.list_lines[j].get_length() > 0.2):  # 벽, 문 두께 제외
                        # root에 걸리는 선의 길이를 root의 y좌표 기준으로 잘라서 지정해야 함
                        line_cut = drawing_loader.Line(line_list.list_lines[j].get_start_x(),
                                                       line_list.list_lines[j].get_end_x(),
                                                       cross_y, line_list.list_lines[j].get_end_y(),
                                                       round(line_list.list_lines[j].get_end_y() - cross_y, 2),
                                                       line_list.list_lines[j].get_angle(),
                                                       line_list.list_lines[j].get_layer())
                        upper_hall_r.append(line_cut)
                    elif (line_list.list_lines[j].get_start_y() > cross_y  # root의 y좌표보다 큰 선
                          and line_list.list_lines[j].get_length() > 0.2):
                        upper_hall_r.append(line_list.list_lines[j])

    upper_hall_l = sorted(upper_hall_l)
    upper_hall_r = sorted(upper_hall_r)

    # list에 문 추가
    temp = []
    for i in range(len(upper_hall_l)):
        temp.append(upper_hall_l[i])
        if i < len(upper_hall_l) - 1:
            door_line = drawing_loader.Line(upper_hall_l[i].get_start_x(), upper_hall_l[i].get_end_x(),
                                            upper_hall_l[i].get_end_y(), upper_hall_l[i + 1].get_start_y(),
                                            round(upper_hall_l[i + 1].get_start_y()
                                                  - upper_hall_l[i].get_end_y(), 2),
                                            upper_hall_l[i].get_angle(),
                                            "DR")
            temp.append(door_line)
    upper_hall_l = temp

    temp = []
    for i in range(len(upper_hall_r)):
        temp.append(upper_hall_r[i])
        if i < len(upper_hall_r) - 1:
            door_line = drawing_loader.Line(upper_hall_r[i].get_start_x(), upper_hall_r[i].get_end_x(),
                                            upper_hall_r[i].get_end_y(), upper_hall_r[i + 1].get_start_y(),
                                            round(upper_hall_r[i + 1].get_start_y()
                                                  - upper_hall_r[i].get_end_y(), 2),
                                            upper_hall_r[i].get_angle(),
                                            "DR")
            temp.append(door_line)
    upper_hall_r = temp

    ###########################################################
    # print("\n[upper_hall]")
    # print("-upper_hall_l:")
    # for i in range(len(upper_hall_l)):
    #     print(format(upper_hall_l[i].get_length(), "0.2f")
    #           + " (y: " + str(upper_hall_l[i].get_start_y()) + ") "
    #           + upper_hall_l[i].get_layer())
    # print("-upper_hall_r:")
    # for i in range(len(upper_hall_r)):
    #     print(format(upper_hall_r[i].get_length(), "0.2f")
    #           + " (y: " + str(upper_hall_r[i].get_start_y()) + ") "
    #           + upper_hall_r[i].get_layer())
    ###########################################################

    return right_hall_l, right_hall_r, left_hall_l, left_hall_r, upper_hall_l, upper_hall_r, down_hall_l, down_hall_r
