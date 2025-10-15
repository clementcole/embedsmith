import pytest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner
from embedsmith.cli import main


class TestCLI:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.runner = CliRunner()
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_cli_help(self):
        result = self.runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Create standardized embedded project layouts' in result.output
    
    def test_cli_default_project(self):
        project_path = Path(self.temp_dir) / "test-project"
        result = self.runner.invoke(main, [str(project_path), '--overwrite'])
        
        assert result.exit_code == 0
        assert project_path.exists()
        assert (project_path / "firmware" / "Makefile").exists()
    
    def test_cli_custom_options(self):
        project_path = Path(self.temp_dir) / "custom-project"
        result = self.runner.invoke(main, [
            str(project_path),
            '--mcu', 'cortex-m7',
            '--flash-size', '1M',
            '--project-name', 'custom-firmware',
            '--overwrite'
        ])
        
        assert result.exit_code == 0
        assert (project_path / "project_config.json").exists()
        
        # Verify custom configuration
        with open(project_path / "firmware" / "Makefile", 'r') as f:
            content = f.read()
            assert "cortex-m7" in content
    
    def test_cli_quiet_mode(self):
        project_path = Path(self.temp_dir) / "quiet-project"
        result = self.runner.invoke(main, [
            str(project_path),
            '--overwrite',
            '--quiet'
        ])
        
        assert result.exit_code == 0
        assert project_path.exists()
        # In quiet mode, output should be minimal
        assert "Project created successfully" in result.output