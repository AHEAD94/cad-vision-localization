from dataclasses import dataclass

INFINITY = 999999

"""##### Data structures #####"""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self, data):
        self.name = "default name"
        self.head = Node(data)

    # append new node in ascending order
    def append_node(self, data):  # 시작좌표가 끝 좌표보다 크다면 둘이 스위칭
        if self.head.next is None:
            self.head.next = Node(data)
            return
        start = self.head.next
        cur = start
        new = Node(data)

        if self.name == "Enclosings" or self.name == "Branches":
            while cur.next is not None:
                cur = cur.next
            cur.next = Node(data)
            return

        if self.head.data.slope == INFINITY:
            if self.name == "Lines":
                start_data = start.data.start_y
                new_data = new.data.start_y
            elif self.name == "Points":
                start_data = start.data.y
                new_data = new.data.y
        else:
            if self.name == "Lines":
                start_data = start.data.start_x
                new_data = new.data.start_x
            elif self.name == "Points":
                start_data = start.data.x
                new_data = new.data.x

        if start_data > new_data:
            new.next = self.head.next
            self.head.next = new
            return
        else:
            while cur.next is not None:
                if self.head.data.slope == INFINITY:
                    if self.name == "Lines":
                        cur_next_data = cur.next.data.start_y
                    elif self.name == "Points":
                        cur_next_data = cur.next.data.y
                else:
                    if self.name == "Lines":
                        cur_next_data = cur.next.data.start_x
                    elif self.name == "Points":
                        cur_next_data = cur.next.data.x

                if cur_next_data > new_data:
                    new.next = cur.next
                    cur.next = new
                    return
                cur = cur.next
        cur.next = new

    def reverse_order(self):
        stack = []

        cur = self.head.next
        while cur is not None:
            stack.append(cur.data)
            cur = cur.next

        cur = self.head
        for i in range(len(stack)):
            cur.next = Node(stack.pop())
            cur = cur.next

    def get_endpoints(self):  # 수직인 경우, 그렇지 않은 경우의 연산 재검토
        cur = self.head.next
        starting_point = Point()
        starting_point.x = cur.data.start_x
        starting_point.y = cur.data.start_y

        while cur is not None:
            # print(cur.data)
            if cur.next is None:
                end_point = Point()
                end_point.x = cur.data.end_x
                end_point.y = cur.data.end_y

                return starting_point, end_point
            cur = cur.next

    def remove_node(self, data):
        cur = self.head
        while cur.next is not None:
            if cur.next.data == data:
                # print("지운다?")
                if cur.next.next is None:
                    cur.next = None
                else:
                    cur.next = cur.next.next
                break
            cur = cur.next

    def print_all(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next

    ### 안쓰는 기능들 ###########################
    # # attach new node on the tail
    # def append(self, data): # original
    #     cur = self.head
    #     while cur.next is not None:
    #         cur = cur.next
    #     cur.next = Node(data)
    #
    # def get_node(self, index):
    #     cnt = 0
    #     node = self.head
    #     while cnt < index:
    #         cnt += 1
    #         node = node.next
    #     return node
    #
    # def add_node(self, index, value):
    #     new_node = Node(value)
    #     if index == 0:
    #         new_node.next = self.head
    #         self.head = new_node
    #         return
    #     node = self.get_node(index-1)
    #     next_node = node.next
    #     node.next = new_node
    #     new_node.next = next_node
    #
    # def delete_node(self, index):
    #     if index == 0:
    #         self.head = self.head.next
    #         return
    #     node = self.get_node(index-1)
    #     node.next = node.next.next


@dataclass
class Line:
    layer: str = None
    angle: float = None
    length: float = None
    start_x: float = None
    start_y: float = None
    end_x: float = None
    end_y: float = None

    def get_start_x(self):
        return self.start_x

    def get_end_x(self):
        return self.end_x

    def get_start_y(self):
        return self.start_y

    def get_end_y(self):
        return self.end_y

    def get_length(self):
        return self.length

    def get_angle(self):
        return self.angle

    def get_layer(self):
        return self.layer


@dataclass
class Arc:
    layer: str = None
    radius: float = None
    angle: float = None
    angle_size: float = None
    center_x: float = None
    center_y: float = None


@dataclass
class Block:
    layer: str = None
    name: str = None
    location_x: float = None
    location_y: float = None
    rotation: float = None


@dataclass
class LineEquation:
    slope: float = None
    intercept: float = None


@dataclass
class Point:
    x: float = None
    y: float = None


@dataclass
class Pair:
    # number: int = None
    name: str = None
    intercept1: float = None
    intercept2: float = None
    center: float = None
    slope: float = None
    center_start: Point() = None
    center_end: Point() = None
    intercept1_start: Point() = None
    intercept1_end: Point() = None
    intercept2_start: Point() = None
    intercept2_end: Point() = None
    inter1_link = None
    inter2_link = None
