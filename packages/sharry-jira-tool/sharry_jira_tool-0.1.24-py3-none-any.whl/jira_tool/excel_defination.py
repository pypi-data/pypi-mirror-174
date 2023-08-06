# -*- coding: utf-8 -*-
"""
This module is used to store excel column defination information.
"""
import json
import pathlib
from datetime import datetime

from .milestone import Milestone
from .priority import Priority

__all__ = ["ExcelDefination"]


class ExcelDefination:
    def __init__(self) -> None:
        self.store: list[tuple] = []
        self.sort_strategy_priority: list = []

    def load(self, content: str):
        """
        Load json string to generate the excel defination

        :param content:
            JSON string content
        """

        if content is None:
            raise ValueError("The content is invalid")

        raw_data = json.loads(content)

        for item in raw_data[0]["SortStrategyPriority"]:
            self.sort_strategy_priority.append(item)

        for item in raw_data[1]["Columns"]:
            column_index = 0
            column_name = None
            column_type = None
            column_require_sort = False
            column_sort_order = False
            column_inline_weights = -1
            column_raise_ranking = -1

            for key, value in item.items():
                if key.lower() in "index":
                    column_index = value
                if key.lower() in "name":
                    column_name = value
                if key.lower() in "type":
                    column_type = ExcelDefination.convert_str_to_type(value)
                if key.lower() in "RequireSort".lower():
                    column_require_sort = value
                if key.lower() in "SortOrder".lower():
                    column_sort_order = value
                if key.lower() in "InlineWeights".lower():
                    column_inline_weights = value
                if key.lower() in "RaiseRanking".lower():
                    column_raise_ranking = value

            self.store.append(
                (
                    column_index,
                    column_name,
                    column_type,
                    column_require_sort,
                    column_sort_order,
                    column_inline_weights,
                    column_raise_ranking,
                )
            )

    def load_file(self, file: str):
        """
        Load json file to generate the excel defination

        :param file:
            JSON file location
        """

        if file is None or not pathlib.Path(file).is_absolute():
            raise ValueError("The file is invalid.")

        if not pathlib.Path(file).exists():
            raise ValueError(f"The file is not exist. File: {file}")

        with open(file=file, mode="r") as table_defination_file:
            self.load(table_defination_file.read())
            table_defination_file.close()

    @staticmethod
    def convert_str_to_type(type_str: str) -> type:
        type_str = str(type_str).strip().lower()
        if type_str == "str":
            return str
        elif type_str == "bool":
            return bool
        elif type_str == "datetime":
            return datetime
        elif type_str == "priority":
            return Priority
        elif type_str == "milestone":
            return Milestone
        else:
            return None

    def __iter__(self):
        for item in self.store:
            yield item

    def get_columns(self) -> "list[tuple]":
        result = []
        for item in self.store:
            result.append(item)
        return result

    def get_sort_strategy_priorities(self) -> "list":
        return self.sort_strategy_priority

    def total_count(self):
        return len(self.store)
