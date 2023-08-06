#!/usr/bin/env python

import logging as log
from pathlib import Path

from fameio.source.cli import (
    Options,
    ResolveOptions,
    arg_handling_convert_results,
    get_config_or_default,
)
from fameio.source.logs import log_and_raise_critical, set_up_logger
from fameio.source.results.agent_type import AgentTypeLog
from fameio.source.results.csv_writer import CsvWriter
from fameio.source.results.data_transformer import DataTransformer
from fameio.source.results.output_dao import OutputDAO
from fameio.source.results.reader import Reader

DEFAULT_CONFIG = {
    Options.LOG_LEVEL: "info",
    Options.LOG_FILE: None,
    Options.AGENT_LIST: None,
    Options.OUTPUT: None,
    Options.SINGLE_AGENT_EXPORT: False,
    Options.MEMORY_SAVING: False,
    Options.RESOLVE_COMPLEX_FIELD: ResolveOptions.SPLIT.name,
}


ERR_MEMORY_ERROR = "Out of memory. Try using `-m` or `--memory-saving` option."
ERR_MEMORY_SEVERE = "Out of memory despite memory-saving mode. Reduce output interval in `FAME-Core` and rerun model"


def run(file_path: str, config: dict = None) -> None:
    """Reads file in protobuf format at given `file_path` and extracts its content to .csv file(s)"""
    config = get_config_or_default(config, DEFAULT_CONFIG)
    set_up_logger(level_name=config[Options.LOG_LEVEL], file_name=config[Options.LOG_FILE])

    file_path = Path(file_path)
    writer = CsvWriter(config[Options.OUTPUT], file_path, config[Options.SINGLE_AGENT_EXPORT])
    file_stream = open(file_path, "rb")

    if config[Options.MEMORY_SAVING]:
        log.info("Memory saving mode enabled: Disable on conversion of small files for performance improvements.")

    log.info("Reading and extracting data...")
    reader = Reader.get_reader(file=file_stream, read_single=config[Options.MEMORY_SAVING])
    agent_type_log = AgentTypeLog(requested_agents=config[Options.AGENT_LIST])
    data_transformer = DataTransformer.build(config[Options.RESOLVE_COMPLEX_FIELD])
    try:
        while data_storages := reader.read():
            output = OutputDAO(data_storages, agent_type_log)
            for agent_name in output.get_sorted_agents_to_extract():
                log.debug(f"Extracting data for {agent_name}...")
                data_frames = output.get_agent_data(agent_name, data_transformer)
                log.debug(f"Writing data for {agent_name}...")
                writer.write_to_files(agent_name, data_frames)
        log.info("Data conversion completed.")
    except MemoryError:
        log_and_raise_critical(ERR_MEMORY_SEVERE if Options.MEMORY_SAVING else ERR_MEMORY_ERROR)

    file_stream.close()
    if not agent_type_log.has_any_agent_type():
        log.error("Provided file did not contain any output data.")


if __name__ == "__main__":
    input_file, run_config = arg_handling_convert_results(DEFAULT_CONFIG)
    run(input_file, run_config)
