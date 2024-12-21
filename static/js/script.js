fetch('/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        Username: 'myUsername',
        Password: 'myPassword'
    })
})
