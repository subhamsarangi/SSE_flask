const eventSource = new EventSource('/stream');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    $('#name').text(data.name);
    $('#timestamp').text(data.timestamp);
    $('#image').attr('src', data.image);
};