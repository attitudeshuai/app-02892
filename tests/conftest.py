"""共享测试配置和fixtures"""
import pytest
from hypothesis import settings, Verbosity

# 配置Hypothesis
settings.register_profile("default", max_examples=100, verbosity=Verbosity.normal)
settings.load_profile("default")
