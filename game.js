// Sample network logs (Safe & Malicious)
const logs = [
    { ip: "192.168.1.10", action: "Successful Login", threat: false },
    { ip: "203.0.113.5", action: "Multiple Failed Logins", threat: true },
    { ip: "172.16.5.44", action: "Normal Browsing Activity", threat: false },
    { ip: "45.67.89.12", action: "Large Data Transfer at Midnight", threat: true },
    { ip: "10.0.0.7", action: "Email Sent", threat: false },
    { ip: "198.51.100.22", action: "Port Scan Detected", threat: true },
    { ip: "8.8.8.8", action: "Google Public DNS", threat: false},
    { ip: "1.1.1.1", action: "CloudFare DNS", threat: false},
    { ip: "185.234.219.5", action: "Phishing Site", threat: true },
    { ip: "192.42.116.41", action: "Open Proxy", threat: true}
];

let selectedLog = null;
let score = 0;

// Display logs in UI
function loadLogs() {
    const logList = document.getElementById("log-list");
    logList.innerHTML = "";
    logs.forEach((log, index) => {
        let li = document.createElement("li");
        li.textContent = `[${log.ip}] - ${log.action}`;
        li.dataset.index = index;
        li.onclick = () => selectLog(index);
        logList.appendChild(li);
    });
}

// Highlight selected log
function selectLog(index) {
    const logItems = document.querySelectorAll("#log-list li");
    logItems.forEach(item => item.classList.remove("selected"));
    
    logItems[index].classList.add("selected");
    selectedLog = logs[index];
}

// Block IP function
function blockIP() {
    if (!selectedLog) {
        alert("Select an IP first!");
        return;
    }
    
    if (selectedLog.threat) {
        alert(`✅ Correct! Blocked suspicious IP: ${selectedLog.ip}`);
        score += 10;
    } else {
        alert(`❌ Incorrect! That was a safe IP.`);
        score -= 5;
    }
    
    updateScore();
    removeLog(selectedLog.ip);
}

// Allow IP function
function allowIP() {
    if (!selectedLog) {
        alert("Select an IP first!");
        return;
    }
    
    if (!selectedLog.threat) {
        alert(`✅ Correct! Allowed safe IP: ${selectedLog.ip}`);
        score += 10;
    } else {
        alert(`❌ Incorrect! That was a malicious IP.`);
        score -= 5;
    }

    updateScore();
    removeLog(selectedLog.ip);
}

// Update Score UI
function updateScore() {
    document.getElementById("score").textContent = score;
}

// Remove log after action
function removeLog(ip) {
    const index = logs.findIndex(log => log.ip === ip);
    if (index > -1) {
        logs.splice(index, 1);
        loadLogs();
        selectedLog = null;
    }
}

// Load logs when game starts
window.onload = loadLogs;
