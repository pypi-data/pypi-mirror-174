from abc import ABC
from builtins import staticmethod
from typing import List, Dict, Tuple, Union

import pandas as pd
from fameprotobuf.Services_pb2 import Output
from pandas import DataFrame

from fameio.source.cli import ResolveOptions
from fameio.source.results.agent_type import AgentType

INDEX = ("AgentId", "TimeStep")


class DataTransformer(ABC):
    """Extracts and provides series data from parsed and processed output files for requested agents"""

    MODES = {
        ResolveOptions.IGNORE: lambda: DataTransformerIgnore(),
        ResolveOptions.MERGE: lambda: DataTransformerMerge(),
        ResolveOptions.SPLIT: lambda: DataTransformerSplit(),
    }
    SIMPLE_COLUMN_INDEX = -1

    @staticmethod
    def build(complex_column_mode: ResolveOptions) -> "DataTransformer":
        return DataTransformer.MODES[complex_column_mode]()

    def extract_agent_data(
        self, series: List[Output.Series], agent_type: AgentType
    ) -> Dict[Union[str, None], pd.DataFrame]:
        """
        Returns dict of DataFrame(s) containing all data from given `series` of given `agent_type`.
        When ResolveOption is `SPLIT`, the dict maps each complex column's name to the associated DataFrame.
        In any case, the dict maps `None` to a DataFrame with the content of all simple column / merged columns
        """
        container = self._extract_agent_data(series, agent_type)
        data_frames = {}
        for column_id, agent_data in container.items():
            data_frame = DataFrame.from_dict(agent_data, orient="index")
            column_name = agent_type.get_column_name_for_id(column_id)
            if column_id == DataTransformer.SIMPLE_COLUMN_INDEX:
                data_frame.rename(columns=self._get_column_map(agent_type), inplace=True)
                index = INDEX
            else:
                data_frame.rename(columns={0: column_name}, inplace=True)
                index = INDEX + agent_type.get_inner_columns(column_id)

            if not data_frame.empty:
                data_frame.index = pd.MultiIndex.from_tuples(data_frame.index)
                data_frame.rename_axis(index, inplace=True)
            data_frame.dropna(how="all", axis=1, inplace=True)
            data_frames[column_name] = data_frame
        return data_frames

    def _extract_agent_data(
        self, series: List[Output.Series], agent_type: AgentType
    ) -> Dict[int, Dict[Tuple, List[Union[float, None, str]]]]:
        """Returns mapping of (agentId, timeStep) to fixed-length list of all output columns for given `class_name`"""
        container = DataTransformer._create_container(agent_type)
        mask_simple = agent_type.get_simple_column_mask()
        while series:
            self._add_series_data(series.pop(), mask_simple, container)
        filled_columns = {index: column_data for index, column_data in container.items() if len(column_data) > 0}
        return filled_columns

    @staticmethod
    def _create_container(agent_type: AgentType) -> Dict[int, Dict]:
        """Returns map of complex columns IDs to an empty dict, and one more for the remaining simple columns"""
        field_ids = agent_type.get_complex_column_ids().union([DataTransformer.SIMPLE_COLUMN_INDEX])
        return {field_id: {} for field_id in field_ids}

    def _add_series_data(
        self,
        series: Output.Series,
        mask_simple: List[bool],
        container: Dict[int, Dict[Tuple, List[Union[float, None, str]]]],
    ) -> None:
        """Adds data from given `series` to specified `container` dict as list"""
        dummy_list = [None] * len(mask_simple)
        for line in series.line:
            index = (series.agentId, line.timeStep)
            simple_values = dummy_list.copy()
            for column in line.column:
                if mask_simple[column.fieldId]:
                    simple_values[column.fieldId] = column.value
                else:
                    self._merge_complex_column(column, simple_values)
                    self._store_complex_values(column, container, index)
            container[DataTransformer.SIMPLE_COLUMN_INDEX][index] = simple_values

    @staticmethod
    def _merge_complex_column(column: Output.Series.Line.Column, values: List) -> None:
        """Does not merge complex column data"""
        pass

    @staticmethod
    def _store_complex_values(column: Output.Series.Line.Column, container: Dict[int, Dict], index: Tuple) -> None:
        """Does not store complex column data"""
        pass

    @staticmethod
    def _get_column_map(agent_type: AgentType) -> Dict[int, str]:
        """Returns mapping of simple column IDs to their name for given `agent_type`"""
        return agent_type.get_simple_column_map()


class DataTransformerIgnore(DataTransformer):
    """Ignores complex columns on output"""


class DataTransformerMerge(DataTransformer):
    """Merges complex columns on output into a single column entry"""

    def _get_column_map(self, agent_type: AgentType) -> Dict[int, str]:
        """Returns mapping of simple (and merged) column IDs to their name (or enhanced name) for given `agent_type`"""
        return agent_type.get_merged_column_map()

    @staticmethod
    def _merge_complex_column(column: Output.Series.Line.Column, values: List) -> None:
        """Merges given complex `column` content and saves it to given `values` list"""
        result = []
        for entry in column.entry:
            result.append((tuple(entry.indexValue), entry.value))
        values[column.fieldId] = result


class DataTransformerSplit(DataTransformer):
    @staticmethod
    def _store_complex_values(column: Output.Series.Line.Column, container: Dict[int, Dict], base_index: Tuple) -> None:
        """Adds inner data from `column` to given `container` - split by column type"""
        for entry in column.entry:
            index = base_index + tuple(entry.indexValue)
            container[column.fieldId][index] = entry.value
