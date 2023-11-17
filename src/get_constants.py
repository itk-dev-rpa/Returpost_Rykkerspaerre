from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

def get_constants(orchestrator_connection:OrchestratorConnection) -> dict:
    """Get all constants used by the robot."""
    constants = {}

    # Get email address to send error screenshots to
    error_email = orchestrator_connection.get_constant("Error Email")
    constants["Error Email"] = error_email

    sap_login = orchestrator_connection.get_credential("Mathias SAP")
    constants['SAP Credentials'] = sap_login

    return constants
