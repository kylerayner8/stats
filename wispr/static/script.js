function recolor() {
    this.style.color = 'red';
}

function reset() {
    this.style.color = 'black';
}

function set_listeners() {
        document.getElementById('pname').addEventListener('mouseover', recolor);
        document.getElementById('pname').addEventListener('mouseout', reset);
    }

window.onload = set_listeners;
