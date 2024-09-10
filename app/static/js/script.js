var currentUrl = window.location.href;
var parts = currentUrl.split('/');
var instanceId = parts[parts.length - 1];

async function handleReBuild(event) {
    const response=await fetch('/rebuild/'+instanceId,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    // alert(response.json)
}

