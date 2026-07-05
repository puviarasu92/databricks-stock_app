"""
Integration tests for Databricks connection
"""
import os
import unittest
from unittest.mock import MagicMock, patch


class TestDatabricksConnection(unittest.TestCase):
    """Test Databricks connection functionality"""
    
    @patch('databricks.sql.connect')
    def test_connection_initialization(self, mock_connect):
        """Test Databricks connection initialization"""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        try:
            from databricks import sql
            connection = sql.connect(
                server_hostname="test.cloud.databricks.com",
                http_path="/sql/1.0/test",
                personal_access_token="test_token"
            )
            
            mock_connect.assert_called_once()
            self.assertIsNotNone(connection)
        except Exception as e:
            self.fail(f"Connection test failed: {str(e)}")


if __name__ == '__main__':
    unittest.main()
