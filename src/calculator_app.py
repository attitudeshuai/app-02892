"""计算器主应用程序"""
import tkinter as tk
from tkinter import ttk
import logging
from src.models import CalculatorState
from src.ui_engine import UIEngine
from src.expression_evaluator import ExpressionEvaluator
from src.logger import setup_logger

# 初始化日志
logger = setup_logger("calculator.app")


class CalculatorApp:
    """计算器桌面应用程序主系统（控制器）"""
    
    def __init__(self):
        """初始化计算器应用程序"""
        logger.info("正在初始化计算器应用程序...")
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("炫酷计算器")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # 初始化状态管理
        self.state = CalculatorState()
        
        # 初始化计算引擎
        self.evaluator = ExpressionEvaluator()
        
        # 初始化UI引擎
        self.ui_engine = UIEngine(self.root)
        
        # 应用背景
        self.ui_engine.apply_gradient_background()
        
        # 创建显示区域
        self.display = self.ui_engine.create_display()
        
        # 创建按钮容器框架
        self.button_frame = tk.Frame(self.root, bg="#1a252f")
        self.button_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        # 创建按钮
        self.buttons = self.ui_engine.create_buttons(self.button_frame)
        
        # 布局按钮并绑定点击事件
        self._layout_buttons()
        
        # 绑定键盘事件
        self.root.bind("<Key>", self.on_key_press)
        
        logger.info("计算器应用程序初始化完成")
    
    def _layout_buttons(self):
        """布局按钮并绑定点击事件"""
        # 按钮配置：(值, 行, 列, 列跨度)
        button_layout = [
            ("C", 0, 0, 2),
            ("⌫", 0, 2, 2),
            ("7", 1, 0, 1),
            ("8", 1, 1, 1),
            ("9", 1, 2, 1),
            ("/", 1, 3, 1),
            ("4", 2, 0, 1),
            ("5", 2, 1, 1),
            ("6", 2, 2, 1),
            ("*", 2, 3, 1),
            ("1", 3, 0, 1),
            ("2", 3, 1, 1),
            ("3", 3, 2, 1),
            ("-", 3, 3, 1),
            ("0", 4, 0, 2),
            (".", 4, 2, 1),
            ("+", 4, 3, 1),
            ("=", 5, 0, 4),
        ]
        
        # 配置网格权重
        for i in range(4):
            self.button_frame.columnconfigure(i, weight=1)
        for i in range(6):
            self.button_frame.rowconfigure(i, weight=1)
        
        # 布局按钮（进一步减小间距到1px，更紧凑）
        for value, row, col, colspan in button_layout:
            btn = self.buttons.get(value)
            if btn:
                # 为Canvas按钮设置命令
                if isinstance(btn, tk.Canvas):
                    btn.command = lambda v=value: self.on_button_click(v)
                    btn.grid(
                        row=row,
                        column=col,
                        columnspan=colspan,
                        sticky="nsew",
                        padx=1,  # 减小到1px
                        pady=1   # 减小到1px
                    )
                else:
                    # 兼容其他类型按钮
                    btn.config(command=lambda v=value: self.on_button_click(v))
                    if hasattr(btn, '_frame'):
                        btn._frame.grid(
                            row=row,
                            column=col,
                            columnspan=colspan,
                            sticky="nsew",
                            padx=1,
                            pady=1
                        )
                    else:
                        btn.grid(
                            row=row,
                            column=col,
                            columnspan=colspan,
                            sticky="nsew",
                            padx=1,
                            pady=1
                        )
    
    def run(self):
        """启动应用程序主循环"""
        logger.info("启动应用程序主循环")
        self.root.mainloop()
    
    def on_button_click(self, value: str):
        """处理按钮点击事件"""
        logger.debug(f"按钮点击: {value}")
        button = self.buttons.get(value)
        if button:
            self.ui_engine.play_click_animation(button)
        
        if value == "=":
            self.calculate()
        elif value == "C":
            self.clear()
        elif value == "⌫":
            self.delete_last()
        elif value in "0123456789":
            self._handle_digit(value)
        elif value in "+-*/":
            self._handle_operator(value)
        elif value == ".":
            self._handle_decimal()
    
    def _handle_digit(self, digit: str):
        """处理数字输入"""
        if self.state.is_error_displayed or self.state.is_result_displayed:
            self.state.current_expression = digit
            self.state.is_error_displayed = False
            self.state.is_result_displayed = False
        else:
            self.state.current_expression += digit
        self.ui_engine.update_display(self.state.current_expression)
    
    def _handle_operator(self, op: str):
        """处理运算符输入"""
        if self.state.is_error_displayed:
            self.state.current_expression = op
            self.state.is_error_displayed = False
            self.state.is_result_displayed = False
        elif self.state.is_result_displayed:
            self.state.current_expression = self.state.last_result + op
            self.state.is_result_displayed = False
        else:
            self.state.current_expression += op
        self.ui_engine.update_display(self.state.current_expression)
    
    def _handle_decimal(self):
        """处理小数点输入"""
        if self.state.is_error_displayed or self.state.is_result_displayed:
            self.state.current_expression = "."
            self.state.is_error_displayed = False
            self.state.is_result_displayed = False
        else:
            self.state.current_expression += "."
        self.ui_engine.update_display(self.state.current_expression)
    
    def on_key_press(self, event):
        """处理键盘输入事件"""
        key = event.keysym
        char = event.char
        
        if char in "0123456789":
            self._handle_digit(char)
        elif char in "+-*/":
            self._handle_operator(char)
        elif char == ".":
            self._handle_decimal()
        elif key in ("Return", "KP_Enter"):
            self.calculate()
        elif key == "BackSpace":
            self.delete_last()
        elif key == "Escape":
            self.clear()
    
    def calculate(self):
        """执行计算操作"""
        expression = self.state.current_expression
        if not expression or expression.strip() == "":
            logger.debug("空表达式，跳过计算")
            return
        
        logger.info(f"执行计算: {expression}")
        success, result_or_error = self.evaluator.evaluate(expression)
        
        if success:
            logger.info(f"计算结果: {result_or_error}")
            self.ui_engine.update_display(result_or_error)
            self.state.is_result_displayed = True
            self.state.last_result = result_or_error
            self.state.is_error_displayed = False
        else:
            logger.warning(f"计算错误: {result_or_error}")
            self.ui_engine.show_error(result_or_error)
            self.state.is_error_displayed = True
            self.state.is_result_displayed = False
    
    def clear(self):
        """清空表达式和状态"""
        logger.debug("清空表达式")
        self.state.current_expression = ""
        self.state.is_result_displayed = False
        self.state.is_error_displayed = False
        self.state.last_result = ""
        self.ui_engine.update_display("0")
    
    def delete_last(self):
        """删除表达式最后一个字符"""
        if self.state.is_error_displayed:
            self.state.is_error_displayed = False
        if self.state.is_result_displayed:
            self.state.is_result_displayed = False
        
        if self.state.current_expression:
            self.state.current_expression = self.state.current_expression[:-1]
        
        display_text = self.state.current_expression if self.state.current_expression else "0"
        self.ui_engine.update_display(display_text)
