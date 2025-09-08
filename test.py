import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import matplotlib.font_manager as fm

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class KMeans:
    def __init__(self, n_clusters=3, max_iter=300, tol=1e-4, random_state=None):
        """
        初始化K-Means聚类算法

        参数:
        n_clusters (int): 聚类数量，即要分成的簇的个数
        max_iter (int): 最大迭代次数，防止算法无限循环
        tol (float): 收敛阈值，当质心移动距离小于此值时停止迭代
        random_state (int): 随机种子，用于确保结果可重现
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids = None  # 存储最终的质心坐标
        self.labels = None  # 存储每个样本点的簇标签
        self.inertia_ = None  # 存储平方误差和（SSE），用于评估聚类效果

    def _initialize_centroids(self, X):
        """
        初始化质心 - 随机选择数据点作为初始质心

        参数:
        X (numpy.ndarray): 输入数据，形状为 (n_samples, n_features)

        返回:
        numpy.ndarray: 初始质心坐标
        """
        np.random.seed(self.random_state)  # 设置随机种子确保可重现性
        # 从数据中随机选择n_clusters个不重复的索引
        random_indices = np.random.choice(len(X), self.n_clusters, replace=False)
        return X[random_indices]  # 返回选中的数据点作为初始质心

    def _assign_clusters(self, X, centroids):
        """
        将每个数据点分配到最近的质心（E步：期望步）

        参数:
        X (numpy.ndarray): 输入数据
        centroids (numpy.ndarray): 当前质心坐标

        返回:
        numpy.ndarray: 每个样本点所属的簇标签
        """
        # 计算每个点到所有质心的欧几里得距离
        # X[:, np.newaxis] 将X从(n, d)变为(n, 1, d)，便于广播计算
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        # 找到每个点的最近质心索引，即分配簇标签
        return np.argmin(distances, axis=1)

    def _update_centroids(self, X, labels):
        """
        更新质心为每个簇的均值（M步：最大化步）

        参数:
        X (numpy.ndarray): 输入数据
        labels (numpy.ndarray): 当前簇标签

        返回:
        numpy.ndarray: 更新后的质心坐标
        """
        new_centroids = np.zeros((self.n_clusters, X.shape[1]))  # 初始化新质心数组
        for i in range(self.n_clusters):
            # 获取属于当前簇i的所有数据点
            cluster_points = X[labels == i]
            if len(cluster_points) > 0:
                # 计算簇内所有点的均值作为新质心
                new_centroids[i] = cluster_points.mean(axis=0)
            else:
                # 如果簇为空（没有数据点被分配到此簇），重新随机初始化该质心
                new_centroids[i] = X[np.random.randint(len(X))]
        return new_centroids

    def _calculate_inertia(self, X, labels, centroids):
        """
        计算平方误差和（inertia），即所有点到其所属质心距离的平方和

        参数:
        X (numpy.ndarray): 输入数据
        labels (numpy.ndarray): 簇标签
        centroids (numpy.ndarray): 质心坐标

        返回:
        float: 平方误差和
        """
        inertia = 0
        for i in range(self.n_clusters):
            cluster_points = X[labels == i]  # 获取簇i的所有点
            if len(cluster_points) > 0:
                # 计算簇内所有点到质心距离的平方和
                inertia += np.sum((cluster_points - centroids[i]) ** 2)
        return inertia

    def fit(self, X):
        """
        训练K-Means模型

        参数:
        X (numpy.ndarray): 输入数据，形状为 (n_samples, n_features)

        返回:
        self: 返回训练好的模型实例
        """
        # 初始化质心
        self.centroids = self._initialize_centroids(X)

        # 开始迭代训练
        for iteration in range(self.max_iter):
            # 保存旧的质心坐标，用于收敛判断
            old_centroids = self.centroids.copy()

            # E步：将每个点分配到最近的质心
            self.labels = self._assign_clusters(X, self.centroids)

            # M步：重新计算每个簇的质心
            self.centroids = self._update_centroids(X, self.labels)

            # 计算当前的平方误差和
            self.inertia_ = self._calculate_inertia(X, self.labels, self.centroids)

            # 检查收敛条件：计算质心移动的最大距离
            centroid_shift = np.linalg.norm(self.centroids - old_centroids)
            if centroid_shift < self.tol:
                print(f"算法收敛于第 {iteration + 1} 次迭代")
                break

        return self

    def predict(self, X):
        """
        预测新数据的簇标签

        参数:
        X (numpy.ndarray): 新数据

        返回:
        numpy.ndarray: 预测的簇标签
        """
        if self.centroids is None:
            raise ValueError("请先调用 fit() 方法训练模型")
        return self._assign_clusters(X, self.centroids)

    def fit_predict(self, X):
        """
        训练模型并返回预测标签（便捷方法）

        参数:
        X (numpy.ndarray): 输入数据

        返回:
        numpy.ndarray: 簇标签
        """
        self.fit(X)
        return self.labels


# 测试手写的K-Means算法
def test_kmeans():
    """
    测试手写K-Means算法并与sklearn版本进行比较
    """
    # 生成测试数据：300个样本，3个中心点，标准差0.6的二维数据
    X, y_true = make_blobs(n_samples=300, centers=3, cluster_std=0.60,
                           random_state=0, n_features=2)

    # 使用手写的K-Means算法
    print("正在运行手写K-Means算法...")
    kmeans = KMeans(n_clusters=3, random_state=42, max_iter=100)
    labels = kmeans.fit_predict(X)
    centroids = kmeans.centroids

    # 使用sklearn的K-Means进行比较（作为基准）
    print("正在运行sklearn K-Means算法...")
    from sklearn.cluster import KMeans as SKKMeans
    sk_kmeans = SKKMeans(n_clusters=3, random_state=42, max_iter=100, n_init=10)
    sk_labels = sk_kmeans.fit_predict(X)
    sk_centroids = sk_kmeans.cluster_centers_

    # 绘制结果对比图
    plt.figure(figsize=(15, 5))

    # 子图1：原始数据（真实标签）
    plt.subplot(1, 3, 1)
    plt.scatter(X[:, 0], X[:, 1], s=50, c=y_true, cmap='viridis', alpha=0.7)
    plt.title("原始数据 (真实标签)")
    plt.xlabel("特征 1")
    plt.ylabel("特征 2")
    plt.grid(True, alpha=0.3)

    # 子图2：手写K-Means结果
    plt.subplot(1, 3, 2)
    plt.scatter(X[:, 0], X[:, 1], s=50, c=labels, cmap='viridis', alpha=0.7)
    plt.scatter(centroids[:, 0], centroids[:, 1], s=200, c='red',
                marker='X', label='质心', edgecolors='black')
    plt.title("手写K-Means聚类结果")
    plt.xlabel("特征 1")
    plt.ylabel("特征 2")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 子图3：sklearn K-Means结果
    plt.subplot(1, 3, 3)
    plt.scatter(X[:, 0], X[:, 1], s=50, c=sk_labels, cmap='viridis', alpha=0.7)
    plt.scatter(sk_centroids[:, 0], sk_centroids[:, 1], s=200, c='red',
                marker='X', label='质心', edgecolors='black')
    plt.title("sklearn K-Means聚类结果")
    plt.xlabel("特征 1")
    plt.ylabel("特征 2")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # 打印比较结果
    print("\n=== 算法比较结果 ===")
    print(f"手写K-Means的 inertia (平方误差和): {kmeans.inertia_:.4f}")
    print(f"sklearn K-Means的 inertia: {sk_kmeans.inertia_:.4f}")
    print(f"两种算法的inertia差异: {abs(kmeans.inertia_ - sk_kmeans.inertia_):.6f}")

    # 比较质心位置（允许一定的误差）
    centroid_similar = np.allclose(centroids, sk_centroids, atol=0.5)
    print(f"质心位置是否相似 (容差0.5): {centroid_similar}")

    if not centroid_similar:
        print("注意：质心位置有差异，这可能是由于初始质心选择不同导致的")
        print("手写算法质心:\n", centroids)
        print("sklearn算法质心:\n", sk_centroids)

    return kmeans, sk_kmeans


# K-Means的进阶功能：肘部法则确定最佳K值
def find_optimal_k(X, max_k=10):
    """
    使用肘部法则寻找最佳聚类数量K

    参数:
    X (numpy.ndarray): 输入数据
    max_k (int): 最大尝试的K值

    返回:
    list: 每个K值对应的inertia列表
    """
    print(f"\n正在使用肘部法则寻找最佳K值 (1-{max_k})...")
    inertias = []
    k_values = range(1, max_k + 1)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
        print(f"K={k}, inertia={kmeans.inertia_:.2f}")

    # 绘制肘部图
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, inertias, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('聚类数量 K')
    plt.ylabel('平方误差和 (Inertia)')
    plt.title('肘部法则 - 寻找最佳K值')
    plt.grid(True, alpha=0.3)
    plt.xticks(k_values)
    plt.show()

    # 寻找肘部点（简单实现：计算二阶导数最大的点）
    differences = np.diff(inertias)
    second_derivatives = np.diff(differences)
    elbow_point = np.argmin(second_derivatives) + 2  # +2 因为二阶导数少两个点

    print(f"建议的最佳K值（肘部点）: {elbow_point}")

    return inertias


# 主程序入口
if __name__ == "__main__":
    print("开始测试手写K-Means聚类算法")
    print("=" * 50)

    # 生成测试数据
    X, _ = make_blobs(n_samples=500, centers=4, cluster_std=0.8, random_state=42)

    # 测试算法
    my_kmeans, sk_kmeans = test_kmeans()

    # 使用肘部法则
    inertias = find_optimal_k(X, max_k=10)

    print("\n测试完成！")