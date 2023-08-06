import argparse
from enum import Enum, auto

from fameio.source.logs import LOG_LEVELS


class Options(Enum):
    """Specifies command line configuration options"""

    FILE = auto()
    LOG_LEVEL = auto()
    LOG_FILE = auto()
    OUTPUT = auto()
    AGENT_LIST = auto()
    SINGLE_AGENT_EXPORT = auto()
    MEMORY_SAVING = auto()
    RESOLVE_COMPLEX_FIELD = auto()


class ResolveOptions(Enum):
    """Specifies options for resolving complex fields in output files"""

    IGNORE = auto()
    SPLIT = auto()
    MERGE = auto()


def arg_handling_make_config(defaults):
    """Handles command line arguments and returns `input_file` and `run_config` for make_config script"""
    parser = argparse.ArgumentParser()

    add_file_argument(parser, "provide path to configuration file")
    add_log_level_argument(parser, defaults[Options.LOG_LEVEL])
    add_logfile_argument(parser)
    add_output_argument(parser, defaults[Options.OUTPUT], "provide file-path for the file to generate")

    args = parser.parse_args()
    run_config = {
        Options.LOG_LEVEL: args.log,
        Options.LOG_FILE: args.logfile,
        Options.OUTPUT: args.output,
    }
    return args.file, run_config


def arg_handling_convert_results(defaults):
    """Handles command line arguments and returns `input_file` and `run_config` for convert_results script"""
    parser = argparse.ArgumentParser()

    add_file_argument(parser, "provide path to protobuf file")
    add_log_level_argument(parser, defaults[Options.LOG_LEVEL])
    add_logfile_argument(parser)
    add_output_argument(
        parser,
        defaults[Options.OUTPUT],
        "provide path to folder to store output .csv files",
    )
    add_select_agents_argument(parser)
    add_single_export_argument(parser, defaults[Options.SINGLE_AGENT_EXPORT])
    add_memory_saving_argument(parser, defaults[Options.MEMORY_SAVING])
    add_resolve_complex_argument(parser, defaults[Options.RESOLVE_COMPLEX_FIELD])

    args = parser.parse_args()
    run_config = {
        Options.LOG_LEVEL: args.log,
        Options.LOG_FILE: args.logfile,
        Options.OUTPUT: args.output,
        Options.AGENT_LIST: args.agents,
        Options.SINGLE_AGENT_EXPORT: args.single_export,
        Options.MEMORY_SAVING: args.memory_saving,
        Options.RESOLVE_COMPLEX_FIELD: ResolveOptions[args.complex_column],
    }
    return args.file, run_config


def add_file_argument(parser: argparse.ArgumentParser, help_text: str) -> None:
    """Adds required 'file' argument to the provided `parser` with the provided `help_text`"""
    parser.add_argument("-f", "--file", required=True, help=help_text)


def add_select_agents_argument(parser: argparse.ArgumentParser) -> None:
    """Adds optional repeatable string argument 'agent' to given `parser`"""
    help_text = "Provide list of agents to extract (default=None)"
    parser.add_argument("-a", "--agents", nargs="*", type=str, help=help_text)


def add_logfile_argument(parser: argparse.ArgumentParser) -> None:
    """Adds optional argument 'logfile' to given `parser`"""
    help_text = "provide logging file (default=None)"
    parser.add_argument("-lf", "--logfile", help=help_text)


def add_output_argument(parser: argparse.ArgumentParser, default_value, help_text: str) -> None:
    """Adds optional argument 'output' to given `parser` using the given `help_text` and `default_value`"""
    parser.add_argument("-o", "--output", default=default_value, help=help_text)


def add_log_level_argument(parser: argparse.ArgumentParser, default_value: str) -> None:
    """Adds optional argument 'log' to given `parser`"""
    help_text = "choose logging level (default: {})".format(default_value)
    parser.add_argument(
        "-l",
        "--log",
        default=default_value,
        choices=list(LOG_LEVELS.keys()),
        help=help_text,
    )


def add_single_export_argument(parser: argparse.ArgumentParser, default_value: bool) -> None:
    """Adds optional repeatable string argument 'agent' to given `parser`"""
    help_text = "Enable export of single agents (default=False)"
    parser.add_argument(
        "-se",
        "--single-export",
        default=default_value,
        action="store_true",
        help=help_text,
    )


def add_memory_saving_argument(parser: argparse.ArgumentParser, default_value: bool) -> None:
    """Adds optional bool argument to given `parser` to enable memory saving mode"""
    help_text = "Reduces memory usage profile at the cost of runtime (default=False)"
    parser.add_argument(
        "-m",
        "--memory-saving",
        default=default_value,
        action="store_true",
        help=help_text,
    )


def add_resolve_complex_argument(parser, default_value: str):
    """Instructs given `parser` how to deal with complex field outputs"""
    help_text = "How to deal with complex index columns? (default=split)"
    parser.add_argument(
        "-cc",
        "--complex-column",
        default=default_value,
        choices=[e.name for e in ResolveOptions],
        help=help_text,
    )


def get_config_or_default(config: dict, default: dict) -> dict:
    """Returns specified `default` in case given `config` is None"""
    return default if config is None else config
