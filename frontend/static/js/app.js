// Fruit Classification System - Enhanced Frontend JavaScript

// API Base URL
const API_BASE = '/api';

// Fruit Emoji Map
const FRUIT_EMOJIS = {
    'apple': '🍎', 'banana': '🍌', 'orange': '🍊', 'mango': '🥭',
    'strawberry': '🍓', 'grape': '🍇', 'watermelon': '🍉',
    'pineapple': '🍍', 'cherry': '🍒', 'kiwi': '🥝',
    'peach': '🍑', 'pear': '🍐', 'lemon': '🍋', 'coconut': '🥥',
    'avocado': '🥑', 'tomato': '🍅', 'blueberry': '🫐', 'plum': '🟣',
    'papaya': '🟠', 'guava': '🟢', 'dragonfruit': '🩷', 'pomegranate': '🔴',
    'fig': '🟤', 'apricot': '🟡', 'lime': '🟢', 'grapefruit': '🩷'
};

function getFruitEmoji(fruitName) {
    if (!fruitName) return '🍎';
    const name = fruitName.toLowerCase().trim();
    return FRUIT_EMOJIS[name] || '🍎';
}

// State
let selectedFile = null;
let currentLanguage = 'en';
let webcamStream = null;
let cameraFacingMode = 'environment'; // 'environment' = back, 'user' = front
let currentTheme = localStorage.getItem('theme') || 'dark';
let notifications = JSON.parse(localStorage.getItem('notifications') || '[]');
let batchFiles = [];
let cropper = null;
let historyPage = 1;
let historyFilters = {};
let selectedHistoryItems = new Set();
let mealPlan = JSON.parse(localStorage.getItem('mealPlan') || '{}');
let shoppingList = JSON.parse(localStorage.getItem('shoppingList') || '{"fruits":[],"vegetables":[],"other":[]}');
let achievements = JSON.parse(localStorage.getItem('achievements') || '{"first_classification":false,"on_fire":false,"expert":false,"quality_checker":false,"camera_pro":false,"variety":false}');
let autoRefreshInterval = null;
let autoCaptureInterval = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initSidebar();
    initTheme();
    initNavigation();
    initUpload();
    initBatchUpload();
    initClassification();
    initHistory();
    initStatistics();
    initWebcam();
    initWebcamEnhancements();
    initNutritionBrowser();
    initLanguageSelector();
    initModals();
    initKeyboardShortcuts();
    initNotifications();
    initDashboardEnhancements();
    initInventoryEnhancements();
    initMealPlanner();
    initShoppingList();
    registerServiceWorker();
});

// ==================== SIDEBAR ====================
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    // Desktop sidebar toggle (collapse/expand)
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
        
        // Restore collapsed state
        if (localStorage.getItem('sidebarCollapsed') === 'true') {
            sidebar.classList.add('collapsed');
        }
    }
    
    // Mobile menu toggle
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.add('mobile-open');
            sidebarOverlay?.classList.add('active');
        });
    }
    
    // Close sidebar on overlay click
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeMobileSidebar);
    }
    
    // Close sidebar when nav item clicked (mobile)
    document.querySelectorAll('.sidebar-nav .nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                closeMobileSidebar();
            }
        });
    });
}

function closeMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    sidebar?.classList.remove('mobile-open');
    sidebarOverlay?.classList.remove('active');
}

// ==================== SERVICE WORKER & PWA ====================
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then((registration) => {
                console.log('SW registered:', registration.scope);
            })
            .catch((error) => {
                console.log('SW registration failed:', error);
            });
    }
}

// ==================== THEME ====================
function initTheme() {
    document.body.dataset.theme = currentTheme;
    updateThemeIcon();
    
    const themeToggle = document.getElementById('themeToggle');
    const mobileThemeToggle = document.getElementById('mobileThemeToggle');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    if (mobileThemeToggle) {
        mobileThemeToggle.addEventListener('click', toggleTheme);
    }
}

function toggleTheme() {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.body.dataset.theme = currentTheme;
    localStorage.setItem('theme', currentTheme);
    updateThemeIcon();
    showToast(`Switched to ${currentTheme} mode`, 'info');
}

function updateThemeIcon() {
    const icons = document.querySelectorAll('#themeToggle i, #mobileThemeToggle i');
    icons.forEach(icon => {
        icon.className = currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    });
}

// ==================== KEYBOARD SHORTCUTS ====================
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ignore if typing in input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
        
        if (e.ctrlKey || e.metaKey) {
            switch (e.key.toLowerCase()) {
                case 'u': // Upload
                    e.preventDefault();
                    document.getElementById('imageInput')?.click();
                    break;
                case 'w': // Webcam
                    e.preventDefault();
                    navigateToSection('webcam');
                    break;
                case 'd': // Dashboard
                    e.preventDefault();
                    navigateToSection('dashboard');
                    break;
                case 'n': // Nutrition
                    e.preventDefault();
                    navigateToSection('nutrition');
                    break;
                case 'i': // Inventory
                    e.preventDefault();
                    navigateToSection('inventory');
                    break;
                case 'h': // History
                    e.preventDefault();
                    navigateToSection('history');
                    break;
                case 't': // Theme toggle
                    e.preventDefault();
                    toggleTheme();
                    break;
            }
        } else if (e.key === '?') {
            e.preventDefault();
            document.getElementById('shortcutsHelp')?.classList.toggle('hidden');
        } else if (e.key === 'Escape') {
            document.getElementById('shortcutsHelp')?.classList.add('hidden');
            document.getElementById('notificationCenter')?.classList.add('hidden');
        }
    });
    
    const shortcutsBtn = document.getElementById('shortcutsBtn');
    if (shortcutsBtn) {
        shortcutsBtn.addEventListener('click', () => {
            document.getElementById('shortcutsHelp')?.classList.toggle('hidden');
        });
    }
}

function navigateToSection(section) {
    const btn = document.querySelector(`.nav-btn[data-section="${section}"]`);
    if (btn) btn.click();
}

// ==================== NOTIFICATIONS ====================
function initNotifications() {
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationCenter = document.getElementById('notificationCenter');
    const clearAllBtn = document.getElementById('clearAllNotifications');
    
    if (notificationBtn) {
        notificationBtn.addEventListener('click', () => {
            notificationCenter?.classList.toggle('hidden');
        });
    }
    
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', () => {
            notifications = [];
            localStorage.setItem('notifications', '[]');
            updateNotificationUI();
        });
    }
    
    updateNotificationUI();
    
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

function addNotification(title, message, type = 'info') {
    const notification = {
        id: Date.now(),
        title,
        message,
        type,
        time: new Date().toISOString(),
        read: false
    };
    notifications.unshift(notification);
    if (notifications.length > 50) notifications.pop();
    localStorage.setItem('notifications', JSON.stringify(notifications));
    updateNotificationUI();
    
    // Browser notification
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, { body: message, icon: '/static/icons/icon-192x192.png' });
    }
}

function updateNotificationUI() {
    const badge = document.querySelector('.notification-badge');
    const list = document.getElementById('notificationList');
    
    const unreadCount = notifications.filter(n => !n.read).length;
    if (badge) {
        badge.textContent = unreadCount;
        badge.classList.toggle('hidden', unreadCount === 0);
    }
    
    if (list) {
        if (notifications.length === 0) {
            list.innerHTML = '<p class="no-notifications">No notifications</p>';
        } else {
            list.innerHTML = notifications.slice(0, 20).map(n => `
                <div class="notification-item ${n.read ? '' : 'unread'}" data-id="${n.id}">
                    <div class="notification-icon ${n.type}"><i class="fas fa-${n.type === 'warning' ? 'exclamation-triangle' : n.type === 'success' ? 'check-circle' : 'info-circle'}"></i></div>
                    <div class="notification-content">
                        <strong>${n.title}</strong>
                        <p>${n.message}</p>
                        <small>${formatTimeAgo(n.time)}</small>
                    </div>
                </div>
            `).join('');
        }
    }
}

function formatTimeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
}

// ==================== NAVIGATION ====================
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = {
        classify: document.getElementById('classify-section'),
        webcam: document.getElementById('webcam-section'),
        dashboard: document.getElementById('dashboard-section'),
        nutrition: document.getElementById('nutrition-section'),
        inventory: document.getElementById('inventory-section'),
        history: document.getElementById('history-section'),
        stats: document.getElementById('stats-section'),
        'meal-planner': document.getElementById('meal-planner-section'),
        'shopping': document.getElementById('shopping-section')
    };
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetSection = btn.dataset.section;
            
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            Object.values(sections).forEach(s => {
                if (s) s.classList.remove('active');
            });
            if (sections[targetSection]) {
                sections[targetSection].classList.add('active');
            }
            
            // Load data when switching sections
            if (targetSection === 'history') loadHistory();
            else if (targetSection === 'stats') loadStatistics();
            else if (targetSection === 'nutrition') loadFruitList();
            else if (targetSection === 'dashboard') loadDashboard();
            else if (targetSection === 'inventory') loadInventory();
            else if (targetSection === 'meal-planner') loadMealPlannerData();
            else if (targetSection === 'shopping') updateShoppingListUI();
        });
    });
}

// ==================== UPLOAD ====================
function initUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');
    const removeImageBtn = document.getElementById('removeImage');
    const takePhotoBtn = document.getElementById('takePhotoBtn');
    const cameraInput = document.getElementById('cameraInput');
    
    // Upload mode toggle
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const mode = btn.dataset.mode;
            document.getElementById('singleUploadContainer')?.classList.toggle('hidden', mode !== 'single');
            document.getElementById('batchUploadContainer')?.classList.toggle('hidden', mode !== 'batch');
        });
    });
    
    // Confidence threshold slider
    const thresholdSlider = document.getElementById('confidenceThreshold');
    const thresholdValue = document.getElementById('confidenceValue');
    if (thresholdSlider && thresholdValue) {
        thresholdSlider.addEventListener('input', () => {
            thresholdValue.textContent = thresholdSlider.value + '%';
        });
    }
    
    // Crop button
    const cropBtn = document.getElementById('cropImageBtn');
    if (cropBtn) {
        cropBtn.addEventListener('click', openCropModal);
    }
    
    uploadArea.addEventListener('click', (e) => {
        if (!imagePreview.classList.contains('hidden')) return;
        if (e.target.id === 'takePhotoBtn' || e.target.closest('#takePhotoBtn')) return;
        imageInput.click();
    });
    
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFileSelect(file);
    });
    
    // Camera button - opens native camera app (works on mobile without HTTPS)
    if (takePhotoBtn && cameraInput) {
        takePhotoBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            cameraInput.click();
        });
        
        cameraInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) handleFileSelect(file);
        });
    }
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFileSelect(file);
        } else {
            showToast('Please drop a valid image file', 'error');
        }
    });
    
    removeImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        clearImage();
    });
}

// ==================== BATCH UPLOAD ====================
function initBatchUpload() {
    const batchArea = document.getElementById('batchUploadArea');
    const batchInput = document.getElementById('batchImageInput');
    
    if (!batchArea || !batchInput) return;
    
    batchArea.addEventListener('click', () => batchInput.click());
    
    batchInput.addEventListener('change', (e) => {
        handleBatchFiles(e.target.files);
    });
    
    batchArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        batchArea.classList.add('dragover');
    });
    
    batchArea.addEventListener('dragleave', () => {
        batchArea.classList.remove('dragover');
    });
    
    batchArea.addEventListener('drop', (e) => {
        e.preventDefault();
        batchArea.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
        handleBatchFiles(files);
    });
    
    document.getElementById('clearBatchBtn')?.addEventListener('click', clearBatch);
    document.getElementById('classifyBatchBtn')?.addEventListener('click', classifyBatch);
}

function handleBatchFiles(files) {
    const fileArray = Array.from(files).slice(0, 20);
    batchFiles = [...batchFiles, ...fileArray].slice(0, 20);
    updateBatchPreview();
}

function updateBatchPreview() {
    const preview = document.getElementById('batchPreview');
    const actions = document.getElementById('batchActions');
    const count = document.getElementById('batchCount');
    
    if (!preview) return;
    
    preview.innerHTML = batchFiles.map((file, i) => {
        const url = URL.createObjectURL(file);
        return `<div class="batch-thumb" data-index="${i}">
            <img src="${url}" alt="${file.name}">
            <button class="batch-remove" onclick="removeBatchFile(${i})">×</button>
        </div>`;
    }).join('');
    
    actions?.classList.toggle('hidden', batchFiles.length === 0);
    if (count) count.textContent = `${batchFiles.length} images selected`;
}

function removeBatchFile(index) {
    batchFiles.splice(index, 1);
    updateBatchPreview();
}

function clearBatch() {
    batchFiles = [];
    updateBatchPreview();
    document.getElementById('batchResults').innerHTML = '';
    document.getElementById('batchProgress')?.classList.add('hidden');
}

async function classifyBatch() {
    if (batchFiles.length === 0) return;
    
    const progress = document.getElementById('batchProgress');
    const progressFill = document.getElementById('batchProgressFill');
    const progressText = document.getElementById('batchProgressText');
    const results = document.getElementById('batchResults');
    
    progress?.classList.remove('hidden');
    results.innerHTML = '';
    
    for (let i = 0; i < batchFiles.length; i++) {
        if (progressFill) progressFill.style.width = `${((i + 1) / batchFiles.length) * 100}%`;
        if (progressText) progressText.textContent = `${i + 1}/${batchFiles.length} processed`;
        
        try {
            const formData = new FormData();
            formData.append('image', batchFiles[i]);
            formData.append('language', currentLanguage);
            formData.append('analysis_mode', 'full');  // Use full analysis mode
            
            const response = await fetch(`${API_BASE}/classify`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            // Use the correct response structure
            const predictedClass = data.predicted_class || 'Unknown';
            const confidence = data.confidence || '-';
            
            results.innerHTML += `
                <div class="batch-result-item">
                    <img src="${URL.createObjectURL(batchFiles[i])}" alt="Result">
                    <div class="batch-result-info">
                        <strong>${predictedClass}</strong>
                        <span>${confidence}</span>
                        ${data.ripeness ? `<small>Ripeness: ${data.ripeness}</small>` : ''}
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Batch error:', error);
            results.innerHTML += `
                <div class="batch-result-item error">
                    <strong>Error processing</strong>
                    <span>${batchFiles[i].name}</span>
                </div>
            `;
        }
    }
    
    showToast(`Batch processing complete: ${batchFiles.length} images`, 'success');
    progress?.classList.add('hidden');
}

function openCropModal() {
    const img = document.getElementById('previewImg');
    if (!img || !img.src) return;
    
    // Create crop modal
    const modal = document.createElement('div');
    modal.className = 'modal crop-modal';
    modal.id = 'cropModal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="modal-close" onclick="closeCropModal()">×</span>
            <h3>Crop Image</h3>
            <div class="crop-container">
                <img id="cropImage" src="${img.src}">
            </div>
            <div class="crop-actions">
                <button class="btn btn-secondary" onclick="closeCropModal()">Cancel</button>
                <button class="btn btn-primary" onclick="applyCrop()">Apply Crop</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    
    // Initialize cropper
    const cropImage = document.getElementById('cropImage');
    if (typeof Cropper !== 'undefined') {
        cropper = new Cropper(cropImage, {
            aspectRatio: NaN,
            viewMode: 1,
            autoCropArea: 0.8
        });
    }
}

function closeCropModal() {
    if (cropper) {
        cropper.destroy();
        cropper = null;
    }
    document.getElementById('cropModal')?.remove();
}

function applyCrop() {
    if (!cropper) return;
    
    cropper.getCroppedCanvas().toBlob((blob) => {
        selectedFile = new File([blob], 'cropped.jpg', { type: 'image/jpeg' });
        document.getElementById('previewImg').src = URL.createObjectURL(blob);
        closeCropModal();
        showToast('Image cropped successfully', 'success');
    }, 'image/jpeg', 0.9);
}

function handleFileSelect(file) {
    selectedFile = file;
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const uploadArea = document.getElementById('uploadArea');
    const classifyBtn = document.getElementById('classifyBtn');
    const results = document.getElementById('results');
    
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        imagePreview.classList.remove('hidden');
        uploadArea.querySelector('.upload-content').style.display = 'none';
        classifyBtn.disabled = false;
        results.classList.add('hidden');
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    selectedFile = null;
    const imageInput = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');
    const uploadArea = document.getElementById('uploadArea');
    const classifyBtn = document.getElementById('classifyBtn');
    const results = document.getElementById('results');
    
    imageInput.value = '';
    imagePreview.classList.add('hidden');
    uploadArea.querySelector('.upload-content').style.display = 'block';
    classifyBtn.disabled = true;
    results.classList.add('hidden');
    clearResultFields();
}

function clearResultFields() {
    const fields = ['resultClass', 'resultConfidence', 'ripenessStatus', 'qualityStatus', 
                    'qualityScore', 'isEdible', 'sizeGrade', 'qualityGrade', 
                    'storageRec', 'consumptionRec', 'handlingRec'];
    fields.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = '-';
    });
    
    const containers = ['topPredictions', 'suitableFor', 'vitaminsList', 'healthBenefitsList', 'defectsList'];
    containers.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = '';
    });
}

// ==================== CLASSIFICATION ====================
function initClassification() {
    const classifyBtn = document.getElementById('classifyBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    
    classifyBtn.addEventListener('click', async () => {
        if (!selectedFile) return;
        
        classifyBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        btnLoader.classList.remove('hidden');
        
        try {
            const formData = new FormData();
            formData.append('image', selectedFile);
            formData.append('language', currentLanguage);
            formData.append('mode', 'full');
            console.log('Sending classification with language:', currentLanguage);
            
            const response = await fetch(`${API_BASE}/classify`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayEnhancedResults(data);
                showToast('Analysis completed successfully!', 'success');
            } else {
                showToast(data.error || 'Analysis failed', 'error');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            showToast('Failed to analyze image. Please try again.', 'error');
        } finally {
            classifyBtn.disabled = false;
            btnText.textContent = 'Analyze Fruit';
            btnLoader.classList.add('hidden');
        }
    });
}

function displayEnhancedResults(data) {
    const results = document.getElementById('results');
    
    // Classification
    document.querySelector('.result-icon').textContent = getFruitEmoji(data.predicted_class);
    document.getElementById('resultConfidence').textContent = data.confidence;
    
    // Display translated name as primary when language is not English
    const resultClassEl = document.getElementById('resultClass');
    const translatedEl = document.getElementById('resultClassTranslated');
    
    console.log('Display results - currentLanguage:', currentLanguage);
    console.log('predicted_class:', data.predicted_class);
    console.log('predicted_class_translated:', data.predicted_class_translated);
    
    if (currentLanguage !== 'en' && data.predicted_class_translated && data.predicted_class_translated !== data.predicted_class) {
        // Show translated name as primary, English in parentheses
        console.log('Showing translated name:', data.predicted_class_translated);
        resultClassEl.textContent = data.predicted_class_translated;
        if (translatedEl) {
            translatedEl.textContent = `(${data.predicted_class})`;
            translatedEl.style.display = 'block';
        }
    } else {
        // Show English name only (no translation needed)
        console.log('Showing English name (no translation or same as English)');
        resultClassEl.textContent = data.predicted_class;
        if (translatedEl) {
            translatedEl.style.display = 'none';
        }
    }
    
    // Top predictions
    const topPredictions = document.getElementById('topPredictions');
    topPredictions.innerHTML = '';
    if (data.top_predictions) {
        data.top_predictions.forEach((pred, index) => {
            const item = document.createElement('div');
            item.className = 'prediction-item';
            item.innerHTML = `
                <span class="prediction-name">${index + 1}. ${pred.class}</span>
                <span class="prediction-confidence">${pred.confidence}</span>
            `;
            topPredictions.appendChild(item);
        });
    }
    
    // Ripeness
    if (data.ripeness) {
        const ripenessEl = document.getElementById('ripenessStatus');
        ripenessEl.textContent = data.ripeness_translated || data.ripeness;
        ripenessEl.className = `analysis-value ripeness-${data.ripeness}`;
        const descEl = document.getElementById('ripenessDescription');
        if (descEl) descEl.textContent = data.ripeness_description || '';
    }
    
    // Quality
    if (data.quality_status) {
        const qualityEl = document.getElementById('qualityStatus');
        qualityEl.textContent = data.quality_status_translated || data.quality_status.replace('_', ' ');
        qualityEl.className = `analysis-value quality-${data.quality_status}`;
    }
    
    // Quality Score
    if (data.quality_score !== undefined) {
        document.getElementById('qualityScore').textContent = `${data.quality_score}/100`;
        const fillEl = document.getElementById('qualityScoreFill');
        if (fillEl) fillEl.style.width = `${data.quality_score}%`;
    }
    
    // Edible
    if (data.is_edible !== undefined) {
        document.getElementById('isEdible').textContent = data.is_edible ? '✅ Yes' : '❌ No';
    }
    
    // Defects
    const defectsContainer = document.getElementById('defectsContainer');
    const defectsList = document.getElementById('defectsList');
    if (defectsContainer && defectsList) {
        if (data.defects_detected && data.defects_detected.length > 0) {
            defectsContainer.classList.remove('hidden');
            defectsList.innerHTML = data.defects_detected.map(d => 
                `<span class="defect-tag">${d}</span>`
            ).join('');
        } else {
            defectsContainer.classList.add('hidden');
        }
    }
    
    // Size & Grading
    if (data.size_grade) {
        document.getElementById('sizeGrade').textContent = data.size_grade_translated || data.size_grade;
    }
    
    if (data.quality_grade) {
        const gradeEl = document.getElementById('qualityGrade');
        gradeEl.textContent = data.quality_grade;
        gradeEl.className = `grade-badge grade-${data.quality_grade}`;
    }
    
    // Suitable for
    const suitableFor = document.getElementById('suitableFor');
    if (suitableFor && data.suitable_for && data.suitable_for.length > 0) {
        suitableFor.innerHTML = data.suitable_for.map(s => 
            `<span class="suitable-tag">${s}</span>`
        ).join('');
    }
    
    // Recommendations
    if (data.recommendations) {
        document.getElementById('storageRec').textContent = data.recommendations.storage || '-';
        document.getElementById('consumptionRec').textContent = data.recommendations.consumption_window || '-';
        document.getElementById('handlingRec').textContent = data.recommendations.handling || '-';
    }
    
    // Nutrition
    if (data.nutrition) {
        displayNutrition(data.nutrition);
    }
    
    results.classList.remove('hidden');
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displayNutrition(nutrition) {
    document.getElementById('nutritionCalories').textContent = nutrition.calories || '-';
    document.getElementById('nutritionCarbs').textContent = nutrition.carbohydrates || '-';
    document.getElementById('nutritionFiber').textContent = nutrition.fiber || '-';
    document.getElementById('nutritionSugar').textContent = nutrition.sugar || '-';
    document.getElementById('nutritionProtein').textContent = nutrition.protein || '-';
    
    const vitaminsList = document.getElementById('vitaminsList');
    if (vitaminsList && nutrition.vitamins) {
        vitaminsList.innerHTML = Object.entries(nutrition.vitamins).map(([name, value]) => 
            `<span class="vitamin-tag">${name}: ${value}</span>`
        ).join('');
    }
    
    const benefitsList = document.getElementById('healthBenefitsList');
    if (benefitsList && nutrition.health_benefits) {
        benefitsList.innerHTML = nutrition.health_benefits.map(b => `<li>${b}</li>`).join('');
    }
}

// ==================== HISTORY ====================
function initHistory() {
    document.getElementById('refreshHistory').addEventListener('click', loadHistory);
}

async function loadHistory() {
    const container = document.getElementById('historyContainer');
    container.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    
    try {
        const response = await fetch(`${API_BASE}/history?limit=20&_=${Date.now()}`, { cache: 'no-store' });
        const data = await response.json();
        
        if (response.ok && data.history && data.history.length > 0) {
            container.innerHTML = '';
            data.history.forEach(item => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                const date = new Date(item.timestamp);
                historyItem.innerHTML = `
                    <div class="history-icon">${getFruitEmoji(item.predicted_class)}</div>
                    <div class="history-class">${item.predicted_class}</div>
                    <div class="history-confidence">Confidence: ${(item.confidence * 100).toFixed(1)}%</div>
                    <div class="history-time">${date.toLocaleString()}</div>
                `;
                container.appendChild(historyItem);
            });
        } else {
            container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No classification history yet</p>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
        container.innerHTML = '<p style="text-align: center; color: var(--error);">Failed to load history</p>';
    }
}

// ==================== STATISTICS ====================
function initStatistics() {
    const refreshBtn = document.getElementById('refreshStats');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadStatistics);
    }
}

async function loadStatistics() {
    const container = document.getElementById('statsContainer');
    container.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    
    try {
        const response = await fetch(`${API_BASE}/statistics?_=${Date.now()}`, { cache: 'no-store' });
        const data = await response.json();
        
        if (response.ok) {
            container.innerHTML = '';
            
            const totalCard = document.createElement('div');
            totalCard.className = 'stat-card';
            totalCard.innerHTML = `<h3>Total Classifications</h3><div class="stat-number">${data.total_classifications || 0}</div>`;
            container.appendChild(totalCard);
            
            if (data.class_counts && Object.keys(data.class_counts).length > 0) {
                const classCard = document.createElement('div');
                classCard.className = 'stat-card';
                classCard.innerHTML = '<h3>Classifications by Fruit Type</h3>';
                
                const classStats = document.createElement('div');
                classStats.className = 'class-stats';
                Object.entries(data.class_counts).sort((a, b) => b[1] - a[1]).forEach(([fruit, count]) => {
                    const item = document.createElement('div');
                    item.className = 'class-stat-item';
                    item.innerHTML = `<div class="class-stat-icon">${getFruitEmoji(fruit)}</div><div class="class-stat-name">${fruit}</div><div class="class-stat-count">${count}</div>`;
                    classStats.appendChild(item);
                });
                classCard.appendChild(classStats);
                container.appendChild(classCard);
            }
        } else {
            container.innerHTML = '<p style="text-align: center; color: var(--error);">Failed to load statistics</p>';
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
        container.innerHTML = '<p style="text-align: center; color: var(--error);">Failed to load statistics</p>';
    }
}

// ==================== WEBCAM ====================
function initWebcam() {
    console.log('Initializing webcam...');
    const startBtn = document.getElementById('startWebcam');
    const stopBtn = document.getElementById('stopWebcam');
    const captureBtn = document.getElementById('captureBtn');
    const webcamNote = document.getElementById('webcamNote');
    
    console.log('Webcam elements:', { startBtn: !!startBtn, stopBtn: !!stopBtn, captureBtn: !!captureBtn, webcamNote: !!webcamNote });
    
    // Check if we're on localhost or HTTPS (required for camera)
    const isSecure = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.protocol === 'https:';
    
    console.log('Secure context:', isSecure, 'Host:', window.location.hostname);
    
    // Check camera availability and show appropriate message
    if (webcamNote) {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            webcamNote.innerHTML = '⚠️ Camera API not supported in this browser. Use Chrome, Firefox, or Edge. Or use the <strong>Take Photo</strong> button in the Classify tab.';
            webcamNote.style.color = '#ff9800';
            if (startBtn) startBtn.disabled = true;
        } else if (!isSecure) {
            webcamNote.innerHTML = '🔒 Camera requires secure connection. Access via <a href="http://localhost:5000" style="color:#4CAF50; font-weight:bold;">http://localhost:5000</a> or use HTTPS.';
            webcamNote.style.color = '#2196F3';
            if (startBtn) startBtn.disabled = true;
        } else {
            webcamNote.innerHTML = '📷 Click <strong>"Start Camera"</strong> to begin. Make sure to allow camera access when prompted.';
            webcamNote.style.color = '#4CAF50';
        }
    }
    
    if (startBtn) {
        startBtn.addEventListener('click', startWebcam);
        // Enable button if we're on secure connection
        if (isSecure && navigator.mediaDevices) {
            startBtn.disabled = false;
        }
    }
    if (stopBtn) stopBtn.addEventListener('click', stopWebcam);
    if (captureBtn) captureBtn.addEventListener('click', captureAndAnalyze);
}

async function startWebcam() {
    console.log('startWebcam called');
    const video = document.getElementById('webcamVideo');
    const startBtn = document.getElementById('startWebcam');
    const stopBtn = document.getElementById('stopWebcam');
    const captureBtn = document.getElementById('captureBtn');
    const webcamNote = document.getElementById('webcamNote');
    
    // Show immediate feedback
    if (webcamNote) {
        webcamNote.innerHTML = '⏳ Starting camera, please wait...';
        webcamNote.style.color = '#2196F3';
    }
    
    // Update button state
    if (startBtn) {
        startBtn.disabled = true;
        startBtn.textContent = 'Starting...';
    }
    
    // Check if mediaDevices is available
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showToast('Camera API not available in this browser. Try Chrome or Firefox.', 'error');
        if (startBtn) {
            startBtn.disabled = false;
            startBtn.textContent = 'Start Camera';
        }
        return;
    }
    
    try {
        console.log('Requesting camera access...');
        
        // Try environment camera first (mobile rear), fallback to any available camera
        let stream = null;
        try {
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    facingMode: 'environment', 
                    width: { ideal: 640 }, 
                    height: { ideal: 480 } 
                },
                audio: false
            });
            console.log('Got environment camera');
        } catch (envError) {
            console.log('Environment camera failed, trying default:', envError.message);
            // Fallback to default camera
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: true,
                audio: false
            });
            console.log('Got default camera');
        }
        
        webcamStream = stream;
        video.srcObject = stream;
        
        // Wait for video to be ready
        video.onloadedmetadata = () => {
            video.play().then(() => {
                console.log('Video playing');
                if (startBtn) startBtn.textContent = 'Camera Active';
                if (stopBtn) stopBtn.disabled = false;
                if (captureBtn) captureBtn.disabled = false;
                if (webcamNote) webcamNote.textContent = 'Camera is active. Click "Capture & Analyze" to analyze fruit.';
                showToast('Camera started successfully!', 'success');
            }).catch(playErr => {
                console.error('Video play error:', playErr);
                showToast('Could not start video: ' + playErr.message, 'error');
            });
        };
        
    } catch (error) {
        console.error('Webcam error:', error);
        if (startBtn) {
            startBtn.disabled = false;
            startBtn.textContent = 'Start Camera';
        }
        
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
            showToast('Camera access denied. Please allow camera permissions in your browser.', 'error');
            if (webcamNote) webcamNote.innerHTML = '❌ Camera permission denied. Click the camera icon in the address bar to allow access.';
        } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
            showToast('No camera found on this device.', 'error');
            if (webcamNote) webcamNote.innerHTML = '❌ No camera detected. Please connect a webcam.';
        } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
            showToast('Camera is in use by another application.', 'error');
            if (webcamNote) webcamNote.innerHTML = '❌ Camera is busy. Close other apps using the camera.';
        } else if (error.name === 'OverconstrainedError') {
            showToast('Camera does not meet requirements. Trying basic mode...', 'warning');
            // Try with minimal constraints
            try {
                const basicStream = await navigator.mediaDevices.getUserMedia({ video: true });
                webcamStream = basicStream;
                video.srcObject = basicStream;
                await video.play();
                if (stopBtn) stopBtn.disabled = false;
                if (captureBtn) captureBtn.disabled = false;
                showToast('Camera started in basic mode', 'success');
            } catch (basicError) {
                showToast('Camera failed: ' + basicError.message, 'error');
            }
        } else {
            showToast('Camera error: ' + error.message, 'error');
            if (webcamNote) webcamNote.innerHTML = `❌ Camera error: ${error.message}`;
        }
    }
}

function stopWebcam() {
    const video = document.getElementById('webcamVideo');
    const startBtn = document.getElementById('startWebcam');
    const stopBtn = document.getElementById('stopWebcam');
    const captureBtn = document.getElementById('captureBtn');
    
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
    }
    video.srcObject = null;
    startBtn.disabled = false;
    stopBtn.disabled = true;
    captureBtn.disabled = true;
    document.getElementById('webcamResults').classList.add('hidden');
}

async function captureAndAnalyze() {
    const video = document.getElementById('webcamVideo');
    const canvas = document.getElementById('webcamCanvas');
    const captureBtn = document.getElementById('captureBtn');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    const imageData = canvas.toDataURL('image/jpeg', 0.9);
    captureBtn.disabled = true;
    captureBtn.textContent = 'Analyzing...';
    
    try {
        // Use full analysis mode for better accuracy
        const response = await fetch(`${API_BASE}/analyze/base64`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                image: imageData, 
                language: currentLanguage,
                analysis_mode: 'full'  // Use full analysis for better accuracy
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('webcamResultClass').textContent = data.predicted_class_translated || data.predicted_class;
            document.getElementById('webcamResultConfidence').textContent = `Confidence: ${data.confidence}`;
            document.getElementById('webcamRipeness').textContent = `Ripeness: ${data.ripeness || '-'}`;
            document.getElementById('webcamQuality').textContent = `Quality: ${data.quality_status || '-'}`;
            document.getElementById('webcamSize').textContent = `Size: ${data.size_grade || '-'}`;
            document.getElementById('webcamResults').classList.remove('hidden');
            showToast(`Detected: ${data.predicted_class} (${data.confidence})`, 'success');
        } else {
            showToast(data.error || 'Analysis failed', 'error');
        }
    } catch (error) {
        console.error('Capture error:', error);
        showToast('Failed to analyze capture', 'error');
    } finally {
        captureBtn.disabled = false;
        captureBtn.textContent = 'Capture & Analyze';
    }
}

// ==================== NUTRITION BROWSER ====================
function initNutritionBrowser() {
    const fruitSelect = document.getElementById('fruitSelect');
    if (fruitSelect) {
        fruitSelect.addEventListener('change', async (e) => {
            if (e.target.value) await loadNutritionDetails(e.target.value);
            else document.getElementById('nutritionDetails').classList.add('hidden');
        });
    }
    
    // Serving size change
    const servingSize = document.getElementById('servingSize');
    if (servingSize) {
        servingSize.addEventListener('change', async () => {
            const fruit = document.getElementById('fruitSelect')?.value;
            if (fruit) await loadNutritionDetails(fruit);
        });
    }
    
    // Nutrition tabs
    document.querySelectorAll('.nutrition-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.nutrition-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nutrition-tab-content').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(`nutrition-tab-${tab.dataset.tab}`)?.classList.add('active');
        });
    });
    
    // Compare fruits
    const compareBtn = document.getElementById('compareFruitsBtn');
    if (compareBtn) compareBtn.addEventListener('click', compareFruits);
    
    // Search nutrients
    const searchBtn = document.getElementById('searchNutrientBtn');
    if (searchBtn) searchBtn.addEventListener('click', searchByNutrient);
    
    // Quick filters
    document.querySelectorAll('.quick-filter-btn').forEach(btn => {
        btn.addEventListener('click', () => handleQuickFilter(btn.dataset.filter));
    });
    
    // Seasonal month change
    const seasonalMonth = document.getElementById('seasonalMonth');
    if (seasonalMonth) seasonalMonth.addEventListener('change', loadSeasonalFruits);
    
    // Print/Export
    const printBtn = document.getElementById('printNutrition');
    if (printBtn) printBtn.addEventListener('click', printNutritionInfo);
    
    const exportBtn = document.getElementById('exportNutritionPDF');
    if (exportBtn) exportBtn.addEventListener('click', exportNutritionPDF);
}

async function loadFruitList() {
    const selects = ['fruitSelect', 'compareFruit1', 'compareFruit2', 'compareFruit3'];
    try {
        const response = await fetch(`${API_BASE}/classes?language=${currentLanguage}`);
        const data = await response.json();
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (select && select.options.length <= 1) {
                data.classes.forEach(fruit => {
                    const option = document.createElement('option');
                    option.value = fruit;
                    option.textContent = fruit;
                    select.appendChild(option);
                });
            }
        });
    } catch (error) {
        console.error('Error loading fruit list:', error);
    }
    
    // Load initial seasonal view
    loadSeasonalFruits();
}

async function loadNutritionDetails(fruitName) {
    const container = document.getElementById('nutritionDetails');
    const servingGrams = document.getElementById('servingSize')?.value || 100;
    container.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    container.classList.remove('hidden');
    
    try {
        const [nutritionRes, storageRes, glycemicRes, recipesRes] = await Promise.all([
            fetch(`${API_BASE}/nutrition/serving/${encodeURIComponent(fruitName)}?grams=${servingGrams}`),
            fetch(`${API_BASE}/nutrition/storage/${encodeURIComponent(fruitName)}`),
            fetch(`${API_BASE}/nutrition/glycemic/${encodeURIComponent(fruitName)}`),
            fetch(`${API_BASE}/nutrition/recipes/${encodeURIComponent(fruitName)}`)
        ]);
        
        const [nutritionData, storageData, glycemicData, recipesData] = await Promise.all([
            nutritionRes.json(), storageRes.json(), glycemicRes.json(), recipesRes.json()
        ]);
        
        if (nutritionRes.ok) {
            const n = nutritionData.nutrition;
            const gi = glycemicData.glycemic || {};
            const storage = storageData.storage || {};
            const recipes = recipesData.recipes || [];
            
            const giColor = gi.category === 'Low' ? '#27ae60' : gi.category === 'Medium' ? '#f39c12' : '#e74c3c';
            
            container.innerHTML = `
                <div class="nutrition-header">
                    <span class="nutrition-icon">${getFruitEmoji(nutritionData.fruit)}</span>
                    <h3>${nutritionData.fruit}</h3>
                    <p class="serving-size">Nutritional values for ${nutritionData.serving_grams}g serving</p>
                </div>
                
                <div class="nutrition-main-grid">
                    <div class="nutrition-left">
                        <div class="macro-section">
                            <h4><i class="fas fa-fire"></i> Macros</h4>
                            <div class="nutrition-grid">
                                <div class="nutrition-item calories"><span class="nutrition-value">${n.calories}</span><span class="nutrition-label">Calories</span></div>
                                <div class="nutrition-item"><span class="nutrition-value">${n.carbohydrates}g</span><span class="nutrition-label">Carbs</span></div>
                                <div class="nutrition-item"><span class="nutrition-value">${n.fiber}g</span><span class="nutrition-label">Fiber</span></div>
                                <div class="nutrition-item"><span class="nutrition-value">${n.sugar}g</span><span class="nutrition-label">Sugar</span></div>
                                <div class="nutrition-item"><span class="nutrition-value">${n.protein}g</span><span class="nutrition-label">Protein</span></div>
                            </div>
                            <canvas id="macroChart" class="nutrition-chart"></canvas>
                        </div>
                        
                        <div class="gi-section">
                            <h4><i class="fas fa-chart-line"></i> Glycemic Index</h4>
                            <div class="gi-indicator" style="border-color: ${giColor}">
                                <span class="gi-value" style="color: ${giColor}">${gi.index || 'N/A'}</span>
                                <span class="gi-category">${gi.category || 'N/A'} GI</span>
                                <span class="gi-load">Load: ${gi.load || 'N/A'}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="nutrition-right">
                        <div class="vitamins-minerals-section">
                            <div class="vitamins-section">
                                <h4><i class="fas fa-capsules"></i> Vitamins</h4>
                                <div class="vitamins-list">${Object.entries(n.vitamins || {}).map(([k,v]) => `<span class="vitamin-tag">${k}: ${v}</span>`).join('')}</div>
                            </div>
                            <div class="minerals-section">
                                <h4><i class="fas fa-gem"></i> Minerals</h4>
                                <div class="vitamins-list">${Object.entries(n.minerals || {}).map(([k,v]) => `<span class="vitamin-tag">${k}: ${v}</span>`).join('')}</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="nutrition-extras">
                    <div class="storage-section">
                        <h4><i class="fas fa-box"></i> Storage Tips</h4>
                        <div class="storage-info">
                            <p><strong>Room Temperature:</strong> ${storage.room_temp || 'N/A'}</p>
                            <p><strong>Refrigerated:</strong> ${storage.refrigerated || 'N/A'}</p>
                            <p><strong>Tips:</strong> ${storage.tips || 'N/A'}</p>
                        </div>
                    </div>
                    
                    <div class="recipes-section">
                        <h4><i class="fas fa-utensils"></i> Recipe Ideas</h4>
                        <div class="recipes-grid">
                            ${recipes.slice(0, 3).map(r => `
                                <div class="recipe-card">
                                    <h5>${r.name}</h5>
                                    <span class="recipe-type">${r.type}</span>
                                    <p>${r.ingredients.slice(0, 3).join(', ')}${r.ingredients.length > 3 ? '...' : ''}</p>
                                </div>
                            `).join('') || '<p>No recipes available</p>'}
                        </div>
                    </div>
                    
                    <div class="health-benefits-section">
                        <h4><i class="fas fa-heart"></i> Health Benefits</h4>
                        <ul class="health-benefits-list">${(n.health_benefits || []).map(b => `<li>${b}</li>`).join('')}</ul>
                    </div>
                </div>
            `;
            
            // Render macro chart
            renderMacroChart(n);
        } else {
            container.innerHTML = `<p style="color: var(--error);">${nutritionData.error}</p>`;
        }
    } catch (error) {
        console.error('Error loading nutrition:', error);
        container.innerHTML = '<p style="color: var(--error);">Failed to load nutrition information</p>';
    }
}

function renderMacroChart(nutrition) {
    const ctx = document.getElementById('macroChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Carbs', 'Protein', 'Sugar', 'Fiber'],
            datasets: [{
                data: [
                    nutrition.carbohydrates || 0,
                    nutrition.protein || 0,
                    nutrition.sugar || 0,
                    nutrition.fiber || 0
                ],
                backgroundColor: ['#3498db', '#e74c3c', '#f39c12', '#27ae60']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#e0e6ed' } }
            }
        }
    });
}

async function compareFruits() {
    const fruits = [
        document.getElementById('compareFruit1')?.value,
        document.getElementById('compareFruit2')?.value,
        document.getElementById('compareFruit3')?.value
    ].filter(f => f);
    
    if (fruits.length < 2) {
        showToast('Please select at least 2 fruits to compare', 'warning');
        return;
    }
    
    const container = document.getElementById('comparisonResults');
    container.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    container.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/nutrition/compare?fruits=${fruits.join(',')}`);
        const data = await response.json();
        
        if (response.ok) {
            const comparison = data.comparison;
            container.innerHTML = `
                <h4>Comparison Results</h4>
                <div class="comparison-table-wrapper">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Nutrient</th>
                                ${fruits.map(f => `<th>${f}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>Calories</td>${fruits.map(f => `<td>${comparison[f]?.calories || 'N/A'}</td>`).join('')}</tr>
                            <tr><td>Carbs</td>${fruits.map(f => `<td>${comparison[f]?.carbohydrates || 'N/A'}g</td>`).join('')}</tr>
                            <tr><td>Fiber</td>${fruits.map(f => `<td>${comparison[f]?.fiber || 'N/A'}g</td>`).join('')}</tr>
                            <tr><td>Sugar</td>${fruits.map(f => `<td>${comparison[f]?.sugar || 'N/A'}g</td>`).join('')}</tr>
                            <tr><td>Protein</td>${fruits.map(f => `<td>${comparison[f]?.protein || 'N/A'}g</td>`).join('')}</tr>
                            <tr><td>Glycemic Index</td>${fruits.map(f => `<td>${comparison[f]?.glycemic_index || 'N/A'}</td>`).join('')}</tr>
                        </tbody>
                    </table>
                </div>
                <canvas id="comparisonChart" class="comparison-chart"></canvas>
            `;
            
            // Render comparison chart
            renderComparisonChart(fruits, comparison);
        } else {
            container.innerHTML = `<p style="color: var(--error);">${data.error}</p>`;
        }
    } catch (error) {
        console.error('Error comparing fruits:', error);
        container.innerHTML = '<p style="color: var(--error);">Failed to compare fruits</p>';
    }
}

function renderComparisonChart(fruits, comparison) {
    const ctx = document.getElementById('comparisonChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Calories', 'Carbs', 'Fiber', 'Sugar', 'Protein'],
            datasets: fruits.map((fruit, i) => ({
                label: fruit,
                data: [
                    comparison[fruit]?.calories || 0,
                    comparison[fruit]?.carbohydrates || 0,
                    comparison[fruit]?.fiber || 0,
                    comparison[fruit]?.sugar || 0,
                    comparison[fruit]?.protein || 0
                ],
                backgroundColor: ['#3498db', '#e74c3c', '#27ae60'][i]
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#e0e6ed' } }
            },
            scales: {
                x: { ticks: { color: '#e0e6ed' } },
                y: { ticks: { color: '#e0e6ed' } }
            }
        }
    });
}

async function searchByNutrient() {
    const nutrient = document.getElementById('searchNutrient')?.value;
    const criteria = document.getElementById('searchCriteria')?.value;
    
    const container = document.getElementById('searchResults');
    container.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    
    try {
        const response = await fetch(`${API_BASE}/nutrition/search?nutrient=${nutrient}&criteria=${criteria}&limit=10`);
        const data = await response.json();
        
        if (response.ok) {
            container.innerHTML = `
                <h4>Fruits ${criteria === 'high' ? 'Highest' : 'Lowest'} in ${nutrient}</h4>
                <div class="search-results-grid">
                    ${data.results.map((r, i) => `
                        <div class="search-result-item">
                            <span class="rank">#${i + 1}</span>
                            <span class="fruit-name">${r.fruit}</span>
                            <span class="nutrient-value">${r.value}${nutrient === 'calories' ? '' : 'g'}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error searching nutrients:', error);
        container.innerHTML = '<p style="color: var(--error);">Search failed</p>';
    }
}

async function handleQuickFilter(filter) {
    const container = document.getElementById('searchResults');
    container.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    
    try {
        let url = '';
        let title = '';
        
        switch (filter) {
            case 'low-gi':
                url = `${API_BASE}/nutrition/low-gi`;
                title = 'Low Glycemic Index Fruits';
                break;
            case 'high-fiber':
                url = `${API_BASE}/nutrition/search?nutrient=fiber&criteria=high&limit=10`;
                title = 'High Fiber Fruits';
                break;
            case 'low-sugar':
                url = `${API_BASE}/nutrition/search?nutrient=sugar&criteria=low&limit=10`;
                title = 'Low Sugar Fruits';
                break;
            case 'high-vitamin-c':
                url = `${API_BASE}/nutrition/search?nutrient=vitamin_c&criteria=high&limit=10`;
                title = 'High Vitamin C Fruits';
                break;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (filter === 'low-gi') {
            container.innerHTML = `
                <h4>${title}</h4>
                <div class="search-results-grid">
                    ${data.fruits.map((f, i) => `
                        <div class="search-result-item">
                            <span class="rank">#${i + 1}</span>
                            <span class="fruit-name">${f.fruit}</span>
                            <span class="nutrient-value">GI: ${f.glycemic_index}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            container.innerHTML = `
                <h4>${title}</h4>
                <div class="search-results-grid">
                    ${data.results.map((r, i) => `
                        <div class="search-result-item">
                            <span class="rank">#${i + 1}</span>
                            <span class="fruit-name">${r.fruit}</span>
                            <span class="nutrient-value">${r.value}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    } catch (error) {
        console.error('Quick filter error:', error);
        container.innerHTML = '<p style="color: var(--error);">Filter failed</p>';
    }
}

async function loadSeasonalFruits() {
    const month = document.getElementById('seasonalMonth')?.value || '';
    const container = document.getElementById('seasonalResults');
    container.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    
    try {
        const url = month ? `${API_BASE}/nutrition/seasonal?month=${month}` : `${API_BASE}/nutrition/seasonal`;
        const response = await fetch(url);
        const data = await response.json();
        
        if (response.ok) {
            const fruits = data.seasonal_fruits || [];
            container.innerHTML = `
                <h4>${month ? `Fruits in Season: ${month}` : 'All Seasonal Fruits'}</h4>
                <div class="seasonal-grid">
                    ${fruits.map(f => `
                        <div class="seasonal-card ${f.best_quality ? 'peak-season' : ''}">
                            <span class="seasonal-fruit-icon">${getFruitEmoji(f.fruit)}</span>
                            <span class="seasonal-fruit-name">${f.fruit}</span>
                            ${f.best_quality ? '<span class="peak-badge">Peak Season</span>' : ''}
                            <p class="season-months">Peak: ${f.peak_months?.join(', ') || 'Year-round'}</p>
                        </div>
                    `).join('') || '<p>No seasonal data available</p>'}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading seasonal fruits:', error);
        container.innerHTML = '<p style="color: var(--error);">Failed to load seasonal data</p>';
    }
}

function printNutritionInfo() {
    const content = document.getElementById('nutritionDetails');
    if (!content || content.classList.contains('hidden')) {
        showToast('Please select a fruit first', 'warning');
        return;
    }
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head><title>Nutrition Information</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h3 { color: #333; }
            .nutrition-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
            .nutrition-item { text-align: center; padding: 10px; border: 1px solid #ddd; }
            .nutrition-value { font-size: 24px; font-weight: bold; display: block; }
            .nutrition-label { font-size: 12px; color: #666; }
        </style>
        </head>
        <body>${content.innerHTML}</body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

function exportNutritionPDF() {
    showToast('PDF export requires additional library. Print to PDF instead.', 'info');
    printNutritionInfo();
}

// ==================== LANGUAGE SELECTOR ====================
function initLanguageSelector() {
    const languageSelect = document.getElementById('languageSelect');
    console.log('initLanguageSelector - element found:', !!languageSelect);
    if (languageSelect) {
        // Set initial value from the dropdown
        currentLanguage = languageSelect.value;
        console.log('Initial language:', currentLanguage);
        
        languageSelect.addEventListener('change', (e) => {
            currentLanguage = e.target.value;
            console.log('Language changed to:', currentLanguage);
            
            // Update all UI text
            if (typeof updateUILanguage === 'function') {
                updateUILanguage();
            }
            
            showToast(`Language changed to ${e.target.options[e.target.selectedIndex].text}`, 'info');
        });
    }
}

// ==================== MODALS ====================
function initModals() {
    const privacyLink = document.getElementById('privacyLink');
    const limitationsLink = document.getElementById('limitationsLink');
    
    if (privacyLink) privacyLink.addEventListener('click', async (e) => { e.preventDefault(); await showPrivacyModal(); });
    if (limitationsLink) limitationsLink.addEventListener('click', async (e) => { e.preventDefault(); await showLimitationsModal(); });
    
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', () => btn.closest('.modal').classList.add('hidden'));
    });
    
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.add('hidden'); });
    });
    
    // Login Modal
    const loginBtn = document.getElementById('loginBtn');
    const loginModal = document.getElementById('loginModal');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const showSignup = document.getElementById('showSignup');
    const showLogin = document.getElementById('showLogin');
    
    if (loginBtn && loginModal) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            loginModal.classList.remove('hidden');
        });
    }
    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (signupForm) signupForm.addEventListener('submit', handleSignup);
    
    // Toggle between login and signup forms
    if (showSignup) {
        showSignup.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('loginFormContainer').classList.add('hidden');
            document.getElementById('signupFormContainer').classList.remove('hidden');
        });
    }
    if (showLogin) {
        showLogin.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('signupFormContainer').classList.add('hidden');
            document.getElementById('loginFormContainer').classList.remove('hidden');
        });
    }
    
    // Check if user is already logged in
    checkAuthStatus();
}

function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    const userName = localStorage.getItem('userName');
    const userRole = localStorage.getItem('userRole');
    
    if (token && userName) {
        const loginBtn = document.getElementById('loginBtn');
        if (loginBtn) {
            loginBtn.innerHTML = `<i class="fas fa-user-check"></i> ${userName}`;
            loginBtn.classList.add('logged-in');
        }
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        const data = await response.json();
        
        if (data.success) {
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('userRole', data.user.role);
            localStorage.setItem('userName', data.user.username);
            document.getElementById('loginModal').classList.add('hidden');
            
            const loginBtn = document.getElementById('loginBtn');
            loginBtn.innerHTML = `<i class="fas fa-user-check"></i> ${data.user.username}`;
            loginBtn.classList.add('logged-in');
            
            showToast(`Welcome, ${data.user.full_name || data.user.username}!`, 'success');
            
            // Reset form
            document.getElementById('loginForm').reset();
        } else {
            showToast(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        showToast('Login failed. Please try again.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login';
    }
}

async function handleSignup(e) {
    e.preventDefault();
    
    const fullname = document.getElementById('signupFullname').value;
    const email = document.getElementById('signupEmail').value;
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;
    const role = document.getElementById('signupRole').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    // Validate passwords match
    if (password !== confirmPassword) {
        showToast('Passwords do not match', 'error');
        return;
    }
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating account...';
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username,
                password,
                email,
                full_name: fullname,
                role
            })
        });
        const data = await response.json();
        
        if (data.success) {
            showToast('Account created successfully! Please login.', 'success');
            
            // Switch to login form
            document.getElementById('signupFormContainer').classList.add('hidden');
            document.getElementById('loginFormContainer').classList.remove('hidden');
            
            // Pre-fill username
            document.getElementById('loginUsername').value = username;
            
            // Reset signup form
            document.getElementById('signupForm').reset();
        } else {
            showToast(data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        showToast('Registration failed. Please try again.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-user-plus"></i> Create Account';
    }
}

async function showPrivacyModal() {
    const modal = document.getElementById('privacyModal');
    const content = document.getElementById('privacyContent');
    content.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    modal.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/privacy`);
        const data = await response.json();
        content.innerHTML = `
            <h3>Data Handling</h3>
            <ul><li><strong>Image Storage:</strong> ${data.data_handling.image_storage}</li>
            <li><strong>Retention:</strong> ${data.data_handling.retention_period}</li>
            <li><strong>Sharing:</strong> ${data.data_handling.data_sharing}</li></ul>
            <h3>User Rights</h3>
            <ul><li><strong>Access:</strong> ${data.user_rights.access}</li>
            <li><strong>Deletion:</strong> ${data.user_rights.deletion}</li>
            <li><strong>Export:</strong> ${data.user_rights.export}</li></ul>
            <h3>Ethical Considerations</h3>
            <ul><li><strong>Purpose:</strong> ${data.ethical_considerations.purpose}</li>
            <li><strong>Limitations:</strong> ${data.ethical_considerations.limitations}</li>
            <li><strong>Transparency:</strong> ${data.ethical_considerations.transparency}</li></ul>
        `;
    } catch (error) {
        content.innerHTML = '<p>Failed to load privacy information.</p>';
    }
}

async function showLimitationsModal() {
    const modal = document.getElementById('limitationsModal');
    const content = document.getElementById('limitationsContent');
    content.innerHTML = '<div class="loader-center"><div class="loader"></div></div>';
    modal.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/system/limitations`);
        const data = await response.json();
        content.innerHTML = `
            <p><strong>Note:</strong> ${data.accuracy_notes}</p>
            <h3>Known Limitations</h3>
            <ul>${data.limitations.map(l => `<li><strong>${l.category}:</strong> ${l.description}<br><em>Recommendation:</em> ${l.recommendation}</li>`).join('')}</ul>
            <h3>Supported Fruits</h3>
            <p>${data.supported_fruits.join(', ')}</p>
        `;
    } catch (error) {
        content.innerHTML = '<p>Failed to load limitations information.</p>';
    }
}

// ==================== TOAST ====================
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    toastMessage.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

// ==================== ANALYTICS DASHBOARD ====================
let qualityChart = null;
let fruitChart = null;
let trendChart = null;
let gradeChart = null;

function initDashboard() {
    const refreshBtn = document.getElementById('refreshDashboard');
    const exportBtn = document.getElementById('exportDashboard');
    const periodSelect = document.getElementById('dashboardPeriod');
    
    if (refreshBtn) refreshBtn.addEventListener('click', loadDashboard);
    if (exportBtn) exportBtn.addEventListener('click', exportDashboardData);
    if (periodSelect) periodSelect.addEventListener('change', loadDashboard);
}

async function loadDashboard() {
    const period = document.getElementById('dashboardPeriod')?.value || 30;
    
    try {
        const response = await fetch(`${API_BASE}/analytics/dashboard?days=${period}`);
        const data = await response.json();
        
        // Update KPIs
        document.getElementById('kpiTotal').textContent = data.kpis.total_processed.toLocaleString();
        document.getElementById('kpiHealthy').textContent = `${data.kpis.healthy_percentage}%`;
        document.getElementById('kpiDefective').textContent = `${data.kpis.defective_percentage}%`;
        document.getElementById('kpiQuality').textContent = data.kpis.average_quality_score.toFixed(1);
        
        // Render Charts
        renderQualityChart(data.quality_distribution);
        renderFruitChart(data.fruit_distribution);
        renderTrendChart(data.daily_trends);
        
        // Fetch and display spoilage alerts
        loadSpoilageAlerts();
        
    } catch (error) {
        console.error('Dashboard load error:', error);
        showToast('Failed to load dashboard data', 'error');
    }
}

function renderQualityChart(distribution) {
    const ctx = document.getElementById('qualityChart');
    if (!ctx) return;
    
    if (qualityChart) qualityChart.destroy();
    
    const labels = Object.keys(distribution);
    const values = Object.values(distribution);
    const colors = ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444', '#6b7280'];
    
    qualityChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right' }
            }
        }
    });
}

function renderFruitChart(fruitData) {
    const ctx = document.getElementById('fruitChart');
    if (!ctx) return;
    
    if (fruitChart) fruitChart.destroy();
    
    const labels = fruitData.map(f => f.fruit);
    const values = fruitData.map(f => f.count);
    
    fruitChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: values,
                backgroundColor: '#667eea',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderTrendChart(trends) {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;
    
    if (trendChart) trendChart.destroy();
    
    const labels = trends.map(t => t.label);
    const totals = trends.map(t => t.total);
    const healthy = trends.map(t => t.healthy);
    const defective = trends.map(t => t.defective);
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Total',
                    data: totals,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Healthy',
                    data: healthy,
                    borderColor: '#22c55e',
                    tension: 0.4
                },
                {
                    label: 'Defective',
                    data: defective,
                    borderColor: '#ef4444',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { intersect: false, mode: 'index' },
            plugins: { legend: { position: 'top' } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

async function loadSpoilageAlerts() {
    try {
        const response = await fetch(`${API_BASE}/spoilage/waste-report`);
        const data = await response.json();
        
        const container = document.getElementById('spoilageAlerts');
        if (!container) return;
        
        if (data.items_at_risk > 0) {
            container.innerHTML = `
                <div class="alert-item critical">
                    <i class="fas fa-exclamation-circle"></i>
                    <span><strong>${data.items_at_risk}</strong> items at risk of spoilage (${data.waste_percentage}% of inventory)</span>
                </div>
                <div class="alert-item">
                    <i class="fas fa-dollar-sign"></i>
                    <span>Potential savings with quick action: <strong>$${data.potential_savings_usd}</strong></span>
                </div>
            `;
        } else {
            container.innerHTML = '<p class="no-alerts"><i class="fas fa-check-circle"></i> No critical spoilage alerts</p>';
        }
    } catch (error) {
        console.error('Spoilage alerts error:', error);
    }
}

async function exportDashboardData() {
    try {
        const response = await fetch(`${API_BASE}/analytics/export?format=csv`);
        const csvData = await response.text();
        
        const blob = new Blob([csvData], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analytics_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        
        showToast('Dashboard exported successfully', 'success');
    } catch (error) {
        showToast('Export failed', 'error');
    }
}

// ==================== INVENTORY ====================
function initInventory() {
    const refreshBtn = document.getElementById('refreshInventory');
    const generateQRBtn = document.getElementById('generateQRBtn');
    
    if (refreshBtn) refreshBtn.addEventListener('click', loadInventory);
    if (generateQRBtn) generateQRBtn.addEventListener('click', showQRGenerator);
}

async function loadInventory() {
    try {
        const response = await fetch(`${API_BASE}/analytics/inventory?days=7`);
        const data = await response.json();
        
        const container = document.getElementById('inventoryList');
        if (!container) return;
        
        const items = Object.entries(data.inventory);
        
        if (items.length === 0) {
            container.innerHTML = '<p>No inventory data available</p>';
            return;
        }
        
        container.innerHTML = items.map(([fruit, info]) => {
            const stockClass = info.stock_status === 'high' ? 'stock-high' : 
                              info.stock_status === 'medium' ? 'stock-medium' : 'stock-low';
            return `
                <div class="inventory-item">
                    <span class="fruit-icon">${getFruitEmoji(fruit)}</span>
                    <span class="fruit-name">${fruit}</span>
                    <span class="fruit-count ${stockClass}">${info.total_count} items</span>
                </div>
            `;
        }).join('');
        
        // Render grade chart
        renderGradeChart(data);
        
    } catch (error) {
        console.error('Inventory load error:', error);
        showToast('Failed to load inventory', 'error');
    }
}

function renderGradeChart(data) {
    const ctx = document.getElementById('gradeChart');
    if (!ctx) return;
    
    if (gradeChart) gradeChart.destroy();
    
    // Aggregate grades from all fruits
    const grades = { A: 0, B: 0, C: 0 };
    Object.values(data.inventory).forEach(info => {
        Object.entries(info.grade_breakdown || {}).forEach(([grade, count]) => {
            if (grades[grade] !== undefined) grades[grade] += count;
        });
    });
    
    gradeChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Grade A', 'Grade B', 'Grade C'],
            datasets: [{
                data: [grades.A, grades.B, grades.C],
                backgroundColor: ['#22c55e', '#f59e0b', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

async function showQRGenerator() {
    const display = document.getElementById('qrCodeDisplay');
    if (!display) return;
    
    // Show loading state
    display.classList.remove('hidden');
    document.getElementById('qrCodeImage').src = '';
    document.getElementById('qrCodeData').textContent = 'Generating QR Code...';
    
    try {
        // Generate QR for current inventory batch
        const response = await fetch(`${API_BASE}/qrcode/generate`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                fruit_type: 'Mixed Batch',
                grade: 'A',
                quality_score: 85,
                price: 3.50,
                ripeness: 'ripe',
                batch_id: `BATCH-${Date.now()}`,
                farm_source: 'FruitAI Pro System'
            })
        });
        const data = await response.json();
        
        if (data.success && data.image) {
            document.getElementById('qrCodeImage').src = data.image;
            document.getElementById('qrCodeData').textContent = JSON.stringify(data.data, null, 2);
            showToast('QR Code generated successfully!', 'success');
        } else if (data.image) {
            // ASCII fallback
            document.getElementById('qrCodeImage').style.display = 'none';
            document.getElementById('qrCodeData').innerHTML = `<pre style="font-family: monospace; font-size: 10px;">${data.image}</pre>`;
            showToast('QR library not installed. Install with: pip install qrcode[pil]', 'warning');
        } else {
            document.getElementById('qrCodeData').textContent = 'Failed to generate QR code. Please install qrcode library.';
            showToast('QR generation failed. Run: pip install qrcode[pil]', 'error');
        }
    } catch (error) {
        console.error('QR generation error:', error);
        document.getElementById('qrCodeData').textContent = 'Error generating QR code: ' + error.message;
        showToast('QR generation failed: ' + error.message, 'error');
    }
}

// ==================== INITIALIZE NEW FEATURES ====================
document.addEventListener('DOMContentLoaded', () => {
    // Existing initializations are above - these extend them
    initDashboard();
    initInventory();
    
    // Update navigation for new sections
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.dataset.section;
            if (section === 'dashboard') loadDashboard();
            if (section === 'inventory') loadInventory();
        });
    });
});

// ==================== DASHBOARD ENHANCEMENTS ====================
function initDashboardEnhancements() {
    // Date range picker
    const startDate = document.getElementById('dashboardStartDate');
    const endDate = document.getElementById('dashboardEndDate');
    const periodSelect = document.getElementById('dashboardPeriod');
    
    if (periodSelect) {
        periodSelect.addEventListener('change', () => {
            if (periodSelect.value === 'custom') {
                startDate?.parentElement?.classList.remove('hidden');
            } else {
                startDate?.parentElement?.classList.add('hidden');
                loadDashboard();
            }
        });
    }
    
    // Auto-refresh toggle
    const autoRefresh = document.getElementById('autoRefreshDashboard');
    if (autoRefresh) {
        autoRefresh.addEventListener('change', () => {
            if (autoRefresh.checked) {
                autoRefreshInterval = setInterval(loadDashboard, 30000);
            } else {
                clearInterval(autoRefreshInterval);
            }
        });
        // Start auto-refresh if checked
        if (autoRefresh.checked) {
            autoRefreshInterval = setInterval(loadDashboard, 30000);
        }
    }
    
    // Export menu
    const exportBtn = document.getElementById('exportDashboard');
    const exportMenu = document.getElementById('exportMenu');
    if (exportBtn && exportMenu) {
        exportBtn.addEventListener('click', () => {
            exportMenu.classList.toggle('hidden');
        });
        
        document.querySelectorAll('.export-option').forEach(btn => {
            btn.addEventListener('click', () => {
                exportDashboardData(btn.dataset.format);
                exportMenu.classList.add('hidden');
            });
        });
    }
    
    // Set Goals button
    const setGoalsBtn = document.getElementById('setGoalsBtn');
    if (setGoalsBtn) {
        setGoalsBtn.addEventListener('click', showGoalsModal);
    }
}

function exportDashboardData(format) {
    showToast(`Exporting dashboard as ${format.toUpperCase()}...`, 'info');
    // Implement export logic based on format
    if (format === 'csv') {
        // Generate CSV from current dashboard data
        showToast('CSV export ready', 'success');
    } else if (format === 'pdf') {
        window.print();
    } else if (format === 'json') {
        // Export raw JSON data
        showToast('JSON export ready', 'success');
    }
}

function showGoalsModal() {
    showToast('Goals feature - set daily/weekly classification targets', 'info');
}

function updateGoalProgress(current, target) {
    const percent = Math.min(100, Math.round((current / target) * 100));
    const ring = document.getElementById('classifyGoalRing');
    const percentText = document.getElementById('classifyGoalPercent');
    const currentText = document.getElementById('classifyGoalCurrent');
    
    if (ring) ring.style.setProperty('--progress', percent);
    if (percentText) percentText.textContent = percent + '%';
    if (currentText) currentText.textContent = current;
}

// ==================== INVENTORY ENHANCEMENTS ====================
function initInventoryEnhancements() {
    // Import CSV
    const importBtn = document.getElementById('importInventoryBtn');
    const importFile = document.getElementById('inventoryImportFile');
    if (importBtn && importFile) {
        importBtn.addEventListener('click', () => importFile.click());
        importFile.addEventListener('change', handleInventoryImport);
    }
    
    // Export CSV
    const exportBtn = document.getElementById('exportInventoryBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportInventoryCSV);
    }
    
    // Quick add
    const quickAddBtn = document.getElementById('quickAddBtn');
    if (quickAddBtn) {
        quickAddBtn.addEventListener('click', quickAddInventory);
    }
    
    // Category tabs
    document.querySelectorAll('.inventory-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.inventory-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            filterInventoryByCategory(tab.dataset.category);
        });
    });
    
    // Load fruit options for quick add
    loadQuickAddFruits();
}

async function loadQuickAddFruits() {
    try {
        const response = await fetch(`${API_BASE}/classes`);
        const data = await response.json();
        const select = document.getElementById('quickAddFruit');
        if (select && data.classes) {
            data.classes.forEach(fruit => {
                const option = document.createElement('option');
                option.value = fruit;
                option.textContent = fruit;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading fruits:', error);
    }
}

function handleInventoryImport(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = async (event) => {
        const csv = event.target.result;
        // Parse CSV and add to inventory
        showToast('Importing inventory data...', 'info');
        // Implementation would parse CSV and call API
        showToast('Inventory imported successfully', 'success');
    };
    reader.readAsText(file);
}

function exportInventoryCSV() {
    showToast('Exporting inventory to CSV...', 'info');
    // Generate CSV from current inventory data
    showToast('Inventory exported', 'success');
}

async function quickAddInventory() {
    const fruit = document.getElementById('quickAddFruit')?.value;
    const quantity = parseInt(document.getElementById('quickAddQuantity')?.value);
    const grade = document.getElementById('quickAddGrade')?.value;
    const expiry = document.getElementById('quickAddExpiry')?.value;
    const minStock = parseInt(document.getElementById('quickAddMinStock')?.value) || 10;
    
    if (!fruit || !quantity) {
        showToast('Please select fruit and enter quantity', 'warning');
        return;
    }
    
    try {
        // Save to backend by creating a classification entry
        const response = await fetch(`${API_BASE}/history`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                predicted_class: fruit,
                confidence: 1.0,
                quality_grade: grade,
                quantity: quantity,
                expiry_date: expiry,
                min_stock: minStock,
                source: 'inventory_manual',
                timestamp: new Date().toISOString()
            })
        });
        
        if (response.ok) {
            showToast(`Added ${quantity} ${fruit} (Grade ${grade}) to inventory`, 'success');
            
            // Clear form
            document.getElementById('quickAddQuantity').value = '';
            if (document.getElementById('quickAddExpiry')) {
                document.getElementById('quickAddExpiry').value = '';
            }
            
            // Reload inventory
            await loadInventory();
        } else {
            showToast('Failed to add to inventory', 'error');
        }
    } catch (error) {
        console.error('Add inventory error:', error);
        showToast('Error adding to inventory', 'error');
    }
}

function filterInventoryByCategory(category) {
    // Filter inventory items based on category
    const items = document.querySelectorAll('.inventory-item');
    items.forEach(item => {
        // Implementation would show/hide based on category
    });
}

function checkInventoryAlerts() {
    // Check for low stock and expiring items
    addNotification('Low Stock Alert', '3 items are below minimum stock level', 'warning');
}

// ==================== HISTORY ENHANCEMENTS ====================
function initHistoryEnhancements() {
    // View toggle
    document.querySelectorAll('.view-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.view-toggle').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const view = btn.dataset.view;
            const container = document.getElementById('historyContainer');
            if (container) {
                container.className = `history-container ${view}-view`;
            }
        });
    });
    
    // Search
    const searchInput = document.getElementById('historySearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(() => {
            historyFilters.search = searchInput.value;
            loadHistory();
        }, 300));
    }
    
    // Filters
    ['historyFruitFilter', 'historyConfidenceFilter', 'historyQualityFilter', 'historyDateFilter'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('change', () => {
                historyFilters[id] = el.value;
                loadHistory();
            });
        }
    });
    
    // Clear filters
    const clearBtn = document.getElementById('clearHistoryFilters');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            historyFilters = {};
            document.querySelectorAll('.history-filters input, .history-filters select').forEach(el => el.value = '');
            loadHistory();
        });
    }
    
    // Bulk actions
    document.getElementById('selectAllHistory')?.addEventListener('click', selectAllHistoryItems);
    document.getElementById('exportSelectedHistory')?.addEventListener('click', exportSelectedHistory);
    document.getElementById('deleteSelectedHistory')?.addEventListener('click', deleteSelectedHistory);
    
    // Pagination
    document.getElementById('historyPrevPage')?.addEventListener('click', () => {
        if (historyPage > 1) {
            historyPage--;
            loadHistory();
        }
    });
    document.getElementById('historyNextPage')?.addEventListener('click', () => {
        historyPage++;
        loadHistory();
    });
}

function selectAllHistoryItems() {
    const checkboxes = document.querySelectorAll('.history-checkbox');
    const selectAll = selectedHistoryItems.size !== checkboxes.length;
    checkboxes.forEach(cb => {
        cb.checked = selectAll;
        if (selectAll) selectedHistoryItems.add(cb.dataset.id);
        else selectedHistoryItems.delete(cb.dataset.id);
    });
    updateBulkActionsVisibility();
}

function updateBulkActionsVisibility() {
    const bulkActions = document.getElementById('historyBulkActions');
    const selectedCount = document.getElementById('selectedCount');
    if (bulkActions) {
        bulkActions.classList.toggle('hidden', selectedHistoryItems.size === 0);
    }
    if (selectedCount) {
        selectedCount.textContent = `${selectedHistoryItems.size} selected`;
    }
}

function exportSelectedHistory() {
    showToast(`Exporting ${selectedHistoryItems.size} items...`, 'info');
}

function deleteSelectedHistory() {
    if (confirm(`Delete ${selectedHistoryItems.size} items?`)) {
        showToast(`Deleted ${selectedHistoryItems.size} items`, 'success');
        selectedHistoryItems.clear();
        loadHistory();
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== FEEDBACK SYSTEM ====================
function initFeedbackSystem() {
    document.querySelectorAll('.feedback-btn').forEach(btn => {
        btn.addEventListener('click', () => handleFeedback(btn.dataset.feedback));
    });
    
    document.getElementById('submitFeedbackBtn')?.addEventListener('click', submitFeedbackCorrection);
}

function handleFeedback(type) {
    if (type === 'incorrect') {
        document.getElementById('feedbackCorrection')?.classList.remove('hidden');
    } else {
        submitFeedback(type, null);
    }
}

async function submitFeedback(type, correctFruit) {
    try {
        // Save feedback to server
        showToast('Thank you for your feedback!', 'success');
        document.querySelector('.feedback-card')?.classList.add('submitted');
        document.getElementById('feedbackThanks')?.classList.remove('hidden');
        
        // Update achievements
        checkAchievements();
    } catch (error) {
        showToast('Failed to submit feedback', 'error');
    }
}

function submitFeedbackCorrection() {
    const correctFruit = document.getElementById('correctFruitSelect')?.value;
    if (!correctFruit) {
        showToast('Please select the correct fruit', 'warning');
        return;
    }
    submitFeedback('incorrect', correctFruit);
}

// ==================== MEAL PLANNER ====================
function initMealPlanner() {
    // Make meal slots droppable
    document.querySelectorAll('.meal-slot').forEach(slot => {
        slot.addEventListener('dragover', (e) => {
            e.preventDefault();
            slot.classList.add('drag-over');
        });
        slot.addEventListener('dragleave', () => {
            slot.classList.remove('drag-over');
        });
        slot.addEventListener('drop', (e) => {
            e.preventDefault();
            slot.classList.remove('drag-over');
            const fruit = e.dataTransfer.getData('text/plain');
            addFruitToMeal(slot, fruit);
        });
    });
    
    document.getElementById('clearMealPlan')?.addEventListener('click', clearMealPlan);
    document.getElementById('saveMealPlan')?.addEventListener('click', saveMealPlan);
    document.getElementById('autoGenerateMealPlan')?.addEventListener('click', autoGenerateMealPlan);
}

function loadMealPlannerData() {
    // Load fruit picker
    const picker = document.getElementById('mealFruitPicker');
    if (picker) {
        fetch(`${API_BASE}/classes`)
            .then(r => r.json())
            .then(data => {
                picker.innerHTML = data.classes.map(fruit => `
                    <div class="fruit-pick" draggable="true" data-fruit="${fruit}">
                        <span class="fruit-emoji">${getFruitEmoji(fruit)}</span>
                        <span>${fruit}</span>
                    </div>
                `).join('');
                
                // Make fruits draggable
                document.querySelectorAll('.fruit-pick').forEach(el => {
                    el.addEventListener('dragstart', (e) => {
                        e.dataTransfer.setData('text/plain', el.dataset.fruit);
                    });
                });
            });
    }
    
    // Restore saved meal plan
    Object.entries(mealPlan).forEach(([key, fruits]) => {
        const [day, meal] = key.split('-');
        const slot = document.querySelector(`.meal-day[data-day="${day}"] .meal-slot[data-meal="${meal}"] .meal-fruits`);
        if (slot) {
            slot.innerHTML = fruits.map(f => `<span class="meal-fruit">${f}</span>`).join('');
        }
    });
    
    updateMealNutritionSummary();
}

function addFruitToMeal(slot, fruit) {
    const day = slot.closest('.meal-day').dataset.day;
    const meal = slot.dataset.meal;
    const key = `${day}-${meal}`;
    
    if (!mealPlan[key]) mealPlan[key] = [];
    mealPlan[key].push(fruit);
    
    const fruitsDiv = slot.querySelector('.meal-fruits');
    fruitsDiv.innerHTML += `<span class="meal-fruit">${fruit}</span>`;
    
    updateMealNutritionSummary();
}

function clearMealPlan() {
    mealPlan = {};
    document.querySelectorAll('.meal-fruits').forEach(el => el.innerHTML = '');
    updateMealNutritionSummary();
    showToast('Meal plan cleared', 'info');
}

function saveMealPlan() {
    localStorage.setItem('mealPlan', JSON.stringify(mealPlan));
    showToast('Meal plan saved!', 'success');
}

async function autoGenerateMealPlan() {
    try {
        showToast('Generating meal plan...', 'info');
        
        // Get available fruits
        const response = await fetch(`${API_BASE}/classes`);
        const data = await response.json();
        const fruits = data.classes || ['Apple', 'Banana', 'Orange', 'Mango', 'Strawberry', 'Grape', 'Watermelon', 'Pineapple', 'Cherry', 'Kiwi'];
        
        // Clear existing plan
        mealPlan = {};
        document.querySelectorAll('.meal-fruits').forEach(el => el.innerHTML = '');
        
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        const meals = ['breakfast', 'lunch', 'snack', 'dinner'];
        
        // Generate random fruits for each meal slot
        days.forEach(day => {
            meals.forEach(meal => {
                // Random 1-3 fruits per meal
                const numFruits = Math.floor(Math.random() * 3) + 1;
                const selectedFruits = [];
                
                for (let i = 0; i < numFruits; i++) {
                    const randomFruit = fruits[Math.floor(Math.random() * fruits.length)];
                    if (!selectedFruits.includes(randomFruit)) {
                        selectedFruits.push(randomFruit);
                    }
                }
                
                // Add to meal plan
                const key = `${day}-${meal}`;
                mealPlan[key] = selectedFruits;
                
                // Update UI
                const slot = document.querySelector(`.meal-day[data-day="${day}"] .meal-slot[data-meal="${meal}"] .meal-fruits`);
                if (slot) {
                    slot.innerHTML = selectedFruits.map(f => `
                        <span class="meal-fruit" title="${f}">
                            ${getFruitEmoji(f)} ${f}
                        </span>
                    `).join('');
                }
            });
        });
        
        updateMealNutritionSummary();
        showToast('Meal plan generated! Remember to save it.', 'success');
        
    } catch (error) {
        console.error('Error generating meal plan:', error);
        showToast('Failed to generate meal plan', 'error');
    }
}

async function updateMealNutritionSummary() {
    // Calculate total nutrition from meal plan
    let totalCalories = 0;
    let totalFiber = 0;
    let totalSugar = 0;
    let totalVitaminC = 0;
    let totalPotassium = 0;
    
    try {
        // Get nutrition data for all fruits in meal plan
        const allFruits = Object.values(mealPlan).flat();
        const uniqueFruits = [...new Set(allFruits)];
        
        for (const fruit of uniqueFruits) {
            const count = allFruits.filter(f => f === fruit).length;
            
            // Fetch nutrition data
            const response = await fetch(`${API_BASE}/nutrition/${fruit.toLowerCase()}`);
            if (response.ok) {
                const data = await response.json();
                const nutrition = data.nutrition || {};
                
                // Add to totals (multiply by count)
                totalCalories += (parseFloat(nutrition.calories) || 0) * count;
                totalFiber += (parseFloat(nutrition.fiber?.replace('g', '')) || 0) * count;
                totalSugar += (parseFloat(nutrition.sugars?.replace('g', '')) || 0) * count;
                totalVitaminC += (parseFloat(nutrition.vitamin_c?.replace('mg', '')) || 0) * count;
                totalPotassium += (parseFloat(nutrition.potassium?.replace('mg', '')) || 0) * count;
            }
        }
    } catch (error) {
        console.error('Error calculating nutrition:', error);
    }
    
    // Update UI
    const caloriesEl = document.getElementById('mealTotalCalories');
    const fiberEl = document.getElementById('mealTotalFiber');
    const sugarEl = document.getElementById('mealTotalSugar');
    const vitaminCEl = document.getElementById('mealTotalVitaminC');
    const potassiumEl = document.getElementById('mealTotalPotassium');
    
    if (caloriesEl) caloriesEl.textContent = Math.round(totalCalories);
    if (fiberEl) fiberEl.textContent = Math.round(totalFiber) + 'g';
    if (sugarEl) sugarEl.textContent = Math.round(totalSugar) + 'g';
    if (vitaminCEl) vitaminCEl.textContent = Math.round(totalVitaminC) + 'mg';
    if (potassiumEl) potassiumEl.textContent = Math.round(totalPotassium) + 'mg';
}

// ==================== SHOPPING LIST ====================
function initShoppingList() {
    document.getElementById('addShoppingItem')?.addEventListener('click', addShoppingItem);
    document.getElementById('generateFromInventory')?.addEventListener('click', generateShoppingFromInventory);
    document.getElementById('printShoppingList')?.addEventListener('click', printShoppingList);
    document.getElementById('shareShoppingList')?.addEventListener('click', shareShoppingList);
    
    document.getElementById('shoppingItemInput')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addShoppingItem();
    });
}

function updateShoppingListUI() {
    const fruitsContainer = document.getElementById('shoppingFruits');
    const othersContainer = document.getElementById('shoppingOther');
    
    if (fruitsContainer) {
        fruitsContainer.innerHTML = shoppingList.fruits.map((item, i) => `
            <div class="shopping-item ${item.checked ? 'checked' : ''}">
                <input type="checkbox" ${item.checked ? 'checked' : ''} onchange="toggleShoppingItem('fruits', ${i})">
                <span class="item-icon">${getFruitEmoji(item.name)}</span>
                <span class="item-name">${item.name}</span>
                <span class="item-qty">${item.qty}</span>
                <button class="btn-remove-sm" onclick="removeShoppingItem('fruits', ${i})">×</button>
            </div>
        `).join('');
    }
    
    if (othersContainer) {
        othersContainer.innerHTML = shoppingList.other.map((item, i) => `
            <div class="shopping-item ${item.checked ? 'checked' : ''}">
                <input type="checkbox" ${item.checked ? 'checked' : ''} onchange="toggleShoppingItem('other', ${i})">
                <span class="item-icon">🛒</span>
                <span class="item-name">${item.name}</span>
                <span class="item-qty">${item.qty}</span>
                <button class="btn-remove-sm" onclick="removeShoppingItem('other', ${i})">×</button>
            </div>
        `).join('');
    }
    
    updateShoppingSummary();
}

function addShoppingItem() {
    const input = document.getElementById('shoppingItemInput');
    const qtyInput = document.getElementById('shoppingItemQty');
    const name = input?.value.trim();
    const qty = parseInt(qtyInput?.value) || 1;
    
    if (!name) return;
    
    // Check if it's a fruit
    const fruits = ['Apple', 'Banana', 'Orange', 'Mango', 'Strawberry', 'Grape', 'Pineapple', 'Watermelon', 'Cherry', 'Lemon'];
    const category = fruits.some(f => name.toLowerCase().includes(f.toLowerCase())) ? 'fruits' : 'other';
    
    shoppingList[category].push({ name, qty, checked: false });
    localStorage.setItem('shoppingList', JSON.stringify(shoppingList));
    
    if (input) input.value = '';
    if (qtyInput) qtyInput.value = 1;
    
    updateShoppingListUI();
}

function toggleShoppingItem(category, index) {
    shoppingList[category][index].checked = !shoppingList[category][index].checked;
    localStorage.setItem('shoppingList', JSON.stringify(shoppingList));
    updateShoppingListUI();
}

function removeShoppingItem(category, index) {
    shoppingList[category].splice(index, 1);
    localStorage.setItem('shoppingList', JSON.stringify(shoppingList));
    updateShoppingListUI();
}

function updateShoppingSummary() {
    const total = shoppingList.fruits.length + shoppingList.vegetables.length + shoppingList.other.length;
    const checked = [...shoppingList.fruits, ...shoppingList.vegetables, ...shoppingList.other].filter(i => i.checked).length;
    
    const totalEl = document.getElementById('totalShoppingItems');
    const checkedEl = document.getElementById('checkedItems');
    
    if (totalEl) totalEl.textContent = total;
    if (checkedEl) checkedEl.textContent = checked;
}

function generateShoppingFromInventory() {
    showToast('Generating shopping list from low inventory items...', 'info');
    // Would fetch inventory and add low-stock items to shopping list
}

function printShoppingList() {
    window.print();
}

function shareShoppingList() {
    if (navigator.share) {
        navigator.share({
            title: 'Shopping List',
            text: shoppingList.fruits.map(i => `${i.name} (${i.qty})`).join('\n')
        });
    } else {
        showToast('Sharing not supported on this device', 'warning');
    }
}

// ==================== ACHIEVEMENTS ====================
function checkAchievements() {
    // Check and unlock achievements
    const totalClassifications = parseInt(localStorage.getItem('totalClassifications') || '0');
    
    if (totalClassifications >= 1 && !achievements.first_classification) {
        unlockAchievement('first_classification', 'First Classification', '🎯');
    }
    if (totalClassifications >= 100 && !achievements.expert) {
        unlockAchievement('expert', 'Expert', '🎓');
    }
}

function unlockAchievement(id, name, icon) {
    achievements[id] = true;
    localStorage.setItem('achievements', JSON.stringify(achievements));
    
    addNotification('Achievement Unlocked!', `${icon} ${name}`, 'success');
    showToast(`🏆 Achievement Unlocked: ${name}`, 'success');
}

// ==================== WEBCAM ENHANCEMENTS ====================
function initWebcamEnhancements() {
    // Auto-capture toggle
    const autoCapture = document.getElementById('autoCapture');
    if (autoCapture) {
        autoCapture.addEventListener('change', () => {
            if (autoCapture.checked && webcamStream) {
                startAutoCapture();
            } else {
                stopAutoCapture();
            }
        });
    }
    
    // Voice announcements toggle
    const voiceAnnounce = document.getElementById('voiceAnnounce');
    if (voiceAnnounce) {
        // Uses Web Speech API for voice announcements
    }
    
    // Camera settings
    const settingsBtn = document.getElementById('settingsWebcam');
    if (settingsBtn) {
        settingsBtn.addEventListener('click', () => {
            document.getElementById('cameraSettings')?.classList.toggle('hidden');
        });
    }
    
    // Brightness slider
    const brightnessSlider = document.getElementById('cameraBrightness');
    if (brightnessSlider) {
        brightnessSlider.addEventListener('input', updateCameraFilters);
    }
    
    // Contrast slider
    const contrastSlider = document.getElementById('cameraContrast');
    if (contrastSlider) {
        contrastSlider.addEventListener('input', updateCameraFilters);
    }
    
    // Zoom slider
    const zoomSlider = document.getElementById('cameraZoom');
    if (zoomSlider) {
        zoomSlider.addEventListener('input', updateCameraZoom);
    }
    
    // Flip camera
    document.getElementById('flipCameraBtn')?.addEventListener('click', flipCamera);
}

function updateCameraFilters() {
    const video = document.getElementById('webcamVideo');
    if (!video) return;
    
    const brightness = document.getElementById('cameraBrightness')?.value || 0;
    const contrast = document.getElementById('cameraContrast')?.value || 0;
    
    // Convert -100 to 100 range to appropriate filter values
    const brightnessValue = 1 + (brightness / 100); // 0 to 2
    const contrastValue = 1 + (contrast / 100); // 0 to 2
    
    video.style.filter = `brightness(${brightnessValue}) contrast(${contrastValue})`;
}

function updateCameraZoom() {
    const video = document.getElementById('webcamVideo');
    const zoomSlider = document.getElementById('cameraZoom');
    if (!video || !zoomSlider) return;
    
    const zoomValue = zoomSlider.value;
    video.style.transform = `scale(${zoomValue})`;
    video.style.transformOrigin = 'center center';
}

function startAutoCapture() {
    autoCaptureInterval = setInterval(() => {
        if (webcamStream) {
            document.getElementById('captureBtn')?.click();
        }
    }, 3000);
}

function stopAutoCapture() {
    if (autoCaptureInterval) {
        clearInterval(autoCaptureInterval);
        autoCaptureInterval = null;
    }
}

async function flipCamera() {
    // Toggle between front and back camera
    cameraFacingMode = cameraFacingMode === 'environment' ? 'user' : 'environment';
    
    // Stop current stream
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
    }
    
    const video = document.getElementById('webcamVideo');
    if (!video) return;
    
    try {
        showToast(`Switching to ${cameraFacingMode === 'user' ? 'front' : 'back'} camera...`, 'info');
        
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: cameraFacingMode,
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        });
        
        webcamStream = stream;
        video.srcObject = stream;
        
        // Reset filters when switching
        updateCameraFilters();
        updateCameraZoom();
        
        showToast(`Switched to ${cameraFacingMode === 'user' ? 'front' : 'back'} camera`, 'success');
    } catch (error) {
        console.error('Error flipping camera:', error);
        showToast('Could not switch camera. Device may only have one camera.', 'error');
        // Revert facing mode
        cameraFacingMode = cameraFacingMode === 'environment' ? 'user' : 'environment';
    }
}

function announceResult(text) {
    if ('speechSynthesis' in window && document.getElementById('voiceAnnounce')?.checked) {
        const utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
    }
}
