import pygame
import sys

# 初始化pygame
pygame.init()

# 初始化手柄
pygame.joystick.init()

# 检查是否有手柄连接
if pygame.joystick.get_count() == 0:
    print("没有连接手柄")
    sys.exit()

# 创建手柄对象
joystick = pygame.joystick.Joystick(0)
joystick.init()

# 获取手柄属性
joystick_name = joystick.get_name()
num_axes = joystick.get_numaxes()
num_buttons = joystick.get_numbuttons()
num_hats = joystick.get_numhats()

# 创建窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("虚拟手柄状态显示")

# 加载字体
font_path = "C:\\Windows\\Fonts\\msyh.ttc"
font = pygame.font.Font(font_path, 20)

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DPURPLE = (128, 0, 128)
PURPLE = (192, 132, 252)
LIGHT_PURPLE = (230, 200, 230)
DARK_PINK = (255, 228, 225)
LIGHT_PINK = (255, 235, 240)

# 虚拟手柄布局
triggers_pos = {
    'LT': (100, 100),  # 左扳机键位置（左侧）
    'RT': (700, 100),  # 右扳机键位置（右侧）
}
left_stick_pos = (200, 310)  # 左摇杆位置
right_stick_pos = (500, 400)  # 右摇杆位置
buttons_pos = [(550 + i * 30, 300) for i in range(4)]  # 按钮的模拟位置
dpad_center = (300, 400)  # 方向键中心
buttons_pos = {
    'A': (600, 350),  # 右侧钻石按钮，A按钮（下）
    'B': (640, 310),  # 右侧钻石按钮，B按钮（右）
    'X': (560, 310),  # 右侧钻石按钮，X按钮（左）
    'Y': (600, 270),  # 右侧钻石按钮，Y按钮（上）
    'LB': (200, 200),  # 左肩键
    'RB': (600, 200),  # 右肩键
    '-': (300, 250),  # 中心起始按钮
    '+': (500, 250),  # 中心选择按钮
}

def draw_rounded_rect(surface, color, rect, radius):
    #绘制圆角矩形
    x, y, w, h = rect
    # 创建一个新的 Surface 来绘制圆角矩形
    shape = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(shape, color, (radius, 0, w - radius * 2, h))  # 中间部分
    pygame.draw.rect(shape, color, (0, radius, w, h - radius * 2))  # 中间部分
    pygame.draw.circle(shape, color, (radius, radius), radius)  # 左上角圆角
    pygame.draw.circle(shape, color, (w - radius, radius), radius)  # 右上角圆角
    pygame.draw.circle(shape, color, (radius, h - radius), radius)  # 左下角圆角
    pygame.draw.circle(shape, color, (w - radius, h - radius), radius)  # 右下角圆角
    # 将新绘制的 Surface blit 到目标 surface 上
    surface.blit(shape, (x, y))

def draw_virtual_controller(screen, joystick):
    # 绘制左摇杆
    left_pressed = joystick.get_button(8)  # 左摇杆按压按钮（假设为按钮索引 8）
    left_color = DPURPLE if left_pressed else PURPLE
    left_x = joystick.get_axis(0)  # 左摇杆X轴
    left_y = joystick.get_axis(1)  # 左摇杆Y轴
    pygame.draw.circle(screen, LIGHT_PURPLE, left_stick_pos, 40, 2)  # 外圈
    pygame.draw.circle(screen, left_color, (int(left_stick_pos[0] + left_x * 40),
                                       int(left_stick_pos[1] + left_y * 40)), 15)  # 中心圆

    # 绘制右摇杆
    right_pressed = joystick.get_button(9)  # 右摇杆按压按钮（假设为按钮索引 9）
    right_color = DPURPLE if right_pressed else PURPLE
    right_x = joystick.get_axis(2)  # 右摇杆X轴
    right_y = joystick.get_axis(3)  # 右摇杆Y轴
    pygame.draw.circle(screen, LIGHT_PURPLE, right_stick_pos, 40, 2)  # 外圈
    pygame.draw.circle(screen, right_color, (int(right_stick_pos[0] + right_x * 40),
                                       int(right_stick_pos[1] + right_y * 40)), 15)  # 中心圆

    # 绘制按钮（优化布局）
    button_names = ['A', 'B', 'X', 'Y', 'LB', 'RB', '-', '+']
    for i, name in enumerate(button_names):
        if name == 'LB' or name == 'RB': continue   # 跳过肩键
        pos = buttons_pos[name]
        button_state = joystick.get_button(i)
        color = PURPLE if button_state else LIGHT_PURPLE
        pygame.draw.circle(screen, color, pos, 15)
        # 添加字符到按钮上
        text_surface = font.render(name, True, WHITE)  # 创建文本图层，使用白色作为字体颜色
        text_rect = text_surface.get_rect(center=pos)  # 获取文本轮廓矩形并居中在按钮位置
        screen.blit(text_surface, text_rect)  # 绘制文本

    # 绘制方向键
    hat_value = joystick.get_hat(0)  # 方向键状态
    # 方向键箭头偏移距离
    arrow_offset = 40  # 增加偏移，使箭头远离中心
    # 上箭头
    pygame.draw.polygon(screen,PURPLE if hat_value[1] == 1 else LIGHT_PURPLE,[(dpad_center[0], dpad_center[1] - arrow_offset),(dpad_center[0] - 15, dpad_center[1] - arrow_offset + 20),(dpad_center[0] + 15, dpad_center[1] - arrow_offset + 20),],)
    # 下箭头
    pygame.draw.polygon(screen,PURPLE if hat_value[1] == -1 else LIGHT_PURPLE,[(dpad_center[0], dpad_center[1] + arrow_offset),(dpad_center[0] - 15, dpad_center[1] + arrow_offset - 20),(dpad_center[0] + 15, dpad_center[1] + arrow_offset - 20),],)
    # 左箭头
    pygame.draw.polygon(screen,PURPLE if hat_value[0] == -1 else LIGHT_PURPLE,[(dpad_center[0] - arrow_offset, dpad_center[1]),(dpad_center[0] - arrow_offset + 20, dpad_center[1] - 15),(dpad_center[0] - arrow_offset + 20, dpad_center[1] + 15),],)
    # 右箭头
    pygame.draw.polygon(screen,PURPLE if hat_value[0] == 1 else LIGHT_PURPLE,[(dpad_center[0] + arrow_offset, dpad_center[1]),(dpad_center[0] + arrow_offset - 20, dpad_center[1] - 15),(dpad_center[0] + arrow_offset - 20, dpad_center[1] + 15),],)
    trigger_values = {
        'LT': joystick.get_axis(4),  # 左扳机键轴值
        'RT': joystick.get_axis(5),  # 右扳机键轴值
    }
    for name, pos in triggers_pos.items():
        value = (trigger_values[name] + 1) / 2  # 将轴值[-1, 1]映射到[0, 1]
        bar_height = int(value * 100)  # 根据值计算填充高度
        pygame.draw.rect(screen, LIGHT_PURPLE, (pos[0], pos[1], 20, 100), 2)  # 绘制进度条边框
        pygame.draw.rect(screen, PURPLE, (pos[0], pos[1] + 100 - bar_height, 20, bar_height))  # 绘制填充条    
    # 绘制肩键（圆角矩形）
    lb_pos = buttons_pos['LB']
    rb_pos = buttons_pos['RB']
    lb_rect = (lb_pos[0] - 30, lb_pos[1] - 10, 60, 20)  # 左肩键圆角矩形
    rb_rect = (rb_pos[0] - 30, rb_pos[1] - 10, 60, 20)  # 右肩键圆角矩形
    draw_rounded_rect(screen, PURPLE if joystick.get_button(4) else LIGHT_PURPLE, lb_rect, 10)  # 绘制左肩键圆角矩形
    draw_rounded_rect(screen, PURPLE if joystick.get_button(5) else LIGHT_PURPLE, rb_rect, 10)  # 绘制右肩键圆角矩形

# 渐变背景
def draw_gradient_background(surface, start_color, end_color):
    width, height = surface.get_size()
    gradient = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * y / height)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * y / height)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * y / height)
        pygame.draw.line(gradient, (r, g, b), (0, y), (width, y))
    surface.blit(gradient, (0, 0))

# 主循环
try:
    while True:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 更新手柄状态
        pygame.joystick.Joystick(0).init()

        # 清空窗口
        draw_gradient_background(screen, DARK_PINK, LIGHT_PINK)

        # 显示手柄名称
        title_text = font.render(f"手柄名称: {joystick_name}", True, BLACK)
        screen.blit(title_text, (20, 20))

        # 绘制虚拟手柄
        draw_virtual_controller(screen, joystick)

        # 更新显示
        pygame.display.flip()

        # 延时
        pygame.time.wait(10)

except KeyboardInterrupt:
    pass
finally:
    pygame.quit()
