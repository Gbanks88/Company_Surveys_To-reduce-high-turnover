class VentionDashboard {
    constructor(machineId = '1') {
        this.machineId = machineId;
        this.connected = false;
        this.ws = null;
        this.updateInterval = null;
        this.offlineMode = false;
        this.lastKnownData = this.loadFromLocalStorage() || {};
        this.initializeEventListeners();
        this.setupOfflineDetection();
        this.connect();
    }

    setupOfflineDetection() {
        window.addEventListener('online', () => {
            document.body.classList.remove('offline');
            this.offlineMode = false;
            this.connect();
        });

        window.addEventListener('offline', () => {
            document.body.classList.add('offline');
            this.offlineMode = true;
            this.updateMetrics(this.lastKnownData);
        });

        // Initial check
        if (!navigator.onLine) {
            document.body.classList.add('offline');
            this.offlineMode = true;
        }
    }

    loadFromLocalStorage() {
        try {
            const data = localStorage.getItem('dashboardData');
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('Error loading from localStorage:', error);
            return null;
        }
    }

    saveToLocalStorage(data) {
        try {
            localStorage.setItem('dashboardData', JSON.stringify(data));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }

    initializeEventListeners() {
        // Handle tab changes
        const tabs = document.querySelectorAll('[data-bs-toggle="tab"]');
        tabs.forEach(tab => {
            tab.addEventListener('shown.bs.tab', (event) => {
                if (event.target.id === 'requirements-tab') {
                    this.updateRequirements();
                } else if (event.target.id === 'vehicle-tab') {
                    this.updateVehicleMetrics();
                }
            });
        });
    }

    connect() {
        if (this.offlineMode) return;

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${this.machineId}`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('Connected to WebSocket');
            this.connected = true;
            this.updateConnectionStatus(true);
            this.startMetricUpdates();
        };
        
        this.ws.onclose = () => {
            console.log('Disconnected from WebSocket');
            this.connected = false;
            this.updateConnectionStatus(false);
            this.stopMetricUpdates();
            // Attempt to reconnect after 5 seconds if not offline
            if (!this.offlineMode) {
                setTimeout(() => this.connect(), 5000);
            }
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus(false);
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.lastKnownData = data;
            this.saveToLocalStorage(data);
            this.updateMetrics(data);
        };
    }

    updateConnectionStatus(connected) {
        const statusIndicator = document.getElementById('connection-status');
        statusIndicator.className = 'status-indicator ' + (connected ? 'status-good' : 'status-error');
    }

    startMetricUpdates() {
        if (this.offlineMode) return;

        // Request metrics every 1 second
        this.updateInterval = setInterval(() => {
            if (this.connected) {
                this.ws.send(JSON.stringify({ action: 'get_metrics' }));
            }
        }, 1000);
    }

    stopMetricUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    updateMetrics(data) {
        if (!data) return;

        // Update Machine Status Tab
        if (data.motion_state) {
            document.getElementById('position').textContent = JSON.stringify(data.motion_state.position);
            document.getElementById('velocity').textContent = JSON.stringify(data.motion_state.velocity);
            document.getElementById('acceleration').textContent = JSON.stringify(data.motion_state.acceleration);
        }

        if (data.safety_status) {
            document.getElementById('collision-risk').textContent = data.safety_status.collision_risk;
            document.getElementById('safety-zones').textContent = data.safety_status.safety_zones;
            document.getElementById('emergency-stop').textContent = data.safety_status.emergency_stop;
        }

        if (data.eco_metrics) {
            document.getElementById('power-usage').textContent = data.eco_metrics.power_usage + ' W';
            document.getElementById('carbon-footprint').textContent = data.eco_metrics.carbon_footprint + ' kg CO2';
            document.getElementById('efficiency-score').textContent = data.eco_metrics.efficiency_score + '%';
        }

        if (data.system_status) {
            document.getElementById('cpu-load').textContent = data.system_status.cpu_load + '%';
            document.getElementById('memory-usage').textContent = data.system_status.memory_usage + ' MB';
            document.getElementById('temperature').textContent = data.system_status.temperature + '°C';
        }

        if (data.maintenance_state) {
            document.getElementById('component-health').textContent = data.maintenance_state.component_health + '%';
            document.getElementById('next-service').textContent = data.maintenance_state.next_service;
            document.getElementById('wear-level').textContent = data.maintenance_state.wear_level + '%';
        }

        // Update Vehicle Metrics Tab
        if (data.vehicle_metrics) {
            if (data.vehicle_metrics.production) {
                document.getElementById('daily-output').textContent = data.vehicle_metrics.production.daily_output + ' units';
                document.getElementById('quality-score').textContent = data.vehicle_metrics.production.quality_score + '%';
                document.getElementById('cycle-time').textContent = data.vehicle_metrics.production.cycle_time + ' min';
            }

            if (data.vehicle_metrics.battery) {
                document.getElementById('battery-capacity').textContent = data.vehicle_metrics.battery.capacity + ' kWh';
                document.getElementById('charge-rate').textContent = data.vehicle_metrics.battery.charge_rate + ' kW';
                document.getElementById('battery-temp').textContent = data.vehicle_metrics.battery.temperature + '°C';
            }

            if (data.vehicle_metrics.safety) {
                document.getElementById('crash-rating').textContent = data.vehicle_metrics.safety.crash_rating;
                document.getElementById('safety-features').textContent = data.vehicle_metrics.safety.features_status;
                document.getElementById('compliance-score').textContent = data.vehicle_metrics.safety.compliance + '%';
            }
        }
    }

    updateRequirements() {
        // This would typically fetch requirements data from the server
        // For now, we're using static data from the HTML
        if (this.offlineMode) {
            console.log('Requirements tab accessed in offline mode');
            return;
        }
        console.log('Requirements tab activated');
    }

    updateVehicleMetrics() {
        // This would typically fetch vehicle metrics from the server
        if (this.offlineMode) {
            console.log('Vehicle metrics tab accessed in offline mode');
            return;
        }
        console.log('Vehicle metrics tab activated');
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.ventionDashboard = new VentionDashboard();
});
