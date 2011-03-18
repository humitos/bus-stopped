// References:
//   http://www.electrictoolbox.com/using-settimeout-javascript/
//   http://bytes.com/topic/javascript/answers/89176-easy-you-how-do-i-add-5-seconds-date
//   http://www.desarrolloweb.com/articulos/549.php
//   http://www.efectosjavascript.com/reloj4.html
function clock_tick(){
    now.setSeconds(now.getSeconds() + 1);
    hours = now.getHours();
    minutes = now.getMinutes();
    seconds = now.getSeconds();

    if (hours <= 9)
        hours = "0" + hours;
    if (minutes <= 9)
        minutes = "0" + minutes;
    if (seconds <= 9)
        seconds = "0" + seconds;

    liveclock = $("#liveclock");
    content = "<b>" + hours + ":" + minutes + ":" + seconds + "</b>";
    liveclock.html(content);
    setTimeout("clock_tick()", 1000);
}

