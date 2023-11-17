from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from OpenOrchestrator.database.constants import Credential

from itk_dev_shared_components.sap import sap_login

def reset(orchestrator_connection:OrchestratorConnection, sap_credentials: Credential) -> None:
    """Clean up, close/kill all programs and start them again. """
    orchestrator_connection.log_trace("Resetting.")
    clean_up(orchestrator_connection)
    close_all(orchestrator_connection)
    kill_all(orchestrator_connection)
    open_all(orchestrator_connection, sap_credentials)


def clean_up(orchestrator_connection: OrchestratorConnection) -> None:
    """Do any cleanup needed to leave a blank slate."""
    pass


def close_all(orchestrator_connection: OrchestratorConnection) -> None:
    """Gracefully close all applications used by the robot."""
    pass


def kill_all(orchestrator_connection: OrchestratorConnection) -> None:
    """Forcefully close all applications used by the robot."""
    sap_login.kill_sap()


def open_all(orchestrator_connection: OrchestratorConnection, sap_credentials: Credential) -> None:
    """Open all programs used by the robot."""
    sap_login.login_using_cli(sap_credentials.username, sap_credentials.password)
