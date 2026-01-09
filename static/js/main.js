// Main JavaScript for Lottery System Web App

// Utility function for API calls
async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Simple alert for now, can be enhanced with a toast library
    if (type === 'error') {
        alert('错误: ' + message);
    } else if (type === 'success') {
        alert('成功: ' + message);
    } else {
        alert(message);
    }
}

// Format numbers for display
function formatNumbers(numbers) {
    if (Array.isArray(numbers)) {
        return numbers.join(', ');
    }
    return numbers;
}

// Highlight current page in navigation
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.backgroundColor = 'rgba(255,255,255,0.3)';
        }
    });
});

// Add loading state to buttons
function setButtonLoading(button, loading) {
    if (loading) {
        button.dataset.originalText = button.textContent;
        button.textContent = '处理中...';
        button.disabled = true;
    } else {
        button.textContent = button.dataset.originalText || button.textContent;
        button.disabled = false;
    }
}

// Format date/time
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Copy text to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('已复制到剪贴板', 'success');
        }).catch(err => {
            console.error('Copy failed:', err);
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
}

// Fallback copy method for older browsers
function fallbackCopy(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
        document.execCommand('copy');
        showNotification('已复制到剪贴板', 'success');
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showNotification('复制失败', 'error');
    }
    
    document.body.removeChild(textArea);
}

// Check if mobile device
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Adjust UI for mobile
if (isMobile()) {
    document.body.classList.add('mobile-device');
}

// Console log for debugging
console.log('Lottery System Web App initialized');
console.log('Device type:', isMobile() ? 'Mobile' : 'Desktop');
