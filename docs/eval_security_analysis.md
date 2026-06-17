# 计算器 eval 白名单过滤安全性分析

## 1. 分析背景

本计算器应用使用 Python 内置的 `eval()` 函数计算数学表达式。由于 `eval()` 可以执行任意 Python 代码，存在代码注入风险。应用在 `eval()` 调用前设置了多层白名单过滤机制。本文档分析这些过滤机制是否足以阻挡危险输入，以及是否存在从键盘输入绕过的可能。

## 2. 现有过滤机制详解

### 2.1 输入路径概览

```
键盘输入 → on_key_press() → 状态管理 → calculate() → evaluate()
                                                          ↓
                                         ┌───────────────────────────┐
                                         │ validate() - 正则格式校验  │
                                         └─────────────┬─────────────┘
                                                       ↓
                                         ┌───────────────────────────┐
                                         │ is_safe_expression()      │
                                         │ - 字符白名单检查           │
                                         │ - 双下划线检查             │
                                         │ - 字母检查                 │
                                         └─────────────┬─────────────┘
                                                       ↓
                                         ┌───────────────────────────┐
                                         │ 除零检测                   │
                                         └─────────────┬─────────────┘
                                                       ↓
                                                    eval()
```

### 2.2 键盘输入层过滤（Controller 层）

位置：[calculator_app.py](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-saturn/src/calculator_app.py#L182-L198)

`on_key_press()` 方法只响应以下按键：

| 按键类型 | 具体按键 | 处理函数 |
|---------|---------|---------|
| 数字键 | `0-9` | `_handle_digit()` |
| 运算符 | `+ - * /` | `_handle_operator()` |
| 小数点 | `.` | `_handle_decimal()` |
| 等号/回车 | `Return`, `KP_Enter` | `calculate()` |
| 退格 | `BackSpace` | `delete_last()` |
| 清空 | `Escape` | `clear()` |

**关键特性**：不在上述列表中的按键会被**直接忽略**，不会添加到表达式字符串中。

### 2.3 表达式格式校验（validate 方法）

位置：[expression_evaluator.py](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-saturn/src/expression_evaluator.py#L12-L36)

```python
pattern = r'^[\d+\-*/().\s]+$'
```

- 允许字符：数字 `\d`、运算符 `+-*/`、括号 `()`、小数点 `.`、空白字符 `\s`
- 使用 `^` 和 `$` 锚定，确保整个字符串都匹配
- 附加检查：左右括号数量必须相等

### 2.4 安全表达式检查（is_safe_expression 方法）

位置：[expression_evaluator.py](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-saturn/src/expression_evaluator.py#L92-L120)

三重检查：

1. **字符白名单**：只允许 `'0123456789+-*/(). '` 中的字符
2. **双下划线检查**：禁止包含 `__`（防止访问 Python 特殊属性）
3. **字母检查**：禁止包含任何字母字符（`c.isalpha()` 为 True 的字符）

### 2.5 除零检测

位置：[expression_evaluator.py](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-saturn/src/expression_evaluator.py#L61-L73)

- 使用正则精确匹配 `/0` 和 `/0.0+` 模式
- 避免误判 `/0.5` 等合法表达式

## 3. 绕过可能性评估

### 3.1 键盘输入层面绕过：不可能

键盘输入在 Controller 层（`on_key_press`）就做了严格的白名单过滤：

- **普通字符键**：只有 `0-9`、`+-*/`、`.` 会被接受，其他字母、符号键全部忽略
- **功能键**：只有回车、退格、ESC 有对应动作，其他功能键无响应
- **组合键**：如 Ctrl+C、Alt+A 等，`event.char` 为空或特殊值，不会被处理
- **输入法输入**：Tkinter 的键盘事件对输入法输入的处理取决于具体平台，但即使输入法能输入特殊字符，后续的 `is_safe_expression()` 也会拦截

**结论**：从键盘输入无法注入白名单以外的字符。

### 3.2 代码注入层面绕过：理论上不可能

即使攻击者能绕过键盘输入（例如通过修改内存、直接调用内部方法等），使恶意字符串到达 `eval()` 之前，`is_safe_expression()` 的白名单过滤也能有效阻挡代码注入。

以下是常见注入攻击向量的分析：

#### 攻击向量 1：函数调用（如 `__import__('os').system('cmd')`）

- **需要字母**：`__import__`、`os`、`system` 都包含字母 → 被字母检查拦截
- **需要下划线**：`__import__` 包含双下划线 → 被双下划线检查拦截
- **需要引号**：`'os'`、`'cmd'` 需要引号 → 不在白名单中
- **结论**：❌ 无法实现

#### 攻击向量 2：属性访问（如 `().__class__.__bases__`）

- **需要字母**：`class`、`bases` 都是字母 → 被字母检查拦截
- **需要下划线**：`__class__`、`__bases__` 包含双下划线 → 被双下划线检查拦截
- **结论**：❌ 无法实现

#### 攻击向量 3：字符串构造（利用数字转字符）

- Python 中没有仅用数字和运算符就能构造字符串并执行的语法
- `chr()` 函数调用需要字母 → 被拦截
- **结论**：❌ 无法实现

#### 攻击向量 4：多语句执行（`;` 或换行）

- 分号 `;` 不在白名单中 → 被字符白名单拦截
- 换行符 `\n` 不在白名单中（`\s` 在 validate 正则中，但 `is_safe_expression` 的白名单只有空格）→ 被拦截
- **结论**：❌ 无法实现

#### 攻击向量 5：Unicode / 全角字符绕过

- 全角数字（如 `１２３`）：`isalpha()` 对全角数字返回 False，但字符白名单检查只包含半角数字 → 被字符白名单拦截
- Unicode 字母：`isalpha()` 会返回 True → 被字母检查拦截
- **结论**：❌ 无法实现

#### 攻击向量 6：空元组副作用（`()` 语法）

- 空括号 `()` 在 Python 中是空元组
- 表达式如 `()*99999999` 会生成一个很大的元组，可能消耗内存
- 但这不是代码注入，最多导致内存耗尽或程序崩溃
- 且键盘输入无法输入连续的 `()`（因为输入运算符才能加括号，逻辑上不太容易构造大量嵌套）
- **结论**：⚠️ 属于 DoS 风险，非代码注入

### 3.3 其他风险评估

| 风险类型 | 严重程度 | 说明 |
|---------|---------|------|
| 代码注入 | 无 | 白名单过滤足够严格 |
| 除零错误 | 低 | 已有专门检测和异常捕获 |
| 数值溢出 | 低 | Python 整数支持大数，浮点数溢出有异常捕获 |
| 内存耗尽（DoS） | 中 | 极长表达式或大量 `()` 可能导致内存问题 |
| 语法错误导致崩溃 | 无 | 有通用异常捕获 |

## 4. 关键防御点总结

### 4.1 纵深防御体系

计算器应用建立了三道防线：

| 防线 | 位置 | 作用 |
|-----|------|------|
| 第一道 | `on_key_press()` | 输入入口处过滤，只允许合法按键 |
| 第二道 | `validate()` | 正则格式校验 + 括号匹配检查 |
| 第三道 | `is_safe_expression()` | 字符白名单 + 双下划线检查 + 字母检查 |

三道防线层层递进，即使某一道失效，后续防线仍能提供保护。

### 4.2 白名单 vs 黑名单

本应用采用的是**白名单**策略（只允许已知安全的字符），而不是黑名单策略（只禁止已知危险的字符）。白名单策略在安全性上远优于黑名单，因为：
- 白名单只允许最小必要字符集
- 不需要枚举所有可能的危险模式
- 不会因为遗漏某种攻击模式而失效

## 5. 结论

### 5.1 核心结论

1. **从键盘输入无法绕过白名单过滤**。Controller 层的 `on_key_press()` 方法只响应数字、运算符、小数点和少数功能键，其他所有按键都被忽略。

2. **eval 前的白名单过滤足以阻挡代码注入**。`is_safe_expression()` 的三重检查（字符白名单、双下划线、字母）构成了严格的安全边界，仅用白名单内的字符无法构造出有意义的恶意代码。

3. **现有架构是安全的**。三道防线（键盘输入层、正则校验层、安全检查层）形成了有效的纵深防御体系。

### 5.2 潜在改进方向（非必需，仅供参考）

虽然当前实现是安全的，但以下改进可进一步提升安全性（不改变现有功能的前提下）：

1. **为 eval 传入空的 globals/locals**：`eval(expression, {}, {})`，即使有漏网之鱼也无法访问任何内置函数
2. **限制表达式长度**：防止超长表达式导致的 DoS 攻击
3. **限制括号嵌套深度**：防止深度嵌套导致的栈溢出

> 注：以上改进建议不影响现有计算器的计算功能和输入响应逻辑，属于安全加固范畴。

## 6. 验证说明

本分析基于对以下代码文件的静态审查：

- [calculator_app.py](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-saturn/src/calculator_app.py) - 控制器层，键盘输入处理
- [expression_evaluator.py](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-saturn/src/expression_evaluator.py) - 计算引擎，eval 和过滤逻辑
- [models.py](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-saturn/src/models.py) - 数据模型
- [ui_engine.py](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-saturn/src/ui_engine.py) - UI 视图层
