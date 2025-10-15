#!/usr/bin/env python3
"""
Command-line interface for embedsmith
"""

import argparse
import sys
import json
from pathlib import Path
from .core import embedsmith, ProjectConfig


def main():
    parser = argparse.ArgumentParser(
        description="embedsmith - Craft professional embedded project layouts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
                Examples:
                embedsmith my-project                          # Create default project
                embedsmith --mcu cortex-m7 --flash 1M         # Custom MCU configuration
                embedsmith --config my_config.json            # Load from config file
                embedsmith . --overwrite                      # Create in current directory

                Quick Start:
                1. embedsmith my-embedded-firmware
                2. cd my-embedded-firmware/firmware
                3. make                                        # Build the project
                4. make flash                                  # Flash to device (configure first)

                Visit https://github.com/embedsmith/embedsmith for more examples and documentation.
        """
    )
    
    parser.add_argument(
        "project_path",
        nargs="?",
        default="embedded-project",
        help="Path where to craft the project (default: embedded-project)"
    )
    
    parser.add_argument(
        "--name", "--project-name",
        dest="project_name",
        default="firmware",
        help="Project name (default: firmware)"
    )
    
    parser.add_argument(
        "--mcu", "--architecture",
        dest="mcu",
        default="cortex-m4",
        help="MCU architecture (default: cortex-m4)"
    )
    
    parser.add_argument(
        "--compiler", "--toolchain",
        dest="compiler",
        default="arm-none-eabi-gcc",
        help="Compiler toolchain (default: arm-none-eabi-gcc)"
    )
    
    parser.add_argument(
        "--flash", "--flash-size",
        dest="flash_size",
        default="512K",
        help="Flash memory size (default: 512K)"
    )
    
    parser.add_argument(
        "--ram", "--ram-size",
        dest="ram_size",
        default="128K",
        help="RAM size (default: 128K)"
    )
    
    parser.add_argument(
        "--author",
        default="Embedded Developer",
        help="Project author (default: Embedded Developer)"
    )
    
    parser.add_argument(
        "--version",
        default="1.0.0",
        help="Project version (default: 1.0.0)"
    )
    
    parser.add_argument(
        "--license",
        default="MIT",
        choices=["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "Proprietary"],
        help="Project license (default: MIT)"
    )
    
    parser.add_argument(
        "--description",
        default="Embedded firmware project",
        help="Project description"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Load configuration from JSON file"
    )
    
    parser.add_argument(
        "--overwrite", "-f",
        action="store_true",
        help="Overwrite existing directory without prompting"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output (minimal messages only)"
    )
    
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available MCU presets and exit"
    )
    
    args = parser.parse_args()
    
    # List presets and exit
    if args.list_presets:
        print("Available MCU Presets:")
        print("  cortex-m0      - ARM Cortex-M0 (entry-level)")
        print("  cortex-m3      - ARM Cortex-M3 (mainstream)") 
        print("  cortex-m4      - ARM Cortex-M4 (DSP capabilities)")
        print("  cortex-m7      - ARM Cortex-M7 (high-performance)")
        print("  cortex-m33     - ARM Cortex-M33 (security features)")
        print("  riscv-rv32     - RISC-V RV32 (open architecture)")
        return
    
    # Load configuration from file if provided
    config = None
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config_data = json.load(f)
            config = ProjectConfig(**config_data)
            if not args.quiet:
                print(f"📁 Loaded configuration from: {args.config}")
        except Exception as e:
            print(f"❌ Error loading config file: {e}")
            sys.exit(1)
    else:
        # Create configuration from command line arguments
        config = ProjectConfig(
            project_name=args.project_name,
            mcu=args.mcu,
            compiler=args.compiler,
            flash_size=args.flash_size,
            ram_size=args.ram_size,
            author=args.author,
            version=args.version,
            license=args.license,
            description=args.description
        )
    
    # Create project
    try:
        success = embedsmith(
            base_path=args.project_path,
            config=config,
            overwrite=args.overwrite
        )
        
        if success:
            if not args.quiet:
                print(f"\n🎉 Successfully crafted '{config.project_name}' at '{args.project_path}'")
                print("🚀 Next steps:")
                print(f"   cd {args.project_path}/firmware")
                print("   make                        # Build the project")
                print("   make flash                  # Flash to device")
                print("   code .                      # Open in VS Code")
            sys.exit(0)
        else:
            if not args.quiet:
                print("❌ Failed to craft project")
            sys.exit(1)
            
    except KeyboardInterrupt:
        if not args.quiet:
            print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        if not args.quiet:
            print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()