import re

with open("frontend/src/styles.css", "r", encoding="utf-8") as f:
    css = f.read()

rule_search = """.status-btn.active-hvac {
  background: #A855F7;
  color: #FFFFFF;
  border-color: #C084FC;
  font-weight: 600;
  box-shadow: 0 0 8px rgba(168, 85, 247, 0.4);
}"""

rule_replace = """.status-btn.active-hvac {
  background: #A855F7;
  color: #FFFFFF;
  border-color: #C084FC;
  font-weight: 600;
  box-shadow: 0 0 8px rgba(168, 85, 247, 0.4);
}

.status-btn.active-resize {
  background: #0284C7;
  color: #FFFFFF;
  border-color: #38BDF8;
  font-weight: 600;
  box-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
}"""

if ".status-btn.active-resize" not in css:
    css = css.replace(rule_search, rule_replace)
    with open("frontend/src/styles.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("styles.css updated with .status-btn.active-resize")
