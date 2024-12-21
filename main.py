import torch
import numpy as np

import object_loader
import processor
import inner_line_harvester
import hallway_maker
import indoor_graph
import visualizer

import image_loader
import video_loader
import vision_processor

"""##### GLOBAL FIELD #####"""
# for the drawing
MAGNIFICATION = 50

# for the calculation
INNER_WALL_THICKNESS = 0.2
OUTER_WALL_THICKNESS = 0.5
MIN_HALL_WIDTH = 1.2

if __name__ == '__main__':
    """ 1. 도면 파일의 데이터 추출 단계 """

    wall_line_list = []
    door_line_list = []
    arc_list = []
    door_block_list = []
    doorList = []
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0

    # csv file load
    csv_data = np.genfromtxt('drawings/8F_wall_trim_no_EV.csv', delimiter=',', dtype=None, encoding='UTF-8')
    # csv_data = np.genfromtxt('drawings/4F_no_EV.csv', delimiter=',', dtype=None, encoding='UTF-8') # -> 닫힌공간 실패, island 문제
    # csv_data = np.genfromtxt('drawings/4F_straight_no_EV.csv', delimiter=',', dtype=None, encoding='UTF-8') # -> 닫힌공간 실패, island 문제

    # csv test cases
    # csv_data = np.genfromtxt('testcases/diagonal.csv', delimiter=',', dtype=None, encoding='UTF-8') # -> 닫힌공간 실패, 세갈래 미구현
    # csv_data = np.genfromtxt('testcases/h-shaped.csv', delimiter=',', dtype=None, encoding='UTF-8')
    # csv_data = np.genfromtxt('testcases/square.csv', delimiter=',', dtype=None, encoding='UTF-8') # -> island 문제

    # classifying elements and obtaining constraints of drawing
    min_x, min_y, max_x, max_y = object_loader.classify_data(csv_data, wall_line_list, door_line_list, arc_list, door_block_list)
    # objectLoader.doorIntegrator(door_block_list, door_line_list, arc_list)
    # test for all of csv data
    print("[wall lines]: " + str(len(wall_line_list)))
    print("[door lines]: " + str(len(door_line_list)))
    print("[arcs]: " + str(len(arc_list)))
    print("[door blocks]: " + str(len(door_block_list)))

    # for i in range(len(wall_line_list)):
    #     print(wall_line_list[i])

    """ 2. 실내 공간 자료 구조 생성 단계 """

    line_equations = []
    wall_pairs = []
    hall_pairs = []

    # <동일 선상의 직선 분류> classifying same equations using linked list
    processor.classify_same_wall_lines(wall_line_list, line_equations)
    # TEST FOR SAME LINE EQUATION
    # print("[line_equations]: " + str(len(line_equations)))
    # for i in range(len(line_equations)):
    #     line_equations[i].print_all()
    # print("")

    # [닫힌 구간 확인]
    enclosings, door_sills = inner_line_harvester.get_enclosings(line_equations, door_block_list)
    # print("ENCLOSINGS")
    # for i in range(len(enclosings)):
    #     enclosings[i].print_all()

    # [내측 벽면 추출]
    inner_lines = inner_line_harvester.get_inner_lines(line_equations, enclosings, door_sills)
    # print("INNER LINES")
    # for i in range(len(inner_lines)):
    #     inner_lines[i].print_all()

    # [복도벽선 페어 생성]
    hall_pairs = hallway_maker.get_hall_pairs(inner_lines)
    # print("HALL PAIRS")
    # for i in range(len(hall_pairs)):
    #     print(hall_pairs[i])

    # [복도트리 생성]
    crossed_halls = hallway_maker.get_crossed_hall(hall_pairs)
    # print("CROSSED HALLS")
    # for i in range(len(crossed_halls)):
    #     print(crossed_halls[i])

    # [복도 분지]
    hall_trees = []
    hall_trees = hallway_maker.break_pairs(crossed_halls, inner_lines)
    # print("HALL TREES")
    # for i in range(len(hall_trees)):
    #     print(str(i)+":", hall_trees[i][0])
    #     print(hall_trees[i][1])
    #     hall_trees[i][2].print_all()

    # [실내그래프 생성]
    indoor_graphs = indoor_graph.build_graph(hall_trees)
    # print("INDOOR GRAPH DFS")
    # for i in range(len(indoor_graphs)):
    #     print("indoor_graph["+str(i)+"]")
    #     indoor_graphs[i].dfs()

    ##### 기준점 두개 이상일때의 그래프 생성 (이전 방법은 22.12.06 버전) #####
    # 1. 복도 트리 구성, hallTree = {기준점, 소교차점 리스트, 교차하는 hall_pair1, hall_pair2}
    # 2. hallTree들 저장
    # 3. 각 hallTree 별 복도 분지
    # 4. 분지된 hallTree 내 hall_pair들에 벽선들 붙이기
    # 5. 분지된 hallTree들의 hall_pair들끼리 비교하면서 중복되면 그래프 합성

    # [drawing test]
    visualizer.drawing_test(MAGNIFICATION, line_equations, door_line_list, door_block_list, door_sills, inner_lines,
                            hall_pairs, crossed_halls, hall_trees, max_x, max_y)
    print("CAD2GRAPH process DONE\n")

    """ 3. 실내 위치 인식 단계 """

    # [graph load]
    hall_nodes, hall_nodes_reverse, end_nodes = indoor_graph.get_nodes(indoor_graphs[0])

    # mps test __23.05.27__
    import torch

    device = torch.device('mps')
    print(f" - device : {device}")
    sample = torch.Tensor([[10, 20, 30], [30, 20, 10]])
    print(f" - cpu tensor : ")
    print(sample)
    sample = sample.to(device)
    print(f" - gpu tensor : ")
    print(sample)

    # [model load]
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best.pt')

    # [images]
    imageFolder = "images"
    image_nums = image_loader.get_image_nums(imageFolder)

    # [videos]
    videoFile = "videos/b1_1.mp4"
    # video_file = "videos/20220707_223612_HoloLens.mp4"
    # video_file = "videos/20220707_223734_HoloLens.mp4"
    # video_file = "videos/20220708_060935_HoloLens.mp4"
    # video_file = "videos/20220708_061059_HoloLens.mp4"
    # video_file = "videos/20220708_061308_HoloLens.mp4" # best case
    capture = video_loader.load(videoFile)

    # Test
    # [1 image]
    # visionProcessor.image_test(model, imageFolder, hall_nodes, hall_nodes_reverse, end_nodes, 175)
    # [images]
    # for i in range(1, image_nums-1):
    #     visionProcessor.image_test(model, imageFolder, hall_nodes, hall_nodes_reverse, i)
    # [video]
    vision_processor.video_test(model, capture, hall_nodes, hall_nodes_reverse, end_nodes)

    # Camera Open - 실시간으로 카메라를 사용할 때
    # As camera captures 2D ratio, compare it to indoor map
    # while CAMERA_OPEN:
    #     frame = getFrame()
    #     door_blabla = doorDetection.blabal
    #     ...
    #     left_ratio, right_ratio = geometrics.get_2d_ratio()
    #
    #     if ratio_is_available:
    #         compare it to indoor map & show the result
    #     else==
    #         continue
