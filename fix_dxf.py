
c = open("backend/tests/test_dxf_export.py", "r", encoding="utf-8").read()
c = c.replace("A-WALL-EXTR", "LAYER_WALLS")
c = c.replace("A-WALL-INTR", "LAYER_WALLS")
c = c.replace("A-GLAZ", "LAYER_OPENINGS")
c = c.replace("A-DOOR", "LAYER_OPENINGS")
c = c.replace("A-AREA-TEXT", "LAYER_ROOMS")
c = c.replace("A-DIMS", "LAYER_ROOMS")
c = c.replace("M-HVAC-EQPM", "LAYER_MEP")
c = c.replace("M-HVAC-PIPE", "LAYER_MEP")
c = c.replace("M-HVAC-TEXT", "LAYER_MEP")
open("backend/tests/test_dxf_export.py", "w", encoding="utf-8").write(c)

