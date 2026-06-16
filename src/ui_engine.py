"""用户界面引擎"""
import tkinter as tk
from tkinter import ttk


class RoundedButton(tk.Canvas):
    """自定义圆角按钮类"""
    
    def __init__(self, parent, text, bg_color, fg_color='#FFFFFF', 
                 active_color=None, command=None, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.active_color = active_color or bg_color
        self.command = command
        self.is_pressed = False
        
        # 绑定事件
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        
        # 延迟绘制，等待尺寸确定
        self.bind('<Configure>', self._on_configure)
    
    def _on_configure(self, event):
        """窗口配置改变时重绘"""
        self._draw()
    
    def _create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """创建圆角矩形（增大圆角半径到25px）"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _draw(self, pressed=False):
        """绘制按钮"""
        self.delete('all')
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # 选择颜色
        color = self.active_color if pressed else self.bg_color
        
        # 绘制多层阴影（更明显的3D效果）
        if not pressed:
            # 第三层阴影（最深）
            self._create_rounded_rect(
                8, 8, width-2, height-2, radius=25,
                fill='#000000', outline='', tags='shadow3'
            )
            # 第二层阴影
            self._create_rounded_rect(
                6, 6, width-2, height-2, radius=25,
                fill='#1a1a1a', outline='', tags='shadow2'
            )
            # 第一层阴影
            self._create_rounded_rect(
                4, 4, width-2, height-2, radius=25,
                fill='#333333', outline='', tags='shadow1'
            )
        
        # 绘制主体圆角矩形
        offset = 4 if pressed else 0
        self._create_rounded_rect(
            4 + offset, 4 + offset,
            width - 8 + offset, height - 8 + offset,
            radius=25,
            fill=color, outline='#FFFFFF', width=3, tags='body'
        )
        
        # 绘制文字
        self.create_text(
            width // 2 + offset, height // 2 + offset,
            text=self.text,
            fill=self.fg_color,
            font=('Helvetica', 24, 'bold'),
            tags='text'
        )
    
    def _on_press(self, event):
        """按下事件"""
        self.is_pressed = True
        self._draw(pressed=True)
        if self.command:
            self.command()
    
    def _on_release(self, event):
        """释放事件"""
        self.is_pressed = False
        self.after(200, lambda: self._draw(pressed=False))
    
    def _on_enter(self, event):
        """鼠标进入"""
        self.config(cursor='hand2')
    
    def _on_leave(self, event):
        """鼠标离开"""
        if not self.is_pressed:
            self._draw(pressed=False)


class UIEngine:
    """负责渲染界面和动画效果的用户界面引擎"""
    
    def __init__(self, root: tk.Tk):
        """
        初始化UI引擎
        
        Args:
            root: Tkinter主窗口
        """
        self.root = root
        self.display = None
        self.buttons = {}
        self.button_colors = {
            'num': {'bg': '#3D5A73', 'active': '#2D4A63', 'pressed': '#1D3A53'},
            'op': {'bg': '#0984E3', 'active': '#0774D3', 'pressed': '#0664C3'},
            'clear': {'bg': '#D63031', 'active': '#C62021', 'pressed': '#B61011'},
            'back': {'bg': '#E17055', 'active': '#D16045', 'pressed': '#C15035'},
            'equal': {'bg': '#00B894', 'active': '#00A884', 'pressed': '#009874'}
        }
        self._setup_styles()
    
    def _setup_styles(self):
        """设置ttk样式"""
        self.style = ttk.Style()
        
        # 尝试使用clam主题（支持自定义颜色）
        try:
            self.style.theme_use('clam')
        except:
            pass
        
        # 数字按钮样式（添加圆角和阴影效果）
        self.style.configure(
            'Num.TButton',
            font=('Helvetica', 24, 'bold'),
            background='#3D5A73',
            foreground='#FFFFFF',
            borderwidth=1,
            relief='raised',
            focuscolor='none',
            anchor='center'
        )
        self.style.map('Num.TButton',
            background=[('active', '#2D4A63'), ('pressed', '#1D3A53')],
            foreground=[('active', '#FFFFFF')],
            relief=[('pressed', 'sunken')]
        )
        
        # 运算符按钮样式（添加圆角和阴影效果）
        self.style.configure(
            'Op.TButton',
            font=('Helvetica', 24, 'bold'),
            background='#0984E3',
            foreground='#FFFFFF',
            borderwidth=1,
            relief='raised',
            focuscolor='none',
            anchor='center'
        )
        self.style.map('Op.TButton',
            background=[('active', '#0774D3'), ('pressed', '#0664C3')],
            foreground=[('active', '#FFFFFF')],
            relief=[('pressed', 'sunken')]
        )
        
        # 清除按钮样式（添加圆角和阴影效果）
        self.style.configure(
            'Clear.TButton',
            font=('Helvetica', 24, 'bold'),
            background='#D63031',
            foreground='#FFFFFF',
            borderwidth=1,
            relief='raised',
            focuscolor='none',
            anchor='center'
        )
        self.style.map('Clear.TButton',
            background=[('active', '#C62021'), ('pressed', '#B61011')],
            foreground=[('active', '#FFFFFF')],
            relief=[('pressed', 'sunken')]
        )
        
        # 退格按钮样式（添加圆角和阴影效果）
        self.style.configure(
            'Back.TButton',
            font=('Helvetica', 24, 'bold'),
            background='#E17055',
            foreground='#FFFFFF',
            borderwidth=1,
            relief='raised',
            focuscolor='none',
            anchor='center'
        )
        self.style.map('Back.TButton',
            background=[('active', '#D16045'), ('pressed', '#C15035')],
            foreground=[('active', '#FFFFFF')],
            relief=[('pressed', 'sunken')]
        )
        
        # 等号按钮样式（添加圆角和阴影效果）
        self.style.configure(
            'Equal.TButton',
            font=('Helvetica', 24, 'bold'),
            background='#00B894',
            foreground='#FFFFFF',
            borderwidth=1,
            relief='raised',
            focuscolor='none',
            anchor='center'
        )
        self.style.map('Equal.TButton',
            background=[('active', '#00A884'), ('pressed', '#009874')],
            foreground=[('active', '#FFFFFF')],
            relief=[('pressed', 'sunken')]
        )
    
    def create_display(self) -> tk.Entry:
        """
        创建显示区域
        
        Returns:
            tk.Entry: 显示区域组件
        """
        # 创建显示区域容器（添加圆角和阴影效果）
        display_frame = tk.Frame(self.root, bg='#0d1b2a', padx=5, pady=5)
        display_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # 创建Entry组件作为显示区域（添加边框模拟圆角和阴影）
        self.display = tk.Entry(
            display_frame,
            font=("Helvetica", 36, "bold"),
            bg="#1E3A5F",
            fg="#FFFFFF",
            justify="right",
            bd=2,
            relief="sunken",
            insertwidth=0,
            state="readonly",
            readonlybackground="#1E3A5F",
            highlightthickness=2,
            highlightbackground="#0d1b2a",
            highlightcolor="#0984E3"
        )
        self.display.pack(fill=tk.X, ipady=15)
        
        return self.display
    
    def create_buttons(self, parent=None) -> dict:
        """
        创建所有按钮并返回按钮字典（使用Canvas绘制自定义按钮）
        
        Args:
            parent: 按钮的父容器，默认为root
        
        Returns:
            dict: 按钮字典，键为按钮值，值为按钮组件
        """
        container = parent if parent else self.root
        
        # 按钮配置：(显示文本, 值, 颜色类型)
        button_configs = [
            ("C", "C", 'clear'),
            ("DEL", "⌫", 'back'),
            ("7", "7", 'num'),
            ("8", "8", 'num'),
            ("9", "9", 'num'),
            ("/", "/", 'op'),
            ("4", "4", 'num'),
            ("5", "5", 'num'),
            ("6", "6", 'num'),
            ("x", "*", 'op'),
            ("1", "1", 'num'),
            ("2", "2", 'num'),
            ("3", "3", 'num'),
            ("-", "-", 'op'),  # 修复：减号应该是运算符，不是数字
            ("0", "0", 'num'),
            (".", ".", 'num'),
            ("+", "+", 'op'),
            ("=", "=", 'equal'),
        ]
        
        buttons = {}
        for text, value, color_type in button_configs:
            colors = self.button_colors[color_type]
            
            # 创建自定义Canvas按钮（不指定宽高，让grid自动分配）
            btn = RoundedButton(
                container,
                text=text,
                bg_color=colors['bg'],
                active_color=colors['pressed'],
                bg=container.cget('bg')
            )
            
            buttons[value] = btn
            btn._color_type = color_type
        
        self.buttons = buttons
        return buttons
    
    def update_display(self, text: str):
        """
        更新显示内容

        Args:
            text: 要显示的文本
        """
        if self.display:
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            self.display.insert(0, text)
            self.display.config(state="readonly")
    
    def play_click_animation(self, button):
        """
        播放按钮点击动画
        
        Args:
            button: 要播放动画的按钮
        """
        # Canvas按钮已经内置了动画效果
        pass
    
    def show_error(self, message: str, duration: int = 2000):
        """
        显示错误信息

        Args:
            message: 错误信息文本
            duration: 显示持续时间（毫秒）
        """
        if self.display:
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            self.display.insert(0, message)
            self.display.config(fg="#FF6B6B")  # 红色
            self.display.config(state="readonly")

            def restore_color():
                if self.display:
                    self.display.config(fg="#FFFFFF")

            self.root.after(duration, restore_color)
    
    def apply_gradient_background(self):
        """应用渐变色背景和视觉效果"""
        # 创建渐变色背景画布
        canvas = tk.Canvas(self.root, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 创建更鲜明的渐变色效果（从紫色到蓝色到青色）
        height = 600
        width = 400
        
        # 使用三段渐变，颜色对比更强烈
        for i in range(height):
            progress = i / height
            
            if progress < 0.33:
                # 第一段：深紫到紫红 (#2C1B47 -> #5B2C6F)
                t = progress / 0.33
                r = int(0x2C + (0x5B - 0x2C) * t)
                g = int(0x1B + (0x2C - 0x1B) * t)
                b = int(0x47 + (0x6F - 0x47) * t)
            elif progress < 0.66:
                # 第二段：紫红到深蓝 (#5B2C6F -> #1E3A8A)
                t = (progress - 0.33) / 0.33
                r = int(0x5B + (0x1E - 0x5B) * t)
                g = int(0x2C + (0x3A - 0x2C) * t)
                b = int(0x6F + (0x8A - 0x6F) * t)
            else:
                # 第三段：深蓝到青色 (#1E3A8A -> #0F4C75)
                t = (progress - 0.66) / 0.34
                r = int(0x1E + (0x0F - 0x1E) * t)
                g = int(0x3A + (0x4C - 0x3A) * t)
                b = int(0x8A + (0x75 - 0x8A) * t)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color, width=1)
        
        # 添加一些光晕效果
        # 顶部光晕
        canvas.create_oval(-100, -100, 500, 200, 
                          fill='', outline='', 
                          stipple='gray50')
        
        # 设置窗口背景色作为备用
        self.root.configure(bg='#2C1B47')
        
        # 保存画布引用
        self.gradient_canvas = canvas
