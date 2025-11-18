// API base URL
const API_BASE = 'http://localhost:5000/api';

// DOM elements
let currentTab = 'dashboard';

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    loadFirewalls();
    loadLogs();
    setupEventListeners();
});

function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('nav a').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            switchTab(tab.dataset.tab);
        });
    });

    // Deploy form
    document.getElementById('deployForm').addEventListener('submit', deployFirewall);

    // Buttons
    document.getElementById('refreshBtn').addEventListener('click', loadFirewalls);
    document.getElementById('refreshLogsBtn').addEventListener('click', loadLogs);
    document.getElementById('deployFromListBtn').addEventListener('click', () => switchTab('deploy'));
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all nav items
    document.querySelectorAll('nav a').forEach(navItem => {
        navItem.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Activate corresponding nav item
    document.querySelector(`nav a[data-tab="${tabName}"]`).classList.add('active');
    
    currentTab = tabName;
    
    // Refresh data if needed
    if (tabName === 'firewalls' || tabName === 'dashboard') {
        loadFirewalls();
    } else if (tabName === 'logs') {
        loadLogs();
    }
}

async function loadFirewalls() {
    try {
        const response = await fetch(`${API_BASE}/firewalls`);
        const data = await response.json();
        
        if (data.firewalls) {
            renderFirewalls(data.firewalls);
            updateStatistics(data.firewalls);
        }
    } catch (error) {
        console.error('Error loading firewalls:', error);
        showNotification('Error loading firewalls', 'error');
    }
}

async function loadLogs() {
    try {
        const response = await fetch(`${API_BASE}/logs`);
        const data = await response.json();
        
        if (data.logs) {
            renderLogs(data.logs);
        }
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

function renderFirewalls(firewalls) {
    const firewallsContainer = document.getElementById('firewallsList');
    const dashboardContainer = document.getElementById('dashboardFirewalls');
    
    if (firewallsContainer) {
        firewallsContainer.innerHTML = firewalls.map(firewall => createFirewallCard(firewall)).join('');
    }
    
    if (dashboardContainer) {
        // Show only running firewalls on dashboard
        const runningFirewalls = firewalls.filter(fw => fw.status === 'running');
        dashboardContainer.innerHTML = runningFirewalls.map(firewall => createFirewallCard(firewall)).join('');
    }
    
    // Add event listeners to action buttons
    document.querySelectorAll('.btn-start, .btn-stop, .btn-configure, .btn-delete').forEach(btn => {
        btn.addEventListener('click', handleFirewallAction);
    });
}

function createFirewallCard(firewall) {
    const statusClass = `status-${firewall.status}`;
    const actionButton = firewall.status === 'running' ? 
        '<button class="btn btn-danger btn-stop" data-id="' + firewall.id + '"><span>⏹️</span> Stop</button>' :
        '<button class="btn btn-success btn-start" data-id="' + firewall.id + '"><span>▶️</span> Start</button>';
    
    return `
        <div class="card">
            <div class="card-header">
                <div class="card-title"><span>🛡️</span> ${firewall.name}</div>
                <div class="status ${statusClass}">${firewall.status}</div>
            </div>
            <div class="card-content">
                <p><strong>IP:</strong> ${firewall.management_ip}</p>
                <p><strong>Subnet:</strong> ${firewall.subnet}</p>
                <p><strong>Resources:</strong> ${firewall.vcpu} vCPU, ${firewall.ram}GB RAM</p>
                <p><strong>Policy:</strong> ${firewall.security_policy}</p>
                <div class="tech-badge">OSM</div>
                <div class="tech-badge">OpenFlow</div>
                <div class="tech-badge">NETCONF</div>
            </div>
            <div class="card-footer">
                ${actionButton}
                <button class="btn btn-configure" data-id="${firewall.id}"><span>⚙️</span> Configure</button>
                <button class="btn btn-danger btn-delete" data-id="${firewall.id}"><span>🗑️</span> Delete</button>
            </div>
        </div>
    `;
}

function updateStatistics(firewalls) {
    const statsContainer = document.getElementById('statistics');
    if (!statsContainer) return;
    
    const running = firewalls.filter(fw => fw.status === 'running').length;
    const stopped = firewalls.filter(fw => fw.status === 'stopped').length;
    const total = firewalls.length;
    
    statsContainer.innerHTML = `
        <div class="stat-card">
            <div class="stat-value">${running}</div>
            <div class="stat-label">Active Firewalls</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${stopped}</div>
            <div class="stat-label">Stopped Firewalls</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${total}</div>
            <div class="stat-label">Total Firewalls</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">98.7%</div>
            <div class="stat-label">System Uptime</div>
        </div>
    `;
}

function renderLogs(logs) {
    const logsContainer = document.getElementById('systemLogs');
    if (!logsContainer) return;
    
    logsContainer.innerHTML = logs.map(log => {
        const level = log.match(/\[(INFO|ERROR|WARNING|SUCCESS)\]/)?.[1] || 'INFO';
        return `<div class="log-entry log-${level.toLowerCase()}">${log}</div>`;
    }).join('');
    
    logsContainer.scrollTop = logsContainer.scrollHeight;
}

async function deployFirewall(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('fwName').value,
        management_ip: document.getElementById('managementIP').value,
        subnet: document.getElementById('subnet').value,
        vcpu: parseInt(document.getElementById('vCPU').value),
        ram: parseInt(document.getElementById('ram').value),
        security_policy: document.getElementById('securityPolicy').value,
        config_method: document.getElementById('configMethod').value
    };
    
    try {
        showDeploymentProgress();
        
        const response = await fetch(`${API_BASE}/firewalls/deploy`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('Firewall deployed successfully!', 'success');
            document.getElementById('deployForm').reset();
            hideDeploymentProgress();
            loadFirewalls();
            loadLogs();
        } else {
            throw new Error(result.error || 'Deployment failed');
        }
    } catch (error) {
        console.error('Deployment error:', error);
        showNotification('Deployment failed: ' + error.message, 'error');
        hideDeploymentProgress();
    }
}

async function handleFirewallAction(e) {
    const firewallId = e.target.dataset.id;
    const action = e.target.classList[2]; // btn-start, btn-stop, etc.
    
    try {
        let endpoint, method;
        
        switch (action) {
            case 'btn-start':
                endpoint = `${API_BASE}/firewalls/${firewallId}/start`;
                method = 'POST';
                break;
            case 'btn-stop':
                endpoint = `${API_BASE}/firewalls/${firewallId}/stop`;
                method = 'POST';
                break;
            case 'btn-delete':
                if (!confirm('Are you sure you want to delete this firewall?')) return;
                endpoint = `${API_BASE}/firewalls/${firewallId}`;
                method = 'DELETE';
                break;
            case 'btn-configure':
                // Open configuration modal or page
                showNotification('Configuration feature coming soon!', 'info');
                return;
        }
        
        const response = await fetch(endpoint, { method });
        const result = await response.json();
        
        if (result.success) {
            showNotification(`Firewall ${action.replace('btn-', '')} operation successful!`, 'success');
            loadFirewalls();
            loadLogs();
        } else {
            throw new Error(result.error || 'Operation failed');
        }
    } catch (error) {
        console.error('Action error:', error);
        showNotification('Operation failed: ' + error.message, 'error');
    }
}

function showDeploymentProgress() {
    const progressElement = document.getElementById('deploymentProgress');
    const progressBar = document.getElementById('progressBar');
    
    progressElement.style.display = 'block';
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += 5;
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 200);
}

function hideDeploymentProgress() {
    const progressElement = document.getElementById('deploymentProgress');
    const progressBar = document.getElementById('progressBar');
    
    progressElement.style.display = 'none';
    progressBar.style.width = '0%';
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
        <span class="notification-message">${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}