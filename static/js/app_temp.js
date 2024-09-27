const eventSource = new EventSource('/stream_temp');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    $('#temp').text(data.text);
};
