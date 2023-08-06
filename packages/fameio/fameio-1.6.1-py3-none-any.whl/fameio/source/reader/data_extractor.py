import logging as log
from builtins import staticmethod
from pathlib import Path
from typing import List, Dict, Tuple, Union

import pandas as pd
from fameprotobuf.DataStorage_pb2 import DataStorage
from fameprotobuf.Services_pb2 import Output
from pandas import DataFrame

from fameio.source.reader.reader import Reader


class DataExtractor:
    """Extracts and provides content from parsed protobuf file"""

    ERR_AGENT_TYPE_MISSING = "Requested AgentType `{}` not found."
    ERR_AGENT_DATA_MISSING = "No output present for AgentType `{}` - Please check spelling."

    def __init__(self, file: str, requested_agents: List[str]) -> None:
        """Reads given `file` and extracts data for `requested_agents`"""
        log.debug("Reading raw data from file...")
        with open(Path(file).as_posix(), "rb") as file:
            data_storages = Reader.get_reader(file).read()
        log.debug("Extracting existing agent types...")
        self.agent_types = self._get_all_agent_types(data_storages)
        self.agents_to_extract = self._get_agents_to_extract(requested_agents)
        log.debug("Extracting requested data series...")
        self.all_series = self._get_requested_series(data_storages)

    @staticmethod
    def _get_all_agent_types(data_storages: List[DataStorage]) -> List[Output.AgentType]:
        """Returns all agentType definitions from given list of `data_storages`"""
        list_of_agent_type_lists = [
            data_storage.output.agentType
            for data_storage in data_storages
            if data_storage.HasField("output") and len(data_storage.output.agentType) > 0
        ]
        return [item for sublist in list_of_agent_type_lists for item in sublist]

    def _get_agents_to_extract(self, requested_agents: List[str]) -> List[str]:
        """Returns existing agent types that match `requested_agents` or all available types if given list is emtpy"""
        agents_to_extract = list()
        available_agent_types = {agent_type.className.upper(): agent_type.className for agent_type in self.agent_types}
        if requested_agents:
            for agent in requested_agents:
                if agent.upper() in available_agent_types.keys():
                    agents_to_extract.append(available_agent_types[agent.upper()])
                else:
                    log.error(self.ERR_AGENT_DATA_MISSING.format(agent))
        else:
            agents_to_extract = available_agent_types.values()
        return agents_to_extract

    def _get_requested_series(self, data_storages: List[DataStorage]) -> Dict[str, List[Output.Series]]:
        """Returns series data from given `data_storages` mapped to the className of requested agents"""
        list_of_series_lists = [
            data_storage.output.series
            for data_storage in data_storages
            if data_storage.HasField("output") and len(data_storage.output.series) > 0
        ]
        list_of_series = [
            series
            for sublist in list_of_series_lists
            for series in sublist
            if series.className in self.agents_to_extract
        ]
        result = {className: list() for className in self.agents_to_extract}
        for series in list_of_series:
            if series.className in result:
                result[series.className].append(series)
        return result

    def has_agent_data(self) -> bool:
        """Returns True if data for any agent is present"""
        return len(self.agent_types) > 0

    def get_agents_to_extract(self) -> List[str]:
        """Returns list of names for agents determined for data extraction and existing data"""
        return self.agents_to_extract

    def extract_agent_data(self, agent: str) -> pd.DataFrame:
        """Returns DataFrame containing all data of given `agent`"""
        agent_data = self._extract_agent_data(agent)
        data_frame = DataFrame.from_dict(agent_data, orient="index")
        data_frame = data_frame[data_frame.columns[::-1]]
        data_frame.rename(columns={i: k for i, k in enumerate(self._get_reversed_column_list(agent))}, inplace=True)
        data_frame.rename(columns=self._get_column_map(agent), inplace=True)
        if not data_frame.empty:
            data_frame.index = pd.MultiIndex.from_tuples(data_frame.index)
            data_frame.rename_axis(("AgentId", "TimeStep"), inplace=True)
        return data_frame

    def _extract_agent_data(self, class_name: str) -> Dict[Tuple[int, int], List[Union[float, None]]]:
        """Returns mapping of (agentId, timeStep) to fixed-length list of all output columns for given `class_name`"""
        reversed_column_list = self._get_reversed_column_list(class_name)
        series_data = dict()
        list_of_agent_series = self.all_series.pop(class_name)
        while list_of_agent_series:
            self._add_series_data_to(list_of_agent_series.pop(), reversed_column_list, series_data)
        return series_data

    def _get_reversed_column_list(self, agent_name: str) -> List[int]:
        """Returns reversed list of output column ids for given agent"""
        agent_type = self._get_agent_type_by_name(agent_name)
        output_column_count = len(agent_type.field)
        return [i for i in reversed(range(output_column_count))]

    @staticmethod
    def _add_series_data_to(
        series, reversed_column_list: List[int], container: Dict[Tuple[int, int], List[Union[float, None]]]
    ) -> None:
        """Adds data from given protobuf `series` to specified `container` dict"""
        for line in series.line:
            index = (series.agentId, line.timeStep)
            values = [
                line.column.pop().value if line.column and line.column[-1].fieldId == i else None
                for i in reversed_column_list
            ]
            container[index] = values

    def _get_column_map(self, agent_name: str) -> Dict[int, str]:
        """Returns dictionary of column IDs mapping to their name for given `agent_name`"""
        agent_type = self._get_agent_type_by_name(agent_name)
        return {field.fieldId: field.fieldName for field in agent_type.field}

    def _get_agent_type_by_name(self, name: str) -> Output.AgentType:
        """Returns `AgentType` of given agent `name`"""
        for agent in self.agent_types:
            if agent.className == name:
                return agent
        raise Exception(self.ERR_AGENT_TYPE_MISSING.format(name))

    def sort_agent_types_in_ascending_length(self) -> List:
        """Returns list of agent types sorted by their amount of series"""
        length_of_agent_types = {agent: len(value) for agent, value in self.all_series.items()}
        sorted_dict = sorted(length_of_agent_types.items(), key=lambda item: item[1])
        sorted_list = [agent_type for agent_type, _ in sorted_dict]
        return sorted_list
