import os
from pathlib import Path
from string import Template


class TemplateManager:
    """Manage template loading and rendering for embedsmith"""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent
    
    def get_available_templates(self):
        """List all available templates"""
        return [f.name for f in self.template_dir.glob("*.j2")]
    
    def render(self, template_name: str, context: dict) -> str:
        """Render a template with the given context"""
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Simple template substitutions
        template = Template(template_content)
        return template.safe_substitute(context)