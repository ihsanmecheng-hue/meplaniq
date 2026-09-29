with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add state
search_state = "const [showHvac, setShowHvac] = useState(true);"
replace_state = """const [showHvac, setShowHvac] = useState(true);
  const [isResizeModeActive, setIsResizeModeActive] = useState(false);"""

if "isResizeModeActive" not in code:
    code = code.replace(search_state, replace_state, 1)

# 2. Add isResizeModeActive to Canvas
search_canvas = """            showHvac={showHvac}
              onLiveItemUpdate={handleLiveItemUpdate}"""

replace_canvas = """            showHvac={showHvac}
            isResizeModeActive={isResizeModeActive}
            onLiveItemUpdate={handleLiveItemUpdate}"""

code = code.replace(search_canvas, replace_canvas, 1)

# 3. Add isResizeModeActive and onToggleResizeMode to StatusBar
search_statusbar = """            showHvac={showHvac}
              onLiveItemUpdate={handleLiveItemUpdate}
            onToggleHvac={() => setShowHvac(prev => !prev)}
            onResetView={handleResetView}"""

replace_statusbar = """            showHvac={showHvac}
            onToggleHvac={() => setShowHvac(prev => !prev)}
            isResizeModeActive={isResizeModeActive}
            onToggleResizeMode={() => setIsResizeModeActive(prev => !prev)}
            onResetView={handleResetView}"""

code = code.replace(search_statusbar, replace_statusbar, 1)

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(code)

print("EditorPage.jsx updated with isResizeModeActive state & controls.")
