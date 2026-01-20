import logging

logger = logging.getLogger(__name__)

class MockSSH:
    def connect(self, host: str):
        logger.info(f"  🔐 MOCK_SSH: Connecting to {host}...")
    
    def execute_command(self, command: str):
        logger.info(f"  🔐 MOCK_SSH: Executing command: {command}")

class MockRDP:
    def validate_connection(self, host: str):
        logger.info(f"  🖥️  MOCK_RDP: Validating connection to {host}...")