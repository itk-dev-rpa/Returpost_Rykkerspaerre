"""This module contains the main process of the robot."""

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from itk_dev_shared_components.sap import multi_session

from .sap import handle_7, handle_q, common


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")

    sessions = multi_session.spawn_sessions(2)
    session1 = sessions[0]
    session2 = sessions[1]

    orchestrator_connection.log_trace("Opening afklaringsliste.")
    common.open_afklaringsliste(session1)

    orchestrator_connection.log_trace("Starting Q.")
    common.select_layout(session1, '/RPA_RS_Q')
    handle_q.handle_q(orchestrator_connection, session1)
    orchestrator_connection.log_trace("Q done.")

    orchestrator_connection.log_trace("Starting 7.")
    common.select_layout(session1, '/RPA_RS_7')
    handle_7.handle_7(orchestrator_connection, session1, session2)
    orchestrator_connection.log_trace("7 done.")
