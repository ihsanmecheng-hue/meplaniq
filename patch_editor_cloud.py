import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
import_search = "import Toast from '../Toast';"
import_replace = """import Toast from '../Toast';
import CloudModal from '../CloudModal';
import { getCurrentUser, saveProjectToCloud } from '../supabaseClient';"""

if "CloudModal" not in content:
    content = content.replace(import_search, import_replace)

# 2. Add State in EditorPage
state_search = "const [error, setError] = useState(null);"
state_replace = """const [error, setError] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const [isCloudModalOpen, setIsCloudModalOpen] = useState(false);
  const [cloudModalInitialTab, setCloudModalInitialTab] = useState('projects');"""

if "isCloudModalOpen" not in content:
    content = content.replace(state_search, state_replace)

# 3. Add useEffect to restore user and handlers
handler_search = "  const fileInputRef = useRef(null);"
handler_replace = """  const fileInputRef = useRef(null);

  useEffect(() => {
    getCurrentUser().then(user => {
      if (user) setCurrentUser(user);
    });
  }, []);

  const handleSaveToCloud = async () => {
    if (!currentUser) {
      setCloudModalInitialTab('auth');
      setIsCloudModalOpen(true);
      return;
    }
    if (!solveData) {
      showToast("No active floorplan to save.", "error");
      return;
    }
    try {
      const res = await saveProjectToCloud(currentUser, solveData);
      showToast(`Floorplan successfully saved to ${res.storageType}!`, "success");
    } catch (err) {
      console.error("Cloud save error:", err);
      showToast(err.message || "Failed to save to Cloud.", "error");
    }
  };

  const handleOpenCloudVault = () => {
    if (!currentUser) {
      setCloudModalInitialTab('auth');
    } else {
      setCloudModalInitialTab('projects');
    }
    setIsCloudModalOpen(true);
  };

  const handleLoadCloudProject = async (cadPayload) => {
    if (!cadPayload) return;
    try {
      let solved;
      if (cadPayload.rooms) {
        solved = await createManualProject({
          name: cadPayload.project_name || "Cloud Floorplan",
          rooms: cadPayload.rooms.map(r => ({ name: r.name, points: r.points, fillet_radius: 0.0 })),
          openings: cadPayload.openings || [],
          hvac_equipment: cadPayload.hvac_equipment || []
        });
      }
      if (solved) {
        setSolveData(solved);
        setEditableDoors(solved.doors || []);
        setEditableWindows(solved.windows || []);
        setEditableHvac(solved.hvac_equipment || []);
        setIsDirty(false);
        if (solved.rooms) {
          setViewTransform(calculateFitView(solved.rooms));
        }
        if (solved.project_id) {
          navigate(`/editor/${solved.project_id}`, { replace: true });
        }
        showToast(`Loaded "${cadPayload.project_name || 'Floorplan'}" from Cloud Database!`, "success");
      }
    } catch (err) {
      console.error("Failed to solve cloud floorplan:", err);
      setSolveData(cadPayload);
      showToast("Loaded floorplan from cloud cache.", "info");
    }
  };"""

if "handleSaveToCloud" not in content:
    content = content.replace(handler_search, handler_replace)

# 4. Add Cloud Buttons into .header-actions (right before Save Changes)
header_search = """        <div className="header-actions">
          {/* Save Changes Button */}"""

header_replace = """        <div className="header-actions">
          {/* Cloud Database Integration Buttons */}
          <button
            className="btn-secondary"
            onClick={handleOpenCloudVault}
            style={{
              backgroundColor: '#1E293B',
              borderColor: '#38BDF8',
              color: '#38BDF8',
              padding: '6px 12px',
              fontSize: '12px',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              borderRadius: '6px'
            }}
            title="Open Cloud Floorplans Vault (Supabase Database)"
          >
            <span>☁</span>
            {currentUser ? `Cloud: ${currentUser.email.split('@')[0]}` : "Cloud Account"}
          </button>

          <button
            className="btn-secondary"
            onClick={handleSaveToCloud}
            disabled={!solveData}
            style={{
              backgroundColor: '#0284C7',
              borderColor: '#38BDF8',
              color: '#FFFFFF',
              padding: '6px 12px',
              fontSize: '12px',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              borderRadius: '6px'
            }}
            title="Backup complete CAD project state to Cloud Database"
          >
            <span>☁↑</span>
            Save to Cloud
          </button>

          {/* Save Changes Button */}"""

if "Save to Cloud" not in content:
    content = content.replace(header_search, header_replace)

# 5. Add CloudModal right before Toast
modal_search = """      <Toast toast={toast} onClose={() => setToast(null)} />"""
modal_replace = """      <CloudModal
        isOpen={isCloudModalOpen}
        onClose={() => setIsCloudModalOpen(false)}
        currentUser={currentUser}
        onUserChange={setCurrentUser}
        currentProjectData={solveData}
        onLoadCloudProject={handleLoadCloudProject}
        onSaveToCloud={handleSaveToCloud}
        initialTab={cloudModalInitialTab}
      />
      <Toast toast={toast} onClose={() => setToast(null)} />"""

if "<CloudModal" not in content:
    content = content.replace(modal_search, modal_replace)

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("EditorPage.jsx successfully updated with Cloud Database Integration.")
