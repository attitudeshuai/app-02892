# 炫酷Python计算器

一个具有现代化视觉效果和流畅交互动画的Python桌面计算器应用程序。

## How to Run

```bash
# 1. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动计算器
python3 main.py

# 4. 退出虚拟环境
deactivate
```

> **注意**: Tkinter 是 Python 标准库的一部分。如果在 Linux 上运行时遇到问题，请安装：
> ```bash
> sudo apt-get install python3-tk
> ```

## Services

本项目是一个独立的桌面应用程序，不依赖外部服务。

核心服务模块：
- **Expression_Evaluator** - 表达式计算引擎，负责验证和计算数学表达式
- **UI_Engine** - 界面渲染引擎，负责显示和动画效果
- **Calculator_App** - 主控制器，协调用户输入和计算逻辑

## 测试账号

本项目为本地桌面应用，无需账号登录。

## 题目内容

请用python代码写一个炫酷界面的计算器桌面程序

### 项目要求
- 使用 Python 代码编写
- 桌面应用程序
- 界面必须炫酷
- 增加点击动效
- 功能以最小 MVP 闭环实现

### 实现功能
1. 基本算术运算（加、减、乘、除）
2. 实时表达式显示
3. 炫酷视觉界面
   - 渐变色背景（深蓝→中蓝→深青）
   - 按钮3D立体效果和阴影
   - 显示区域凹陷效果
4. 点击动画效果（200毫秒）
5. 键盘输入支持
6. 连续计算功能
7. 错误处理机制

---

## 功能特性

### 基本功能
- ✅ 基本算术运算（加、减、乘、除）
- ✅ 实时表达式显示
- ✅ 连续计算功能
- ✅ 完善的错误处理

### 炫酷界面
- ✅ 渐变色背景设计（深蓝→中蓝→深青，600行平滑渐变）
- ✅ 按钮3D立体效果（relief=raised, bd=3）
- ✅ 按钮阴影效果（黑色外框模拟阴影）
- ✅ 显示区域凹陷效果和高亮边框
- ✅ 现代化字体和配色方案
- ✅ 流畅的按钮点击动画（200毫秒）

### 输入支持
- ✅ 鼠标点击按钮
- ✅ 键盘数字输入（0-9）
- ✅ 键盘运算符输入（+、-、*、/）
- ✅ 回车键执行计算
- ✅ 退格键删除字符
- ✅ Escape键清空表达式

## 技术栈

- **Python 3.x** - 编程语言
- **Tkinter** - GUI框架（Python标准库）
- **pytest** - 单元测试框架
- **Hypothesis** - 属性测试框架

## 项目结构

```
cool-calculator/
├── src/                          # 源代码目录
│   ├── __init__.py
│   ├── models.py                 # 数据模型
│   ├── expression_evaluator.py   # 表达式求值引擎
│   ├── ui_engine.py              # UI引擎
│   ├── logger.py                 # 日志模块
│   └── calculator_app.py         # 主应用程序
├── tests/                        # 测试目录
│   ├── __init__.py
│   ├── conftest.py               # 测试配置
│   ├── test_models.py
│   ├── test_expression_evaluator.py
│   ├── test_ui_engine.py
│   ├── test_gradient_background.py
│   └── test_calculator_app.py
├── docs/                         # 文档目录
│   └── project_design.md         # 项目设计文档
├── logs/                         # 日志目录
│   └── calculator.log            # 运行日志
├── main.py                       # 程序入口
├── requirements.txt              # 项目依赖
├── pytest.ini                    # pytest配置
├── .gitignore                    # Git忽略配置
└── README.md                     # 项目说明
```

## 操作说明

| 操作 | 鼠标 | 键盘 |
|------|------|------|
| 输入数字 | 点击数字按钮 | 按数字键 0-9 |
| 输入运算符 | 点击运算符按钮 | 按 +、-、*、/ 键 |
| 执行计算 | 点击 = 按钮 | 按回车键 |
| 删除字符 | 点击 ⌫ 按钮 | 按退格键 |
| 清空表达式 | 点击 C 按钮 | 按 Escape 键 |

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_expression_evaluator.py

# 查看详细输出
pytest -v

# 查看测试覆盖率
pytest --cov=src
```

## 架构设计

应用程序采用 MVC（Model-View-Controller）架构模式：

```
┌─────────────────────────────────────────────────┐
│                Calculator_App                    │
│                  (Controller)                    │
└──────────────┬──────────────────┬────────────────┘
               │                  │
               ▼                  ▼
┌──────────────────────┐  ┌─────────────────────┐
│    UI_Engine         │  │ Expression_Evaluator│
│     (View)           │  │      (Model)        │
└──────────────────────┘  └─────────────────────┘
```

## 错误处理

- **除零错误**: 显示"错误: 除数不能为零"
- **语法错误**: 显示"错误: 表达式格式无效"
- **溢出错误**: 显示"错误: 数值过大"
- **代码注入**: 自动过滤非法字符

## 许可证

MIT License
