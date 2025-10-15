"""
Default configuration for embedded projects.
"""

DEFAULT_CONFIG = {
    "project_name": "firmware",
    "mcu": "cortex-m4",
    "compiler": "arm-none-eabi-gcc",
    "flash_size": "512K",
    "ram_size": "128K",
    "flash_start": "0x08000000",
    "ram_start": "0x20000000",
    "author": "Embedded Developer",
    "version": "1.0.0",
    
    # Supported MCU architectures
    "supported_mcus": [
        "cortex-m0",
        "cortex-m0+", 
        "cortex-m3",
        "cortex-m4",
        "cortex-m7",
        "cortex-m33",
        "riscv32",
        "avr"
    ],
    
    # Supported compilers
    "supported_compilers": [
        "arm-none-eabi-gcc",
        "riscv32-unknown-elf-gcc",
        "avr-gcc",
        "clang"
    ],
    
    # Common memory sizes
    "common_flash_sizes": ["64K", "128K", "256K", "512K", "1M", "2M"],
    
    "common_ram_sizes": [ "16K", "32K", "64K", "128K", "256K", "512K", "1M"],
    
    # Default file templates
    "templates": {
        "makefile": "makefile.j2",
        "main_c": "main_c.j2", 
        "config_h": "config_h.j2",
        "linker_script": "linker_script.j2",
        "flash_tool": "flash_tool.j2",
        "debug_config": "debug_config.j2",
        "test_main": "test_main.j2",
        "readme": "readme.j2",
        "gitignore": "gitignore.j2"
    },
    
    # Default directories to create
    "directories": [
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
}