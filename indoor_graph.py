import copy
import math

import data_structures

INFINITY = 999999


class Node:
    def __init__(self, val, name, length, pixel, side, branch_num=None):
        self.val = val
        self.name = name
        self.length = length
        self.pixel = pixel
        self.side = side
        self.branch_num = branch_num
        self.edges = []


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, val, name, length, pixel, side, branch_num=None):
        new_node = Node(val, name, length, pixel, side, branch_num)
        self.nodes.append(new_node)

    def add_edge(self, node1, node2):
        self.nodes[node1].edges.append(self.nodes[node2])
        self.nodes[node2].edges.append(self.nodes[node1])

    def dfs(self):
        if not self.nodes:
            return []
        start = self.nodes[0]
        visited, stack, result = set([start]), [start], []

        while stack:
            node = stack.pop()
            result.append(node)
            for nd in node.edges:
                if nd not in visited:
                    # print("node: ("+str(nd.val)+", "+str(nd.name)+", "+str(nd.length)+")")
                    stack.append(nd)
                    visited.add(nd)

        return result


def get_euclid_dist(p1, p2):
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt((dx * dx) + (dy * dy))
    return dist


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


def is_counter_clockwise(p1, p2, p3):
    cross_prod = (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)

    if cross_prod > 0:
        return 1
    else:
        return -1


def add_node(graph, root_coord, hallway, hall_side, current_number, total_nodes, branch_number):
    node_number = current_number

    wall_start_line = hall_side.head.next.data
    # print(wall_start_line)
    wall_start_point = data_structures.Point(wall_start_line.start_x, wall_start_line.start_y)

    start_point_mismatch = 0
    if root_coord != hallway.center_start:
        start_point_mismatch = 1
        hall_center_end = hallway.center_start
    else:
        hall_center_end = hallway.center_end

    # 1. 각 hallway의 벽면 선들 루트에서 리프까지의 순서로 변경
    if start_point_mismatch == 1:
        hall_side.reverse_order()

    # 2. CCW 알고리즘 이용하여 벽면 왼쪽, 오른쪽 구분
    # Counter-ClockWise algorithm
    # -> if cross product result is (-), clockwise
    # -> if the result is (+), counter clockwise
    # https://gaussian37.github.io/math-algorithm-ccw/
    ccw_result = is_counter_clockwise(root_coord, hall_center_end, wall_start_point)
    # print(ccw_result)

    nodes = 0
    cur = hall_side.head.next
    while cur is not None:
        # print(cur.data)
        drawing_x = round((cur.data.get_start_x() + cur.data.get_end_x()) / 2, 2)
        drawing_y = round((cur.data.get_start_y() + cur.data.get_end_y()) / 2, 2)
        if ccw_result < 0:
            wall_side = 'forward-right'
        else:
            wall_side = 'forward-left'
        if cur.data.get_layer() == "W":
            graph.add_node(node_number, 'wall', cur.data.get_length(), (drawing_x, drawing_y), wall_side, branch_number)
        elif cur.data.get_layer() == "DR":
            graph.add_node(node_number, 'door', cur.data.get_length(), (drawing_x, drawing_y), wall_side, branch_number)
        node_number += 1
        nodes += 1

        cur = cur.next

    total_nodes.append(nodes)

    return graph, node_number


def build_graph(hall_trees):
    graphs = []

    print("\n__Building Graph__")

    for i in range(len(hall_trees)):
        # print(hall_trees[i])
        cross_x = hall_trees[i][0].x
        cross_y = hall_trees[i][0].y

        graph = Graph()
        graph.add_node(0, 'root', -1, (cross_x, cross_y), 'root')

        # 그래프 유형 1
        # 루트-hallway-양쪽 linked list
        # 그래프 유형 2
        # 루트-양쪽 노드들 <-= 진행중

        # Add nodes
        root_coord = data_structures.Point(cross_x, cross_y)
        total_nodes = []
        start_node_nums = []
        current_number = 1
        branch_number = 0

        cur = hall_trees[i][2].head.next
        while cur is not None:
            hall_branch = cur.data
            graph, current_number = add_node(graph, root_coord, hall_branch, hall_branch.inter1_link, current_number,
                                             total_nodes, branch_number)
            graph, current_number = add_node(graph, root_coord, hall_branch, hall_branch.inter2_link, current_number,
                                             total_nodes, branch_number)

            branch_number = branch_number + 1
            cur = cur.next

        # print("node numbers")
        # for j in range(len(total_nodes)):
        #     print(total_nodes[j])

        print("node test")
        k = 0
        l = 0
        for j in range(len(graph.nodes)):
            print("N" + str(j) + " (" + str(graph.nodes[j].val) + ", " + str(graph.nodes[j].name) + ", " + str(
                graph.nodes[j].length) + ", " + str(graph.nodes[j].pixel) + ", " + str(graph.nodes[j].side))
            if graph.nodes[j].val == 0:
                print("")
            if l == total_nodes[k]:
                print("")
                k += 1
                l = 0
            l += 1

        idx = 0
        count = 0
        for j in range(len(graph.nodes)):
            count += 1
            if j == 1:
                start_node_nums.append(graph.nodes[j].val)
                count = 0
            if count == total_nodes[idx]:
                start_node_nums.append(graph.nodes[j].val)
                idx += 1
                count = 0

        # for j in range(len(start_node_nums)):
        #     print(start_node_nums[j])

        # edges
        for j in range(len(start_node_nums)):
            # print("start_node: ", start_node_nums[j])
            graph.add_edge(0, start_node_nums[j])
            if j + 1 < len(start_node_nums):
                for k in range(start_node_nums[j], start_node_nums[j + 1]):
                    if k + 1 < start_node_nums[j + 1]:
                        # print("k, k+1: ", k, k+1)
                        graph.add_edge(k, k + 1)  # OK
        last_start_num = start_node_nums[len(start_node_nums) - 1]
        last_total_num = total_nodes[len(total_nodes) - 1]
        for j in range(last_start_num, last_start_num + last_total_num - 1):
            # print("j, j+1: ", j, j+1)
            graph.add_edge(j, j + 1)

        graphs.append(graph)

    print("__Building Graph Done__\n")

    return graphs


def get_nodes(graph):
    # print("[Indoor graph]")
    start_nodes = graph.nodes[0].edges
    # for i in range(len(start_nodes)):
    #     print("-start_nodes: ("+str(start_nodes[i].val)+", "+str(start_nodes[i].name)+", "+str(start_nodes[i].length)+", "+str(start_nodes[i].side)+")")

    end_nodes = []
    hall_nodes = []
    hall_nodes_reverse = []
    for i in range(len(start_nodes) + 1):
        hall_nodes.append([])
        hall_nodes_reverse.append([])

    dfs_result = graph.dfs()
    ###########################################
    # print("dfs_result")
    # for i in range(len(dfs_result)):
    #     print(dfs_result[i].val)
    # print("right_start_nodes")
    # for i in range(len(start_nodes)):
    #     print(start_nodes[i].val)
    ###########################################
    edge_flag = 0
    for i in range(len(dfs_result)):  # 16
        for n in start_nodes:
            if dfs_result[i].val == n.val:
                edge_flag = edge_flag + 1
        hall_nodes[edge_flag].append(dfs_result[i])
    ###########################################
    # print("hall_nodes")
    # for i in range(len(start_nodes) + 1):
    #     print("-"+str(hall_nodes[i][0].val))
    ###########################################

    for i in range(len(hall_nodes)):
        end_nodes.append(hall_nodes[i][len(hall_nodes[i]) - 1])  # 0, 16, 6, 2
        hall_nodes_reverse[i] = list(reversed(hall_nodes[i]))  # 0, 16, 6, 2
        # print("------")
        # for j in range(len(hall_nodes[i])):
        #     print(hall_nodes[i][j].val, hall_nodes[i][j].name,
        #           hall_nodes[i][j].length)

    # for i in range(1, len(end_nodes)):
    #     print("-end_nodes: ("+str(end_nodes[i].val)+", "+str(end_nodes[i].name)+", "+str(end_nodes[i].length)+", "+str(end_nodes[i].side)+")")

    ###########################################
    # print("end_nodes")
    # for i in range(len(hall_nodes)):
    #     print("-"+str(end_nodes[i].val))
    # print("hall_nodes_reverse")
    # for i in range(len(hall_nodes)):
    #     print("-"+str(hall_nodes_reverse[i][0].val))
    ###########################################

    # hall nodes - opposite
    # print("------")
    # print("-----hall nodes - Backward-----")
    # for i in range(len(hall_nodes_reverse)):
    #     print("------")
    #     for j in range(len(hall_nodes_reverse[i])):
    #         print(hall_nodes_reverse[i][j].val, hall_nodes_reverse[i][j].name,
    #               hall_nodes_reverse[i][j].length)

    return hall_nodes, hall_nodes_reverse, end_nodes
