# -*- coding: utf-8 -*-
# Create Time: 2022-10-25 15:30
# Author: nzj
# Function：
import time


class CaplFile:
    """写入Capl文件

    :param file_name: 文件名
    :param description: 文件描述
    :param author: 作者
    :param version: 版本
    """

    def __init__(
            self,
            file_name: str,
            description: str = '',
            author: str = 'author',
            version: str = 'v1.0.0',
    ) -> None:
        self._file_name = file_name
        self._description = description
        self._author = author
        self._version = version
        self._variables = list()
        self._includes = list()
        self._functions = dict()

    @property
    def file_name(self) -> str:
        """获取文件名称

        :return: 文件名称
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str) -> None:
        self._file_name = file_name

    @property
    def description(self) -> str:
        """获取文件简要描述，brief description

        :return: 文件简要描述
        """
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def author(self) -> str:
        """获取作者名字

        :return: 作者名字
        """
        return self._author

    @author.setter
    def author(self, author: str) -> None:
        self._author = author

    @property
    def version(self) -> str:
        """获取文件版本信息

        :return: 版本信息
        """
        return self._version

    @version.setter
    def version(self, version: str) -> None:
        self._version = version

    @property
    def includes(self):
        return self._includes

    @property
    def variables(self):
        return self._variables

    @property
    def functions(self):
        return self._functions

    @property
    def file_description(self) -> str:
        current_date = time.strftime("%Y/%m/%d %H:%M", time.localtime())
        return (
            f'/*@!Encoding:936*/\n'
            f'/**\n'
            f' * @file {self.file_name}\n'
            f' * \n'
            f' * @author {self.author}\n'
            f' * @date {current_date}\n'
            f' * @version {self.version}\n'
            f' * @copyright Copyright (c) 2022-2023 广汽研究院\n'
            f' * @note\n'
            f' *  -# your note\n'
            f' * @par 修改日志:\n'
            f' * 版本|描述|作者|日期\n'
            f' * :----:|:----:|:----:|:----:\n'
            f' * {self.version}|创建文档|{self.author}|{current_date}\n'
            f' */'
        )

    def _write_include(self, file) -> None:
        """capl文件include部分信息写入"""
        print('includes', file=file)
        print('{', file=file)
        for include_info in self.includes:
            print(f"    {include_info}", file=file)
        print('', file=file)
        print('}', file=file)

    def _write_variables(self, file):
        """capl文件variables部分信息写入"""
        print('variables', file=file)
        print('{', file=file)
        for variable in self.variables:
            if type(variable) == list:
                for inner_content in variable:
                    print(f"    {inner_content}", file=file)
            elif type(variable) == str:
                print(f"    {variable}", file=file)
        print('', file=file)
        print('}', file=file)

    def _write_function(self, file):
        """capl文件function部分信息写入"""
        for function_name, function_define in self.functions.items():
            print(function_name, file=file)
            print('{', file=file)
            for one_row in function_define:
                print(f"    {one_row}", file=file)
            print('}', file=file)
            print('', file=file)

    def write(self, path) -> None:
        """capl相关信息写入文件

        :param path: 写入文件路径

        >>> obj = CaplFile(file_name='test.cin', description='test', author='nzj')
        >>> obj.includes.append('#pragma library("..\\dll\\Func_Lib_CAPL_DLL.dll")')
        >>> obj.includes.append(r'#include "T2_basic_function.cin"')
        >>> obj.includes
        ['#pragma library("..\\\\dll\\\\Func_Lib_CAPL_DLL.dll")', '#include "T2_basic_function.cin"']
        >>> obj.variables.append(r'const long  g_T2LOG_TABLE_LENGTH = 100; ///< 利用分隔符分割表格的最大分割数')
        >>> obj.variables.append(r'char g_T2LOG_STEP_PREFIX[50] = "======== ";')
        >>> list1 = [
        ... 'enum T2Log_TableResult',
        ... '{',
        ... '    g_T2LOG_TABLE_RESULT_FAIL = 0, ///< 表格汇总结果为失败',
        ... '    g_T2LOG_TABLE_RESULT_PASS = 1, ///< 表格汇总结果为成功',
        ... '};',
        ... ]
        >>> obj.variables.append(list1)
        >>> obj.write('test.cin')
        """
        with open(path, 'w+') as file:
            print(self.file_description, file=file)
            print('', file=file)
            self._write_include(file=file)
            print('', file=file)
            self._write_variables(file=file)
            print('', file=file)
            self._write_function(file=file)