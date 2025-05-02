document.getElementById("explore-btn").addEventListener("click", function() {
    alert("Welcome to the world of calisthenics!");
});

// Dark Mode Toggle
document.getElementById("dark-mode-toggle").addEventListener("click", function() {
    document.body.classList.toggle("dark-mode");
});

// Workout Timer
let timer;
let seconds = 0;

function startTimer() {
    if (!timer) {
        timer = setInterval(() => {
            seconds++;
            document.getElementById("time-display").innerText = new Date(seconds * 1000).toISOString().substr(14, 5);
        }, 1000);
    }
}

function resetTimer() {
    clearInterval(timer);
    timer = null;
    seconds = 0;
    document.getElementById("time-display").innerText = "00:00";
}