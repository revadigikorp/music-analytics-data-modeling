/**
 * Music Analytics Dashboard
 * JavaScript for data loading and chart rendering
 */

// Chart.js default configuration
Chart.defaults.color = '#a0aec0';
Chart.defaults.borderColor = 'rgba(139, 92, 246, 0.2)';

// Color palette for charts
const chartColors = {
    primary: '#8b5cf6',
    secondary: '#a78bfa',
    gradient: (ctx) => {
        const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(139, 92, 246, 0.8)');
        gradient.addColorStop(1, 'rgba(139, 92, 246, 0.1)');
        return gradient;
    },
    pieColors: ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#ec4899']
};

// Dashboard data
let dashboardData = null;

/**
 * Load dashboard data from JSON file
 */
async function loadData() {
    try {
        const response = await fetch('data/dashboard_data.json');
        if (!response.ok) {
            throw new Error('Data file not found. Run generate_data.py first.');
        }
        dashboardData = await response.json();
        renderDashboard();
    } catch (error) {
        console.error('Error loading data:', error);
        showError(error.message);
    }
}

/**
 * Show error message
 */
function showError(message) {
    document.querySelector('.main-content').innerHTML = `
        <div class="chart-card full-width" style="text-align: center; padding: 60px;">
            <h3>⚠️ Unable to Load Data</h3>
            <p style="margin-top: 16px; color: var(--text-secondary);">${message}</p>
            <p style="margin-top: 8px; color: var(--text-muted);">
                Run: <code style="background: var(--bg-secondary); padding: 4px 8px; border-radius: 4px;">
                python dashboard/generate_data.py</code>
            </p>
        </div>
    `;
}

/**
 * Render all dashboard components
 */
function renderDashboard() {
    updateStats();
    updateTopSongs();
    updateTopArtists();
    updateTopLocations();
    updateRecentActivity();
    renderHourlyChart();
    renderDailyChart();
    renderLevelsChart();
    updateLastUpdated();
}

/**
 * Update stat cards
 */
function updateStats() {
    const { overview } = dashboardData;

    animateValue('totalUsers', 0, overview.total_users, 800);
    animateValue('totalSongs', 0, overview.total_songs, 800);
    animateValue('totalArtists', 0, overview.total_artists, 800);
    animateValue('totalPlays', 0, overview.total_songplays, 800);
}

/**
 * Animate number counting
 */
function animateValue(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    const range = end - start;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeProgress = 1 - Math.pow(1 - progress, 3); // Ease out cubic

        element.textContent = Math.floor(start + range * easeProgress).toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/**
 * Update top songs list
 */
function updateTopSongs() {
    const container = document.getElementById('topSongsList');
    const { topSongs } = dashboardData;

    container.innerHTML = topSongs.map((song, i) => `
        <div class="list-item">
            <span class="list-item-rank">${i + 1}</span>
            <div class="list-item-info">
                <div class="list-item-title">${song.title}</div>
                <div class="list-item-subtitle">${song.artist}</div>
            </div>
            <span class="list-item-value">${song.plays} plays</span>
        </div>
    `).join('');
}

/**
 * Update top artists list
 */
function updateTopArtists() {
    const container = document.getElementById('topArtistsList');
    const { topArtists } = dashboardData;

    container.innerHTML = topArtists.map((artist, i) => `
        <div class="list-item">
            <span class="list-item-rank">${i + 1}</span>
            <div class="list-item-info">
                <div class="list-item-title">${artist.name}</div>
            </div>
            <span class="list-item-value">${artist.plays} plays</span>
        </div>
    `).join('');
}

/**
 * Update top locations list
 */
function updateTopLocations() {
    const container = document.getElementById('topLocationsList');
    const { topLocations } = dashboardData;

    container.innerHTML = topLocations.map((loc, i) => `
        <div class="list-item">
            <span class="list-item-rank">${i + 1}</span>
            <div class="list-item-info">
                <div class="list-item-title">${loc.location}</div>
            </div>
            <span class="list-item-value">${loc.plays} plays</span>
        </div>
    `).join('');
}

/**
 * Update recent activity table
 */
function updateRecentActivity() {
    const tbody = document.getElementById('recentActivityBody');
    const { recentActivity } = dashboardData;

    tbody.innerHTML = recentActivity.map(activity => `
        <tr>
            <td>${activity.time}</td>
            <td>${activity.user}</td>
            <td>${activity.song}</td>
            <td>${activity.artist}</td>
        </tr>
    `).join('');
}

/**
 * Render hourly activity chart
 */
function renderHourlyChart() {
    const ctx = document.getElementById('hourlyChart').getContext('2d');
    const { hourlyActivity } = dashboardData;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hourlyActivity.map(h => `${h.hour}:00`),
            datasets: [{
                label: 'Plays',
                data: hourlyActivity.map(h => h.plays),
                backgroundColor: chartColors.gradient,
                borderColor: chartColors.primary,
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(139, 92, 246, 0.1)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

/**
 * Render daily activity chart
 */
function renderDailyChart() {
    const ctx = document.getElementById('dailyChart').getContext('2d');
    const { dailyActivity } = dashboardData;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dailyActivity.map(d => d.day),
            datasets: [{
                label: 'Plays',
                data: dailyActivity.map(d => d.plays),
                borderColor: chartColors.primary,
                backgroundColor: chartColors.gradient,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: chartColors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(139, 92, 246, 0.1)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

/**
 * Render subscription levels chart
 */
function renderLevelsChart() {
    const ctx = document.getElementById('levelsChart').getContext('2d');
    const { userLevels } = dashboardData;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: userLevels.map(l => l.level),
            datasets: [{
                data: userLevels.map(l => l.count),
                backgroundColor: chartColors.pieColors.slice(0, userLevels.length),
                borderColor: '#16213e',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            },
            cutout: '60%'
        }
    });
}

/**
 * Update last updated timestamp
 */
function updateLastUpdated() {
    const element = document.getElementById('lastUpdated');
    const date = new Date(dashboardData.generatedAt);
    element.textContent = `Last updated: ${date.toLocaleString()}`;
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', loadData);
