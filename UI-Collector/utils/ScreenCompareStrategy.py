from RuntimeContent import *

## 抽象文本比较策略类
class BaseTextComparator(object):

    def __init__(self, threshold = 0.9):
        self.threshold = threshold

    def compare_text(self, text1: str, text2: str) -> float:
        pass

## 最小编辑距离进行比较Screen文本
class EditDistanceComparator(BaseTextComparator):

    def get_minEditDistance(self, text1: str, text2: str) -> int:
        n = len(text1)
        m = len(text2)
        
        # 有一个字符串为空串
        if n * m == 0:
            return n + m
        
        # DP 数组
        D = [ [0] * (m + 1) for _ in range(n + 1)]
        
        # 边界状态初始化
        for i in range(n + 1):
            D[i][0] = i
        for j in range(m + 1):
            D[0][j] = j
        
        # 计算所有 DP 值
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                left = D[i - 1][j] + 1
                down = D[i][j - 1] + 1
                left_down = D[i - 1][j - 1] 
                if text1[i - 1] != text2[j - 1]:
                    left_down += 1
                D[i][j] = min(left, down, left_down)

        return D[n][m]

    def compare_text(self, text1: str, text2: str) -> float:
        diff = self.get_minEditDistance(text1, text2)
        similarity = 1 - diff/len(text1)
        return similarity

## 最长公共子序列进行比较Screen文本
class LCSComparator(BaseTextComparator):
    def __init__(self, threshold = 0.9):
        self.threshold = threshold
    def get_lcs(self, s: str, t: str) -> int:
        # m, n = len(text1), len(text2)
        # dp = [[0] * (n + 1) for _ in range(m + 1)]
        #
        # for i in range(1, m + 1):
        #     for j in range(1, n + 1):
        #         if text1[i - 1] == text2[j - 1]:
        #             dp[i][j] = dp[i - 1][j - 1] + 1
        #         else:
        #             dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        # return dp[m][n]

        f = [0] * (len(t) + 1)
        for x in s:
            pre = 0  # f[0]
            for j, y in enumerate(t):
                tmp = f[j + 1]
                f[j + 1] = pre + 1 if x == y else max(f[j + 1], f[j])
                pre = tmp
        return f[-1]


    def compare_text(self, text1: str, text2: str) -> float:
        lcs = self.get_lcs(text1, text2)
        if len(text1) < len(text2):
            similarity = lcs/len(text2)
        else:
            similarity = lcs/len(text1)
        return similarity


## 具体的比较策略
class ScreenCompareStrategy(object):
    def __init__(self, strategy: BaseTextComparator) -> None:
        self.screen_compare_strategy = strategy
    
    def compare_screen(self, text1: str, text2: str) -> float:
        if text1 == text2:
            return 1
        else:
            # 查缓存
            query_res = RuntimeContent.get_instance().query_simi_mem((text1, text2))
            # 缓存找不到
            if query_res is None:
                similarity = self.screen_compare_strategy.compare_text(text1, text2)
                # 回写缓存
                RuntimeContent.get_instance().update_simi_mem((text1, text2), similarity)
                RuntimeContent.get_instance().update_simi_mem((text2, text1), similarity)
                return similarity
            else:
                return query_res

