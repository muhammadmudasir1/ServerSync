async function handleReBuild(event) {
    const response=await fetch('/rebuild',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    // alert(response.json)
}

