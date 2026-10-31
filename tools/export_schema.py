"""Export the canonical embedded JSON Schema without running the application."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
html=(root/'tetris.html').read_text()
value=json.loads(re.search(r'<script id="save-schema" type="application/schema\+json">([\s\S]*?)</script>',html)[1])
(root/'schemas/tetris-save.schema.json').write_text(json.dumps(value,indent=2)+'\n')
