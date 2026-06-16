"""Calculator_App 的测试"""
import pytest
import tkinter as tk
from hypothesis import given, strategies as st
from src.calculator_app import CalculatorApp


class TestCalculatorApp:
    """CalculatorApp 单元测试"""
    
    def test_calculator_app_initialization(self):
        """测试计算器应用初始化"""
        app = CalculatorApp()
        try:
            assert app.root is not None
            assert app.state is not None
            assert app.evaluator is not None
            assert app.ui_engine is not None
            assert app.display is not None
            assert len(app.buttons) > 0
        finally:
            app.root.destroy()
    
    def test_handle_digit_input(self):
        """测试数字输入处理"""
        app = CalculatorApp()
        try:
            app._handle_digit("5")
            assert app.state.current_expression == "5"
            
            app._handle_digit("3")
            assert app.state.current_expression == "53"
        finally:
            app.root.destroy()
    
    def test_handle_operator_input(self):
        """测试运算符输入处理"""
        app = CalculatorApp()
        try:
            app._handle_digit("5")
            app._handle_operator("+")
            assert app.state.current_expression == "5+"
            
            app._handle_digit("3")
            assert app.state.current_expression == "5+3"
        finally:
            app.root.destroy()
    
    def test_calculate_simple_expression(self):
        """测试简单表达式计算"""
        app = CalculatorApp()
        try:
            app.state.current_expression = "2+3"
            app.calculate()
            assert app.state.is_result_displayed
            assert app.state.last_result == "5"
        finally:
            app.root.destroy()
    
    def test_clear_resets_state(self):
        """测试清空功能重置状态"""
        app = CalculatorApp()
        try:
            app.state.current_expression = "123"
            app.state.is_result_displayed = True
            app.clear()
            
            assert app.state.current_expression == ""
            assert not app.state.is_result_displayed
            assert not app.state.is_error_displayed
        finally:
            app.root.destroy()
    
    def test_delete_last_removes_character(self):
        """测试删除最后一个字符"""
        app = CalculatorApp()
        try:
            app.state.current_expression = "123"
            app.delete_last()
            assert app.state.current_expression == "12"
            
            app.delete_last()
            assert app.state.current_expression == "1"
        finally:
            app.root.destroy()
    
    def test_handle_decimal_input(self):
        """测试小数点输入"""
        app = CalculatorApp()
        try:
            app._handle_digit("3")
            app._handle_decimal()
            app._handle_digit("14")
            assert app.state.current_expression == "3.14"
        finally:
            app.root.destroy()
    
    def test_calculate_with_division(self):
        """测试除法计算"""
        app = CalculatorApp()
        try:
            app.state.current_expression = "10/2"
            app.calculate()
            assert app.state.is_result_displayed
            assert app.state.last_result == "5.0"
        finally:
            app.root.destroy()
    
    def test_calculate_division_by_decimal(self):
        """测试除以小数不会误判为除零"""
        app = CalculatorApp()
        try:
            app.state.current_expression = "1/0.5"
            app.calculate()
            assert app.state.is_result_displayed
            assert app.state.last_result == "2.0"
            assert not app.state.is_error_displayed
        finally:
            app.root.destroy()
    
    def test_calculate_with_zero_division_error(self):
        """测试除零错误处理"""
        app = CalculatorApp()
        try:
            app.state.current_expression = "5/0"
            app.calculate()
            assert app.state.is_error_displayed
            assert not app.state.is_result_displayed
        finally:
            app.root.destroy()
    
    def test_continuous_calculation(self):
        """测试连续计算功能"""
        app = CalculatorApp()
        try:
            # 第一次计算
            app.state.current_expression = "2+3"
            app.calculate()
            assert app.state.last_result == "5"
            
            # 使用结果继续计算
            app._handle_operator("*")
            app._handle_digit("2")
            assert app.state.current_expression == "5*2"
            
            app.calculate()
            assert app.state.last_result == "10"
        finally:
            app.root.destroy()


@given(st.integers(min_value=1, max_value=100))
def test_digit_input_property(n):
    """属性测试：任意数字输入应该被正确处理"""
    app = CalculatorApp()
    try:
        digit_str = str(n)
        for digit in digit_str:
            app._handle_digit(digit)
        assert app.state.current_expression == digit_str
    finally:
        app.root.destroy()


@given(st.integers(min_value=1, max_value=100), st.integers(min_value=1, max_value=100))
def test_addition_property(a, b):
    """属性测试：加法运算应该正确"""
    app = CalculatorApp()
    try:
        app.state.current_expression = f"{a}+{b}"
        app.calculate()
        assert app.state.last_result == str(a + b)
    finally:
        app.root.destroy()
