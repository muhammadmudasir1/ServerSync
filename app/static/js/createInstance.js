async function handleSaveInstance(ev) {
    const intanceName=document.getElementById('instanceName').value
    const logFile=document.getElementById('logFile').value
    const containerized=document.getElementById('containerized').value

    const response = await fetch('/createServerInstance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({instanceName: intanceName,logFile:logFile,containerized:containerized}),
    })
    const popup=document.getElementById('popup')
    const innerDiv=popup.querySelector('div')
    console.log(response)
    if (response.status==200){
        window.location.href = response.url;
    }
    else{
        // data=await response.json()
        // console.log(data)
        popup.style.display='block'
        innerDiv.style.backgroundColor='rgba(255, 0, 0, 0.5)'; 
        innerDiv.style.color='red'; 
        innerDiv.innerHTML='Instance Creation Failed'
        setTimeout(() => {
            popup.style.display='none'
            innerDiv.innerHTML=''
        }, 3000)
    }
}

function handleSetProject(event){
    const Value=event.target.innerHTML
    const projectField=document.getElementById('projectName')
    projectField.value=Value

}