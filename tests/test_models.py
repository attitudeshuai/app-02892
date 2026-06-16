"""数据模型的测试"""
import pytest
from src.models import CalculatorState, ButtonConfig, AnimationConfig


def test_calculator_state_defaults():
    """测试 CalculatorState 的默认值"""
    state = CalculatorState()
    assert state.current_expression == ""
    assert state.last_result == ""
    assert state.is_result_displayed is False
    assert state.is_error_displayed is False


def test_button_config_creation():
    """测试 ButtonConfig 的创建"""
    config = ButtonConfig(
        text="7",
        value="7",
        row=1,
        col=0
    )
    assert config.text == "7"
    assert config.value == "7"
    assert config.row == 1
    assert config.col == 0
    assert config.colspan == 1
    assert config.bg_color == "#4A90E2"
    assert config.fg_color == "#FFFFFF"


def test_animation_config_defaults():
    """测试 AnimationConfig 的默认值"""
    config = AnimationConfig()
    assert config.duration == 200
    assert config.scale_factor == 0.95
    assert config.color_change == "#357ABD"
