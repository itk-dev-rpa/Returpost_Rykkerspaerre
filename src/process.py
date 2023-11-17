from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from itk_dev_shared_components.sap import multi_session

from SAP import handle_7, handle_q, startup

def process(orchestrator_connection:OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    sessions = multi_session.spawn_sessions(2)
    session1 = sessions[0]
    session2 = sessions[1]

    orchestrator_connection.log_trace("Opening afklaringsliste.")
    startup.open_afklaringsliste(session1)

    orchestrator_connection.log_trace("Starting Q.")
    startup.select_layout(session1, '/RPA_RS_Q')
    handle_q.handle_Q(session1)
    orchestrator_connection.log_trace("Q done.")

    orchestrator_connection.log_trace("Starting 7.")
    startup.select_layout(session1, '/RPA_RS_7')
    handle_7.handle_7(orchestrator_connection, session1, session2)
    orchestrator_connection.log_trace("7 done.")