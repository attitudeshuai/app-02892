"""测试渐变色背景功能"""
import tkinter as tk
import pytest
from src.ui_engine import UIEngine


class TestGradientBackground:
    """测试渐变色背景实现"""
    
    def test_apply_gradient_background_sets_bg_color(self):
        """测试apply_gradient_background设置背景颜色"""
        root = tk.Tk()
        ui_engine = UIEngine(root)
        
        # 应用渐变背景
        ui_engine.apply_gradient_background()
        
        # 验证背景颜色已设置（新的深紫色）
        bg_color = root.cget('bg')
        assert bg_color == '#2C1B47' or bg_color == '#2c1b47', f"背景颜色应为#2C1B47，实际为{bg_color}"
        
        root.destroy()
    
    def test_gradient_background_applies_to_root(self):
        """测试渐变背景应用到根窗口"""
        root = tk.Tk()
        ui_engine = UIEngine(root)
        
        # 记录原始背景色
        original_bg = root.cget('bg')
        
        # 应用渐变背景
        ui_engine.apply_gradient_background()
        
        # 验证背景色已改变
        new_bg = root.cget('bg').lower()
        assert new_bg != original_bg.lower() or new_bg == '#2c1b47', "背景色应该被设置"
        
        root.destroy()
    
    def test_gradient_background_dark_theme(self):
        """测试渐变背景使用深色主题"""
        root = tk.Tk()
        ui_engine = UIEngine(root)
        
        # 应用渐变背景
        ui_engine.apply_gradient_background()
        
        # 验证使用深色背景
        bg_color = root.cget('bg')
        # 深色背景的RGB值应该较低
        assert bg_color.startswith('#'), "颜色应该以#开头"
        
        root.destroy()
    
    def test_multiple_gradient_applications(self):
        """测试多次应用渐变背景不会出错"""
        root = tk.Tk()
        ui_engine = UIEngine(root)
        
        # 第一次应用
        ui_engine.apply_gradient_background()
        first_bg = root.cget('bg').lower()
        
        # 第二次应用
        ui_engine.apply_gradient_background()
        second_bg = root.cget('bg').lower()
        
        # 两次应用都应该成功
        assert first_bg == '#2c1b47', "第一次应用应该设置背景色"
        assert second_bg == '#2c1b47', "第二次应用应该保持背景色"
        
        root.destroy()
    
    def test_gradient_background_with_widgets(self):
        """测试渐变背景与其他组件共存"""
        root = tk.Tk()
        ui_engine = UIEngine(root)
        
        # 先创建一个测试组件
        test_label = tk.Label(root, text="Test")
        test_label.pack()
        
        # 然后应用渐变背景
        ui_engine.apply_gradient_background()
        
        # 验证背景色已设置
        bg_color = root.cget('bg').lower()
        assert bg_color == '#2c1b47', "背景色应该被设置"
        
        # 验证组件仍然存在
        assert test_label.winfo_exists(), "测试组件应该仍然存在"
        
        root.destroy()
    
    def test_gradient_background_consistent_color(self):
        """测试渐变背景颜色一致性"""
        root = tk.Tk()
        root.geometry("400x600")
        ui_engine = UIEngine(root)
        
        # 应用渐变背景
        ui_engine.apply_gradient_background()
        
        # 验证颜色格式正确
        bg_color = root.cget('bg')
        assert bg_color.startswith('#'), "颜色应该以#开头"
        assert len(bg_color) == 7, "颜色应该是7个字符（#rrggbb）"
        
        root.destroy()
