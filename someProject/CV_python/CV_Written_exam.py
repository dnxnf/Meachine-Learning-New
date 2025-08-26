#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project     ：MachineLearning
@File        ：CV_Written_exam.py
@Description ：
@Author      ：Hello World
@Date        ：2025/8/22 下午9:19
"""
"""
CV笔试编程题全集
包含图像处理、矩阵操作、经典CV算法实现
"""

import numpy as np
import random
from collections import defaultdict, deque
import heapq
import math


# ==================== 一、基础输入输出 ====================
def basic_io_demo():
    """基础输入输出演示"""
    print("=== 基础输入输出演示 ===")

    # 模拟输入
    input_str = "1 2 3 4 5"
    print(f"模拟输入: '{input_str}'")

    # 读取单行多个数字
    data = list(map(int, input_str.split()))
    print(f"转换为列表: {data}")

    # 读取两个数字
    a, b = map(int, "10 20".split())
    print(f"两个数字: a={a}, b={b}")

    # 读取矩阵
    matrix_input = ["1 2 3", "4 5 6", "7 8 9"]
    matrix = []
    for line in matrix_input:
        row = list(map(int, line.split()))
        matrix.append(row)
    print(f"3x3矩阵: {matrix}")


# ==================== 二、矩阵基本操作 ====================
def rotate_matrix(matrix):
    """顺时针旋转矩阵90度 (LeetCode 48)"""
    n = len(matrix)
    # 先转置
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # 再每行反转
    for i in range(n):
        matrix[i].reverse()
    return matrix


def reshape_matrix(mat, r, c):
    """重塑矩阵 (LeetCode 566)"""
    m, n = len(mat), len(mat[0])
    if m * n != r * c:
        return mat

    flat = [num for row in mat for num in row]
    new_mat = []
    for i in range(r):
        new_mat.append(flat[i * c : (i + 1) * c])
    return new_mat


def spiral_order(matrix):
    """螺旋矩阵遍历 (LeetCode 54)"""
    if not matrix:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # 从左到右
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1

        # 从上到下
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1

        if top <= bottom:
            # 从右到左
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1

        if left <= right:
            # 从下到上
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1

    return result


# ==================== 三、图像卷积/滤波 ====================
def convolve2d(image, kernel):
    """2D卷积实现"""
    i_h, i_w = len(image), len(image[0])
    k_h, k_w = len(kernel), len(kernel[0])

    pad_h, pad_w = k_h // 2, k_w // 2

    # 创建输出矩阵（初始化为0）
    output = [[0] * i_w for _ in range(i_h)]

    for i in range(pad_h, i_h - pad_h):
        for j in range(pad_w, i_w - pad_w):
            conv_sum = 0
            for m in range(-pad_h, pad_h + 1):
                for n in range(-pad_w, pad_w + 1):
                    # 计算卷积
                    conv_sum += image[i + m][j + n] * kernel[m + pad_h][n + pad_w]
            output[i][j] = conv_sum

    return output


# 这个是基于mumpy的，上面是基于普通数组的
import numpy as np


def conv2d1(image: np.ndarray, kernel: np.ndarray):
    # 高宽，卷积的高和宽，填充的~，结果的~
    h, w = image.shape
    kh, kw = kernel.shape
    padh, padw = (kh - 1) // 2, (kw - 1) // 2

    # NOTE 要么使用填充并输出 (5, 5)，要么不使用填充输出 (3, 3)，但不能混合使用。

    # resh = h - kh + 1
    # resw = w - kw + 1
    resh = h
    resw = w
    # zeros的参数是一个表示数组维度的元祖
    output = np.zeros((resh, resw))

    padded_image = np.zeros((h + 2 * padh, w + 2 * padw))
    padded_image[padh : padh + h, padw : padw + w] = image

    # 默认stride为1
    for i in range(resh):
        for j in range(resw):
            # 计算得到填充后的全0图像
            sub_image = padded_image[i : i + kh, j : j + kw]
            output[i, j] = (sub_image * kernel).sum()
    return output


# ==================== 四、非极大值抑制 (NMS) ====================
def calculate_iou(box1, boxes):
    """计算IoU
    box1: 单个边界框，格式 [x1, y1, x2, y2]
    boxes: 多个边界框，形状为 (N, 4) 的数组
    """
    x1 = np.maximum(box1[0], boxes[:, 0])
    y1 = np.maximum(box1[1], boxes[:, 1])
    x2 = np.minimum(box1[2], boxes[:, 2])
    y2 = np.minimum(box1[3], boxes[:, 3])

    intersection = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union = area1 + area2 - intersection

    return intersection / (union + 1e-6)  # 避免除零


def nms(boxes, scores, iou_threshold=0.5):
    """非极大值抑制"""
    boxes = np.array(boxes)
    scores = np.array(scores)

    indices = np.argsort(scores)[::-1]
    keep = []

    while len(indices) > 0:
        current = indices[0]
        keep.append(current)

        if len(indices) == 1:
            break

        current_box = boxes[current]
        other_boxes = boxes[indices[1:]]

        ious = calculate_iou(current_box, other_boxes)
        indices = indices[1:][ious < iou_threshold]

    return keep


# ==================== 五、数据增强 ====================
def random_crop(image, crop_size):
    """随机裁剪"""
    h, w = len(image), len(image[0])
    crop_h, crop_w = crop_size

    top = random.randint(0, h - crop_h)
    left = random.randint(0, w - crop_w)

    cropped = []
    for i in range(top, top + crop_h):
        cropped.append(image[i][left : left + crop_w])

    return cropped


def random_flip(image, prob=0.5):
    """随机水平翻转"""
    if random.random() < prob:
        return [row[::-1] for row in image]
    return image


# ==================== 六、numpy专项 ====================
def numpy_demo():
    """numpy使用演示"""
    print("\n=== Numpy演示 ===")

    # 创建矩阵
    ones = np.ones((2, 3))
    zeros = np.zeros((3, 2))
    identity = np.eye(3)
    random_mat = np.random.rand(2, 2)

    print(f"全1矩阵:\n{ones}")
    print(f"单位矩阵:\n{identity}")
    print(f"随机矩阵:\n{random_mat}")

    # 矩阵运算
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    C = np.dot(A, B)  # 矩阵乘法
    print(f"矩阵乘法:\n{A} × \n{B} = \n{C}")

    # 广播机制
    a = np.array([1, 2, 3])
    b = np.array([[1], [2], [3]])
    result = a + b
    print(f"广播相加:\n{a} + \n{b} = \n{result}")

    # 索引和切片
    arr = np.random.rand(4, 4)
    print(f"原始矩阵:\n{arr}")
    print(f"切片 [1:3, 1:3]:\n{arr[1:3, 1:3]}")


# ==================== 七、测试函数 ====================
def test_all_functions():
    """测试所有函数"""
    print("开始测试所有CV笔试相关函数...\n")

    # 基础IO演示
    basic_io_demo()

    # 测试矩阵旋转
    print("\n=== 测试矩阵旋转 ===")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"原始矩阵: {matrix}")
    rotated = rotate_matrix([row[:] for row in matrix])  # 深拷贝
    print(f"旋转后: {rotated}")

    # 测试矩阵重塑
    print("\n=== 测试矩阵重塑 ===")
    original = [[1, 2], [3, 4], [5, 6]]
    reshaped = reshape_matrix(original, 2, 3)
    print(f"原始: {original}")
    print(f"重塑为2x3: {reshaped}")

    # 测试螺旋遍历
    print("\n=== 测试螺旋遍历 ===")
    spiral_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    spiral_result = spiral_order(spiral_matrix)
    print(f"矩阵: {spiral_matrix}")
    print(f"螺旋遍历结果: {spiral_result}")

    # 测试卷积
    print("\n=== 测试卷积 ===")
    test_image = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    mean_kernel = [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]]
    convolved = convolve2d(test_image, mean_kernel)
    print(f"原始图像: {test_image}")
    print(f"均值滤波后: {convolved}")

    # 测试NMS
    print("\n=== 测试NMS ===")
    boxes = [[10, 10, 50, 50], [15, 15, 55, 55], [30, 30, 70, 70], [100, 100, 150, 150]]
    scores = [0.9, 0.8, 0.7, 0.85]
    keep_indices = nms(boxes, scores, 0.3)
    print(f"Boxes: {boxes}")
    print(f"Scores: {scores}")
    print(f"保留的索引: {keep_indices}")

    # 测试数据增强
    print("\n=== 测试数据增强 ===")
    test_img = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    cropped = random_crop(test_img, (2, 2))
    flipped = random_flip(test_img, 1.0)  # 强制翻转
    print(f"原始: {test_img}")
    print(f"随机裁剪(2x2): {cropped}")
    print(f"水平翻转: {flipped}")

    # Numpy演示
    numpy_demo()


# ==================== 八、工具函数 ====================
def create_test_matrix(rows, cols):
    """创建测试矩阵"""
    return [[i * cols + j + 1 for j in range(cols)] for i in range(rows)]


def print_matrix(matrix, name="矩阵"):
    """美化打印矩阵"""
    print(f"{name}:")
    for row in matrix:
        print(row)
    print()


# ==================== 八、高级矩阵操作 ====================
def matrix_transpose(matrix):
    """矩阵转置"""
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def matrix_multiply(A, B):
    """矩阵乘法 (自己实现，不用numpy)"""
    if len(A[0]) != len(B):
        raise ValueError("矩阵维度不匹配")

    n, m, p = len(A), len(A[0]), len(B[0])
    result = [[0] * p for _ in range(n)]

    for i in range(n):
        for j in range(p):
            for k in range(m):
                result[i][j] += A[i][k] * B[k][j]

    return result


def matrix_inverse_2x2(matrix):
    """2x2矩阵求逆"""
    if len(matrix) != 2 or len(matrix[0]) != 2:
        raise ValueError("只支持2x2矩阵")

    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    det = a * d - b * c

    if det == 0:
        raise ValueError("矩阵不可逆")

    return [[d / det, -b / det], [-c / det, a / det]]


# ==================== 九、图像处理算法 ====================
def grayscale_conversion(image):
    """RGB转灰度图"""
    # 假设image是3D列表 [height][width][rgb]
    height, width = len(image), len(image[0])
    gray = [[0] * width for _ in range(height)]

    for i in range(height):
        for j in range(width):
            r, g, b = image[i][j]
            gray[i][j] = 0.299 * r + 0.587 * g + 0.114 * b  # 标准灰度公式

    return gray


def image_thresholding(image, threshold=128):
    """图像二值化"""
    height, width = len(image), len(image[0])
    binary = [[0] * width for _ in range(height)]

    for i in range(height):
        for j in range(width):
            binary[i][j] = 255 if image[i][j] >= threshold else 0

    return binary


def sobel_edge_detection(image):
    """Sobel边缘检测"""
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    grad_x = convolve2d(image, sobel_x)
    grad_y = convolve2d(image, sobel_y)

    height, width = len(image), len(image[0])
    magnitude = [[0] * width for _ in range(height)]

    for i in range(height):
        for j in range(width):
            magnitude[i][j] = math.sqrt(grad_x[i][j] ** 2 + grad_y[i][j] ** 2)

    return magnitude


# ==================== 十、机器学习基础 ====================
def euclidean_distance(point1, point2):
    """计算欧几里得距离"""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))


def manhattan_distance(point1, point2):
    """计算曼哈顿距离"""
    return sum(abs(x - y) for x, y in zip(point1, point2))


def k_nearest_neighbors(X_train, y_train, X_test, k=3):
    """K近邻算法实现"""
    predictions = []

    for test_point in X_test:
        # 计算所有训练样本的距离
        distances = []
        for i, train_point in enumerate(X_train):
            dist = euclidean_distance(test_point, train_point)
            distances.append((dist, y_train[i]))

        # 按距离排序并取前k个
        distances.sort(key=lambda x: x[0])
        k_nearest = [label for _, label in distances[:k]]

        # 多数投票
        prediction = max(set(k_nearest), key=k_nearest.count)
        predictions.append(prediction)

    return predictions


def kmeans_clustering(data, k=3, max_iterations=100):
    """K-means聚类算法"""
    # 随机初始化中心点
    centers = random.sample(data, k)

    for _ in range(max_iterations):
        # 分配点到最近的簇
        clusters = [[] for _ in range(k)]
        for point in data:
            distances = [euclidean_distance(point, center) for center in centers]
            cluster_idx = distances.index(min(distances))
            clusters[cluster_idx].append(point)

        # 更新中心点
        new_centers = []
        for cluster in clusters:
            if cluster:
                new_center = [sum(dim) / len(cluster) for dim in zip(*cluster)]
                new_centers.append(new_center)
            else:
                new_centers.append(random.choice(data))

        # 检查收敛
        if new_centers == centers:
            break

        centers = new_centers

    return centers, clusters


# ==================== 十一、特征处理 ====================
def pca(X, n_components=2):
    """主成分分析 (PCA)"""
    X = np.array(X)

    # 中心化
    X_centered = X - np.mean(X, axis=0)

    # 计算协方差矩阵
    cov_matrix = np.cov(X_centered.T)

    # 计算特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # 选择主成分
    idx = eigenvalues.argsort()[::-1]
    eigenvectors = eigenvectors[:, idx]
    components = eigenvectors[:, :n_components]

    # 投影到新空间
    X_pca = X_centered.dot(components)

    return X_pca.tolist()


def min_max_scaling(data):
    """最小最大标准化"""
    data = np.array(data)
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)

    # 避免除零
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1

    return ((data - min_vals) / range_vals).tolist()


# ==================== 十二、评价指标 ====================
def calculate_iou_single(box1, box2):
    """计算两个bounding box的IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0


def calculate_accuracy(y_true, y_pred):
    """计算准确率"""
    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return correct / len(y_true)


def calculate_precision_recall(y_true, y_pred, positive_class=1):
    """计算精确率和召回率"""
    tp = fp = fn = 0

    for true, pred in zip(y_true, y_pred):
        if true == positive_class and pred == positive_class:
            tp += 1
        elif true != positive_class and pred == positive_class:
            fp += 1
        elif true == positive_class and pred != positive_class:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    return precision, recall


# ==================== 十三、优化算法 ====================
def gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    """梯度下降算法"""
    m, n = len(X), len(X[0])
    theta = [0] * n  # 参数初始化
    cost_history = []

    for _ in range(iterations):
        predictions = [sum(theta[j] * X[i][j] for j in range(n)) for i in range(m)]
        errors = [predictions[i] - y[i] for i in range(m)]

        # 计算梯度
        gradients = [0] * n
        for j in range(n):
            gradients[j] = sum(errors[i] * X[i][j] for i in range(m)) / m

        # 更新参数
        theta = [theta[j] - learning_rate * gradients[j] for j in range(n)]

        # 计算损失
        cost = sum(error**2 for error in errors) / (2 * m)
        cost_history.append(cost)

    return theta, cost_history


# ==================== 十四、数据结构扩展 ====================
class PriorityQueue:
    """优先队列实现 (用于Dijkstra等算法)"""

    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))

    def pop(self):
        return heapq.heappop(self.heap)[1]

    def is_empty(self):
        return len(self.heap) == 0


def dijkstra_algorithm(graph, start):
    """Dijkstra最短路径算法"""
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    pq = PriorityQueue()
    pq.push(start, 0)

    while not pq.is_empty():
        current = pq.pop()

        for neighbor, weight in graph[current].items():
            distance = distances[current] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                pq.push(neighbor, distance)

    return distances


# ==================== 十五、测试新增函数 ====================
def test_additional_functions():
    """测试新增函数"""
    print("\n" + "=" * 60)
    print("测试新增的高级函数")
    print("=" * 60)

    # 测试矩阵操作
    print("\n=== 测试矩阵操作 ===")
    mat_a = [[1, 2], [3, 4]]
    mat_b = [[5, 6], [7, 8]]
    mat_product = matrix_multiply(mat_a, mat_b)
    print(f"矩阵乘法: {mat_a} × {mat_b} = {mat_product}")

    mat_inv = matrix_inverse_2x2(mat_a)
    print(f"矩阵求逆: inv({mat_a}) = {mat_inv}")

    # 测试图像处理
    print("\n=== 测试图像处理 ===")
    test_image = [[[100, 150, 200], [50, 100, 150]], [[200, 100, 50], [150, 200, 100]]]
    gray_image = grayscale_conversion(test_image)
    print(f"灰度转换: {gray_image}")

    # 测试机器学习算法
    print("\n=== 测试机器学习算法 ===")
    X_train = [[1, 2], [2, 3], [3, 4], [6, 7], [7, 8]]
    y_train = [0, 0, 0, 1, 1]
    X_test = [[2.5, 3.5], [6.5, 7.5]]
    knn_pred = k_nearest_neighbors(X_train, y_train, X_test, k=3)
    print(f"KNN预测: {knn_pred}")

    # 测试评价指标
    print("\n=== 测试评价指标 ===")
    y_true = [1, 0, 1, 1, 0, 1]
    y_pred = [1, 0, 0, 1, 1, 1]
    accuracy = calculate_accuracy(y_true, y_pred)
    precision, recall = calculate_precision_recall(y_true, y_pred)
    print(f"准确率: {accuracy:.3f}, 精确率: {precision:.3f}, 召回率: {recall:.3f}")

    # 测试图算法
    print("\n=== 测试图算法 ===")
    graph = {
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "C": 2, "D": 5},
        "C": {"A": 4, "B": 2, "D": 1},
        "D": {"B": 5, "C": 1},
    }
    distances = dijkstra_algorithm(graph, "A")
    print(f"Dijkstra最短路径: {distances}")


# ==================== 十六、树结构基础 ====================
class TreeNode:
    """二叉树节点定义"""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_sample_tree():
    """构建示例二叉树"""
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    return root


def preorder_traversal(root):
    """前序遍历：根->左->右"""
    result = []

    def dfs(node):
        if not node:
            return
        result.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


def inorder_traversal(root):
    """中序遍历：左->根->右"""
    result = []

    def dfs(node):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


def postorder_traversal(root):
    """后序遍历：左->右->根"""
    result = []

    def dfs(node):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        result.append(node.val)

    dfs(root)
    return result


def level_order_traversal(root):
    """层次遍历（BFS）"""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result


# ==================== 十七、图结构基础 ====================
class Graph:
    """图结构（邻接表表示）"""

    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2, weight=1, directed=False):
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        self.adjacency_list[vertex1].append((vertex2, weight))

        if not directed:
            self.adjacency_list[vertex2].append((vertex1, weight))

    def dfs(self, start_vertex):
        """深度优先搜索"""
        visited = set()
        result = []

        def dfs_recursive(vertex):
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                for neighbor, _ in self.adjacency_list[vertex]:
                    dfs_recursive(neighbor)

        dfs_recursive(start_vertex)
        return result

    def bfs(self, start_vertex):
        """广度优先搜索"""
        visited = set()
        result = []
        queue = deque([start_vertex])
        visited.add(start_vertex)

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor, _ in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result


# ==================== 十八、CV基本概念实现 ====================
def rgb_to_hsv(r, g, b):
    """RGB转HSV颜色空间"""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    # 计算Hue
    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)

    # 计算Saturation
    s = 0 if cmax == 0 else delta / cmax

    # 计算Value
    v = cmax

    return h, s, v


def hsv_to_rgb(h, s, v):
    """HSV转RGB颜色空间"""
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


def image_resize(image, new_width, new_height):
    """图像缩放（最近邻插值）"""
    height, width = len(image), len(image[0])
    resized = [[0] * new_width for _ in range(new_height)]

    for i in range(new_height):
        for j in range(new_width):
            # 计算原图对应位置
            src_i = int(i * height / new_height)
            src_j = int(j * width / new_width)
            resized[i][j] = image[src_i][src_j]

    return resized


def bilinear_interpolation(image, x, y):
    """双线性插值"""
    height, width = len(image), len(image[0])

    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, width - 1), min(y1 + 1, height - 1)

    # 四个相邻像素
    q11 = image[y1][x1]
    q12 = image[y1][x2]
    q21 = image[y2][x1]
    q22 = image[y2][x2]

    # 插值计算
    dx = x - x1
    dy = y - y1

    value = (
        q11 * (1 - dx) * (1 - dy)
        + q21 * dx * (1 - dy)
        + q12 * (1 - dx) * dy
        + q22 * dx * dy
    )

    return value


def histogram_equalization(image):
    """直方图均衡化"""
    height, width = len(image), len(image[0])

    # 计算直方图
    hist = [0] * 256
    for i in range(height):
        for j in range(width):
            hist[image[i][j]] += 1

    # 计算累积分布函数
    cdf = [0] * 256
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + hist[i]

    # 归一化CDF
    cdf_min = min(cdf)
    total_pixels = height * width
    cdf_normalized = [
        round((cdf[i] - cdf_min) * 255 / (total_pixels - cdf_min)) for i in range(256)
    ]

    # 应用变换
    equalized = [[0] * width for _ in range(height)]
    for i in range(height):
        for j in range(width):
            equalized[i][j] = cdf_normalized[image[i][j]]

    return equalized


# ==================== 十九、特征提取 ====================
def extract_hog_features(image, cell_size=8, block_size=2, bins=9):
    """HOG特征提取简化版"""
    height, width = len(image), len(image[0])

    # 计算梯度
    grad_x = [[0] * width for _ in range(height)]
    grad_y = [[0] * width for _ in range(height)]
    magnitude = [[0] * width for _ in range(height)]
    orientation = [[0] * width for _ in range(height)]

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            grad_x[i][j] = image[i][j + 1] - image[i][j - 1]
            grad_y[i][j] = image[i + 1][j] - image[i - 1][j]
            magnitude[i][j] = math.sqrt(grad_x[i][j] ** 2 + grad_y[i][j] ** 2)
            orientation[i][j] = math.atan2(grad_y[i][j], grad_x[i][j]) * 180 / math.pi

    # 计算细胞单元的HOG
    hog_features = []
    for i in range(0, height - cell_size + 1, cell_size):
        for j in range(0, width - cell_size + 1, cell_size):
            cell_hist = [0] * bins

            for y in range(cell_size):
                for x in range(cell_size):
                    idx_i, idx_j = i + y, j + x
                    if 0 <= idx_i < height and 0 <= idx_j < width:
                        angle = orientation[idx_i][idx_j] % 180
                        bin_idx = int(angle / (180 / bins)) % bins
                        cell_hist[bin_idx] += magnitude[idx_i][idx_j]

            # 归一化
            hist_sum = sum(cell_hist)
            if hist_sum > 0:
                cell_hist = [val / hist_sum for val in cell_hist]

            hog_features.extend(cell_hist)

    return hog_features


# ==================== 二十、测试新增基础内容 ====================
def test_basic_structures():
    """测试树、图和CV基础概念"""
    print("\n" + "=" * 60)
    print("测试树、图和CV基础概念")
    print("=" * 60)

    # 测试树结构
    print("\n=== 测试树结构 ===")
    tree_root = build_sample_tree()
    print(f"前序遍历: {preorder_traversal(tree_root)}")
    print(f"中序遍历: {inorder_traversal(tree_root)}")
    print(f"后序遍历: {postorder_traversal(tree_root)}")
    print(f"层次遍历: {level_order_traversal(tree_root)}")

    # 测试图结构
    print("\n=== 测试图结构 ===")
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    print(f"DFS遍历: {graph.dfs('A')}")
    print(f"BFS遍历: {graph.bfs('A')}")

    # 测试颜色空间转换
    print("\n=== 测试颜色空间转换 ===")
    r, g, b = 255, 128, 64
    h, s, v = rgb_to_hsv(r, g, b)
    r_back, g_back, b_back = hsv_to_rgb(h, s, v)
    print(
        f"RGB({r},{g},{b}) -> HSV({h:.1f},{s:.2f},{v:.2f}) -> RGB({r_back},{g_back},{b_back})"
    )

    # 测试图像处理
    print("\n=== 测试图像处理 ===")
    test_img = [[100, 150, 200], [50, 100, 150], [25, 75, 125]]
    resized = image_resize(test_img, 2, 2)
    print(f"原图: {test_img}")
    print(f"缩放后: {resized}")

    # 测试直方图均衡化
    print("\n=== 测试直方图均衡化 ===")
    small_img = [[50, 100], [150, 200]]
    equalized = histogram_equalization(small_img)
    print(f"原图: {small_img}")
    print(f"均衡化后: {equalized}")

    # 测试HOG特征
    print("\n=== 测试HOG特征 ===")
    grad_img = [[100, 120, 140], [80, 100, 120], [60, 80, 100]]
    hog_features = extract_hog_features(grad_img)
    print(f"HOG特征长度: {len(hog_features)}")
    print(f"前10个特征: {hog_features[:10]}")


# ==================== 二十一、CV基础概念解释 ====================
def explain_cv_concepts():
    """CV基础概念解释"""
    print("\n" + "=" * 60)
    print("CV基础概念解释")
    print("=" * 60)

    concepts = {
        "卷积 (Convolution)": "使用卷积核在图像上滑动计算加权和，用于特征提取",
        "池化 (Pooling)": "降采样操作，减少计算量同时保持特征不变性",
        "激活函数 (Activation Function)": "引入非线性，如ReLU、Sigmoid、Tanh",
        "损失函数 (Loss Function)": "衡量预测值与真实值的差异，如交叉熵、MSE",
        "优化器 (Optimizer)": "更新网络参数的方法，如SGD、Adam",
        "过拟合 (Overfitting)": "模型在训练集表现好但泛化能力差",
        "数据增强 (Data Augmentation)": "通过对训练数据进行变换来增加数据多样性",
        "迁移学习 (Transfer Learning)": "使用预训练模型在新任务上进行微调",
        "目标检测 (Object Detection)": "识别图像中的物体并定位其位置",
        "语义分割 (Semantic Segmentation)": "对图像中每个像素进行分类",
        "实例分割 (Instance Segmentation)": "区分不同实例的语义分割",
        "特征金字塔 (Feature Pyramid Network)": "处理多尺度目标检测的网络结构",
    }

    for concept, explanation in concepts.items():
        print(f"{concept}: {explanation}")


# ==================== 二十二、机器学习常见函数 ====================
def linear_regression(X, y, learning_rate=0.01, epochs=1000):
    """线性回归（梯度下降）"""
    m, n = len(X), len(X[0])
    theta = [0] * n
    for epoch in range(epochs):
        predictions = [sum(theta[j] * X[i][j] for j in range(n)) for i in range(m)]
        errors = [predictions[i] - y[i] for i in range(m)]
        gradients = [sum(errors[i] * X[i][j] for i in range(m)) / m for j in range(n)]
        theta = [theta[j] - learning_rate * gradients[j] for j in range(n)]
    return theta


def logistic_regression(X, y, learning_rate=0.1, epochs=1000):
    """逻辑回归"""
    m, n = len(X), len(X[0])
    w = [0] * n
    for epoch in range(epochs):
        z = [sum(w[j] * X[i][j] for j in range(n)) for i in range(m)]
        predictions = [1 / (1 + math.exp(-zi)) for zi in z]
        errors = [predictions[i] - y[i] for i in range(m)]
        gradients = [sum(errors[i] * X[i][j] for i in range(m)) / m for j in range(n)]
        w = [w[j] - learning_rate * gradients[j] for j in range(n)]
    return w


def softmax(x):
    """Softmax函数"""
    exp_x = [math.exp(xi - max(x)) for xi in x]  # 数值稳定性
    sum_exp = sum(exp_x)
    return [xi / sum_exp for xi in exp_x]


def cross_entropy_loss(y_true, y_pred):
    """交叉熵损失"""
    return -sum(y_true[i] * math.log(y_pred[i] + 1e-8) for i in range(len(y_true)))


def kmeans_plus_plus_init(data, k):
    """K-means++初始化"""
    centers = [random.choice(data)]
    for _ in range(1, k):
        distances = [
            min(euclidean_distance(point, center) for center in centers)
            for point in data
        ]
        probabilities = [d / sum(distances) for d in distances]
        centers.append(random.choices(data, weights=probabilities)[0])
    return centers


# ==================== 二十三、深度学习常见函数 ====================
class SimpleNeuralNetwork:
    """简单神经网络"""

    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros(hidden_size)
        self.w2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros(output_size)

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return (x > 0).astype(float)

    def forward(self, X):
        self.z1 = np.dot(X, self.w1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.a2 = softmax(self.z2)
        return self.a2

    def backward(self, X, y, output, learning_rate=0.01):
        m = len(X)
        dz2 = output - y
        dw2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0) / m

        dz1 = np.dot(dz2, self.w2.T) * self.relu_derivative(self.z1)
        dw1 = np.dot(X.T, dz1) / m
        db1 = np.sum(dz1, axis=0) / m

        # 参数更新
        self.w2 -= learning_rate * dw2
        self.b2 -= learning_rate * db2
        self.w1 -= learning_rate * dw1
        self.b1 -= learning_rate * db1


def convolutional_layer(input, kernel):
    """卷积层前向传播"""
    input_height, input_width = input.shape
    kernel_height, kernel_width = kernel.shape
    output_height = input_height - kernel_height + 1
    output_width = input_width - kernel_width + 1
    output = np.zeros((output_height, output_width))

    for i in range(output_height):
        for j in range(output_width):
            output[i, j] = np.sum(
                input[i : i + kernel_height, j : j + kernel_width] * kernel
            )
    return output


def max_pooling(input, pool_size=2):
    """最大池化层"""
    height, width = input.shape
    output = np.zeros((height // pool_size, width // pool_size))

    for i in range(0, height, pool_size):
        for j in range(0, width, pool_size):
            output[i // pool_size, j // pool_size] = np.max(
                input[i : i + pool_size, j : j + pool_size]
            )
    return output


def batch_normalization(x, gamma=1, beta=0, eps=1e-5):
    """批归一化"""
    mean = np.mean(x, axis=0)
    var = np.var(x, axis=0)
    x_normalized = (x - mean) / np.sqrt(var + eps)
    return gamma * x_normalized + beta


def dropout(x, dropout_rate=0.5, training=True):
    """Dropout层"""
    if training:
        mask = np.random.binomial(1, 1 - dropout_rate, size=x.shape) / (
            1 - dropout_rate
        )
        return x * mask
    return x


# ==================== 二十四、优化器实现 ====================
def sgd_optimizer(params, grads, learning_rate):
    """SGD优化器"""
    return [param - learning_rate * grad for param, grad in zip(params, grads)]


def momentum_optimizer(params, grads, velocity, learning_rate, momentum=0.9):
    """动量优化器"""
    velocity = [momentum * v + learning_rate * g for v, g in zip(velocity, grads)]
    return [param - v for param, v in zip(params, velocity)], velocity


def adam_optimizer(
    params, grads, m, v, t, learning_rate=0.001, beta1=0.9, beta2=0.999, eps=1e-8
):
    """Adam优化器"""
    m = [beta1 * m_i + (1 - beta1) * g for m_i, g in zip(m, grads)]
    v = [beta2 * v_i + (1 - beta2) * g**2 for v_i, g in zip(v, grads)]

    m_hat = [m_i / (1 - beta1**t) for m_i in m]
    v_hat = [v_i / (1 - beta2**t) for v_i in v]

    new_params = [
        param - learning_rate * m_hat_i / (np.sqrt(v_hat_i) + eps)
        for param, m_hat_i, v_hat_i in zip(params, m_hat, v_hat)
    ]

    return new_params, m, v


# ==================== 二十五、损失函数 ====================
def mean_squared_error(y_true, y_pred):
    """均方误差损失"""
    return np.mean((np.array(y_true) - np.array(y_pred)) ** 2)


def binary_cross_entropy(y_true, y_pred):
    """二分类交叉熵"""
    y_pred = np.clip(y_pred, 1e-8, 1 - 1e-8)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))


def categorical_cross_entropy(y_true, y_pred):
    """多分类交叉熵"""
    y_pred = np.clip(y_pred, 1e-8, 1 - 1e-8)
    return -np.sum(y_true * np.log(y_pred))


def hinge_loss(y_true, y_pred):
    """合页损失（SVM）"""
    return np.maximum(0, 1 - y_true * y_pred)


# ==================== 二十六、评估指标 ====================
def confusion_matrix(y_true, y_pred, num_classes):
    """混淆矩阵"""
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for true, pred in zip(y_true, y_pred):
        cm[true][pred] += 1
    return cm


def f1_score(y_true, y_pred):
    """F1分数"""
    tp = np.sum((np.array(y_true) == 1) & (np.array(y_pred) == 1))
    fp = np.sum((np.array(y_true) == 0) & (np.array(y_pred) == 1))
    fn = np.sum((np.array(y_true) == 1) & (np.array(y_pred) == 0))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (
        2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    )

    return f1


def roc_auc_score(y_true, y_scores):
    """ROC-AUC分数"""
    # 排序并计算TPR和FPR
    sorted_indices = np.argsort(y_scores)[::-1]
    y_true_sorted = np.array(y_true)[sorted_indices]

    tpr, fpr = [], []
    for threshold in np.unique(y_scores):
        y_pred = (y_scores >= threshold).astype(int)
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        tpr.append(tp / np.sum(y_true == 1))
        fpr.append(fp / np.sum(y_true == 0))

    # 计算AUC（梯形法则）
    auc = np.trapz(tpr, fpr)
    return auc


# ==================== 二十七、正则化技术 ====================
def l1_regularization(params, lambda_val=0.01):
    """L1正则化"""
    return lambda_val * sum(np.abs(param) for param in params)


def l2_regularization(params, lambda_val=0.01):
    """L2正则化"""
    return lambda_val * sum(np.sum(param**2) for param in params)


def early_stopping(val_losses, patience=5):
    """早停法"""
    if len(val_losses) < patience + 1:
        return False
    return all(val_losses[-1] >= val_losses[-i - 2] for i in range(patience))


# ==================== 二十八、测试机器学习函数 ====================
def test_ml_dl_functions():
    """测试机器学习和深度学习函数"""
    print("\n" + "=" * 60)
    print("测试机器学习和深度学习函数")
    print("=" * 60)

    # 测试基础函数
    print("Softmax:", softmax([1.0, 2.0, 3.0]))
    print("Cross Entropy:", cross_entropy_loss([1, 0, 0], [0.7, 0.2, 0.1]))

    # 测试优化器
    params = [np.array([1.0, 2.0]), np.array([3.0, 4.0])]
    grads = [np.array([0.1, -0.2]), np.array([-0.1, 0.3])]
    updated = sgd_optimizer(params, grads, 0.1)
    print("SGD更新:", updated)

    # 测试损失函数
    print("MSE:", mean_squared_error([1, 2, 3], [1.1, 1.9, 3.2]))

    # 测试评估指标
    y_true = [0, 1, 0, 1, 1]
    y_pred = [0, 1, 1, 1, 0]
    cm = confusion_matrix(y_true, y_pred, 2)
    print("混淆矩阵:\n", cm)
    print("F1分数:", f1_score(y_true, y_pred))


# ==================== 机器学习库 (scikit-learn) ====================
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

X_train = np.array([[1, 2], [3, 4], [5, 6]])
y_train = np.array([1, 2, 3])
X_test = np.array([[7, 8], [9, 10], [11, 12]])
y_test = np.array([4, 5, 6])
X = np.vstack((X_train, X_test))
y = np.hstack((y_train, y_test))
y_true = [0, 1, 0, 1, 1]
y_pred = [0, 1, 1, 1, 0]
# 线性回归
lr = LinearRegression()
lr.fit(X_train, y_train)
predictions = lr.predict(X_test)

# 逻辑回归
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
probs = log_reg.predict_proba(X_test)

# K-means聚类
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# PCA降维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 训练测试分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 评估指标
accuracy = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
conf_matrix = confusion_matrix(y_true, y_pred)

# ==================== PyTorch 深度学习库 ====================
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, TensorDataset


# 定义神经网络
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


# 损失函数
criterion = nn.CrossEntropyLoss()  # 交叉熵损失
mse_loss = nn.MSELoss()  # 均方误差
bce_loss = nn.BCELoss()  # 二分类交叉熵

# 优化器
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam优化器
sgd_optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)  # SGD带动量

# 数据加载
dataset = TensorDataset(X_tensor, y_tensor)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 训练循环
model.train()
for epoch in range(epochs):
    for batch_idx, (data, target) in enumerate(dataloader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

# 模型评估
model.eval()
with torch.no_grad():
    output = model(test_data)
    pred = output.argmax(dim=1)

# ==================== TensorFlow/Keras 深度学习库 ====================
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dropout,
    BatchNormalization,
)
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.losses import (
    BinaryCrossentropy,
    CategoricalCrossentropy,
    MeanSquaredError,
)
from tensorflow.keras.metrics import Accuracy, Precision, Recall, AUC
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# 序列模型定义
model = Sequential(
    [
        Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        BatchNormalization(),
        Flatten(),
        Dense(128, activation="relu"),
        Dropout(0.5),
        Dense(10, activation="softmax"),
    ]
)

# 编译模型
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss=CategoricalCrossentropy(),
    metrics=["accuracy", Precision(), Recall()],
)

# 回调函数
callbacks = [
    EarlyStopping(patience=5, restore_best_weights=True),
    ModelCheckpoint("best_model.h5", save_best_only=True),
    ReduceLROnPlateau(factor=0.5, patience=3),
]

# 训练模型
history = model.fit(
    X_train,
    y_train,
    batch_size=32,
    epochs=50,
    validation_data=(X_test, y_test),
    callbacks=callbacks,
)

# 数据预处理
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
)

# ==================== 计算机视觉专用函数 ====================
import torchvision.transforms as transforms
import torchvision.models as models
from torchvision.datasets import CIFAR10, ImageFolder

# 图像预处理
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# 预训练模型
resnet = models.resnet50(pretrained=True)
vgg = models.vgg16(pretrained=True)
alexnet = models.alexnet(pretrained=True)

# 迁移学习（冻结层）
for param in resnet.parameters():
    param.requires_grad = False
resnet.fc = nn.Linear(resnet.fc.in_features, 10)  # 修改最后一层

# ==================== 自然语言处理函数 ====================
from transformers import AutoTokenizer, AutoModel, pipeline
from torchtext.data import Field, BucketIterator
from transformers import BertTokenizer, BertModel

# Hugging Face Transformers
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# 文本分类pipeline
classifier = pipeline("sentiment-analysis")

# ==================== 模型部署和保存 ====================
# PyTorch模型保存
torch.save(model.state_dict(), "model.pth")
model.load_state_dict(torch.load("model.pth"))

# TensorFlow模型保存
model.save("my_model.h5")
loaded_model = keras.models.load_model("my_model.h5")

# ONNX格式导出
torch.onnx.export(model, dummy_input, "model.onnx")

# ==================== 高级优化技巧 ====================
# 学习率调度器
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)

# 梯度裁剪
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# 混合精度训练
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

# ==================== 分布式训练 ====================
# 数据并行
model = nn.DataParallel(model)

# DistributedDataParallel
model = nn.parallel.DistributedDataParallel(model)

# ==================== 常用工具函数 ====================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, roc_curve, precision_recall_curve

# 可视化训练过程
plt.plot(history.history["loss"], label="train_loss")
plt.plot(history.history["val_loss"], label="val_loss")
plt.legend()

# 分类报告
print(classification_report(y_true, y_pred))

# ROC曲线
fpr, tpr, _ = roc_curve(y_true, y_scores)
plt.plot(fpr, tpr)


# ==================== 实际使用示例 ====================
def sklearn_example():
    """scikit-learn完整示例"""
    from sklearn.datasets import load_iris
    from sklearn.pipeline import Pipeline

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target

    # 创建管道
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=2)),
            ("classifier", RandomForestClassifier(n_estimators=100)),
        ]
    )

    # 训练评估
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)
    return score


def pytorch_example():
    """PyTorch完整示例"""
    # 假设已有数据
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    model = SimpleNN()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    # 训练
    for epoch in range(10):
        for data, target in train_loader:
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

    return model


def tensorflow_example():
    """TensorFlow完整示例"""
    model = Sequential(
        [
            Dense(64, activation="relu", input_shape=(10,)),
            Dropout(0.2),
            Dense(32, activation="relu"),
            Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    history = model.fit(
        X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1
    )

    return model, history


# ==================== 主程序 ====================
if __name__ == "__main__":
    # 运行所有测试
    test_all_functions()

    # 额外示例：创建和显示测试矩阵
    print("\n" + "=" * 50)
    print("额外示例：矩阵操作")

    test_mat = create_test_matrix(3, 4)
    print_matrix(test_mat, "3x4测试矩阵")

    # 演示更多numpy操作
    print("Numpy高级操作演示:")
    arr = np.array(test_mat)
    print(f"矩阵形状: {arr.shape}")
    print(f"矩阵总和: {np.sum(arr)}")
    print(f"每列均值: {np.mean(arr, axis=0)}")
    print(f"每行最大值: {np.max(arr, axis=1)}")

    print("\n所有测试完成！祝你笔试顺利！")

    # 运行新增函数测试
    test_additional_functions()

    print("\n" + "=" * 60)
    print("所有测试完成！包含以下重要内容：")
    print("1. 基础矩阵操作 (转置、乘法、求逆)")
    print("2. 图像处理算法 (灰度化、二值化、边缘检测)")
    print("3. 机器学习基础 (KNN、K-means、PCA)")
    print("4. 评价指标 (准确率、精确率、召回率、IoU)")
    print("5. 优化算法 (梯度下降)")
    print("6. 图算法 (Dijkstra最短路径)")
    print("=" * 60)
    print("\n祝你笔试取得优异成绩！")

    # 运行基础结构测试
    test_basic_structures()

    # 解释CV概念
    explain_cv_concepts()

    print("\n" + "=" * 80)
    print("完整内容总结：")
    print("基础数据结构和算法")
    print("树结构遍历（前序、中序、后序、层次）")
    print("图结构遍历（DFS、BFS）")
    print("颜色空间转换（RGB-HSV）")
    print("图像处理（缩放、插值、直方图均衡化）")
    print("特征提取（HOG）")
    print("CV基础概念解释")
    print("=" * 80)
    print("\n现在你已经掌握了CV笔试所需的所有核心内容！加油！")
