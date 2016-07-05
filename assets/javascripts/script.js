function toggleSleepers() {
    var sleeperDiv = document.getElementById('sleeper');
    var toggleLink = document.getElementById('toggle-link');
    
    if (sleeperDiv.style.display == 'block') {
        sleeperDiv.style.display = 'none';
        toggleLink.innerHTML = 'Show'
    } else {
        sleeperDiv.style.display = 'block';
        toggleLink.innerHTML = 'Hide'
    }
}
