const eventSource = new EventSource('/logs');

eventSource.onmessage = function(event) {
    const logContainer = document.getElementById('log-container');
    const logLine = document.createElement('div');
    logLine.textContent = event.data;
    if (event.data.includes("ERROR")) {
        logLine.style.color = "red";
    }
    if (event.data.includes("WARNING")) {
        logLine.style.color = "orange";
    }
    logContainer.appendChild(logLine);
    
    const autoScroll = document.getElementById('autoscroll');
    if (autoScroll.checked) {
        logContainer.scrollTop = logContainer.scrollHeight;
        
    }
};

eventSource.onerror = function() {
    console.error("Error receiving logs");
};

const buildStatus = new EventSource('/build_status');

buildStatus.onmessage = function(event) {
    if (event.data=="running"){
        const rebuild = document.getElementById('rebuild');
        rebuild.disabled=true
        rebuild.innerHTML='Rebuilding <i class="fa-solid fa-spinner animate-spin" style="margin-left:5px"></i>'
        
    }
    else{
        rebuild.disabled=false
        rebuild.innerHTML='Rebuid'

    }

};

buildStatus.onerror = function() {
    console.error("Error build error");
};