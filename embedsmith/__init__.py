"""
embedsmith - A cli tool for creating standardized embedded project layouts.
Craft your embedded firmware with structure and best practices from day one.
"""

__version__ = "1.0.1"
__author__ = "Clement Cole"
__email__ = "clementacole75@gmail.com"

from .core import embedsmith, ProjectConfig, EmbeddedProjectCreator

__all__ = ['embedsmith', 'ProjectConfig', 'EmbeddedProjectCreator']