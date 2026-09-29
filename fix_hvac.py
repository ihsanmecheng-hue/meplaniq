
with open("backend/tests/test_hvac.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("backend/tests/test_hvac.py", "w", encoding="utf-8") as f:
    for line in lines[:131]:
        f.write(line)
    f.write("""    # Verify MEP layers
    layer_names = [l.dxf.name for l in doc.layers]
    assert "LAYER_MEP" in layer_names

    eq_layer = doc.layers.get("LAYER_MEP")
    assert eq_layer.color == 6  # Magenta
    assert eq_layer.dxf.lineweight == 35

    msp = doc.modelspace()

    # Check equipment boxes and fan circle
    eq_polylines = [e for e in msp if e.dxftype() == "LWPOLYLINE" and e.dxf.layer == "LAYER_MEP"]
    assert len(eq_polylines) >= 2  # IDU and ODU

    circles = [e for e in msp if e.dxftype() == "CIRCLE" and e.dxf.layer == "LAYER_MEP"]
    assert len(circles) == 1  # 1 ODU condenser fan

    # Check text
    texts = [e for e in msp if e.dxftype() == "MTEXT" and e.dxf.layer == "LAYER_MEP"]
    assert len(texts) >= 3  # 2 eq + 1 pipe callout
""")

