document.addEventListener('DOMContentLoaded', function() {
    console.log('🔮 FalsifyX Detection Lab - Initializing...');
    
    // Check if we're on the login page
    if (window.location.pathname.includes('/login') || window.location.pathname.includes('/register')) {
        console.log('On auth page, skipping initialization');
        return;
    }
    
    // Initialize the lab
    initializeLab();
});

// Global state management
const LabState = {
    currentSection: 'image',
    analysisHistory: {
        image: JSON.parse(localStorage.getItem('imageHistory') || '[]'),
        video: JSON.parse(localStorage.getItem('videoHistory') || '[]'),
        audio: JSON.parse(localStorage.getItem('audioHistory') || '[]')
    },
    totalAnalyses: 0,
    fakeDetected: 0
};

function initializeLab() {
    console.log('🧠 Initializing FalsifyX Detection Lab...');
    
    // Get all DOM elements
    const elements = getDOMElements();
    if (!elements) return;
    
    // Initialize navigation
    initializeNavigation(elements);
    
    // Initialize each section
    initializeImageSection(elements);
    initializeVideoSection(elements);
    initializeAudioSection(elements);
    
    // Initialize modals
    initializeModals(elements);
    
    // Load existing history
    loadAllHistory(elements);
    
    // Update statistics
    updateStatistics(elements);
    
    console.log('✅ FalsifyX Detection Lab initialized successfully');
}

function getDOMElements() {
    const elements = {
        // Navigation
        navItems: document.querySelectorAll('.nav-item'),
        sections: {
            image: document.getElementById('imageSection'),
            video: document.getElementById('videoSection'),
            audio: document.getElementById('audioSection')
        },
        
        // File inputs
        imageInput: document.getElementById('imageInput'),
        videoInput: document.getElementById('videoInput'),
        audioInput: document.getElementById('audioInput'),
        
        // Upload areas
        imageUploadArea: document.getElementById('imageUploadArea'),
        videoUploadArea: document.getElementById('videoUploadArea'),
        audioUploadArea: document.getElementById('audioUploadArea'),
        
        // Preview areas
        imagePreviewArea: document.getElementById('imagePreviewArea'),
        videoPreviewArea: document.getElementById('videoPreviewArea'),
        audioPreviewArea: document.getElementById('audioPreviewArea'),
        
        // Preview elements
        imagePreview: document.getElementById('imagePreview'),
        videoPreview: document.getElementById('videoPreview'),
        audioPreview: document.getElementById('audioPreview'),
        
        // Action buttons
        analyzeImageBtn: document.getElementById('analyzeImageBtn'),
        analyzeVideoBtn: document.getElementById('analyzeVideoBtn'),
        analyzeAudioBtn: document.getElementById('analyzeAudioBtn'),
        clearImageBtn: document.getElementById('clearImageBtn'),
        clearVideoBtn: document.getElementById('clearVideoBtn'),
        clearAudioBtn: document.getElementById('clearAudioBtn'),
        
        // History elements
        imageHistory: document.getElementById('imageHistory'),
        videoHistory: document.getElementById('videoHistory'),
        audioHistory: document.getElementById('audioHistory'),
        imageHistoryFilter: document.getElementById('imageHistoryFilter'),
        videoHistoryFilter: document.getElementById('videoHistoryFilter'),
        audioHistoryFilter: document.getElementById('audioHistoryFilter'),
        
        // Clear history buttons
        clearImageHistory: document.getElementById('clearImageHistory'),
        clearVideoHistory: document.getElementById('clearVideoHistory'),
        clearAudioHistory: document.getElementById('clearAudioHistory'),
        
        // Statistics
        totalAnalyses: document.getElementById('totalAnalyses'),
        fakeDetected: document.getElementById('fakeDetected'),
        imageBadge: document.getElementById('imageBadge'),
        videoBadge: document.getElementById('videoBadge'),
        audioBadge: document.getElementById('audioBadge'),
        
        // Modals
        analysisModal: document.getElementById('analysisModal'),
        resultsModal: document.getElementById('resultsModal'),
        closeModal: document.getElementById('closeModal'),
        closeResultsModal: document.getElementById('closeResultsModal'),
        analysisStatus: document.getElementById('analysisStatus'),
        analysisStep: document.getElementById('analysisStep'),
        progressFill: document.getElementById('progressFill'),
        progressText: document.getElementById('progressText'),
        resultsContent: document.getElementById('resultsContent'),
        resultsTitle: document.getElementById('resultsTitle'),
        saveResults: document.getElementById('saveResults'),
        newAnalysis: document.getElementById('newAnalysis')
    };
    
    // Check if required elements exist
    if (!elements.navItems.length) {
        console.error('Required DOM elements not found');
        return null;
    }
    
    return elements;
}

function initializeNavigation(elements) {
    console.log('🔧 Setting up navigation...');
    
    elements.navItems.forEach(item => {
        item.addEventListener('click', () => {
            const section = item.dataset.section;
            switchSection(section, elements);
        });
    });
}

function switchSection(section, elements) {
    console.log(`🔄 Switching to ${section} section`);
    
    LabState.currentSection = section;
    
    // Update navigation
    elements.navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.section === section);
    });
    
    // Update sections
    Object.keys(elements.sections).forEach(key => {
        elements.sections[key].classList.toggle('active', key === section);
    });
    
    // Clear any open modals
    closeAllModals(elements);
}

function initializeImageSection(elements) {
    console.log('📸 Setting up image section...');
    
    // File input handler
    elements.imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            showImagePreview(file, elements);
        } else if (file) {
            showNotification('Please select a valid image file', 'error');
        }
    });
    
    // Drag and drop
    setupDragAndDrop(elements.imageUploadArea, elements.imageInput, 'image');
    
    // Action buttons
    elements.analyzeImageBtn.addEventListener('click', () => {
        const file = elements.imageInput.files[0];
        if (file) {
            analyzeFile(file, 'image', elements);
        }
    });
    
    elements.clearImageBtn.addEventListener('click', () => {
        clearImagePreview(elements);
    });
    
    // History controls
    elements.clearImageHistory.addEventListener('click', () => {
        clearHistory('image', elements);
    });
    
    elements.imageHistoryFilter.addEventListener('change', () => {
        filterHistory('image', elements);
    });
}

function initializeVideoSection(elements) {
    console.log('🎬 Setting up video section...');
    
    // File input handler
    elements.videoInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('video/')) {
            showVideoPreview(file, elements);
        } else if (file) {
            showNotification('Please select a valid video file', 'error');
        }
    });
    
    // Drag and drop
    setupDragAndDrop(elements.videoUploadArea, elements.videoInput, 'video');
    
    // Action buttons
    elements.analyzeVideoBtn.addEventListener('click', () => {
        const file = elements.videoInput.files[0];
        if (file) {
            analyzeFile(file, 'video', elements);
        }
    });
    
    elements.clearVideoBtn.addEventListener('click', () => {
        clearVideoPreview(elements);
    });
    
    // History controls
    elements.clearVideoHistory.addEventListener('click', () => {
        clearHistory('video', elements);
    });
    
    elements.videoHistoryFilter.addEventListener('change', () => {
        filterHistory('video', elements);
    });
}

function initializeAudioSection(elements) {
    console.log('🎵 Setting up audio section...');
    
    // File input handler
    elements.audioInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('audio/')) {
            showAudioPreview(file, elements);
        } else if (file) {
            showNotification('Please select a valid audio file', 'error');
        }
    });
    
    // Drag and drop
    setupDragAndDrop(elements.audioUploadArea, elements.audioInput, 'audio');
    
    // Action buttons
    elements.analyzeAudioBtn.addEventListener('click', () => {
        const file = elements.audioInput.files[0];
        if (file) {
            analyzeFile(file, 'audio', elements);
        }
    });
    
    elements.clearAudioBtn.addEventListener('click', () => {
        clearAudioPreview(elements);
    });
    
    // History controls
    elements.clearAudioHistory.addEventListener('click', () => {
        clearHistory('audio', elements);
    });
    
    elements.audioHistoryFilter.addEventListener('change', () => {
        filterHistory('audio', elements);
    });
}

function setupDragAndDrop(uploadArea, input, type) {
    const uploadZone = uploadArea.querySelector('.upload-zone');
    
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });
    
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith(type + '/')) {
                input.files = files;
                input.dispatchEvent(new Event('change'));
            } else {
                showNotification(`Please drop a ${type} file`, 'error');
            }
        }
    });
}

function showImagePreview(file, elements) {
    console.log('📸 Showing image preview...');
    
    const url = URL.createObjectURL(file);
    elements.imagePreview.src = url;
    elements.imagePreviewArea.classList.remove('hidden');
}

function showVideoPreview(file, elements) {
    console.log('🎬 Showing video preview...');
    
    const url = URL.createObjectURL(file);
    elements.videoPreview.src = url;
    elements.videoPreviewArea.classList.remove('hidden');
}

function showAudioPreview(file, elements) {
    console.log('🎵 Showing audio preview...');
    
    const url = URL.createObjectURL(file);
    elements.audioPreview.src = url;
    elements.audioPreviewArea.classList.remove('hidden');
}

function clearImagePreview(elements) {
    elements.imagePreviewArea.classList.add('hidden');
    elements.imageInput.value = '';
    if (elements.imagePreview.src.startsWith('blob:')) {
        URL.revokeObjectURL(elements.imagePreview.src);
    }
    elements.imagePreview.src = '';
}

function clearVideoPreview(elements) {
    elements.videoPreviewArea.classList.add('hidden');
    elements.videoInput.value = '';
    if (elements.videoPreview.src.startsWith('blob:')) {
        URL.revokeObjectURL(elements.videoPreview.src);
    }
    elements.videoPreview.src = '';
}

function clearAudioPreview(elements) {
    elements.audioPreviewArea.classList.add('hidden');
    elements.audioInput.value = '';
    if (elements.audioPreview.src.startsWith('blob:')) {
        URL.revokeObjectURL(elements.audioPreview.src);
    }
    elements.audioPreview.src = '';
}

async function analyzeFile(file, type, elements) {
    console.log(`🔍 Starting ${type} analysis...`);
    
    // Show analysis modal
    showAnalysisModal(type, elements);
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Analysis failed: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Analysis complete:', data);
        
        // Process and save results (include analysis_id from server)
        const analysisResult = processAnalysisResults(data.results, type, file.name, data.analysis_id);
        saveToHistory(analysisResult, type);
        
        // Show results
        showResultsModal(analysisResult, type, elements);
        
        // Update UI
        updateStatistics(elements);
        loadHistory(type, elements);
        
    } catch (error) {
        console.error('Analysis error:', error);
        showNotification('Analysis failed: ' + error.message, 'error');
        closeAllModals(elements);
    }
}

function processAnalysisResults(results, type, filename, analysis_id) {
    const timestamp = new Date().toISOString();
    const id = analysis_id || Date.now().toString();  // Use server-provided ID or generate one
    
    let processedResult = {
        id,
        filename,
        type,
        timestamp,
        results: results,
        analysis_id: id  // Store analysis_id for learning system
    };
    
    if (Array.isArray(results)) {
        // Video results - Enhanced for AI-generated content detection
        const frameResults = results.filter(frame => frame.frame !== undefined); // Filter out summary
        const videoSummary = results.find(item => item.video_summary);
        
        const fakeFrames = frameResults.filter(frame => 
            frame.face && frame.face.some(face => face.is_fake)
        ).length;
        
        const aiGeneratedFrames = frameResults.filter(frame =>
            frame.ai_generated && typeof frame.ai_generated === 'object' && frame.ai_generated.is_ai_generated
        ).length;
        
        // Calculate overall confidence from multiple sources
        let totalConfidence = 0;
        let confidenceCount = 0;
        
        frameResults.forEach(frame => {
            if (frame.face && frame.face.length > 0) {
                frame.face.forEach(face => {
                    totalConfidence += face.confidence;
                    confidenceCount++;
                });
            }
            if (frame.ai_generated && frame.ai_generated.ai_confidence) {
                totalConfidence += frame.ai_generated.ai_confidence;
                confidenceCount++;
            }
        });
        
        const avgConfidence = confidenceCount > 0 ? totalConfidence / confidenceCount : 0;
        
        // Determine if video is fake based on multiple criteria
        const deepfakeDetected = fakeFrames > frameResults.length * 0.3; // 30% threshold
        const aiGeneratedDetected = aiGeneratedFrames > frameResults.length * 0.3;
        const overallAiScore = videoSummary ? videoSummary.video_summary.overall_ai_score : 0;
        
        const overallFake = deepfakeDetected || aiGeneratedDetected || overallAiScore > 0.7;
        
        processedResult.summary = {
            totalFrames: frameResults.length,
            fakeFrames,
            aiGeneratedFrames,
            overallFake,
            confidence: Math.max(avgConfidence, overallAiScore || 0),
            deepfakeDetected,
            aiGeneratedDetected,
            overallAiScore,
            temporalConsistency: videoSummary ? videoSummary.video_summary.temporal_consistency_score : 0,
            recommendation: videoSummary ? videoSummary.video_summary.recommendation : 'UNKNOWN'
        };
    } else if (results && results.length > 0) {
        // Image results - Enhanced for AI-generated content
        const imageResults = results.filter(item => !item.image_summary); // Filter out summary
        const imageSummary = results.find(item => item.image_summary);
        
        const fakeCount = imageResults.filter(face => face.is_fake).length;
        const aiGeneratedCount = imageResults.filter(face => face.ai_generated).length;
        
        // Calculate overall confidence from multiple sources
        let totalConfidence = 0;
        let confidenceCount = 0;
        
        imageResults.forEach(item => {
            if (item.confidence !== undefined) {
                totalConfidence += item.confidence;
                confidenceCount++;
            }
            if (item.ai_confidence !== undefined) {
                totalConfidence += item.ai_confidence;
                confidenceCount++;
            }
        });
        
        const avgConfidence = confidenceCount > 0 ? totalConfidence / confidenceCount : 0;
        const overallAiScore = imageSummary ? imageSummary.image_summary.ai_generated_likelihood : 0;
        
        // Determine if image is fake based on multiple criteria
        const deepfakeDetected = fakeCount > 0;
        const aiGeneratedDetected = aiGeneratedCount > 0 || overallAiScore > 0.7;
        const overallFake = deepfakeDetected || aiGeneratedDetected;
        
        processedResult.summary = {
            totalFaces: imageResults.filter(item => item.face_id !== null && item.face_id !== undefined).length,
            fakeFaces: fakeCount,
            aiGeneratedContent: aiGeneratedCount,
            overallFake,
            confidence: Math.max(avgConfidence, overallAiScore || 0),
            deepfakeDetected,
            aiGeneratedDetected,
            overallAiScore,
            generationMethod: imageSummary ? imageSummary.image_summary.detected_generation_method : 'Unknown',
            authenticity: imageSummary ? imageSummary.image_summary.overall_authenticity : 'UNKNOWN'
        };
    } else if (results && results.audio) {
        // Audio results - Enhanced for AI-generated content
        const audioSummary = results.audio_summary || {};
        
        const deepfakeDetected = results.audio.is_fake;
        const aiGeneratedDetected = results.audio.ai_generated;
        const overallFake = deepfakeDetected || aiGeneratedDetected;
        
        processedResult.summary = {
            overallFake,
            confidence: Math.max(results.audio.confidence, results.audio.ai_confidence || 0),
            duration: results.audio.duration,
            deepfakeDetected,
            aiGeneratedDetected,
            overallAiScore: audioSummary.overall_ai_score || 0,
            generationMethod: results.audio.generation_method || 'Unknown',
            authenticity: audioSummary.authenticity_assessment || 'UNKNOWN',
            confidenceLevel: audioSummary.confidence_level || 'MEDIUM'
        };
    }
    
    return processedResult;
}

function saveToHistory(result, type) {
    LabState.analysisHistory[type].unshift(result);
    
    // Keep only last 50 results
    if (LabState.analysisHistory[type].length > 50) {
        LabState.analysisHistory[type] = LabState.analysisHistory[type].slice(0, 50);
    }
    
    // Save to localStorage
    localStorage.setItem(`${type}History`, JSON.stringify(LabState.analysisHistory[type]));
    
    // Update statistics
    LabState.totalAnalyses++;
    if (result.summary && result.summary.overallFake) {
        LabState.fakeDetected++;
    }
}

function loadAllHistory(elements) {
    loadHistory('image', elements);
    loadHistory('video', elements);
    loadHistory('audio', elements);
}

function loadHistory(type, elements) {
    const historyElement = elements[`${type}History`];
    const history = LabState.analysisHistory[type];
    
    if (history.length === 0) {
        historyElement.innerHTML = `
            <div class="empty-history">
                <div class="empty-icon">📊</div>
                <p>No analysis history yet</p>
                <small>Upload ${type === 'image' ? 'an image' : type === 'video' ? 'a video' : 'audio'} to start detecting deepfakes</small>
            </div>
        `;
        return;
    }
    
    const filter = elements[`${type}HistoryFilter`].value;
    const filteredHistory = filterHistoryData(history, filter);
    
    historyElement.innerHTML = filteredHistory.map(item => createHistoryItem(item)).join('');
    
    // Update badge
    elements[`${type}Badge`].textContent = history.length;
}

function filterHistoryData(history, filter) {
    if (filter === 'all') return history;
    if (filter === 'fake') return history.filter(item => item.summary && item.summary.overallFake);
    if (filter === 'real') return history.filter(item => item.summary && !item.summary.overallFake);
    return history;
}

function createHistoryItem(item) {
    const date = new Date(item.timestamp).toLocaleString();
    const isFake = item.summary && item.summary.overallFake;
    const confidence = item.summary && item.summary.confidence ? (item.summary.confidence * 100).toFixed(1) : '0.0';
    const userFeedback = item.userFeedback || null;
    const isCorrect = userFeedback ? (userFeedback.actualResult === isFake) : null;
    
    let feedbackIcon = '';
    let feedbackClass = '';
    
    if (userFeedback) {
        if (isCorrect) {
            feedbackIcon = '✅';
            feedbackClass = 'feedback-correct';
        } else {
            feedbackIcon = '❌';
            feedbackClass = 'feedback-incorrect';
        }
    } else {
        feedbackIcon = '❓';
        feedbackClass = 'feedback-pending';
    }
    
    return `
        <div class="history-item ${isFake ? 'fake' : 'real'} ${feedbackClass}" onclick="showHistoryDetails('${item.id}')">
            <div class="history-meta">
                <span>${item.filename}</span>
                <span>${date}</span>
            </div>
            <div class="history-result">
                ${isFake ? '🚨 FAKE DETECTED' : '✅ AUTHENTIC'}
                <span class="feedback-indicator" title="${userFeedback ? (isCorrect ? 'AI was correct' : 'AI was incorrect') : 'Feedback needed'}">${feedbackIcon}</span>
            </div>
            <div class="history-confidence">
                Confidence: ${confidence}%
                ${userFeedback && !isCorrect ? `<br><small>Actually: ${userFeedback.actualResult ? 'FAKE' : 'AUTHENTIC'}</small>` : ''}
            </div>
        </div>
    `;
}

function filterHistory(type, elements) {
    loadHistory(type, elements);
}

function clearHistory(type, elements) {
    if (confirm(`Are you sure you want to clear all ${type} analysis history?`)) {
        LabState.analysisHistory[type] = [];
        localStorage.removeItem(`${type}History`);
        loadHistory(type, elements);
        updateStatistics(elements);
        showNotification(`${type.charAt(0).toUpperCase() + type.slice(1)} history cleared`, 'success');
    }
}

function updateStatistics(elements) {
    const total = Object.values(LabState.analysisHistory).reduce((acc, history) => acc + history.length, 0);
    const fakes = Object.values(LabState.analysisHistory).reduce((acc, history) => {
        return acc + history.filter(item => item.summary && item.summary.overallFake).length;
    }, 0);
    
    // Calculate accuracy from user feedback
    const feedbackItems = Object.values(LabState.analysisHistory).flat().filter(item => item.userFeedback);
    const correctPredictions = feedbackItems.filter(item => item.userFeedback.isCorrect).length;
    const accuracy = feedbackItems.length > 0 ? ((correctPredictions / feedbackItems.length) * 100).toFixed(1) : 'N/A';
    
    elements.totalAnalyses.textContent = total;
    elements.fakeDetected.textContent = fakes;
    
    // Update badges with feedback indicators
    elements.imageBadge.textContent = LabState.analysisHistory.image.length;
    elements.videoBadge.textContent = LabState.analysisHistory.video.length;
    elements.audioBadge.textContent = LabState.analysisHistory.audio.length;
    
    // Add accuracy display if it doesn't exist
    if (!document.getElementById('accuracyStat')) {
        const accuracyDiv = document.createElement('div');
        accuracyDiv.className = 'stat-item';
        accuracyDiv.id = 'accuracyStat';
        accuracyDiv.innerHTML = `
            <div class="stat-value" id="accuracyValue">${accuracy}${accuracy !== 'N/A' ? '%' : ''}</div>
            <div class="stat-label">AI Accuracy</div>
        `;
        elements.fakeDetected.parentElement.parentElement.appendChild(accuracyDiv);
    } else {
        document.getElementById('accuracyValue').textContent = `${accuracy}${accuracy !== 'N/A' ? '%' : ''}`;
    }
}

function initializeModals(elements) {
    elements.closeModal.addEventListener('click', () => {
        closeAllModals(elements);
    });
    
    elements.closeResultsModal.addEventListener('click', () => {
        closeAllModals(elements);
    });
    
    elements.newAnalysis.addEventListener('click', () => {
        closeAllModals(elements);
        clearAllPreviews(elements);
    });
    
    // Close modals on outside click
    elements.analysisModal.addEventListener('click', (e) => {
        if (e.target === elements.analysisModal) {
            closeAllModals(elements);
        }
    });
    
    elements.resultsModal.addEventListener('click', (e) => {
        if (e.target === elements.resultsModal) {
            closeAllModals(elements);
        }
    });
}

function showAnalysisModal(type, elements) {
    elements.analysisModal.classList.remove('hidden');
    
    const steps = {
        image: [
            'Initializing neural networks...',
            'Loading face detection models...',
            'Analyzing facial features...',
            'Detecting manipulation patterns...',
            'Computing confidence scores...',
            'Finalizing results...'
        ],
        video: [
            'Initializing video processing...',
            'Extracting video frames...',
            'Loading temporal analysis models...',
            'Analyzing facial movements...',
            'Detecting blink patterns...',
            'Processing temporal data...',
            'Generating final report...'
        ],
        audio: [
            'Initializing audio processing...',
            'Loading voice analysis models...',
            'Processing audio signal...',
            'Analyzing voice patterns...',
            'Detecting synthetic markers...',
            'Computing authenticity score...',
            'Preparing results...'
        ]
    };
    
    const analysisSteps = steps[type] || steps.image;
    let currentStep = 0;
    let progress = 0;
    
    const updateProgress = () => {
        if (currentStep < analysisSteps.length) {
            elements.analysisStep.textContent = analysisSteps[currentStep];
            progress = ((currentStep + 1) / analysisSteps.length) * 100;
            elements.progressFill.style.width = progress + '%';
            elements.progressText.textContent = Math.round(progress) + '%';
            currentStep++;
            
            setTimeout(updateProgress, 800 + Math.random() * 400);
        }
    };
    
    updateProgress();
}

function showResultsModal(result, type, elements) {
    closeAllModals(elements);
    elements.resultsModal.classList.remove('hidden');
    
    elements.resultsTitle.textContent = `📊 ${type.charAt(0).toUpperCase() + type.slice(1)} Analysis Results`;
    
    const resultsHTML = createDetailedResults(result);
    elements.resultsContent.innerHTML = resultsHTML;
}

function createDetailedResults(result) {
    const isFake = result.summary && result.summary.overallFake;
    const confidence = result.summary && result.summary.confidence ? (result.summary.confidence * 100).toFixed(1) : '0.0';
    const userFeedback = result.userFeedback || null;
    const isCorrect = userFeedback ? (userFeedback.actualResult === isFake) : null;
    
    let html = `
        <div class="result-item ${isFake ? 'fake' : 'real'} ${userFeedback ? (isCorrect ? 'feedback-correct' : 'feedback-incorrect') : ''}">
            <div class="result-header">
                <div class="result-status ${isFake ? 'fake' : 'real'}">
                    ${isFake ? '🚨 DEEPFAKE DETECTED' : '✅ AUTHENTIC MEDIA'}
                </div>
                <div class="confidence-score confidence-${getConfidenceLevel(result.summary.confidence)}">
                    ${confidence}%
                </div>
            </div>
            
            ${userFeedback ? `
                <div class="feedback-status ${isCorrect ? 'correct' : 'incorrect'}">
                    ${isCorrect ? 
                        '✅ AI Prediction: CORRECT' : 
                        `❌ AI Prediction: INCORRECT - Actually ${userFeedback.actualResult ? 'FAKE' : 'AUTHENTIC'}`
                    }
                    <small>Feedback provided by user</small>
                </div>
            ` : ''}
            
            <div class="result-details">
                <p><strong>Filename:</strong> ${result.filename}</p>
                <p><strong>Analysis Time:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
    `;
    
    if (result.type === 'image' && result.summary) {
        html += `
                <p><strong>Faces Detected:</strong> ${result.summary.totalFaces}</p>
                <p><strong>Deepfake Faces:</strong> ${result.summary.fakeFaces}</p>
                <p><strong>AI-Generated Content:</strong> ${result.summary.aiGeneratedContent}</p>
                <p><strong>Overall AI Score:</strong> ${((result.summary.overallAiScore || 0) * 100).toFixed(1)}%</p>
                <p><strong>Generation Method:</strong> ${result.summary.generationMethod || 'Unknown'}</p>
                <p><strong>Assessment:</strong> <span class="assessment-${result.summary.authenticity ? result.summary.authenticity.toLowerCase() : 'unknown'}">${result.summary.authenticity || 'UNKNOWN'}</span></p>
                
                <div class="image-analysis-details">
                    <h4>🖼️ Enhanced Image Analysis</h4>
                    <div class="analysis-grid">
                        <div class="analysis-item">
                            <span class="analysis-label">Deepfake Detection:</span>
                            <span class="analysis-value ${result.summary.deepfakeDetected ? 'positive' : 'negative'}">
                                ${result.summary.deepfakeDetected ? '⚠️ DETECTED' : '✅ CLEAR'}
                            </span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">AI Generation:</span>
                            <span class="analysis-value ${result.summary.aiGeneratedDetected ? 'positive' : 'negative'}">
                                ${result.summary.aiGeneratedDetected ? '🤖 DETECTED' : '✅ CLEAR'}
                            </span>
                        </div>
                    </div>
                </div>
        `;
    } else if (result.type === 'video' && result.summary) {
        html += `
                <p><strong>Frames Analyzed:</strong> ${result.summary.totalFrames}</p>
                <p><strong>Deepfake Frames:</strong> ${result.summary.fakeFrames}</p>
                <p><strong>AI-Generated Frames:</strong> ${result.summary.aiGeneratedFrames}</p>
                <p><strong>Overall AI Score:</strong> ${((result.summary.overallAiScore || 0) * 100).toFixed(1)}%</p>
                <p><strong>Temporal Consistency:</strong> ${((result.summary.temporalConsistency || 0) * 100).toFixed(1)}%</p>
                <p><strong>Assessment:</strong> <span class="assessment-${result.summary.recommendation ? result.summary.recommendation.toLowerCase() : 'unknown'}">${result.summary.recommendation || 'UNKNOWN'}</span></p>
                
                <div class="video-analysis-details">
                    <h4>🎬 Enhanced Video Analysis</h4>
                    <div class="analysis-grid">
                        <div class="analysis-item">
                            <span class="analysis-label">Deepfake Detection:</span>
                            <span class="analysis-value ${result.summary.deepfakeDetected ? 'positive' : 'negative'}">
                                ${result.summary.deepfakeDetected ? '⚠️ DETECTED' : '✅ CLEAR'}
                            </span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">AI Generation:</span>
                            <span class="analysis-value ${result.summary.aiGeneratedDetected ? 'positive' : 'negative'}">
                                ${result.summary.aiGeneratedDetected ? '🤖 DETECTED' : '✅ CLEAR'}
                            </span>
                        </div>
                    </div>
                </div>
        `;
    } else if (result.type === 'audio' && result.summary) {
        html += `
                <p><strong>Duration:</strong> ${result.summary.duration ? result.summary.duration.toFixed(1) + 's' : 'N/A'}</p>
                <p><strong>Overall AI Score:</strong> ${((result.summary.overallAiScore || 0) * 100).toFixed(1)}%</p>
                <p><strong>Generation Method:</strong> ${result.summary.generationMethod || 'Unknown'}</p>
                <p><strong>Confidence Level:</strong> ${result.summary.confidenceLevel || 'Medium'}</p>
                <p><strong>Assessment:</strong> <span class="assessment-${result.summary.authenticity ? result.summary.authenticity.toLowerCase() : 'unknown'}">${result.summary.authenticity || 'UNKNOWN'}</span></p>
                
                <div class="audio-analysis-details">
                    <h4>🎵 Enhanced Audio Analysis</h4>
                    <div class="analysis-grid">
                        <div class="analysis-item">
                            <span class="analysis-label">Voice Cloning:</span>
                            <span class="analysis-value ${result.summary.deepfakeDetected ? 'positive' : 'negative'}">
                                ${result.summary.deepfakeDetected ? '⚠️ DETECTED' : '✅ CLEAR'}
                            </span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">AI Generation:</span>
                            <span class="analysis-value ${result.summary.aiGeneratedDetected ? 'positive' : 'negative'}">
                                ${result.summary.aiGeneratedDetected ? '🤖 DETECTED' : '✅ CLEAR'}
                            </span>
                        </div>
                    </div>
                </div>
        `;
    }
    
    html += `
            </div>
            
            ${!userFeedback ? `
                <div class="feedback-section">
                    <div class="feedback-header">
                        <h4>🎯 Help Improve AI Accuracy</h4>
                        <p>Was this analysis correct? Your feedback helps train the system.</p>
                    </div>
                    <div class="feedback-buttons">
                        <button class="feedback-btn correct" onclick="provideFeedback('${result.id}', true)">
                            ✅ AI is Correct
                        </button>
                        <button class="feedback-btn incorrect-fake" onclick="provideFeedback('${result.id}', false, true)">
                            ❌ Actually FAKE
                        </button>
                        <button class="feedback-btn incorrect-real" onclick="provideFeedback('${result.id}', false, false)">
                            ❌ Actually AUTHENTIC
                        </button>
                    </div>
                </div>
            ` : `
                <div class="feedback-section completed">
                    <div class="feedback-header">
                        <h4>📊 Feedback Recorded</h4>
                        <p>Thank you for helping improve the AI system!</p>
                    </div>
                    <div class="feedback-actions">
                        <button class="feedback-btn change" onclick="changeFeedback('${result.id}')">
                            🔄 Change Feedback
                        </button>
                    </div>
                </div>
            `}
        </div>
    `;
    
    return html;
}

function getConfidenceLevel(confidence) {
    if (confidence > 0.8) return 'high';
    if (confidence > 0.5) return 'medium';
    return 'low';
}

function closeAllModals(elements) {
    elements.analysisModal.classList.add('hidden');
    elements.resultsModal.classList.add('hidden');
}

function clearAllPreviews(elements) {
    clearImagePreview(elements);
    clearVideoPreview(elements);
    clearAudioPreview(elements);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${type === 'error' ? '⚠️' : type === 'success' ? '✅' : 'ℹ️'}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    // Add notification styles if not already added
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 1rem;
                z-index: 1001;
                animation: slideInRight 0.3s ease;
                max-width: 400px;
            }
            
            .notification-error {
                border-left: 4px solid var(--danger-color);
            }
            
            .notification-success {
                border-left: 4px solid var(--success-color);
            }
            
            .notification-info {
                border-left: 4px solid var(--accent-color);
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 10px;
                color: var(--text-primary);
            }
            
            .notification-close {
                background: none;
                border: none;
                color: var(--text-muted);
                cursor: pointer;
                padding: 0;
                margin-left: auto;
            }
            
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Global functions for feedback system
window.provideFeedback = function(itemId, isCorrect, actualResult = null) {
    const allHistory = [
        ...LabState.analysisHistory.image,
        ...LabState.analysisHistory.video,
        ...LabState.analysisHistory.audio
    ];
    
    const item = allHistory.find(h => h.id === itemId);
    if (!item) return;
    
    // Determine the actual result
    let actualFake;
    if (isCorrect) {
        actualFake = item.summary && item.summary.overallFake;
    } else {
        actualFake = actualResult;
    }
    
    // Add feedback to the item
    item.userFeedback = {
        isCorrect: isCorrect,
        actualResult: actualFake,
        timestamp: new Date().toISOString(),
        confidence: item.summary ? item.summary.confidence : 0
    };
    
    // Update the item in the appropriate history
    const type = item.type;
    const historyIndex = LabState.analysisHistory[type].findIndex(h => h.id === itemId);
    if (historyIndex !== -1) {
        LabState.analysisHistory[type][historyIndex] = item;
        localStorage.setItem(`${type}History`, JSON.stringify(LabState.analysisHistory[type]));
    }
    
    // Update UI
    const elements = getDOMElements();
    loadHistory(type, elements);
    updateStatistics(elements);
    showResultsModal(item, type, elements);
    
    // Show feedback confirmation
    showNotification(
        isCorrect ? 
            'Thank you! Feedback recorded - AI was correct.' : 
            `Feedback recorded - AI was incorrect. Actually ${actualFake ? 'FAKE' : 'AUTHENTIC'}.`,
        'success'
    );
    
    // Send feedback to server for training (optional)
    sendFeedbackToServer(item);
    
    // Update learning system if feedback was a correction
    if (!isCorrect) {
        updateLearningSystem(item);
    }
};

window.changeFeedback = function(itemId) {
    const allHistory = [
        ...LabState.analysisHistory.image,
        ...LabState.analysisHistory.video,
        ...LabState.analysisHistory.audio
    ];
    
    const item = allHistory.find(h => h.id === itemId);
    if (!item) return;
    
    // Remove existing feedback
    delete item.userFeedback;
    
    // Update the item in the appropriate history
    const type = item.type;
    const historyIndex = LabState.analysisHistory[type].findIndex(h => h.id === itemId);
    if (historyIndex !== -1) {
        LabState.analysisHistory[type][historyIndex] = item;
        localStorage.setItem(`${type}History`, JSON.stringify(LabState.analysisHistory[type]));
    }
    
    // Update UI
    const elements = getDOMElements();
    loadHistory(type, elements);
    updateStatistics(elements);
    showResultsModal(item, type, elements);
    
    showNotification('Feedback cleared. You can now provide new feedback.', 'info');
};

// Global function for history item clicks
window.showHistoryDetails = function(itemId) {
    const allHistory = [
        ...LabState.analysisHistory.image,
        ...LabState.analysisHistory.video,
        ...LabState.analysisHistory.audio
    ];
    
    const item = allHistory.find(h => h.id === itemId);
    if (item) {
        const elements = getDOMElements();
        showResultsModal(item, item.type, elements);
    }
};

// Send feedback to server for model improvement
async function sendFeedbackToServer(item) {
    try {
        const feedbackData = {
            analysisId: item.id,
            filename: item.filename,
            type: item.type,
            aiPrediction: item.summary && item.summary.overallFake,
            aiConfidence: item.summary ? item.summary.confidence : 0,
            userFeedback: item.userFeedback,
            timestamp: item.timestamp
        };
        
        const response = await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(feedbackData)
        });
        
        if (response.ok) {
            console.log('Feedback sent to server successfully');
        } else {
            console.warn('Failed to send feedback to server');
        }
    } catch (error) {
        console.warn('Error sending feedback to server:', error);
    }
}

// Update learning system with user corrections
async function updateLearningSystem(item) {
    try {
        const learningData = {
            analysisId: item.id,
            filename: item.filename,
            type: item.type,
            userFeedback: item.userFeedback,
            timestamp: item.timestamp
        };
        
        console.log('🔄 Sending learning update:', learningData);
        
        const response = await fetch('/update_learning', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(learningData)
        });
        
        const result = await response.json();
        console.log('🧠 Learning response:', result);
        
        if (response.ok) {
            console.log('✅ Learning system updated successfully');
            showNotification(
                `🧠 FalsifyX learned from your feedback! This file is now marked as ${item.userFeedback.actualResult ? 'FAKE' : 'AUTHENTIC'}. Future uploads will be more accurate.`, 
                'success'
            );
        } else {
            console.warn('❌ Failed to update learning system:', result);
            showNotification('Failed to update learning system: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('❌ Error updating learning system:', error);
        showNotification('Error updating learning system: ' + error.message, 'error');
    }
}