#!/usr/bin/env python3
"""
炫酷计算器 - 主程序入口

一个具有现代化视觉效果和流畅交互动画的Python桌面计算器应用程序。
"""
import sys


def main():
    """主程序入口函数"""
    try:
        from src.calculator_app import CalculatorApp
        
        # 实例化计算器应用
        app = CalculatorApp()
        
        # 启动应用程序
        app.run()
        
    except KeyboardInterrupt:
        # 处理 Ctrl+C 中断
        print("\n感谢使用炫酷计算器，再见！")
        sys.exit(0)
    except ImportError as e:
        # 处理导入错误
        print(f"错误: 无法导入必要的模块 - {e}")
        print("请确保已正确安装所有依赖。")
        sys.exit(1)
    except Exception as e:
        # 处理其他未预期的异常
        print(f"发生错误: {e}")
        print("应用程序将退出。")
        sys.exit(1)


if __name__ == "__main__":
    main()
