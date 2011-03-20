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

    day = now.getDate();
    month = now.getMonth();

    if (hours <= 9)
        hours = "0" + hours;
    if (minutes <= 9)
        minutes = "0" + minutes;
    if (seconds <= 9)
        seconds = "0" + seconds;
    if (month <= 9)
	month = "0" + month;
    if (day <= 9)
	day = "0" + day;

    liveclock = $("#liveclock");
    liveclock.html('');
    weekday = '<div style="text-align: center;font-size: 17px">' + WEEKDAY + '</div>';
    liveclock.append(weekday);
    date = '<div style="text-align: center;font-size: 17px">' + day + '/' + month + '/' + now.getFullYear() + '</div>';
    liveclock.append(date);
    content = "<b>" + hours + ":" + minutes + ":" + seconds + "</b>";
    liveclock.append(content);
    setTimeout("clock_tick()", 1000);
}

