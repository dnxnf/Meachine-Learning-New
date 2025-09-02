# 有一幅以 m x n 的二维整数数组表示的图画 Image ，其中 Image[i][j] 表示该图画的像素值大小。你也被给予三个整数 sr , sc 和
# color 。你应该从像素 Image[sr][sc] 开始对图像进行上色 填充 。
# 
#  为了完成 上色工作： 
# 
#  
#  从初始像素开始，将其颜色改为 color。 
#  对初始坐标的 上下左右四个方向上 相邻且与初始像素的原始颜色同色的像素点执行相同操作。 
#  通过检查与初始像素的原始颜色相同的相邻像素并修改其颜色来继续 重复 此过程。 
#  当 没有 其它原始颜色的相邻像素时 停止 操作。 
#  
# 
#  最后返回经过上色渲染 修改 后的图像 。 
# 
#  
# 
#  示例 1: 
# 
#  
# 
#  
#  输入：Image = [[1,1,1],[1,1,0],[1,0,1]]，sr = 1, sc = 1, color = 2
#  
# 
#  
#  输出：[[2,2,2],[2,2,0],[2,0,1]]
#  
# 
#  
#  解释：在图像的正中间，坐标 
#  (sr,sc)=(1,1) （即红色像素）,在路径上所有符合条件的像素点的颜色都被更改成相同的新颜色（即蓝色像素）。
#  
# 
#  
#  注意，右下角的像素 
#  没有 更改为2，因为它不是在上下左右四个方向上与初始点相连的像素点。
#  
# 
#  
#  
#  
# 
#  示例 2: 
# 
#  
#  输入：Image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0
#  
# 
#  
#  输出：[[0,0,0],[0,0,0]]
#  
# 
#  
#  解释：初始像素已经用 0 着色，这与目标颜色相同。因此，不会对图像进行任何更改。
#  
# 
#  
# 
#  提示: 
# 
#  
#  m == Image.length
#  n == Image[i].length
#  1 <= m, n <= 50 
#  0 <= Image[i][j], color < 2¹⁶
#  0 <= sr < m 
#  0 <= sc < n 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 数组 矩阵 👍 527 👎 0

from typing import List, Optional

# favour 经典的深搜和广搜思路 dfs,bfs
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def floodFill1(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        # bfs
        if color == image[sr][sc]:
            return image
        m, n = len(image), len(image[0])
        col = image[sr][sc]
        dict = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        q = [(sr, sc)]
        # 广搜，使用队列，遍历上下左右
        while q:
            i, j = q.pop(0)
            image[i][j] = color
            for direct in dict:
                newi = i + direct[0]
                newj = j + direct[1]
                if 0 <= newi < m and 0 <= newj < n and image[newi][newj] == col:
                    q.append((newi, newj))
        return image

    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        if color == image[sr][sc]:
            return image
        m, n = len(image), len(image[0])
        col = image[sr][sc]

        #         深搜，遇到一个就继续搜上下左右继续搜
        def dfs(i, j):
            # 越界或者循环完了就return,递归结束条件
            if i < 0 or i >= m or j < 0 or j >= n or image[i][j] != col:
                return
            #
            image[i][j] = color
            dfs(i + 1, j)
            dfs(i - 1, j)
            dfs(i, j + 1)
            dfs(i, j - 1)

        dfs(sr, sc)
        return image


# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
