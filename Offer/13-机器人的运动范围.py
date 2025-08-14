''''
题目：
地上有一个m行和n列的方格。一个机器人从坐标0,0的格子开始移动，每一次只能向左，右，上，下四个方向移动一格，
但是不能进入行坐标和列坐标的数位之和大于k的格子。 例如，当k为18时，机器人能够进入方格（35,37），因为3+5+3+7 = 18。
但是，它不能进入方格（35,38），因为3+5+3+8 = 19。请问该机器人能够达到多少个格子？
'''
from collections import deque


class Solution:
    def moving_count(self, threshold, rows, cols):
        if threshold < 0 or rows <= 0 or cols <= 0:
            return 0
        visited = [False for i in range(rows * cols)]
        count = self.moving_count_core(threshold, rows, cols, 0, 0, visited)
        return count

    def moving_count_core(self, threshold, rows, cols, row, col, visited):
        count = 0
        if self.check(threshold, rows, cols, row, col, visited):
            visited[row * cols + col] = True
            count = 1 + self.moving_count_core(threshold, rows, cols, row - 1, col, visited) + self.moving_count_core(
                threshold, rows, cols, row + 1, col, visited) + self.moving_count_core(threshold, rows, cols, row,
                                                                                       col - 1,
                                                                                       visited) + self.moving_count_core(
                threshold, rows, cols, row, col + 1, visited)
        return count

    def check(self, threshold, rows, cols, row, col, visited):
        if 0 <= row < rows and 0 <= col < cols and self.get_digit_sum(row) + self.get_digit_sum(
                col) <= threshold and not visited[row * cols + col]:
            return True
        return False

    def get_digit_sum(self, number):
        sum = 0
        while number > 0:
            sum += number % 10
            number //= 10
        return sum

    def check2(self, threshold, rows, cols, row, col, visited):
        if 0 <= row < rows and 0 <= col < cols and self.get_digit_sum(row) + self.get_digit_sum(
                col) <= threshold and not visited[row][col]:
            return True
        return False
    def moving_count_v2(self, threshold, rows, cols):
        # bfs，向下向右搜索，左上不用考虑
        if threshold < 0 or rows <= 0 or cols <= 0:
            return 0
        # 标记是否访问过
        visited = [[False for i in range(cols)] for j in range(rows)]
        # 队列，记录下一步可以访问的格子
        q = deque()
        q.append((0, 0))
        visited[0][0] = True
        count = 0
        while q:
            x, y = q.popleft()
            count += 1
                # 向下
            if self.check2(threshold, rows, cols, x + 1, y, visited):
                q.append((x + 1, y))
                visited[x + 1][y] = True
            # 向右
            if self.check2(threshold, rows, cols, x, y + 1, visited):
                q.append((x, y + 1))
                visited[x][y + 1] = True
        return count


print(Solution().moving_count_v2(18, 10, 10))
print(Solution().moving_count(18, 10, 10))
