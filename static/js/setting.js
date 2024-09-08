function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function handleSaveScript(event){
    const targetButton=event.target
    targetButton.disabled=true
    targetButton.innerHTML='<i class="fa-solid fa-spinner animate-spin"></i>'
    const script = document.getElementById('script').value;
    const response = await fetch('/save_script',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({script: script}),
    })
    const popup=document.getElementById('popup')
    const innerDiv=popup.querySelector('div')
    targetButton.disabled=false
    targetButton.innerHTML='Save Build Script'
    if (response.status==200){
        popup.style.display='block'
        innerDiv.style.backgroundColor='rgba(0, 128, 0, 0.5)'; 
        innerDiv.style.color='green'; 
        innerDiv.innerHTML='Build Script Saved'
        setTimeout(() => {
            popup.style.display='none'
            innerDiv.innerHTML=''
        }, 3000)
    }
    else{
        popup.style.display='block'
        innerDiv.style.backgroundColor='rgba(255, 0, 0, 0.5)'; 
        innerDiv.style.color='red'; 
        innerDiv.innerHTML='Failed to Save Build Script'
        setTimeout(() => {
            popup.style.display='none'
            innerDiv.innerHTML=''
        }, 3000)
    }
}

async function handleSaveLog(event){
    const targetButton=event.target
    targetButton.disabled=true
    targetButton.innerHTML='<i class="fa-solid fa-spinner animate-spin"></i>'

    const logpath = document.getElementById('logpath').value;
    const response = await fetch('/save_logpath',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({logpath: logpath}),
    })
    const popup=document.getElementById('popup')
    const innerDiv=popup.querySelector('div')
    targetButton.disabled=false
    targetButton.innerHTML='Save Log Path'
    if (response.status==200){
        popup.style.display='block'
        innerDiv.style.backgroundColor='rgba(0, 128, 0, 0.5)'; 
        innerDiv.style.color='green'; 
        innerDiv.innerHTML='Log Path Saved'
        setTimeout(() => {
            popup.style.display='none'
            innerDiv.innerHTML=''
        }, 3000)
    }
    else{
        popup.style.display='block'
        innerDiv.style.backgroundColor='rgba(255, 0, 0, 0.5)'; 
        innerDiv.style.color='red'; 
        innerDiv.innerHTML='Failed to Save Log Path'
        setTimeout(() => {
            popup.style.display='none'
            innerDiv.innerHTML=''
        }, 3000)
    }
}