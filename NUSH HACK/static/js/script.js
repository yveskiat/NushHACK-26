const statusBanner = document.getElementById('statusBanner');
const userInput = document.getElementById('userInput');
const syncStatus = document.getElementById('syncStatus');

// --- 1. LOCAL STORAGE STORAGE ENGINES ---
function setLocalBackup(text) {
    localStorage.setItem('supabaseBackupText', text);
}

function getLocalBackup() {
    return localStorage.getItem('supabaseBackupText') || '';
}

// --- 2. BACKEND COMM LINK TO FLASK ---
async function saveToFlaskBridge(text) {
    try {
        const response = await fetch('/sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        return response.ok;
    } catch (error) {
        console.error("Flask bridge connection down:", error);
        return false;
    }
}

// --- 3. LIVE TYPING AUTO-SAVE ENGINE ---
userInput.addEventListener('input', async (e) => {
    const currentText = e.target.value;
    setLocalBackup(currentText); // Always secure a local JSON string backup first

    if (navigator.onLine) {
        syncStatus.textContent = "Syncing workspace to cloud...";
        const success = await saveToFlaskBridge(currentText);
        if (success) {
            syncStatus.textContent = "● All changes saved in Supabase";
            localStorage.removeItem('offlinePendingSync'); // Clear dirty state
        } else {
            syncStatus.textContent = "⚠️ Server bottleneck. Saved locally as JSON.";
            localStorage.setItem('offlinePendingSync', 'true');
        }
    } else {
        syncStatus.textContent = "○ Saved offline (Pending JSON sync)";
        localStorage.setItem('offlinePendingSync', 'true');
    }
});

// --- 4. NETWORK RECONNECT ENGINE ---
async function handleNetworkReconnect() {
    if (navigator.onLine) {
        statusBanner.textContent = "● ONLINE: Cloud Connection Active";
        statusBanner.className = "status-banner online";
        
        // If we have changes waiting that missed the backend while offline, push them now
        if (localStorage.getItem('offlinePendingSync') === 'true') {
            syncStatus.textContent = "Flushing offline adjustments to Supabase...";
            const success = await saveToFlaskBridge(getLocalBackup());
            if (success) {
                syncStatus.textContent = "● Offline queue flushed & synced successfully!";
                localStorage.removeItem('offlinePendingSync');
            } else {
                syncStatus.textContent = "⚠️ Reconnect flush failed. Retrying on next change.";
            }
        } else {
            syncStatus.textContent = "● All changes saved in Supabase";
        }
    } else {
        statusBanner.textContent = "○ OFFLINE: Storing changes to local JSON queue";
        statusBanner.className = "status-banner offline";
        syncStatus.textContent = "○ Changes locked locally until internet returns";
    }
}

// Bind live connectivity hardware listeners
window.addEventListener('online', handleNetworkReconnect);
window.addEventListener('offline', handleNetworkReconnect);
window.addEventListener('load', () => {
    handleNetworkReconnect();
});
