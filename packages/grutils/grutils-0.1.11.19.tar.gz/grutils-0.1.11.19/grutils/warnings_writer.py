#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import List
from shutil import copy
import xlwings as xw
from .error import Error
from .excel import close_wb, is_excel_file_opened, num_to_column


def create_warnings_file_path(folder_path: str, keywords: str, recover: bool = True):
    file_name = f'{keywords}.warnings.xlsx'
    file_path = os.path.join(folder_path, file_name)

    if not recover:
        i = 0
        while os.path.exists(file_path):
            file_name = f'{keywords}.warnings.{i}.xlsx'
            file_path = os.path.join(folder_path, file_name)
            i += 1

    return file_path


def write_warnings(err: Error, file_path: str, excel_app: xw.App, titles: List[str]):
    if err.has_error() or not err.has_warning():
        return

    if is_excel_file_opened(file_path):
        err.append(f"warnings file '{file_path}' is opened")
        return

    if titles is None or len(titles) == 0:
        raise Exception(f'parameter titles not set or is empty')

    column_indexes: List[int] = list(range(len(titles)))
    columns: List[str] = [num_to_column(i + 1) for i in column_indexes]

    if os.path.exists(file_path):
        wb = excel_app.books.open(file_path)
    else:
        wb = excel_app.books.add()

    try:
        sht = wb.sheets[0]
        if err.has_error():
            return

        # clean exists content and style (not using range.clear_contents(), because it not clean style)
        sht.range("A:Z").api.Delete()

        # write title row
        for i in column_indexes:
            sht.range((1, columns[i])).value = titles[i]

        # write warning rows
        row_num = 2
        for warning in err.warnings:
            for i in column_indexes:
                sht.range((row_num, columns[i])).value = warning[titles[i]]
            row_num += 1

        # set styles
        content_rng = sht.range(f'A1:{columns[-1]}{row_num - 1}')

        # 设置[左, 顶, 底, 右, 内部竖直, 内部水平]的边框样式
        for border in [7, 8, 9, 10, 11, 12]:
            content_rng.api.Borders(border).LineStyle = 1
            content_rng.api.Borders(border).Weight = 3

        # 对齐
        content_rng.api.HorizontalAlignment = -4108  # 水平居中
        content_rng.api.VerticalAlignment = -4108  # 垂直居中

        # 行高列宽
        sht.autofit()
        content_rng.api.RowHeight = 25

        if not err.has_error():
            wb.save(file_path)
    finally:
        close_wb(wb)
