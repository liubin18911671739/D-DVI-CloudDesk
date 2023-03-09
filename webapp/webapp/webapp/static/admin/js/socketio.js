
socket = io.connect(`//${location.host}/administrators`, {
    'query': {'jwt': localStorage.getItem("token")},
    'path': '/api/v3/socket.io/',
    'transports': ['websocket']
})

socket.on('connect', function () {
    connection_done()
})

socket.on('connect_error', function (data) {
    connection_lost()
})

socket.on('user_quota', function (data) {
    drawUserQuota(JSON.parse(data))
})
