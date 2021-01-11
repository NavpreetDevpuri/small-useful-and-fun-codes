durationElements = document.querySelectorAll('span.ytd-thumbnail-overlay-time-status-renderer');

function speedUp(h, m, s, x) {
    sx = (h * 3600 + m * 60 + s) / x;
    hx = parseInt(sx / 3600);
    sx %= 3600;
    mx = parseInt(sx / 60);
    sx %= 60;
    sx = parseInt(sx);
    console.log(`${x}x speed: ${hx}:${mx}:${sx}`);
}

hours = 0;
minutes = 0;
seconds = 0;
for (i = 0; i < durationElements.length; ++i) {
    duration = durationElements[i].innerText.split(":");
    if (duration.length == 2) duration = [0, ...duration];
    hours += parseInt(duration[0]);
    minutes += parseInt(duration[1]);
    seconds += parseInt(duration[2]);
}

minutes += parseInt(seconds / 60);
seconds %= 60;
hours += parseInt(minutes / 60);
minutes %= 60;

console.log(`1x speed: ${hours}:${minutes}:${seconds}`);
speedUp(hours, minutes, seconds, 2);
speedUp(hours, minutes, seconds, 3);