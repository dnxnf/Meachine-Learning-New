
# 给出长度相同的两个字符串s1 和 s2 ，还有一个字符串 baseStr 。
# 
#  其中 s1[i] 和 s2[i] 是一组等价字符。 
# 
#  
#  举个例子，如果 s1 = "abc" 且 s2 = "cde"，那么就有 'a' == 'c', 'b' == 'd', 'c' == 'e'。 
#  
# 
#  等价字符遵循任何等价关系的一般规则： 
# 
#  
#  自反性 ：'a' == 'a' 
#  对称性 ：'a' == 'b' 则必定有 'b' == 'a' 
#  传递性 ：'a' == 'b' 且 'b' == 'c' 就表明 'a' == 'c' 
#  
# 
#  例如， s1 = "abc" 和 s2 = "cde" 的等价信息和之前的例子一样，那么 baseStr = "eed" , "acd" 或 "aab"，
# 这三个字符串都是等价的，而 "aab" 是 baseStr 的按字典序最小的等价字符串 
# 
#  利用 s1 和 s2 的等价信息，找出并返回 baseStr 的按字典序排列最小的等价字符串。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s1 = "parker", s2 = "morris", baseStr = "parser"
# 输出："makkek"
# 解释：根据 A 和 B 中的等价信息，我们可以将这些字符分为 [m,p], [a,o], [k,r,s], [e,i] 共 4 组。每组中的字符都是等价的，
# 并按字典序排列。所以答案是 "makkek"。
#  
# 
#  示例 2： 
# 
#  
# 输入：s1 = "hello", s2 = "world", baseStr = "hold"
# 输出："hdld"
# 解释：根据 A 和 B 中的等价信息，我们可以将这些字符分为 [h,w], [d,e,o], [l,r] 共 3 组。所以只有 S 中的第二个字符 'o' 
# 变成 'd'，最后答案为 "hdld"。
#  
# 
#  示例 3： 
# 
#  
# 输入：s1 = "leetcode", s2 = "programs", baseStr = "sourcecode"
# 输出："aauaaaaada"
# 解释：我们可以把 A 和 B 中的等价字符分为 [a,o,e,r,s,c], [l,p], [g,t] 和 [d,m] 共 4 组，因此 S 中除了 
# 'u' 和 'd' 之外的所有字母都转化成了 'a'，最后答案为 "aauaaaaada"。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s1.length, s2.length, baseStr <= 1000 
#  s1.length == s2.length 
#  字符串s1, s2, and baseStr 仅由从 'a' 到 'z' 的小写英文字母组成。 
#  
# 
#  Related Topics 并查集 字符串 👍 74 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 并查集
class Solution:
    def smallestEquivalentString(self, s1: str, s2: str, baseStr: str) -> str:
        # 初始化并查集数据结构
        # 使用0-25代表26个小写字母(a-z)
        # 初始时每个字母的父节点都是自己
        parent = [i for i in range(26)]
        print(parent)
        # 查找函数（带路径压缩优化）
        def find(x: int) -> int:
            # 如果当前节点的父节点不是自己，说明它不是根节点
            if parent[x] != x:
                # 递归查找根节点，并在回溯时进行路径压缩
                # 路径压缩使得树更扁平，加快后续查询
                parent[x] = find(parent[x])
            return parent[x]

        # 合并函数（按字典序优化）
        def union(x: int, y: int):
            # 找到两个节点的根节点
            x_root = find(x)
            y_root = find(y)

            # 如果根节点不同，需要进行合并
            if x_root != y_root:
                # 关键点：总是将较大的根节点合并到较小的根节点下
                # 这样可以保证每个集合的代表元素都是字典序最小的字符
                if x_root < y_root:
                    parent[y_root] = x_root
                else:
                    parent[x_root] = y_root

        # 处理所有等价关系对
        for a, b in zip(s1, s2):
            # 将字符转换为0-25的数字表示
            x = ord(a) - ord('a')
            y = ord(b) - ord('a')
            # 合并这两个字符所在的集合
            union(x, y)

        # 构建结果字符串
        result = []
        for c in baseStr:
            # 将当前字符转换为数字表示
            x = ord(c) - ord('a')
            # 找到该字符所属集合的根节点
            # 由于我们总是将较大的合并到较小的，根节点就是字典序最小的等价字符
            root = find(x)
            # 将根节点转换回字符并加入结果
            result.append(chr(root + ord('a')))

        # 将结果列表转换为字符串返回
        return ''.join(result)
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    '''
    思路：
    1. 遍历一遍两个字符串，生成len(s1)ge的字典，key为字符，value为字符的最小等价字符
    '''
    solution = Solution()
    # 靠前的字母字典序小
    print(ord('a'), ord('z'))  # 97,122
    print(solution.smallestEquivalentString(s1="parker", s2="morris", baseStr="parser"))
