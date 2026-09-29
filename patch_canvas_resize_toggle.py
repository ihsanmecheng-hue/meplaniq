import re

with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add isResizeModeActive = false to props
code = code.replace(
    "showHvac = true,\n  onCursorMove,",
    "showHvac = true,\n  isResizeModeActive = false,\n  onCursorMove,"
)

# 2. Wrap LAYER_ROOM_HANDLES with isResizeModeActive && ( ... )
pattern_handles = re.compile(
    r"(\{/\* INTERACTIVE ROOM CORNER & WALL RESIZE HANDLES \*/\}\s*)(\s*<g id=\"LAYER_ROOM_HANDLES\">.*?</g>)",
    re.DOTALL
)

def replace_handles(match):
    comment = match.group(1)
    g_tag = match.group(2)
    return f"{comment}{{isResizeModeActive && (\n  {g_tag}\n)}}\n"

code = pattern_handles.sub(replace_handles, code)

# 3. Wrap Floating Canvas Legend Tip with isResizeModeActive && ( ... )
pattern_legend = re.compile(
    r"(\{/\* Floating Canvas Legend Tip \*/\}\s*)(<div style=\{\{\s*position: 'absolute',\s*bottom: 12,.*?</div>)",
    re.DOTALL
)

def replace_legend(match):
    comment = match.group(1)
    div_tag = match.group(2)
    return f"{comment}{{isResizeModeActive && (\n  {div_tag}\n)}}\n"

code = pattern_legend.sub(replace_legend, code)

with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.write(code)

print("Canvas.jsx successfully updated with isResizeModeActive toggle.")
