
import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    code = f.read()

pattern = re.compile(
    r"(\} else if \(itemType === \"Room\"\) \{.*?newRooms = newRooms.map\(r => r.name === itemId \? \{ \.\.\.r, \.\.\.updates \} : r\);\n\s*\})",
    re.DOTALL
)

def replacer(match):
    return match.group(1) + """ else if (itemType === "AddRoom") {
        newRooms = [...newRooms, updates];
    }"""

new_code = pattern.sub(replacer, code)

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(new_code)

