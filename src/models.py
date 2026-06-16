"""数据模型定义"""
from dataclasses import dataclass


@dataclass
class CalculatorState:
    """计算器状态数据模型"""
    current_expression: str = ""  # 当前输入的表达式
    last_result: str = ""  # 上一次计算结果
    is_result_displayed: bool = False  # 是否正在显示结果
    is_error_displayed: bool = False  # 是否正在显示错误


@dataclass
class ButtonConfig:
    """按钮配置数据模型"""
    text: str  # 按钮显示文本
    value: str  # 按钮实际值
    row: int  # 网格行位置
    col: int  # 网格列位置
    colspan: int = 1  # 列跨度
    bg_color: str = "#4A90E2"  # 背景颜色
    fg_color: str = "#FFFFFF"  # 前景颜色


@dataclass
class AnimationConfig:
    """动画配置数据模型"""
    duration: int = 200  # 动画持续时间（毫秒）
    scale_factor: float = 0.95  # 缩放因子
    color_change: str = "#357ABD"  # 点击时的颜色
