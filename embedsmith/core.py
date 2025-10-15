import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import shutil
from .templates import TemplateManager


@dataclass
class ProjectConfig:
    """Configuration for crafting embedded projects"""
    project_name: str = "firmware"
    mcu: str = "cortex-m4"
    compiler: str = "arm-none-eabi-gcc"
    flash_size: str = "512K"
    ram_size: str = "128K"
    flash_start: str = "0x08000000"
    ram_start: str = "0x20000000"
    author: str = "Embedded Developer"
    version: str = "1.0.0"
    license: str = "MIT"
    description: str = "Embedded firmware project"


class EmbeddedProjectCreator:
    """Main class for crafting embedded project layouts"""
    
    def __init__(self, base_path: str = ".", config: Optional[ProjectConfig] = None):
        self.base_path = Path(base_path)
        self.config = config or ProjectConfig()
        self.template_manager = TemplateManager()
        
    def create_directory(self, path: Path) -> bool:
        """Create directory if it doesn't exist"""
        try:
            path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created: {path}")
            return True
        except OSError as error:
            print(f"❌ Error creating {path}: {error}")
            return False
    
    def create_file(self, filepath: Path, content: str = "") -> bool:
        """Create a file with content"""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Make scripts executable
            if filepath.suffix == '.py' or 'flash_tool' in filepath.name:
                filepath.chmod(0o755)
                
            print(f"📄 Created: {filepath}")
            return True
        except OSError as error:
            print(f"❌ Error creating {filepath}: {error}")
            return False
    
    def get_directory_structure(self) -> List[Path]:
        """Get the complete directory structure for embedded projects"""
        return [
            # Firmware structure
            self.base_path / "firmware" / "src",
            self.base_path / "firmware" / "include",
            self.base_path / "firmware" / "linker_scripts",
            self.base_path / "firmware" / "build",
            self.base_path / "firmware" / "drivers",
            
            # Tools structure
            self.base_path / "tools" / "scripts",
            self.base_path / "tools" / "configs",
            self.base_path / "tools" / "utilities",
            
            # Tests and docs
            self.base_path / "tests" / "unit",
            self.base_path / "tests" / "integration",
            self.base_path / "docs" / "api",
            self.base_path / "docs" / "hardware",
            
            # Hardware and deployment
            self.base_path / "hardware" / "schematics",
            self.base_path / "hardware" / "pcb",
            self.base_path / "hardware" / "3d_models",
            
            # Configuration and scripts
            self.base_path / "config",
            self.base_path / "scripts",
            self.base_path / "utils",
        ]
    
    def get_files_to_create(self) -> List[tuple]:
        """Get list of files to create with their templates"""
        template_context = asdict(self.config)
        
        return [
            # Firmware files
            (self.base_path / "firmware" / "Makefile", 
            self.template_manager.render("makefile.j2", template_context)),
            
            (self.base_path / "firmware" / "src" / "main.c", 
            self.template_manager.render("main_c.j2", template_context)),
            
            (self.base_path / "firmware" / "src" / "system.c", 
            self.template_manager.render("system_c.j2", template_context)),
            
            (self.base_path / "firmware" / "include" / "config.h", 
            self.template_manager.render("config_h.j2", template_context)),
            
            (self.base_path / "firmware" / "include" / "system.h", 
            self.template_manager.render("system_h.j2", template_context)),
            
            (self.base_path / "firmware" / "linker_scripts" / "linker_script.ld", 
            self.template_manager.render("linker_script.j2", template_context)),
            
            (self.base_path / "firmware" / "drivers" / "gpio.c", 
            self.template_manager.render("gpio_c.j2", template_context)),
            
            # Tool files
            (self.base_path / "tools" / "scripts" / "flash_tool.py", 
            self.template_manager.render("flash_tool.j2", template_context)),
            
            (self.base_path / "tools" / "scripts" / "debug_tool.py", 
            self.template_manager.render("debug_tool.j2", template_context)),
            
            (self.base_path / "tools" / "configs" / "debug_config.json", 
            self.template_manager.render("debug_config.j2", template_context)),
            
            (self.base_path / "tools" / "utilities" / "memory_analyzer.py", 
            self.template_manager.render("memory_analyzer.j2", template_context)),
            
            # Test files
            (self.base_path / "tests" / "unit" / "test_main.py", 
            self.template_manager.render("test_main.j2", template_context)),
            
            (self.base_path / "tests" / "integration" / "test_hardware.py", 
            self.template_manager.render("test_hardware.j2", template_context)),
            
            # Documentation
            (self.base_path / "docs" / "README.md", 
            self.template_manager.render("readme.j2", template_context)),
            
            (self.base_path / "docs" / "api" / "index.md", 
            self.template_manager.render("api_docs.j2", template_context)),
            
            (self.base_path / "docs" / "hardware" / "specification.md", 
            self.template_manager.render("hardware_spec.j2", template_context)),
            
            # Configuration and meta files
            (self.base_path / ".gitignore", 
            self.template_manager.render("gitignore.j2", template_context)),
            
            (self.base_path / "LICENSE", 
            self.template_manager.render("license.j2", template_context)),
            
            (self.base_path / "embedsmith.json", 
            json.dumps(template_context, indent=2)),
            
            (self.base_path / "project_guide.md", 
            self.template_manager.render("project_guide.j2", template_context)),
            
            # Scripts
            (self.base_path / "scripts" / "build.sh", 
            self.template_manager.render("build_sh.j2", template_context)),
            
            (self.base_path / "scripts" / "deploy.sh", 
            self.template_manager.render("deploy_sh.j2", template_context)),
        ]
    
    def create_project(self, overwrite: bool = False) -> bool:
        """Craft the complete embedded project"""
        
        if self.base_path.exists() and self.base_path.is_dir():
            if not overwrite:
                response = input(f"🔄 The directory '{self.base_path}' already exists. Overwrite? (y/N): ")
                if response.lower() != 'y':
                    print("❌ Operation cancelled.")
                    return False
            else:
                print(f"🔄 Overwriting existing directory: {self.base_path}")
        
        print(f"🚀 Crafting embedded project at: {self.base_path}/")
        print(f"📋 Project: {self.config.project_name}")
        print(f"🔧 MCU: {self.config.mcu}")
        print(f"⚡ Flash: {self.config.flash_size}, RAM: {self.config.ram_size}")
        
        # Create directories
        print("\n📁 Creating project structure...")
        directories = self.get_directory_structure()
        for directory in directories:
            if not self.create_directory(directory):
                return False
        
        # Create files
        print("\n📄 Generating project files...")
        files = self.get_files_to_create()
        for filepath, content in files:
            if not self.create_file(filepath, content):
                return False
        
        return True
    
    def print_structure(self):
        """Print the crafted project structure"""
        print("\n🏗️  Project Structure:")
        print("embedsmith-project/")
        print("├── firmware/")
        print("│   ├── src/                 # Source files")
        print("│   ├── include/             # Header files")
        print("│   ├── linker_scripts/      # Memory configuration")
        print("│   ├── drivers/             # Hardware drivers")
        print("│   └── build/               # Build artifacts")
        print("├── tools/")
        print("│   ├── scripts/             # Flash/debug scripts")
        print("│   ├── configs/             # Tool configurations")
        print("│   └── utilities/           # Analysis tools")
        print("├── tests/")
        print("│   ├── unit/                # Unit tests")
        print("│   └── integration/         # Hardware tests")
        print("├── docs/")
        print("│   ├── api/                 # API documentation")
        print("│   └── hardware/            # Hardware docs")
        print("├── hardware/")
        print("│   ├── schematics/          # Circuit diagrams")
        print("│   ├── pcb/                 # PCB layouts")
        print("│   └── 3d_models/           # Mechanical models")
        print("├── scripts/                 # Build/deploy scripts")
        print("├── config/                  # Project configuration")
        print("├── utils/                   # Utility functions")
        print("├── embedsmith.json          # Project metadata")
        print("└── project_guide.md         # Development guide")


def embedsmith(base_path: str = "embedded-project", config: Optional[ProjectConfig] = None, overwrite: bool = False) -> bool:
    """
    Convenience function to craft an embedded project.
    
    Args:
        base_path: Path where to create the project
        config: Project configuration
        overwrite: Whether to overwrite existing directory
    
    Returns:
        bool: True if successful, False otherwise
    """
    crafter = EmbeddedProjectCreator(base_path, config)
    success = crafter.create_project(overwrite)
    if success:
        crafter.print_structure()
        print(f"\n✅ Successfully crafted project at: {base_path}/")
        print("🎉 Happy coding! Start with 'firmware/src/main.c'")
    return success