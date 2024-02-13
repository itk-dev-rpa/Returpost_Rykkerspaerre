"""This module is the primary module of the robot framework. It collects the functionality of the rest of the framework."""

import traceback
import sys

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from src import initialize
from src import get_constants
from src import reset
from src import error_screenshot
from src import process


def main():
    """The entry point for the framework. Should be called as the first thing when running the robot."""
    orchestrator_connection = OrchestratorConnection.create_connection_from_args()
    sys.excepthook = log_exception(orchestrator_connection)

    orchestrator_connection.log_trace("Process started.")

    initialize.initialize(orchestrator_connection)

    constants = get_constants.get_constants(orchestrator_connection)

    error_count = 0
    max_retry_count = 3
    for _ in range(max_retry_count):
        try:
            reset.reset(orchestrator_connection, constants['SAP Credentials'])
            process.process(orchestrator_connection)
            break

        # If any business rules are broken the robot should stop entirely.
        except BusinessError as error:
            orchestrator_connection.log_error(f"BusinessError: {error}\nTrace: {traceback.format_exc()}")
            error_screenshot.send_error_screenshot(constants['Error Email'], error, orchestrator_connection.process_name)
            break

        # We actually want to catch all exceptions possible here.
        # pylint: disable-next = broad-exception-caught
        except Exception as error:
            error_count += 1
            error_type = type(error).__name__
            orchestrator_connection.log_error(f"Error caught during process. Number of errors caught: {error_count}. {error_type}: {error}\nTrace: {traceback.format_exc()}")
            error_screenshot.send_error_screenshot(constants['Error Email'].value, error, orchestrator_connection.process_name)

    orchestrator_connection.log_trace("Running cleanup before end.")
    reset.clean_up(orchestrator_connection)
    reset.close_all(orchestrator_connection)
    reset.kill_all(orchestrator_connection)

    orchestrator_connection.log_trace("Framework done.")


def log_exception(orchestrator_connection: OrchestratorConnection) -> callable:
    """Creates a function to be used as an exception hook that logs any uncaught exception in OpenOrchestrator.

    Args:
        orchestrator_connection: The connection to OpenOrchestrator.

    Returns:
        callable: A function that can be assigned to sys.excepthook.
    """
    def inner(exception_type, value, traceback_string):
        orchestrator_connection.log_error(f"Uncaught Exception:\nType: {exception_type}\nValue: {value}\nTrace: {traceback_string}")
    return inner


class BusinessError(Exception):
    """An empty exception used to identify errors caused by breaking business rules"""
