"""表达式求值引擎"""
import re
import logging

logger = logging.getLogger("calculator.evaluator")


class ExpressionEvaluator:
    """负责解析和计算数学表达式的计算引擎"""
    
    @staticmethod
    def validate(expression: str) -> bool:
        """
        验证表达式是否合法
        
        Args:
            expression: 要验证的数学表达式
            
        Returns:
            bool: 表达式是否合法
        """
        # 处理空表达式
        if not expression or expression.strip() == "":
            return False
        
        # 使用正则表达式验证表达式格式
        # 允许：数字（整数和小数）、运算符（+、-、*、/）、括号、空格
        pattern = r'^[\d+\-*/().\s]+$'
        if not re.match(pattern, expression):
            return False
        
        # 检查括号是否匹配
        if expression.count('(') != expression.count(')'):
            return False
        
        return True
    
    @staticmethod
    def evaluate(expression: str) -> tuple[bool, str]:
        """
        计算表达式
        
        Args:
            expression: 要计算的数学表达式
            
        Returns:
            tuple[bool, str]: (成功标志, 结果或错误信息)
        """
        logger.debug(f"开始计算表达式: {expression}")
        
        # 验证表达式格式
        if not ExpressionEvaluator.validate(expression):
            logger.warning(f"表达式格式无效: {expression}")
            return (False, "错误: 表达式格式无效")
        
        # 检查表达式安全性
        if not ExpressionEvaluator.is_safe_expression(expression):
            logger.warning(f"表达式包含非法字符: {expression}")
            return (False, "错误: 表达式包含非法字符")
        
        # 检测除零错误（使用正则表达式精确匹配除以零的情况）
        import re
        # 匹配 /0 后面不是小数点或数字，或者 /0.0+ 这样的零值小数
        # 避免误判 /0.5 等合法表达式
        expr_no_space = expression.replace(" ", "")
        # 匹配 /0 后面跟着运算符、右括号或结束
        if re.search(r'/0(?:[+\-*/)]|$)', expr_no_space):
            logger.warning(f"检测到除零操作: {expression}")
            return (False, "错误: 除数不能为零")
        # 匹配 /0.0+ 这样的零值小数
        if re.search(r'/0\.0+(?:[+\-*/)]|$)', expr_no_space):
            logger.warning(f"检测到除零操作: {expression}")
            return (False, "错误: 除数不能为零")
        
        try:
            # 安全地使用 eval() 计算表达式
            result = eval(expression)
            logger.info(f"计算成功: {expression} = {result}")
            return (True, str(result))
        except ZeroDivisionError:
            logger.error(f"除零错误: {expression}")
            return (False, "错误: 除数不能为零")
        except OverflowError:
            logger.error(f"数值溢出: {expression}")
            return (False, "错误: 数值过大")
        except Exception as e:
            # 捕获其他所有异常，确保程序不会崩溃
            logger.error(f"计算失败: {expression}, 错误: {e}")
            return (False, "错误: 计算失败")
    
    @staticmethod
    def is_safe_expression(expression: str) -> bool:
        """
        检查表达式是否安全（防止代码注入）
        
        Args:
            expression: 要检查的表达式
            
        Returns:
            bool: 表达式是否安全
        """
        # 处理空表达式
        if not expression or expression.strip() == "":
            return False
        
        # 白名单验证：只允许数字、运算符、括号、小数点和空格
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
        
        return True
