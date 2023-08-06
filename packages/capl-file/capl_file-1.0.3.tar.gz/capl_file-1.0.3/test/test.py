# -*- coding: utf-8 -*-
# Create Time: 2022-10-26 11:23
# Author: nzj
# Function：
import capl_file

obj = capl_file.CaplFile(file_name='test.cin', description='test', author='nzj')
obj.includes.append('#pragma library("..\\dll\\Func_Lib_CAPL_DLL.dll")')
obj.includes.append(r'#include "T2_basic_function.cin"')

obj.variables.append(r'const long  g_T2LOG_TABLE_LENGTH = 100; ///< 利用分隔符分割表格的最大分割数')
obj.variables.append(r'char g_T2LOG_STEP_PREFIX[50] = "======== ";')
list1 = [
    'enum T2Log_TableResult',
    '{',
    '    g_T2LOG_TABLE_RESULT_FAIL = 0, ///< 表格汇总结果为失败',
    '    g_T2LOG_TABLE_RESULT_PASS = 1, ///< 表格汇总结果为成功',
    '};',
]
obj.variables.append(list1)
obj.write('test.cin')