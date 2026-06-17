# 计算器 eval 白名单过滤安全性分析

## 一、分析背景

本计算器应用使用 Python `eval()` 函数计算数学表达式。由于 `eval()` 可以执行任意 Python 代码，存在代码注入风险。应用通过多层白名单过滤来降低风险。本文档分析这些过滤机制是否能有效阻挡危险输入，以及是否存在通过键盘输入绕过的可能。

---

## 二、安全架构概览

### 2.1 整体数据流

```
键盘输入 / 按钮点击
       ↓
输入层过滤 (on_key_press / on_button_click)
       ↓
状态层 (CalculatorState.current_expression)
       ↓
计算层 (evaluate)
   ├─ validate()       ← 第一层：正则格式验证
   ├─ is_safe_expression()  ← 第二层：白名单字符检查
   └─ eval()           ← 实际执行
```

### 2.2 防御层次

| 层次 | 位置 | 作用 |
|------|------|------|
| 输入层 | `calculator_app.py` - `on_key_press` / `on_button_click` | 只允许特定字符进入表达式 |
| 验证层 1 | `expression_evaluator.py` - `validate()` | 正则表达式格式验证 |
| 验证层 2 | `expression_evaluator.py` - `is_safe_expression()` | 白名单字符逐字检查 + 危险模式检测 |

---

## 三、逐层详细分析

### 3.1 输入层：键盘输入处理

**代码位置**：[calculator_app.py #L182-L198](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-jupiter/src/calculator_app.py#L182-L198)

```python
def on_key_press(self, event):
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
```

**分析**：

1. **字符白名单**：只接受 `0123456789+-*.` 这些可打印字符
2. **功能键白名单**：只接受 Return、KP_Enter、BackSpace、Escape
3. **未匹配的输入直接忽略**：不在白名单中的键不会修改表达式

**结论**：通过正常键盘输入**无法直接注入**危险字符。输入层本身就是一道有效的白名单过滤。

---

### 3.2 验证层 1：正则格式验证

**代码位置**：[expression_evaluator.py #L12-L36](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-jupiter/src/expression_evaluator.py#L12-L36)

```python
pattern = r'^[\d+\-*/().\s]+$'
if not re.match(pattern, expression):
    return False
```

**允许的字符**：
- `\d` - 数字（0-9）
- `+` `-` `*` `/` - 四则运算符
- `(` `)` - 括号
- `.` - 小数点
- `\s` - 空白字符（空格、制表符等）

**额外检查**：括号数量匹配

---

### 3.3 验证层 2：白名单字符检查 + 危险模式检测

**代码位置**：[expression_evaluator.py #L92-L120](file:///d:/charles/program/ai/apps/02.work%20session/session-gsb0617/source%20code/app-02892/app-02892-jupiter/src/expression_evaluator.py#L92-L120)

```python
allowed_chars = set('0123456789+-*/(). ')
for char in expression:
    if char not in allowed_chars:
        return False

# 检查是否包含危险的模式（双下划线，可能用于访问特殊属性）
if '__' in expression:
    return False

# 检查是否包含字母（可能是函数调用或变量名）
if any(c.isalpha() for c in expression):
    return False
```

**三重检查**：

1. **逐字白名单**：只允许 `0123456789+-*/(). ` 共 18 个字符
2. **双下划线检测**：防止 `__import__`、`__builtins__` 等特殊属性访问
3. **字母检测**：防止函数调用、变量名、关键字

---

## 四、关键安全问题分析

### 4.1 能否用白名单字符构造危险代码？

**核心问题**：只使用 `0123456789+-*/(). ` 这些字符，能否构造出有危害的 Python 代码？

**分析结论**：**不能**。原因如下：

| 攻击手段 | 所需字符 | 是否在白名单内 | 结果 |
|----------|----------|----------------|------|
| 函数调用 | 字母、括号 | 字母不在 | ❌ 无法构造 |
| 字符串注入 | 引号 `'` `"` | 不在 | ❌ 无法构造字符串 |
| 属性访问 | 下划线 `_` | 不在 | ❌ 无法访问 `__builtins__` |
| 导入模块 | `import` 关键字 | 字母不在 | ❌ 无法使用 |
| 变量赋值 | `=` 等号 | 不在 | ❌ 无法赋值 |
| 注释 | `#` 或 `"""` | 不在 | ❌ 无法注入注释 |

**理论验证**：

纯数字、运算符、括号、小数点和空格的组合，在 Python 中只能构成：
- 数值字面量（整数、浮点数）
- 算术运算表达式
- 元组 `()` （但空元组或数值元组无安全风险）

这些都是**纯计算操作**，不具备代码执行能力。

---

### 4.2 键盘输入能否绕过过滤？

**核心问题**：有没有办法通过键盘输入绕过所有过滤，直接执行恶意代码？

**分析结论**：**不能**。原因如下：

#### 路径 1：通过 on_key_press 注入
- `on_key_press` 只接受白名单字符（数字、运算符、小数点）
- 其他键直接忽略，不会进入表达式
- **结论**：无法通过此路径注入

#### 路径 2：通过剪贴板粘贴
- 当前代码**没有绑定粘贴事件**处理
- Tkinter 的 Entry 组件设置为 `state="readonly"`，用户无法直接编辑
- 但需要确认：右键菜单或快捷键是否能触发粘贴？
- **实际情况**：Entry 在 readonly 状态下，用户无法通过键盘或鼠标修改内容
- **结论**：无法通过剪贴板注入

#### 路径 3：通过按钮点击注入
- 按钮是固定的 18 个（数字、运算符、功能键）
- 按钮值是硬编码的，用户无法修改
- **结论**：无法通过按钮注入

---

### 4.3 两层验证的冗余性分析

`validate()` 和 `is_safe_expression()` 存在功能重叠：

| 检查项 | validate() | is_safe_expression() |
|--------|------------|----------------------|
| 数字 | ✅ (正则 `\d`) | ✅ (白名单) |
| 运算符 | ✅ | ✅ |
| 括号 | ✅ | ✅ |
| 小数点 | ✅ | ✅ |
| 空白字符 | ✅ (含制表符等) | ✅ (仅空格) |
| 字母检测 | ❌ | ✅ |
| 双下划线检测 | ❌ | ✅ |
| 括号匹配 | ✅ | ❌ |

**注意**：两个函数对空白字符的定义不一致：
- `validate()` 允许所有空白字符（`\s`），包括制表符 `\t`、换行符 `\n` 等
- `is_safe_expression()` 只允许空格 `' '`

**潜在问题**：如果输入包含制表符，`validate()` 会通过，但 `is_safe_expression()` 会拒绝。这不会造成安全问题（因为先松后严），但属于不一致的设计。

---

### 4.4 其他潜在风险

#### 风险 1：正则表达式中的 `-` 位置

`validate()` 的正则：`r'^[\d+\-*/().\s]+$'`

- `-` 在字符类中如果不在首尾，可能被解释为范围符
- 这里使用了 `\-` 转义，是正确的
- **结论**：无风险

#### 风险 2：除零检测的完整性

代码使用正则检测除零，但可能存在绕过方式：
- `1/(0)` - 括号包裹的零
- `1/(0+0)` - 计算结果为零的表达式
- 这些情况会被 `eval()` 抛出 `ZeroDivisionError` 并被捕获
- **结论**：有兜底，不会崩溃，但正则检测有漏网之鱼

#### 风险 3：数值溢出

极大或极小的数可能导致 `OverflowError` 或内存问题
- 代码已捕获 `OverflowError`
- **结论**：有防护

---

## 五、攻击面总结

### 5.1 已覆盖的攻击面

✅ 代码注入（字母、关键字、函数调用）
✅ 特殊属性访问（双下划线）
✅ 字符串注入（引号）
✅ 键盘输入注入（输入层白名单）
✅ 除零错误（正则 + 异常捕获）
✅ 数值溢出（异常捕获）

### 5.2 未覆盖但不构成安全威胁的情况

⚠️ 纯语法错误的表达式（会被异常捕获，不影响安全）
⚠️ 括号不匹配（会被 validate 拒绝）
⚠️ 多个小数点（语法错误，不影响安全）

---

## 六、结论

### 6.1 核心结论

1. **eval 前的白名单过滤能够挡住所有危险输入**
   - 白名单字符集（18 个字符）无法构造有意义的恶意代码
   - 字母检测和双下划线检测提供了额外的安全保障

2. **键盘输入无法绕过去**
   - 输入层 `on_key_press` 本身就是白名单过滤
   - 只有数字、运算符、小数点能进入表达式
   - Entry 组件的 readonly 状态防止了直接编辑和粘贴

3. **整体安全架构是可靠的**
   - 多层防御：输入层 → 正则验证 → 逐字白名单 → 危险模式检测
   - 即使某一层失效，其他层仍能提供保护

### 6.2 改进建议（非必须，仅作参考）

1. **统一空白字符处理**：`validate()` 和 `is_safe_expression()` 对空白字符的定义应保持一致
2. **合并重复验证**：两层验证功能重叠，可考虑合并为一个函数以提高可维护性
3. **考虑使用 ast.literal_eval**：比 eval 更安全，只支持 Python 字面量结构
4. **考虑使用数学表达式解析库**：如 `sympy` 或手写的递归下降解析器，彻底避免 eval

---

## 七、验证测试建议

建议补充以下测试用例来验证安全性：

```python
# 测试危险字符被拒绝
assert not ExpressionEvaluator.is_safe_expression("__import__('os')")
assert not ExpressionEvaluator.is_safe_expression("open('file.txt')")
assert not ExpressionEvaluator.is_safe_expression("1+2;print('hello')")

# 测试键盘输入边界
# （模拟按键事件验证非白名单字符被忽略）
```

---

**文档版本**：v1.0  
**分析日期**：2026-06-18
