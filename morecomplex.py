import random
import time
import sys

class FullDaYanSimulation:
    def __init__(self):
        self.lines = []  # 存储六爻结果
        self.total_stalks = 50

    def type_print(self, text, speed=0.01):
        """打字机效果，模拟叙述感"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def wait(self, seconds):
        """模拟动作的自然停顿"""
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
        sys.stdout.write(f"      [{pile_name}手] 揲四计数: ")
        sys.stdout.flush()
        
        current = count
        # 视觉特效：每减一次显示一个点
        while current > 4:
            current -= 4
            sys.stdout.write(".") # 每一个点代表数走了4根
            sys.stdout.flush()
            time.sleep(0.02) # 数数的速度
            
        # 易经规则：若整除（剩0），则取4根为余数
        remainder = 4 if current == 0 else current
        
        print(f" 剩 {remainder} 策")
        return remainder

    def process_change(self, line_idx, change_idx, current_total):
        """
        执行【一变】的完整物理流程
        """
        print(f"    < 第 {line_idx} 爻 - 第 {change_idx} 变 >")
        
        # 1. 分二
        left, right = self.human_split(current_total)
        print(f"      [分二]  左手: {left}  |  右手: {right}  (总: {current_total})")
        self.wait(0.3)
        
        # 2. 挂一
        right -= 1
        hang_one = 1
        print(f"      [挂一]  取右一策，挂于左手小指")
        
        # 3. 揲四 (左)
        left_rem = self.physical_count("左", left)
        
        # 4. 揲四 (右)
        right_rem = self.physical_count("右", right)
        
        # 5. 归奇
        removed = hang_one + left_rem + right_rem
        new_total = current_total - removed
        
        print(f"      [归奇]  挂1 + 左余{left_rem} + 右余{right_rem} = 去掉 {removed} 策")
        print(f"      [结余]  当前剩余: {new_total} 策")
        print("-" * 60)
        self.wait(0.5)
        
        return new_total

    def generate_line(self, line_idx):
        """
        生成【一爻】的过程 (三变成一爻)
        """
        pos_names = ["初", "二", "三", "四", "五", "上"]
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
        
        print(f"  >>> {pos_names[line_idx-1]}爻 结果判定: 剩 {current_stalks} 策 ÷ 4 = {final_num}")
        print(f"  >>> 获得: {result_text}")
        self.wait(1.5)
        
        return final_num

    def run(self):
        """
        主程序
        """
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
            
        # 2. 输出最终卦象
        self.display_hexagram()

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
            if num == 6: # 老阴 -> 变阳
                left = f"{yin} x"
                right = yang
                name = "老阴"
            elif num == 7: # 少阳 -> 不变
                left = f"{yang}  "
                right = yang
                name = "少阳"
            elif num == 8: # 少阴 -> 不变
                left = f"{yin}  "
                right = yin
                name = "少阴"
            elif num == 9: # 老阳 -> 变阴
                left = f"{yang} o"
                right = yin
                name = "老阳"
                
            # 格式化输出
            # 例如: 上九: ———— o (老阳)      ->      —  —
            print(f"{p_name}{'九' if num%2!=0 else '六'}: {left} ({name}){'':<8} -> {'':<8}{right}")
            
        print("="*60)
        self.analyze_summary()
        
    def analyze_summary(self):
        # 统计变爻
        changes = []
        for idx, val in enumerate(self.lines):
            if val == 6 or val == 9:
                changes.append(idx + 1) # 记录是第几爻动
        
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
    sim = FullDaYanSimulation()
    sim.run()