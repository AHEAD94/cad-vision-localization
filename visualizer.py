import cv2
import numpy as np
import random

COLOR_CHANNEL = 3
BRIGHTNESS = 255


### drawing test for same line equations ###
def m2p(magnification, meter):  # meter to pixel
    mag = magnification
    return round(meter * mag)


def flip(y, limit_y):  # OpenCV의 y축을 CAD의 y축에 맞추어 반전
    return limit_y - y


### drawing test for center lines ###
def draw_wall_lines(magnification, drawing, limit_y, line_equations):
    for i in range(len(line_equations)):
        cur = line_equations[i].head.next

        while cur is not None:
            x1 = m2p(magnification, cur.data.start_x)
            y1 = flip(m2p(magnification, cur.data.start_y), limit_y)
            x2 = m2p(magnification, cur.data.end_x)
            y2 = flip(m2p(magnification, cur.data.end_y), limit_y)

            cv2.line(drawing,
                     pt1=(x1, y1),
                     pt2=(x2, y2),
                     color=(0, 0, 0),
                     thickness=2,
                     lineType=cv2.LINE_AA)
            cur = cur.next


def draw_wall_center_lines(magnification, drawing, limit_y, wall_pairs):
    for i in range(len(wall_pairs)):
        x1 = m2p(magnification, wall_pairs[i].center_start.x)
        y1 = flip(m2p(magnification, wall_pairs[i].center_start.y), limit_y)
        x2 = m2p(magnification, wall_pairs[i].center_end.x)
        y2 = flip(m2p(magnification, wall_pairs[i].center_end.y), limit_y)

        cv2.line(drawing,
                 pt1=(x1, y1),
                 pt2=(x2, y2),
                 color=(0, 0, 255),
                 thickness=2,
                 lineType=cv2.LINE_AA)


def draw_hall_lines(magnification, drawing, limit_x, limit_y, hall_pairs):
    for i in range(len(hall_pairs)):
        x1 = m2p(magnification, hall_pairs[i].center_start.x)
        y1 = flip(m2p(magnification, hall_pairs[i].center_start.y), limit_y)
        x2 = m2p(magnification, hall_pairs[i].center_end.x)
        y2 = flip(m2p(magnification, hall_pairs[i].center_end.y), limit_y)
        inner1_x1 = m2p(magnification, hall_pairs[i].intercept1_start.x)
        inner1_y1 = flip(m2p(magnification, hall_pairs[i].intercept1_start.y), limit_y)
        inner1_x2 = m2p(magnification, hall_pairs[i].intercept1_end.x)
        inner1_y2 = flip(m2p(magnification, hall_pairs[i].intercept1_end.y), limit_y)
        inner2_x1 = m2p(magnification, hall_pairs[i].intercept2_start.x)
        inner2_y1 = flip(m2p(magnification, hall_pairs[i].intercept2_start.y), limit_y)
        inner2_x2 = m2p(magnification, hall_pairs[i].intercept2_end.x)
        inner2_y2 = flip(m2p(magnification, hall_pairs[i].intercept2_end.y), limit_y)

        cv2.line(drawing,
                 pt1=(x1, y1),
                 pt2=(x2, y2),
                 color=(255, 0, 255),
                 thickness=1,
                 lineType=cv2.LINE_AA)
        cv2.line(drawing,
                 pt1=(inner1_x1, inner1_y1),
                 pt2=(inner1_x2, inner1_y2),
                 color=(255, 255, 0),
                 thickness=1,
                 lineType=cv2.LINE_AA)
        cv2.line(drawing,
                 pt1=(inner2_x1, inner2_y1),
                 pt2=(inner2_x2, inner2_y2),
                 color=(255, 255, 0),
                 thickness=1,
                 lineType=cv2.LINE_AA)


def draw_cross_points(magnification, drawing, limit_y, cross_points):
    for i in range(len(cross_points)):
        cur = cross_points[i].head.next

        while cur is not None:
            x = int(m2p(magnification, cur.data.x))
            y = int(flip(m2p(magnification, cur.data.y), limit_y))

            if len(cross_points) == 1:
                cv2.line(drawing,
                         pt1=(x, y),
                         pt2=(x, y),
                         color=(255, 0, 0),
                         thickness=20,
                         lineType=cv2.LINE_AA)
                cv2.putText(drawing,
                            str(cur.data.x) + ", " + str(cur.data.y),
                            (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 0, 0), 2)
            else:
                cv2.line(drawing,
                         pt1=(x, y),
                         pt2=(x, y),
                         color=(0, 0, 0),
                         thickness=8,
                         lineType=cv2.LINE_AA)
                cv2.putText(drawing,
                            str(cur.data.x) + ", " + str(cur.data.y),
                            (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 0), 1)
            cur = cur.next


# def draw_wall_length(magnification, drawing, limit_y, inner_lines):
#     for i in range(len(inner_lines)):
#         cur = inner_lines[i].head.next
#
#         while cur is not None:
#             length = cur.data.length
#             if inner_lines[i].head.data.slope == 0:
#                 x = int(m2p(magnification, (cur.data.start_x+cur.data.end_x)/2))
#                 y = int(flip(m2p(magnification, cur.data.start_y), limit_y))
#             else:
#                 x = int(m2p(magnification, cur.data.start_x))
#                 y = int(flip(m2p(magnification, (cur.data.start_y+cur.data.end_y)/2), limit_y))
#
#             cv2.putText(drawing, str(length), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
#             cur = cur.next

def draw_wall_length(magnification, drawing, limit_y, hall_trees):
    color = (155, 155, 155)
    # case_1
    offset_x = -15
    offset_y = 10
    font_size = 0.5

    # case_2
    # offset_x = -35
    # offset_y = 14
    # font_size = 1.15

    for i in range(len(hall_trees)):
        cur_branch = hall_trees[i][2].head.next
        while cur_branch is not None:
            cur_side1 = cur_branch.data.inter1_link.head.next
            cur_side2 = cur_branch.data.inter2_link.head.next

            while cur_side1 is not None:
                length = cur_side1.data.length
                if cur_branch.data.inter1_link.head.data.slope == 0:
                    x = int(m2p(magnification, (cur_side1.data.start_x + cur_side1.data.end_x) / 2))
                    y = int(flip(m2p(magnification, cur_side1.data.start_y), limit_y))
                else:
                    x = int(m2p(magnification, cur_side1.data.start_x))
                    y = int(flip(m2p(magnification, (cur_side1.data.start_y + cur_side1.data.end_y) / 2), limit_y))
                x = x + offset_x
                y = y - offset_y
                cv2.putText(drawing, str(length), (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 2)
                cur_side1 = cur_side1.next

            while cur_side2 is not None:
                length = cur_side2.data.length
                if cur_branch.data.inter1_link.head.data.slope == 0:
                    x = int(m2p(magnification, (cur_side2.data.start_x + cur_side2.data.end_x) / 2))
                    y = int(flip(m2p(magnification, cur_side2.data.start_y), limit_y))
                else:
                    x = int(m2p(magnification, cur_side2.data.start_x))
                    y = int(flip(m2p(magnification, (cur_side2.data.start_y + cur_side2.data.end_y) / 2), limit_y))
                x = x + offset_x
                y = y - offset_y
                cv2.putText(drawing, str(length), (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 2)
                cur_side2 = cur_side2.next

            cur_branch = cur_branch.next


def draw_door_lines(magnification, drawing, limit_y, door_line_list, door_block_list):
    for i in range(len(door_line_list)):
        x1 = m2p(magnification, door_line_list[i].start_x)
        y1 = flip(m2p(magnification, door_line_list[i].start_y), limit_y)
        x2 = m2p(magnification, door_line_list[i].end_x)
        y2 = flip(m2p(magnification, door_line_list[i].end_y), limit_y)

        cv2.line(drawing,
                 pt1=(x1, y1),
                 pt2=(x2, y2),
                 color=(255, 0, 255),
                 thickness=1,
                 lineType=cv2.LINE_AA)

    # for i in range(len(arc_list)):
    #     xc = m2p(magnification, arc_list[i].center_x)
    #     yc = flip(m2p(magnification, arc_list[i].center_y), limit_y)
    #
    #     rad = m2p(magnification, arc_list[i].radius)
    #     start_angle = arc_list[i].start_angle
    #     total_angle = arc_list[i].total_angle
    #     end_angle = start_angle+total_angle
    #
    #     cv2.ellipse(drawing, (xc, yc), (rad, rad), 0, start_angle, end_angle,
    #                 color=(255, 0, 255),
    #                 thickness=1,
    #                 lineType=cv2.LINE_AA)

    for i in range(len(door_block_list)):
        xl = m2p(magnification, door_block_list[i].location_x)
        yl = flip(m2p(magnification, door_block_list[i].location_y), limit_y)

        cv2.line(drawing,
                 pt1=(xl, yl),
                 pt2=(xl, yl),
                 color=(255, 0, 255),
                 thickness=10,
                 lineType=cv2.LINE_AA)


def draw_inner_lines(magnification, drawing, limit_y, enclosings):
    for i in range(len(enclosings)):
        cur = enclosings[i].head.next
        while cur is not None:
            x1 = m2p(magnification, cur.data.start_x)
            y1 = flip(m2p(magnification, cur.data.start_y), limit_y)
            x2 = m2p(magnification, cur.data.end_x)
            y2 = flip(m2p(magnification, cur.data.end_y), limit_y)

            cv2.line(drawing,
                     pt1=(x1, y1),
                     pt2=(x2, y2),
                     color=(0, 255, 0),
                     thickness=4,
                     lineType=cv2.LINE_AA)
            cur = cur.next


def draw_hall_trees(magnification, drawing, limit_y, hall_trees):
    color_old = []
    diff_rgb = 20
    diff_color = 60
    line_thickness = 6

    for i in range(len(hall_trees)):
        cur_branch = hall_trees[i][2].head.next
        while cur_branch is not None:

            while True:
                rand_red = random.randrange(155, 255)
                rand_green = random.randrange(155, 255)
                rand_blue = random.randrange(155, 255)
                color_avg = (rand_red + rand_green + rand_blue) / 3
                if (abs(rand_red - color_avg) > diff_rgb
                        and abs(rand_green - color_avg) > diff_rgb
                        and abs(rand_blue - color_avg) > diff_rgb):
                    if len(color_old) == 0:
                        break
                    score = 0
                    for j in range(len(color_old)):
                        if (abs(rand_red - color_old[j][0]) > diff_color
                                or abs(rand_green - color_old[j][1]) > diff_color
                                or abs(rand_blue - color_old[j][2]) > diff_color):
                            score = score + 1
                    if score == len(color_old):
                        break

            rand_color = (rand_red, rand_green, rand_blue)
            color_old.append(rand_color)

            cur = cur_branch.data.inter1_link.head.next
            while cur is not None:
                if cur.data.layer == 'W':
                    x1 = m2p(magnification, cur.data.start_x)
                    y1 = flip(m2p(magnification, cur.data.start_y), limit_y)
                    x2 = m2p(magnification, cur.data.end_x)
                    y2 = flip(m2p(magnification, cur.data.end_y), limit_y)
                    cv2.line(drawing,
                             pt1=(x1, y1),
                             pt2=(x2, y2),
                             color=(rand_blue, rand_green, rand_red),
                             thickness=line_thickness,
                             lineType=cv2.LINE_AA)
                cur = cur.next

            cur = cur_branch.data.inter2_link.head.next
            while cur is not None:
                if cur.data.layer == 'W':
                    x1 = m2p(magnification, cur.data.start_x)
                    y1 = flip(m2p(magnification, cur.data.start_y), limit_y)
                    x2 = m2p(magnification, cur.data.end_x)
                    y2 = flip(m2p(magnification, cur.data.end_y), limit_y)
                    cv2.line(drawing,
                             pt1=(x1, y1),
                             pt2=(x2, y2),
                             color=(rand_blue, rand_green, rand_red),
                             thickness=line_thickness,
                             lineType=cv2.LINE_AA)
                cur = cur.next

            cur_branch = cur_branch.next


def draw_door_sills(magnification, drawing, limit_y, door_sills):
    for i in range(len(door_sills)):
        cur = door_sills[i].head.next
        while cur is not None:
            if cur.data.length != 0.2:
                x1 = m2p(magnification, cur.data.start_x)
                y1 = flip(m2p(magnification, cur.data.start_y), limit_y)
                x2 = m2p(magnification, cur.data.end_x)
                y2 = flip(m2p(magnification, cur.data.end_y), limit_y)

                cv2.line(drawing,
                         pt1=(x1, y1),
                         pt2=(x2, y2),
                         color=(255, 0, 255),
                         thickness=4,
                         lineType=cv2.LINE_AA)
            cur = cur.next


def draw_tree_points(magnification, drawing, limit_y, hall_trees):
    for i in range(len(hall_trees)):
        x = int(m2p(magnification, hall_trees[i][0].x))
        y = int(flip(m2p(magnification, hall_trees[i][0].y), limit_y))
        cv2.line(drawing,
                 pt1=(x, y),
                 pt2=(x, y),
                 color=(255, 0, 0),
                 thickness=20,
                 lineType=cv2.LINE_AA)
        x = x + 10
        y = y - 15
        cv2.putText(drawing,
                    str(hall_trees[i][0].x) + ", " + str(hall_trees[i][0].y),
                    (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2)

        cross_points = hall_trees[i][1]
        for j in range(len(cross_points)):
            x = int(m2p(magnification, cross_points[j].x))
            y = int(flip(m2p(magnification, cross_points[j].y), limit_y))
            cv2.line(drawing,
                     pt1=(x, y),
                     pt2=(x, y),
                     color=(0, 0, 0),
                     thickness=8,
                     lineType=cv2.LINE_AA)
            x = x + 8
            y = y + 25
            cv2.putText(drawing,
                        str(cross_points[j].x) + ", " + str(cross_points[j].y),
                        (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 0, 0), 1)


def drawing_test(magnification, line_equations, door_line_list, door_block_list, door_sills, inner_lines, hall_pairs,
                 crossed_halls, hall_trees, max_x, max_y):
    limit_x = int(m2p(magnification, max_x))
    limit_y = int(m2p(magnification, max_y))
    color_channel = COLOR_CHANNEL
    brightness = BRIGHTNESS
    drawing = np.zeros((limit_y, limit_x, color_channel), np.uint8) + brightness

    draw_wall_lines(magnification, drawing, limit_y, line_equations)
    # draw_door_lines(magnification, drawing, limit_y, door_line_list, door_block_list)
    draw_door_sills(magnification, drawing, limit_y, door_sills)
    draw_inner_lines(magnification, drawing, limit_y, inner_lines)
    draw_hall_lines(magnification, drawing, limit_x, limit_y, hall_pairs)  # Problems in DIAGONAL

    draw_hall_trees(magnification, drawing, limit_y, hall_trees)
    draw_tree_points(magnification, drawing, limit_y, crossed_halls)

    # draw_wall_length(magnification, drawing, limit_y, inner_lines)
    # draw_wall_length(magnification, drawing, limit_y, hall_trees)

    cv2.imshow('Floor plan drawing test', drawing)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
