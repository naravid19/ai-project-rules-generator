from __future__ import annotations
import re
import subprocess
import json
import tempfile
from pathlib import Path
from typing import Any

class DesignTokenEngine:
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def extract(self) -> dict[str, Any]:
        tokens = {"colors": {}, "fonts": {}, "spacing": {}}
        
        # 1. Tailwind
        tailwind_files = list(self.project_root.glob("tailwind.config.*"))
        for tf in tailwind_files:
            tw_tokens = self._extract_tailwind_via_node(tf)
            if not tw_tokens["colors"]:
                tw_tokens = self._extract_tailwind_fallback_regex(tf)
            
            self._deep_update(tokens, tw_tokens)
            
        # 2. CSS
        css_files = []
        for ext in ["*.css", "*.scss"]:
            css_files.extend(list(self.project_root.glob(ext)))
            css_files.extend(list((self.project_root / "src").glob(f"**/{ext}")))
        
        for cf in css_files:
            if "node_modules" in cf.parts:
                continue
            try:
                content = cf.read_text(encoding="utf-8", errors="ignore")
                css_tokens = self._parse_css_content(content)
                self._deep_update(tokens, css_tokens)
            except Exception:
                pass

        return tokens

    def _extract_tailwind_fallback_regex(self, config_path: Path) -> dict[str, Any]:
        tokens = {"colors": {}, "fonts": {}, "spacing": {}}
        try:
            content = config_path.read_text(encoding="utf-8", errors="ignore")
            # Simple regex for colors: "primary": "#hex"
            color_matches = re.findall(r'[\'"]([a-zA-Z0-9-]+)[\'"]\s*:\s*[\'"](#[a-fA-F0-9]{3,8}|(?:rgb|hsl)a?\([^)]+\))[\'"]', content)
            for name, value in color_matches:
                tokens["colors"][name] = value
            
            # Fonts: "sans": ["Inter", "sans-serif"]
            font_matches = re.findall(r'[\'"]([a-zA-Z0-9-]+)[\'"]\s*:\s*\[\s*([^\]]+)\s*\]', content)
            for name, value_list in font_matches:
                items = [v.strip().strip("'\"") for v in value_list.split(",")]
                tokens["fonts"][name] = items
        except Exception:
            pass
        return tokens

    def _deep_update(self, base: dict[str, Any], update: dict[str, Any]):
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key].update(value)
            else:
                base[key] = value

    def _parse_css_content(self, content: str) -> dict[str, Any]:
        tokens = {"colors": {}, "fonts": {}, "spacing": {}}
        # Match --var: value; patterns
        matches = re.findall(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);', content)
        for name, value in matches:
            v = value.strip()
            if v.startswith("#") or v.startswith("rgb") or v.startswith("hsl"):
                tokens["colors"][name] = v
            elif "font" in name.lower():
                tokens["fonts"][name] = v
            elif any(k in name.lower() for k in ["spacing", "gap", "padding", "margin"]):
                tokens["spacing"][name] = v
        return tokens

    def _extract_tailwind_via_node(self, config_path: Path) -> dict[str, Any]:
        if not config_path.exists(): return {"colors": {}, "fonts": {}, "spacing": {}}
        
        js_helper = f"""
        try {{
            const config = require('{config_path.resolve().as_posix()}');
            let theme = config.theme || config;
            
            // Try to resolve if tailwindcss is present
            try {{
                const resolveConfig = require('tailwindcss/resolveConfig');
                const fullConfig = resolveConfig(config);
                theme = fullConfig.theme;
            }} catch (e) {{}}
            
            console.log(JSON.stringify({{theme}}));
        }} catch (e) {{
            process.exit(1);
        }}
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(js_helper)
            temp_js = Path(f.name)
            
        try:
            res = subprocess.run(['node', str(temp_js)], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                theme = data.get("theme", {})
                return {
                    "colors": theme.get("colors", {}),
                    "fonts": theme.get("fontFamily", {}),
                    "spacing": theme.get("spacing", {})
                }
        except Exception:
            pass
        finally:
            temp_js.unlink(missing_ok=True)
        return {"colors": {}, "fonts": {}, "spacing": {}}
