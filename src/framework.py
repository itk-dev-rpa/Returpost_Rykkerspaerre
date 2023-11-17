import traceback
import sys

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from src import initialize
from src import get_constants
from src import reset
from src import error_screenshot
from src import process

def main():
    orchestrator_connection = OrchestratorConnection.create_connection_from_args()
    sys.excepthook = log_exception(orchestrator_connection)

    orchestrator_connection.log_trace("Process started.")

    orchestrator_connection.log_trace("Initializing.")
    initialize.initialize(orchestrator_connection)

    orchestrator_connection.log_trace("Getting constants.")
    constants = get_constants.get_constants(orchestrator_connection)

    error_count = 0
    max_retry_count = 3
    for _ in range(max_retry_count):
        try:
            reset.reset(orchestrator_connection, constants['SAP Credentials'])

            orchestrator_connection.log_trace("Running process.")
            process.process(orchestrator_connection)

            break

        except BusinessError as error:
            orchestrator_connection.log_error(f"BusinessError: {error}\nTrace: {traceback.format_exc()}")
            error_screenshot.send_error_screenshot(constants['Error Email'], error, orchestrator_connection.process_name)
            break

        except Exception as error:
            error_count += 1
            error_type = type(error).__name__
            orchestrator_connection.log_error(f"Error caught during process. Number of errors caught: {error_count}. {error_type}: {error}\nTrace: {traceback.format_exc()}")
            error_screenshot.send_error_screenshot(constants['Error Email'], error, orchestrator_connection.process_name)

    orchestrator_connection.log_trace("Running cleanup before end.")
    reset.clean_up(orchestrator_connection)
    reset.close_all(orchestrator_connection)
    reset.kill_all(orchestrator_connection)

    orchestrator_connection.log_trace("Framework done.")


def log_exception(orchestrator_connection:OrchestratorConnection) -> callable:
    def inner(type, value, traceback):
        orchestrator_connection.log_error(f"Uncaught Exception:\nType: {type}\nValue: {value}\nTrace: {traceback}")
    return inner


class BusinessError(Exception):
    pass
