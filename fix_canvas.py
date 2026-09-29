
import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    c = f.read()

# Fix the Date.now() mistake first
c = c.replace("<Canvas key={solveData?.created_at || Date.now()}", "<Canvas key={canvasRenderKey}")

# Add canvasRenderKey to state
if "const [canvasRenderKey, setCanvasRenderKey]" not in c:
    c = c.replace(
        "const [activeTab, setActiveTab] = useState(", 
        "const [canvasRenderKey, setCanvasRenderKey] = useState(Date.now());\n  const [activeTab, setActiveTab] = useState("
    )

# Update canvasRenderKey when solveData is set
c = c.replace("setSolveData(updated);", "setSolveData(updated);\n      setCanvasRenderKey(Date.now());")
c = c.replace("setSolveData(solved);", "setSolveData(solved);\n      setCanvasRenderKey(Date.now());")

# Also on initial fetch!
if "setSolveData(data);" in c:
    c = c.replace("setSolveData(data);", "setSolveData(data);\n        setCanvasRenderKey(Date.now());")

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(c)

