# m*n 的二维数组 plants 记录了园林景观的植物排布情况，具有以下特性： 
# 
#  
#  每行中，每棵植物的右侧相邻植物不矮于该植物； 
#  每列中，每棵植物的下侧相邻植物不矮于该植物。 
#  
# 
#  
# 
#  请判断 plants 中是否存在目标高度值 target。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：plants = [[2,3,6,8],[4,5,8,9],[5,9,10,12]], target = 8
# 
# 输出：true
#  
# 
#  
# 
#  示例 2： 
# 
#  
# 输入：plants = [[1,3,5],[2,5,7]], target = 4
# 
# 输出：false
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= n <= 1000 
#  0 <= m <= 1000 
#  
# 
#  注意：本题与主站 240 题相同：https://leetcode-cn.com/problems/search-a-2d-matrix-ii/ 
# 
#  
# 
#  Related Topics 数组 二分查找 分治 矩阵 👍 1037 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findTargetIn2DPlants(self, plants: List[List[int]], target: int) -> bool:
        for i in range(len(plants)):
            for j in range(len(plants[0])):
                if plants[i][j] == target:
                    return True
                if j > 0 and plants[i][j] > plants[i][j-1]:
                    continue
                if i > 0 and plants[i][j] > plants[i-1][j]:
                    continue
                if i > 0 and j > 0 and plants[i][j] == plants[i-1][j] + plants[i][j-1]:
                    continue
                if i > 0 and j < len(plants[0])-1 and plants[i][j] == plants[i-1][j+1] + plants[i][j+1]:
                    continue
                if i < len(plants)-1 and j > 0 and plants[i][j] == plants[i+1][j-1] + plants[i][j-1]:
                    continue
                if i < len(plants)-1 and j < len(plants[0])-1 and plants[i][j] == plants[i+1][j+1] + plants[i][j+1]:
                    continue
        return False
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)