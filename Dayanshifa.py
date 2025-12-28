import random
import time
import sys

class DaYanHexagram:
    def __init__(self):
        self.lines = [] # 存储六个爻的数字 [初爻, 二爻, ..., 上爻]
        
    def slow_print(self, text, delay=0.01):
        """模拟说话或思考的节奏输出"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def wait(self, seconds):
        """仪式感的停顿"""
        time.sleep(seconds)

    def human_split(self, total_stalks):
        """
        模拟【分二】：高斯分布模拟人手分草的随机误差
        """
        half = total_stalks / 2
        # 均值在中间，标准差为2.5，模拟手感误差
        left = int(random.gauss(half, 2.5))
        
        # 物理限制修正
        if left < 1: left = 1
        if left >= total_stalks: left = total_stalks - 1
        
        right = total_stalks - left
        return left, right

    def physical_count(self, pile_name, count):
        """
        模拟【揲四】：每4根一数，模拟物理循环
        """
        # 为了不刷屏太快，只打印最终结果，但保留计算耗时
        current = count
        while current > 4:
            current -= 4
            # 极短的延迟，模拟手指拨动
            # time.sleep(0.005) 
            
        remainder = 4 if current == 0 else current
        return remainder

    def process_one_change(self, change_seq, current_total):
        """
        模拟【一变】 (分二 -> 挂一 -> 揲四 -> 归奇)
        """
        # 1. 分二
        left, right = self.human_split(current_total)
        
        # 2. 挂一 (右手取1挂左手小指)
        right -= 1
        hang_one = 1
        
        # 3. 揲四 (左右分别数)
        left_rem = self.physical_count("左", left)
        right_rem = self.physical_count("右", right)
        
        # 4. 归奇
        removed = hang_one + left_rem + right_rem
        new_total = current_total - removed
        
        # 打印简略进度条，避免刷屏过多
        sys.stdout.write(f"    -> 第{change_seq}变: 分({left},{right+1}) 挂1 左余{left_rem} 右余{right_rem} | 去{removed} 剩{new_total}\n")
        time.sleep(0.3)
        
        return new_total

    def get_one_line(self, line_position):
        """
        生成单爻：三变成一爻
        """
        position_names = ["初", "二", "三", "四", "五", "上"]
        name = position_names[line_position - 1]
        
        print(f"\n--- 正在演算第 {line_position} 爻 ({name}爻) ---")
        
        current_stalks = 49 # 大衍之数五十，其用四十有九
        
        # 历经三变
        for i in range(1, 4):
            current_stalks = self.process_one_change(i, current_stalks)
            
        # 定爻
        final_number = current_stalks // 4
        
        # 简单的文字反馈
        type_map = {6: "老阴", 7: "少阳", 8: "少阴", 9: "老阳"}
        print(f"  >>> 得数: {final_number} ({type_map[final_number]})")
        
        return final_number

    def start_divination(self):
        """
        主程序：循环6次
        """
        print("\n" + "="*40)
        print("      大衍筮法 · 完整起卦仪式")
        print("="*40)
        self.slow_print("... 净手，焚香，默念所测之事 ...", 0.05)
        self.wait(1.5)
        
        self.lines = []
        
        # 循环 1 到 6，生成六爻
        for i in range(1, 7):
            num = self.get_one_line(i)
            self.lines.append(num)
            self.wait(0.5)
            
        self.print_final_hexagram()

    def print_final_hexagram(self):
        """
        绘制卦象：本卦 与 之卦
        注意：self.lines 存储的是 [初, 二, 三, 四, 五, 上]
        但在画卦时，上爻在最上面，所以要倒序遍历
        """
        print("\n" + "="*60)
        print(f"{'【 本 卦 】':^25} -> {'【 之 卦 (变卦) 】':^25}")
        print("="*60)
        
        # 符号定义
        # 本卦符号
        yin_symbol = "—  —"
        yang_symbol = "————"
        old_yin_symbol = "—X—" # 老阴，本卦为阴，变卦为阳
        old_yang_symbol = "—O—" # 老阳，本卦为阳，变卦为阴
        
        # 辅助字典
        pos_names = ["初", "二", "三", "四", "五", "上"]
        
        # 倒序：从 index 5 (上爻) 到 0 (初爻)
        for i in range(5, -1, -1):
            num = self.lines[i]
            pos_name = pos_names[i]
            
            # 构造本卦图形
            if num == 6: # 老阴
                origin_graph = f"{yin_symbol} (老阴)"
                changed_graph = f"{yang_symbol} (变阳)"
                label = "六"
            elif num == 7: # 少阳
                origin_graph = f"{yang_symbol} (少阳)"
                changed_graph = f"{yang_symbol} (不变)"
                label = "九"
            elif num == 8: # 少阴
                origin_graph = f"{yin_symbol} (少阴)"
                changed_graph = f"{yin_symbol} (不变)"
                label = "六"
            elif num == 9: # 老阳
                origin_graph = f"{yang_symbol} (老阳)"
                changed_graph = f"{yin_symbol} (变阴)"
                label = "九"
            
            # 格式化输出一行
            # 例如: 上六 : —X— (老阴)       ->       ———— (变阳)
            left_part = f"{pos_name}{label} : {origin_graph}"
            right_part = f"{changed_graph}"
            print(f"{left_part:<30} -> {right_part:>20}")

        print("="*60)
        self.analyze_changes()

    def analyze_changes(self):
        """简单的变爻统计"""
        changes = [i+1 for i, x in enumerate(self.lines) if x in [6, 9]]
        if not changes:
            print("\n结果：六爻安静，无变爻。以本卦卦辞占断。")
        elif len(changes) == 1:
            print(f"\n结果：{changes[0]}爻动。以本卦变爻之辞占断。")
        else:
            print(f"\n结果：{len(changes)}爻动 ({changes})。需结合变爻与本之卦辞综合占断。")

# --- 运行 ---
if __name__ == "__main__":
    divination = DaYanHexagram()
    divination.start_divination()