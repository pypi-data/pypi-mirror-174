import os
import logging as log
from pathlib import Path
from typing import Dict, Union

import pandas as pd

from fameio.source.results.data_transformer import INDEX


class CsvWriter:
    """Writes dataframes to different csv files"""

    _INFO_USING_PATH = "Using specified output path: {}"
    _INFO_USING_DERIVED_PATH = "No output path specified - writing to new local folder: {}"

    def __init__(self, config_output: str, input_file_path: Path, single_export: bool) -> None:
        self._single_export = single_export
        self._output_folder = self._get_output_folder_name(config_output, input_file_path)
        self._files = {}
        self._create_output_folder()

    @staticmethod
    def _get_output_folder_name(config_output: str, input_file_path: Path) -> str:
        """Returns name of the output folder derived either from the specified `config_output` or `input_file_path`"""
        if config_output:
            output_folder_name = config_output
            log.info(CsvWriter._INFO_USING_PATH.format(config_output))
        else:
            output_folder_name = input_file_path.stem
            log.info(CsvWriter._INFO_USING_DERIVED_PATH.format(output_folder_name))
        return output_folder_name

    def _create_output_folder(self) -> None:
        """Creates output folder if not yet present"""
        log.debug("Creating output folder if required...")
        if not os.path.exists(self._output_folder):
            os.mkdir(self._output_folder)

    def write_to_files(self, agent_name: str, data: Dict[Union[None, str], pd.DataFrame]) -> None:
        """Writes `data` for given `agent_name` to .csv file(s)"""
        for column_name, column_data in data.items():
            column_data.sort_index(inplace=True)
            if self._single_export:
                for agent_id, agent_data in column_data.groupby(INDEX[0]):
                    identifier = self._get_identifier(agent_name, column_name, str(agent_id))
                    self._write_data_frame(agent_data, identifier)
            else:
                identifier = self._get_identifier(agent_name, column_name)
                self._write_data_frame(column_data, identifier)

    @staticmethod
    def _get_identifier(agent_name: str, column_name: str, agent_id: str = None) -> str:
        """Returns unique identifier for given `agent_name` and (optional) `agent_id` and `column_name`"""
        identifier = str(agent_name)
        if column_name:
            identifier += f"_{column_name}"
        if agent_id:
            identifier += f"_{agent_id}"
        return identifier

    def _write_data_frame(self, data: pd.DataFrame, identifier: str) -> None:
        """
        Appends `data` to existing csv file derived from `identifier` without headers,
        or writes new file with headers instead
        """
        if self._has_file(identifier):
            outfile_name = self._get_outfile_name(identifier)
            data.to_csv(outfile_name, sep=";", index=True, header=False, mode="a")
        else:
            outfile_name = self._create_outfile_name(identifier)
            self._save_outfile_name(outfile_name, identifier)
            data.to_csv(outfile_name, sep=";", index=True, header=True)

    def _has_file(self, identifier: str) -> bool:
        """Returns True if a file for given `identifier` was already written"""
        return identifier in self._files

    def _get_outfile_name(self, identifier: str) -> str:
        """Returns file name for given `agent_name` and (optional) `agent_id`"""
        return self._files[identifier]

    def _create_outfile_name(self, identifier: str) -> str:
        """Returns fully qualified file name based on given `agent_name` and (optional) `agent_id`"""
        return f"{self._output_folder}/{identifier}.csv"

    def _save_outfile_name(self, outfile_name: str, identifier: str) -> None:
        """Stores given name for given `agent_name` and (optional) `agent_id`"""
        self._files[identifier] = outfile_name
