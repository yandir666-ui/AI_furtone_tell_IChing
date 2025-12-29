# -*- coding: utf-8 -*-
"""
大衍筮法模拟器
Dayan Divination Simulator

模拟传统的大衍筮法起卦过程，通过三变成一爻，六爻成卦的方式
生成本卦和之卦，用于周易占卜。
"""

import random
import time
import sys


class DayanDivination:
    """大衍筮法模拟器"""
    
    def __init__(self, verbose=True):
        """
        初始化大衍筮法模拟器
        
        Args:
            verbose: 是否显示详细过程，默认True
        """
        self.lines = []  # 存储六爻结果
        self.total_stalks = 50
        self.verbose = verbose

    def type_print(self, text, speed=0.01):
        """打字机效果，模拟叙述感"""
        if not self.verbose:
            return
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def wait(self, seconds):
        """模拟动作的自然停顿"""
        if self.verbose:
            time.sleep(seconds)

    def human_split(self, total):
        """
        【分二】模拟：人手分草，符合高斯分布（正态分布）
        """
        half = total / 2
        # 模拟人手误差，大部分时候在中间，偶尔偏多偏少
        left = int(random.gauss(half, 2.0))
        
        # 边界修正：任何一堆至少要有1根
        if left < 1: left = 1
        if left >= total: left = total - 1
        
        right = total - left
        return left, right

    def physical_count(self, pile_name, count):
        """
        【揲四】模拟：每四根一数，不使用取模运算，而是真实的物理减法
        """
        if self.verbose:
            sys.stdout.write(f"      [{pile_name}手] 揲四计数: ")
            sys.stdout.flush()
        
        current = count
        # 视觉特效：每减一次显示一个点
        while current > 4:
            current -= 4
            if self.verbose:
                sys.stdout.write(".")  # 每一个点代表数走了4根
                sys.stdout.flush()
                time.sleep(0.02)  # 数数的速度
            
        # 易经规则：若整除（剩0），则取4根为余数
        remainder = 4 if current == 0 else current
        
        if self.verbose:
            print(f" 剩 {remainder} 策")
        return remainder

    def process_change(self, line_idx, change_idx, current_total):
        """
        执行【一变】的完整物理流程
        """
        if self.verbose:
            print(f"    < 第 {line_idx} 爻 - 第 {change_idx} 变 >")
        
        # 1. 分二
        left, right = self.human_split(current_total)
        if self.verbose:
            print(f"      [分二]  左手: {left}  |  右手: {right}  (总: {current_total})")
            self.wait(0.3)
        
        # 2. 挂一
        right -= 1
        hang_one = 1
        if self.verbose:
            print(f"      [挂一]  取右一策，挂于左手小指")
        
        # 3. 揲四 (左)
        left_rem = self.physical_count("左", left)
        
        # 4. 揲四 (右)
        right_rem = self.physical_count("右", right)
        
        # 5. 归奇
        removed = hang_one + left_rem + right_rem
        new_total = current_total - removed
        
        if self.verbose:
            print(f"      [归奇]  挂1 + 左余{left_rem} + 右余{right_rem} = 去掉 {removed} 策")
            print(f"      [结余]  当前剩余: {new_total} 策")
            print("-" * 60)
            self.wait(0.5)
        
        return new_total

    def generate_line(self, line_idx):
        """
        生成【一爻】的过程 (三变成一爻)
        
        Returns:
            int: 6(老阴), 7(少阳), 8(少阴), 9(老阳)
        """
        pos_names = ["初", "二", "三", "四", "五", "上"]
        
        if self.verbose:
            print("\n" + "#" * 60)
            print(f"###  正在演算：{pos_names[line_idx-1]}爻  ###")
            print("#" * 60)
        
        # 初始用策：49根
        current_stalks = 49
        
        # 必须经过三变
        # 第一变
        current_stalks = self.process_change(line_idx, 1, current_stalks)
        # 第二变
        current_stalks = self.process_change(line_idx, 2, current_stalks)
        # 第三变
        current_stalks = self.process_change(line_idx, 3, current_stalks)
        
        # 三变之后，定爻
        final_num = current_stalks // 4
        
        # 记录结果
        result_text = ""
        if final_num == 6: result_text = "老阴 (六) -> 变"
        elif final_num == 7: result_text = "少阳 (七) -> 不变"
        elif final_num == 8: result_text = "少阴 (八) -> 不变"
        elif final_num == 9: result_text = "老阳 (九) -> 变"
        
        if self.verbose:
            print(f"  >>> {pos_names[line_idx-1]}爻 结果判定: 剩 {current_stalks} 策 ÷ 4 = {final_num}")
            print(f"  >>> 获得: {result_text}")
            self.wait(1.5)
        
        return final_num

    def run(self):
        """
        主程序 - 执行完整的大衍筮法起卦
        
        Returns:
            dict: 包含本卦、之卦、变爻信息的字典
        """
        if self.verbose:
            print("\n" + "="*60)
            print("          大 衍 筮 法 · 全 过 程 模 拟")
            print("="*60)
            self.type_print("大衍之数五十，其用四十有九。")
            self.type_print("分而为二以象两，挂一以象三，")
            self.type_print("揲之以四以象四时，归奇于扐以象润。")
            print("="*60)
            self.wait(1)
        
        self.lines = []
        
        # 1. 循环生成六爻 (从初爻到上爻)
        for i in range(1, 7):
            line_val = self.generate_line(i)
            self.lines.append(line_val)
        
        # 2. 生成卦象
        result = self.get_hexagram_result()
        
        # 3. 显示卦象
        if self.verbose:
            self.display_hexagram()
        
        return result

    def get_hexagram_result(self):
        """
        获取卦象结果
        
        Returns:
            dict: {
                'original_lines': [6,7,8,9,...],  # 原始爻值
                'original_binary': '101010',       # 本卦二进制
                'changed_binary': '101011',        # 之卦二进制
                'changing_lines': [1, 3],          # 变爻位置
                'has_change': True                 # 是否有变爻
            }
        """
        # 计算本卦和之卦的二进制表示
        original_binary = ""
        changed_binary = ""
        changing_lines = []
        
        for idx, val in enumerate(self.lines):
            # 本卦：7,9为阳(1)，6,8为阴(0)
            if val in [7, 9]:
                original_binary += "1"
            else:
                original_binary += "0"
            
            # 之卦：老阴(6)变阳，老阳(9)变阴
            if val == 6:  # 老阴变阳
                changed_binary += "1"
                changing_lines.append(idx + 1)
            elif val == 9:  # 老阳变阴
                changed_binary += "0"
                changing_lines.append(idx + 1)
            elif val == 7:  # 少阳不变
                changed_binary += "1"
            else:  # val == 8, 少阴不变
                changed_binary += "0"
        
        return {
            'original_lines': self.lines.copy(),
            'original_binary': original_binary,
            'changed_binary': changed_binary,
            'changing_lines': changing_lines,
            'has_change': len(changing_lines) > 0
        }

    def display_hexagram(self):
        """
        显示最终的本卦与之卦
        """
        print("\n\n")
        print("="*60)
        print(f"{'【 本 卦 】':^28} {'【 之 卦 】':^28}")
        print("="*60)
        
        pos_names = ["初", "二", "三", "四", "五", "上"]
        
        # 倒序遍历，因为画卦是从上往下画
        for i in range(5, -1, -1):
            num = self.lines[i]
            p_name = pos_names[i]
            
            # 定义符号
            yin = "—  —"
            yang = "————"
            
            # 构建本卦和之卦的图形
            if num == 6:  # 老阴 -> 变阳
                left = f"{yin} x"
                right = yang
                name = "老阴"
            elif num == 7:  # 少阳 -> 不变
                left = f"{yang}  "
                right = yang
                name = "少阳"
            elif num == 8:  # 少阴 -> 不变
                left = f"{yin}  "
                right = yin
                name = "少阴"
            elif num == 9:  # 老阳 -> 变阴
                left = f"{yang} o"
                right = yin
                name = "老阳"
                
            # 格式化输出
            # 例如: 上九: ———— o (老阳)      ->      —  —
            print(f"{p_name}{'九' if num%2!=0 else '六'}: {left} ({name}){'':<8} -> {'':<8}{right}")
            
        print("="*60)
        self.analyze_summary()
        
    def analyze_summary(self):
        """分析变爻情况并给出断语参考"""
        # 统计变爻
        changes = []
        for idx, val in enumerate(self.lines):
            if val == 6 or val == 9:
                changes.append(idx + 1)  # 记录是第几爻动
        
        print("\n[断语参考]")
        if len(changes) == 0:
            print("六爻安静，无变卦。请参考【本卦】卦辞。")
        elif len(changes) == 1:
            print(f"一爻动（第{changes[0]}爻）。请参考【本卦】变爻之爻辞。")
        elif len(changes) == 2:
            print(f"二爻动（第{changes}爻）。以本卦二变爻之辞占，仍以上爻为主。")
        elif len(changes) == 3:
            print(f"三爻动。以本卦与之卦卦辞合占。")
        elif len(changes) > 3:
            print(f"变爻多达{len(changes)}个。请参考【之卦】卦辞为主。")
        print("="*60)


# --- 执行 ---
if __name__ == "__main__":
    sim = DayanDivination(verbose=True)
    result = sim.run()
    print("\n结果数据:")
    print(f"本卦: {result['original_binary']}")
    print(f"之卦: {result['changed_binary']}")
    print(f"变爻: {result['changing_lines']}")
