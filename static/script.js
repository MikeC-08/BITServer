document.getElementById('searchInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        query();
    }
});

document.getElementById('searchButton').addEventListener('click', function() {
    query();
});

function query(){
    method = "byName"
    value = document.getElementById('searchInput').value;
    window.location.href = '?query=' + value + "&method=" + method;
}


const resultButtons = document.getElementsByClassName('resultButton');

for (let button of resultButtons) {
    button.addEventListener('click', function() {
        window.location.href = '/detail?address='+button.id;
    });
}