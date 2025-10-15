import pytest
import tempfile
import shutil
from pathlib import Path
from embedsmith import EmbedSmith, ProjectConfig


class TestEmbeddedProjectCreator:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir) / "test-project"
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_project_default(self):
        es = embedsmith(str(self.base_path))
        success = es.create_project(overwrite=True)
        
        assert success
        assert self.base_path.exists()
        assert (self.base_path / "firmware" / "src").exists()
        assert (self.base_path / "firmware" / "include").exists()
        assert (self.base_path / "firmware" / "Makefile").exists()
    
    def test_create_project_custom_config(self):
        config = ProjectConfig(
            project_name="test-firmware",
            mcu="cortex-m7",
            flash_size="1M"
        )
        
        es = embedsmith(str(self.base_path), config)
        success = es.create_project(overwrite=True)
        
        assert success
        assert (self.base_path / "project_config.json").exists()
        
        # Verify configuration is applied
        with open(self.base_path / "firmware" / "Makefile", 'r') as f:
            makefile_content = f.read()
            assert "cortex-m7" in makefile_content
    
    def test_project_structure(self):
        es = embedsmith(str(self.base_path))
        es.create_project(overwrite=True)
        
        expected_dirs = [
            "firmware/src",
            "firmware/include", 
            "firmware/linker_scripts",
            "firmware/build",
            "tools/scripts",
            "tools/configs",
            "tests",
            "docs",
            "hardware"
        ]
        
        for dir_path in expected_dirs:
            assert (self.base_path / dir_path).exists()
    
    def test_file_creation(self):
        es = embedsmith(str(self.base_path))
        es.create_project(overwrite=True)
        
        expected_files = [
            "firmware/Makefile",
            "firmware/src/main.c", 
            "firmware/include/config.h",
            "firmware/linker_scripts/linker_script.ld",
            "tools/scripts/flash_tool.py",
            "tools/configs/debug_config.json",
            "tests/test_main.py",
            "docs/README.md",
            ".gitignore",
            "project_config.json"