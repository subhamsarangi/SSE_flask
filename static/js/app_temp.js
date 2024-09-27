const eventSource = new EventSource('/stream_temp');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    $('#text').text(data.text);
};
