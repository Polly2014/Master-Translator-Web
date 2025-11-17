// Master Translator Web - 前端交互逻辑
// Version tag for cache busting / debug
const MTW_BUILD_VERSION = '2025-01-17-1';
console.log('[MTW] Loading app.js version', MTW_BUILD_VERSION);

let socket = null;
let currentTaskId = null;
let currentLanguage = 'Japanese';

// ============ 初始化 ============
document.addEventListener('DOMContentLoaded', () => {
    initializeSocketIO();
    initializeFileUpload();
    initializeButtons();
    initializeTerminologyModal();
    initializePreviewModal();
});

// ============ WebSocket 连接 ============
function initializeSocketIO() {
    socket = io('http://localhost:5001', {
        transports: ['websocket', 'polling']
    });
    
    socket.on('connect', () => {
        console.log('✅ WebSocket 已连接');
        updateLogStatus('Connected', 'green');
    });
    
    socket.on('disconnect', () => {
        console.log('❌ WebSocket 已断开');
        updateLogStatus('Disconnected', 'red');
    });
    
    socket.on('log', (data) => {
        appendLog(data.message, data.level, data.timestamp, data.update_last || false);
    });
    
    socket.on('progress', (data) => {
        updateProgress(data.overall, data.chunk, data.current_chunk, data.total_chunks);
    });
}

function updateLogStatus(status, color) {
    const statusEl = document.getElementById('logStatus');
    statusEl.textContent = status;
    statusEl.className = `ml-auto text-sm px-3 py-1 rounded-full bg-${color}-500/20 border border-${color}-500`;
}

// ============ 文件上传 ============
function initializeFileUpload() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    
    // 点击上传
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });
    
    // 文件选择
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
    
    // 拖拽上传
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-blue-500', 'bg-blue-500/10');
    });
    
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-blue-500', 'bg-blue-500/10');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-blue-500', 'bg-blue-500/10');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
}

async function handleFileUpload(file) {
    if (!file.name.endsWith('.md')) {
        alert('Only Markdown (.md) files are supported!');
        return;
    }
    
    appendLog('📤 Uploading file...', 'info');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('上传失败');
        }
        
        const data = await response.json();
        currentTaskId = data.task_id;
        
        // 显示文件信息
        document.getElementById('fileInfo').classList.remove('hidden');
        document.getElementById('fileName').textContent = data.filename;
        document.getElementById('fileSize').textContent = formatBytes(data.size);
        document.getElementById('fileChars').textContent = formatNumber(data.chars);
        
        // 更新统计信息
        document.getElementById('sourceChars').textContent = formatNumber(data.chars);
        
        // 启用分析按钮
        document.getElementById('analyzeBtn').disabled = false;
        
        appendLog(`✅ File uploaded successfully: ${data.filename}`, 'success');
        appendLog(`📊 Size: ${formatBytes(data.size)} | Characters: ${formatNumber(data.chars)}`, 'info');
        
        // 加入 WebSocket 房间
        socket.emit('join', { task_id: currentTaskId });
        
    } catch (error) {
        appendLog(`❌ Upload failed: ${error.message}`, 'error');
    }
}

// ============ 按钮事件 ============
function initializeButtons() {
    // 分析分块
    document.getElementById('analyzeBtn').addEventListener('click', async () => {
        if (!currentTaskId) return;
        
        const analyzeBtn = document.getElementById('analyzeBtn');
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = '🔍 Analyzing...';
        
        currentLanguage = document.getElementById('targetLanguage').value;
        
        appendLog('🔍 Analyzing chapter structure...', 'info');
        
        try {
            const response = await fetch(`/api/analyze/${currentTaskId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    language: currentLanguage
                })
            });
            
            if (!response.ok) {
                throw new Error('分析失败');
            }
            
            const data = await response.json();
            
            appendLog(`✅ Analysis complete!`, 'success');
            appendLog(`✂️  Split into ${data.total_chunks} chunks`, 'info');
            
            // 更新统计信息
            document.getElementById('chunksCount').textContent = data.total_chunks;
            document.getElementById('totalChunks').textContent = data.total_chunks;
            document.getElementById('targetLang').textContent = getLanguageDisplay(currentLanguage);
            
            // 显示分块信息
            displayChunks(data.chunks);
            
            // 启用翻译按钮
            document.getElementById('translateBtn').disabled = false;
            analyzeBtn.textContent = '✅ Analysis Complete';
            
            updateTaskStatus('Analyzed');
            
        } catch (error) {
            appendLog(`❌ Analysis failed: ${error.message}`, 'error');
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = '🔍 Analyze Chunks';
        }
    });
    
    // 开始翻译
    document.getElementById('translateBtn').addEventListener('click', async () => {
        if (!currentTaskId) return;
        
        const translateBtn = document.getElementById('translateBtn');
        translateBtn.disabled = true;
        translateBtn.textContent = '🚀 Translating...';
        
        const useTerminology = document.getElementById('useTerminology').checked;
        
        appendLog('🚀 Starting translation task...', 'info');
        if (useTerminology) {
            appendLog('📚 Using terminology database for consistency', 'info');
        } else {
            appendLog('ℹ️  Terminology database disabled', 'info');
        }
        updateTaskStatus('Translating');
        updateLogStatus('Translating', 'yellow');
        
        try {
            const response = await fetch(`/api/translate/${currentTaskId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    use_terminology: useTerminology
                })
            });
            
            if (!response.ok) {
                throw new Error('启动翻译失败');
            }
            
            appendLog('✅ Translation task started', 'success');
            
        } catch (error) {
            appendLog(`❌ Failed to start: ${error.message}`, 'error');
            translateBtn.disabled = false;
            translateBtn.textContent = '🚀 Start Translation';
            updateTaskStatus('Failed');
        }
    });
    
    // 下载结果
    document.getElementById('downloadBtn').addEventListener('click', () => {
        if (!currentTaskId) return;
        
        window.location.href = `/api/download/${currentTaskId}`;
        appendLog('📥 Starting download...', 'info');
    });
    
    // 预览上传文件
    document.getElementById('previewSourceBtn').addEventListener('click', async () => {
        if (!currentTaskId) return;
        await previewSource();
    });
    
    // 预览翻译结果
    document.getElementById('previewBtn').addEventListener('click', async () => {
        if (!currentTaskId) return;
        
        showPreviewModal();
        await loadPreviewContent(currentTaskId, 'translation');
    });
}

// ============ 分块展示 ============
function displayChunks(chunks) {
    const chunksPanel = document.getElementById('chunksPanel');
    const chunksList = document.getElementById('chunksList');
    
    chunksPanel.classList.remove('hidden');
    chunksList.innerHTML = '';
    
    chunks.forEach(chunk => {
        const chunkEl = document.createElement('div');
        chunkEl.className = 'bg-slate-700/50 rounded-lg p-3 border border-slate-600 cursor-pointer hover:border-blue-500 hover:bg-slate-700 transition-all';
        chunkEl.dataset.chunkId = chunk.id;
        
        let badges = '';
        if (chunk.has_prologue) {
            badges += '<span class="text-xs px-2 py-0.5 bg-blue-500/20 rounded border border-blue-500/50 mr-1">Prologue</span>';
        }
        if (chunk.has_epilogue) {
            badges += '<span class="text-xs px-2 py-0.5 bg-purple-500/20 rounded border border-purple-500/50">Epilogue</span>';
        }
        
        const chaptersText = chunk.chapters.slice(0, 2).join(', ') + (chunk.chapters.length > 2 ? '...' : '');
        
        chunkEl.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <span class="font-bold text-blue-400">Chunk ${chunk.id}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs text-gray-400">${formatNumber(chunk.size)} chars</span>
                    <span class="text-xs text-gray-500">👁️ Click to preview</span>
                </div>
            </div>
            <div class="text-xs text-gray-400 mb-1">${chaptersText}</div>
            ${badges ? `<div class="mt-2">${badges}</div>` : ''}
        `;
        
        // 添加点击事件
        chunkEl.addEventListener('click', () => {
            previewChunk(chunk.id);
        });
        
        chunksList.appendChild(chunkEl);
    });
}

// ============ 日志系统 ============
function appendLog(message, level = 'info', timestamp = null, updateLast = false) {
    const logContainer = document.getElementById('logContainer');
    
    // 清除初始提示
    if (logContainer.querySelector('.text-gray-500.text-center')) {
        logContainer.innerHTML = '';
    }
    
    // 如果是更新模式，并且消息类型相同，更新最后一条
    if (updateLast && logContainer.children.length > 0) {
        const lastEntry = logContainer.lastElementChild;
        // 检查是否是进度消息（包含"已接收"或"📥"）
        if (lastEntry.textContent.includes('📥') || lastEntry.textContent.includes('已接收')) {
            const time = timestamp || new Date().toLocaleTimeString('zh-CN', { hour12: false });
            let color = 'text-gray-400';
            let icon = '📥';
            
            lastEntry.innerHTML = `
                <span class="text-gray-500 text-xs">[${time}]</span>
                <span>${icon}</span>
                <span class="${color} flex-1">${escapeHtml(message)}</span>
            `;
            return;
        }
    }
    
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry flex gap-2 mb-2';
    
    const time = timestamp || new Date().toLocaleTimeString('zh-CN', { hour12: false });
    
    let color = 'text-gray-400';
    let icon = 'ℹ️';
    
    switch(level) {
        case 'success':
            color = 'text-green-400';
            icon = '✅';
            break;
        case 'error':
            color = 'text-red-400';
            icon = '❌';
            break;
        case 'warning':
            color = 'text-yellow-400';
            icon = '⚠️';
            break;
        case 'progress':
            color = 'text-gray-400';
            icon = '📥';
            break;
        case 'info':
        default:
            color = 'text-blue-400';
            icon = 'ℹ️';
    }
    
    logEntry.innerHTML = `
        <span class="text-gray-500 text-xs">[${time}]</span>
        <span>${icon}</span>
        <span class="${color} flex-1">${escapeHtml(message)}</span>
    `;
    
    logContainer.appendChild(logEntry);
    
    // 自动滚动到底部
    logContainer.scrollTop = logContainer.scrollHeight;
    
    // 检查是否完成（支持中英文）
    if (message.includes('翻译完成') || message.includes('Translation completed')) {
        updateTaskStatus('Completed');
        updateLogStatus('Completed', 'green');
        showDownloadPanel();
    }
}

// ============ 进度更新 ============
function updateProgress(overall, chunk, currentChunk, totalChunks) {
    // 整体进度
    document.getElementById('overallProgress').style.width = `${overall}%`;
    document.getElementById('overallPercent').textContent = `${overall}%`;
    
    // 当前块进度
    document.getElementById('chunkProgress').style.width = `${chunk}%`;
    document.getElementById('chunkPercent').textContent = `${chunk}%`;
    
    // 块计数器
    document.getElementById('currentChunk').textContent = currentChunk;
    document.getElementById('totalChunks').textContent = totalChunks;
    
    // 高亮当前块
    const chunksList = document.getElementById('chunksList');
    const chunks = chunksList.children;
    for (let i = 0; i < chunks.length; i++) {
        if (i + 1 === currentChunk) {
            chunks[i].classList.add('border-green-500', 'bg-green-500/10');
            chunks[i].classList.remove('border-slate-600');
        } else if (i + 1 < currentChunk) {
            chunks[i].classList.add('border-blue-500/50', 'bg-blue-500/5');
            chunks[i].classList.remove('border-slate-600');
        }
    }
}

// ============ 辅助函数 ============
function updateTaskStatus(status) {
    const statusEl = document.getElementById('taskStatus');
    statusEl.textContent = status;
    
    const colorMap = {
        'Not Started': 'text-gray-400',
        'Analyzed': 'text-blue-400',
        'Translating': 'text-yellow-400',
        'Completed': 'text-green-400',
        'Failed': 'text-red-400'
    };
    
    statusEl.className = `font-bold ${colorMap[status] || 'text-gray-400'}`;
}

function showDownloadPanel() {
    document.getElementById('downloadPanel').classList.remove('hidden');
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatNumber(num) {
    return num.toLocaleString('zh-CN');
}

function getLanguageDisplay(code) {
    const langMap = {
        'Japanese': '🇯🇵 Japanese',
        'Russian': '🇷🇺 Russian',
        'Arabic': '🇸🇦 Arabic',
        'Hindi': '🇮🇳 Hindi',
        'French': '🇫🇷 French',
        'Spanish': '🇪🇸 Spanish',
        'German': '🇩🇪 German'
    };
    return langMap[code] || code;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============ 术语数据库模态框 ============
function initializeTerminologyModal() {
    const modal = document.getElementById('terminologyModal');
    const viewBtn = document.getElementById('viewTermsBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    
    // 打开模态框
    viewBtn.addEventListener('click', async () => {
        modal.classList.remove('hidden');
        await loadTerminology();
    });
    
    // 关闭模态框
    closeBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });
    
    // 点击背景关闭
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
}

async function loadTerminology() {
    const content = document.getElementById('terminologyContent');
    
    try {
        const response = await fetch('/api/terminology');
        
        if (!response.ok) {
            throw new Error('Failed to load terminology');
        }
        
        const data = await response.json();
        
        // 显示混合模式说明
        let html = `
            <div class="bg-gradient-to-r from-indigo-500/20 to-cyan-500/20 rounded-lg p-4 border border-indigo-500/30 mb-6">
                <div class="flex items-center gap-2 mb-2">
                    <span class="text-2xl">🔄</span>
                    <span class="text-lg font-bold">Hybrid Mode</span>
                </div>
                <p class="text-sm text-gray-300 leading-relaxed">
                    <strong class="text-blue-400">${data.stats.total} curated terms</strong> loaded initially. 
                    After translating the <strong class="text-green-400">first chunk</strong>, 
                    the system will automatically extract and add new terms found in that chunk, 
                    ensuring comprehensive coverage without manual updates.
                </p>
            </div>
        `;
        
        // 显示统计信息
        html += `
            <div class="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-lg p-4 border border-blue-500/30 mb-6">
                <div class="flex items-center gap-2 mb-2">
                    <span class="text-2xl">📊</span>
                    <span class="text-lg font-bold">Curated Database Statistics</span>
                </div>
                <div class="grid grid-cols-2 gap-4 mt-3">
                    <div class="text-center">
                        <div class="text-3xl font-bold text-blue-400">${data.stats.total}</div>
                        <div class="text-sm text-gray-400">Base Terms</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-purple-400">${Object.keys(data.stats.categories).length}</div>
                        <div class="text-sm text-gray-400">Categories</div>
                    </div>
                </div>
                <div class="text-xs text-center text-gray-500 mt-2">
                    + Dynamic terms will be added from first chunk
                </div>
            </div>
        `;
        
        // 显示各类别术语
        const categoryNames = {
            'proper_nouns': { name: 'Proper Nouns', icon: '👤', color: 'blue', description: 'Names of people, companies, places (kept in English)' },
            'technical_terms': { name: 'Technical Terms', icon: '🔧', color: 'green', description: 'AI, ML, and technology-specific terminology' },
            'key_concepts': { name: 'Key Concepts', icon: '💡', color: 'purple', description: 'Important domain-specific concepts' }
        };
        
        for (const [category, info] of Object.entries(categoryNames)) {
            if (data.terminology[category] && data.terminology[category].length > 0) {
                const terms = data.terminology[category];
                html += `
                    <div class="bg-slate-700/50 rounded-lg p-4 border border-slate-600">
                        <div class="flex items-center justify-between mb-3">
                            <div class="flex items-center gap-2">
                                <span class="text-2xl">${info.icon}</span>
                                <div>
                                    <div class="font-bold text-lg">${info.name}</div>
                                    <div class="text-xs text-gray-400">${info.description}</div>
                                </div>
                            </div>
                            <span class="px-3 py-1 bg-${info.color}-500/20 text-${info.color}-400 rounded-full text-sm font-bold">
                                ${terms.length} terms
                            </span>
                        </div>
                        <div class="flex flex-wrap gap-2 mt-3">
                            ${terms.slice(0, 50).map(term => `
                                <span class="px-3 py-1 bg-slate-600 rounded-full text-sm text-gray-300 border border-slate-500">
                                    ${escapeHtml(term)}
                                </span>
                            `).join('')}
                            ${terms.length > 50 ? `
                                <span class="px-3 py-1 text-sm text-gray-500 italic">
                                    ... and ${terms.length - 50} more
                                </span>
                            ` : ''}
                        </div>
                    </div>
                `;
            }
        }
        
        content.innerHTML = html;
        
    } catch (error) {
        content.innerHTML = `
            <div class="text-center text-red-400 py-8">
                <div class="text-4xl mb-2">❌</div>
                <p class="font-bold mb-2">Failed to load terminology</p>
                <p class="text-sm text-gray-500">${escapeHtml(error.message)}</p>
                <p class="text-xs text-gray-600 mt-2">Will use dynamic extraction mode if terminology is enabled</p>
            </div>
        `;
    }
}

// ============ 预览功能 ============
function showPreviewModal() {
    const modal = document.getElementById('previewModal');
    modal.classList.remove('hidden');
}

function hidePreviewModal() {
    const modal = document.getElementById('previewModal');
    modal.classList.add('hidden');
}

async function loadPreviewContent(taskId, previewType = 'translation') {
    const rawContent = document.getElementById('previewRawContent');
    const renderedContent = document.getElementById('previewRenderedContent');
    const statsEl = document.getElementById('previewStats');
    const titleEl = document.getElementById('previewTitle');
    const iconEl = document.getElementById('previewIcon');
    
    // 设置标题和图标
    const titles = {
        'translation': { title: 'Translation Preview', icon: '✅' },
        'source': { title: 'Uploaded File Preview', icon: '📄' },
        'chunk': { title: 'Chunk Preview', icon: '✂️' }
    };
    
    const titleInfo = titles[previewType] || titles['translation'];
    titleEl.textContent = titleInfo.title;
    iconEl.textContent = titleInfo.icon;
    
    // 显示加载状态
    renderedContent.innerHTML = `
        <div class="text-center text-gray-400 py-8">
            <div class="text-4xl mb-2">🔄</div>
            <p>Loading preview...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`/api/preview/${taskId}`);
        
        if (!response.ok) {
            throw new Error('Failed to load preview');
        }
        
        const data = await response.json();
        
        // 设置原始内容
        const rawPre = rawContent.querySelector('pre');
        rawPre.textContent = data.content;
        
        // 渲染 Markdown
        const renderedHtml = marked.parse(data.content);
        renderedContent.innerHTML = `<div class="markdown-content">${renderedHtml}</div>`;
        
        // 更新统计信息
        const wordCount = data.content.split(/\s+/).length;
        const charCount = data.content.length;
        statsEl.textContent = `📊 ${wordCount.toLocaleString()} words • ${charCount.toLocaleString()} characters`;
        
        // 设置下载按钮 (只对翻译结果显示)
        const downloadBtn = document.getElementById('downloadFromPreview');
        if (previewType === 'translation') {
            downloadBtn.classList.remove('hidden');
            downloadBtn.onclick = () => {
                window.location.href = `/api/download/${taskId}`;
            };
        } else {
            downloadBtn.classList.add('hidden');
        }
        
    } catch (error) {
        renderedContent.innerHTML = `
            <div class="text-center text-red-400 py-8">
                <div class="text-4xl mb-2">❌</div>
                <p class="font-bold mb-2">Failed to load preview</p>
                <p class="text-sm text-gray-500">${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}

// 预览上传的源文件
async function previewSource() {
    if (!currentTaskId) return;
    
    const titleEl = document.getElementById('previewTitle');
    const iconEl = document.getElementById('previewIcon');
    const rawContent = document.getElementById('previewRawContent');
    const renderedContent = document.getElementById('previewRenderedContent');
    const statsEl = document.getElementById('previewStats');
    
    titleEl.textContent = 'Uploaded File Preview';
    iconEl.textContent = '📄';
    
    showPreviewModal();
    
    // 显示加载状态
    renderedContent.innerHTML = `
        <div class="text-center text-gray-400 py-8">
            <div class="text-4xl mb-2">🔄</div>
            <p>Loading uploaded file...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`/api/preview-source/${currentTaskId}`);
        
        if (!response.ok) {
            throw new Error('Failed to load source file');
        }
        
        const data = await response.json();
        
        // 设置原始内容
        const rawPre = rawContent.querySelector('pre');
        rawPre.textContent = data.content;
        
        // 渲染 Markdown
        const renderedHtml = marked.parse(data.content);
        renderedContent.innerHTML = `<div class="markdown-content">${renderedHtml}</div>`;
        
        // 更新统计信息
        const wordCount = data.content.split(/\s+/).length;
        const charCount = data.content.length;
        statsEl.textContent = `📊 ${wordCount.toLocaleString()} words • ${charCount.toLocaleString()} characters`;
        
        // 隐藏下载按钮
        document.getElementById('downloadFromPreview').classList.add('hidden');
        
    } catch (error) {
        renderedContent.innerHTML = `
            <div class="text-center text-red-400 py-8">
                <div class="text-4xl mb-2">❌</div>
                <p class="font-bold mb-2">Failed to load source file</p>
                <p class="text-sm text-gray-500">${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}

// 预览特定 chunk
async function previewChunk(chunkId) {
    if (!currentTaskId) return;
    
    const titleEl = document.getElementById('previewTitle');
    const iconEl = document.getElementById('previewIcon');
    const rawContent = document.getElementById('previewRawContent');
    const renderedContent = document.getElementById('previewRenderedContent');
    const statsEl = document.getElementById('previewStats');
    
    titleEl.textContent = `Chunk ${chunkId} Preview`;
    iconEl.textContent = '✂️';
    
    showPreviewModal();
    
    // 显示加载状态
    renderedContent.innerHTML = `
        <div class="text-center text-gray-400 py-8">
            <div class="text-4xl mb-2">🔄</div>
            <p>Loading chunk ${chunkId}...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`/api/preview-chunk/${currentTaskId}/${chunkId}`);
        
        if (!response.ok) {
            throw new Error(`Failed to load chunk ${chunkId}`);
        }
        
        const data = await response.json();
        
        // 设置原始内容
        const rawPre = rawContent.querySelector('pre');
        rawPre.textContent = data.content;
        
        // 渲染 Markdown
        const renderedHtml = marked.parse(data.content);
        renderedContent.innerHTML = `<div class="markdown-content">${renderedHtml}</div>`;
        
        // 更新统计信息
        const wordCount = data.content.split(/\s+/).length;
        const charCount = data.content.length;
        const chunkInfo = data.chapters ? ` • ${data.chapters.join(', ')}` : '';
        statsEl.textContent = `📊 ${wordCount.toLocaleString()} words • ${charCount.toLocaleString()} characters${chunkInfo}`;
        
        // 隐藏下载按钮
        document.getElementById('downloadFromPreview').classList.add('hidden');
        
    } catch (error) {
        renderedContent.innerHTML = `
            <div class="text-center text-red-400 py-8">
                <div class="text-4xl mb-2">❌</div>
                <p class="font-bold mb-2">Failed to load chunk ${chunkId}</p>
                <p class="text-sm text-gray-500">${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}

function initializePreviewModal() {
    const modal = document.getElementById('previewModal');
    const closeBtn = document.getElementById('closePreviewBtn');
    const rawBtn = document.getElementById('previewRawBtn');
    const renderedBtn = document.getElementById('previewRenderedBtn');
    const rawContent = document.getElementById('previewRawContent');
    const renderedContent = document.getElementById('previewRenderedContent');
    
    // 关闭按钮
    closeBtn.addEventListener('click', hidePreviewModal);
    
    // 点击背景关闭
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            hidePreviewModal();
        }
    });
    
    // ESC 键关闭
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            hidePreviewModal();
        }
    });
    
    // 切换视图
    rawBtn.addEventListener('click', () => {
        rawContent.classList.remove('hidden');
        renderedContent.classList.add('hidden');
        rawBtn.classList.remove('bg-slate-600');
        rawBtn.classList.add('bg-blue-600');
        renderedBtn.classList.remove('bg-blue-600');
        renderedBtn.classList.add('bg-slate-600');
    });
    
    renderedBtn.addEventListener('click', () => {
        rawContent.classList.add('hidden');
        renderedContent.classList.remove('hidden');
        rawBtn.classList.remove('bg-blue-600');
        rawBtn.classList.add('bg-slate-600');
        renderedBtn.classList.remove('bg-slate-600');
        renderedBtn.classList.add('bg-blue-600');
    });
}

