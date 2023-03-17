# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : __init__.py
@Modify Time      @Author    @Version    
--------------    -------    --------    
2022/7/20 11:29      Lee       1.0         
@Description
------------------------------------
 
'''

__version__ = "1.1.8"
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    pass  # must not have setuptools
