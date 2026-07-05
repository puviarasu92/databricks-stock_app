"""
Unit tests for Databricks Gold Table Viewer
"""
import unittest
from unittest.mock import MagicMock, patch


class TestConfig(unittest.TestCase):
    """Test configuration module"""
    
    def test_config_imports(self):
        """Test that config module imports successfully"""
        try:
            from src import config
            self.assertIsNotNone(config)
        except ImportError as e:
            self.fail(f"Failed to import config: {str(e)}")
    
    def test_default_values(self):
        """Test default configuration values"""
        from src.config import (
            DEFAULT_MAX_ROWS,
            MAX_ALLOWED_ROWS,
            MIN_ALLOWED_ROWS,
            APP_TITLE
        )
        
        self.assertEqual(DEFAULT_MAX_ROWS, 100)
        self.assertEqual(MAX_ALLOWED_ROWS, 10000)
        self.assertEqual(MIN_ALLOWED_ROWS, 10)
        self.assertIsNotNone(APP_TITLE)


class TestAppImports(unittest.TestCase):
    """Test app module imports"""
    
    def test_app_py_imports(self):
        """Test that app.py has valid imports"""
        try:
            import streamlit
            import pandas
            from databricks import sql
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Missing dependency: {str(e)}")


class TestDeploymentScripts(unittest.TestCase):
    """Test deployment scripts"""
    
    def test_deployment_script_exists(self):
        """Test that deployment scripts exist"""
        import os
        from pathlib import Path
        
        base_path = Path(__file__).parent.parent
        self.assertTrue((base_path / "scripts" / "deploy_to_databricks.py").exists())
        self.assertTrue((base_path / "scripts" / "verify_deployment.py").exists())
        self.assertTrue((base_path / "scripts" / "run_local.py").exists())


if __name__ == '__main__':
    unittest.main()
