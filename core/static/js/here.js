const data = JSON.parse(
    document.currentScript.nextElementSibling.textContent
  );

const header = document.getElementById("header-content");

const tile1 = document.getElementById("tile1");
const arrow1 = document.getElementById("arrow1");
const tile2 = document.getElementById("tile2");
const arrow2 = document.getElementById("arrow2");
const tile3 = document.getElementById("tile3");
const arrow3 = document.getElementById("arrow3");

const tile4 = document.getElementById("tile4");
const arrow4 = document.getElementById("arrow4");
// const tile5 = document.getElementById("tile5");
// const arrow5 = document.getElementById("arrow5");
const tile6 = document.getElementById("tile6");
const arrow6 = document.getElementById("arrow6");

const tile7 = document.getElementById("tile7");
const arrow7 = document.getElementById("arrow7");
const tile8 = document.getElementById("tile8");
const arrow8 = document.getElementById("arrow8");
const tile9 = document.getElementById("tile9");
const arrow9 = document.getElementById("arrow9");

tile1.onmouseover = function () {
    header.innerHTML = data[0]["path"];
    arrow1.style.opacity = 1;
    tile1.style.backgroundImage = "url('/static/"+data[0]['img_dark']+"')";
}

tile1.onmouseout = function () {
    header.innerHTML = "here";
    arrow1.style.opacity = 0;
    tile1.style.backgroundImage = "url('/static/"+data[0]['img_light']+"')";
}

tile2.onmouseover = function () {
    header.innerHTML = data[1]["path"];
    arrow2.style.opacity = 1;
    tile2.style.backgroundImage ="url('/static/"+data[1]['img_dark']+"')";
}

tile2.onmouseout = function () {
    header.innerHTML = "here";
    arrow2.style.opacity = 0;
    tile2.style.backgroundImage = "url('/static/"+data[1]['img_light']+"')";
}

tile3.onmouseover = function () {
    header.innerHTML = data[2]["path"];
    arrow3.style.opacity = 1;
    tile3.style.backgroundImage = "url('/static/"+data[2]['img_dark']+"')";
}

tile3.onmouseout = function () {
    header.innerHTML = "here";
    arrow3.style.opacity = 0;
    tile3.style.backgroundImage =  "url('/static/"+data[2]['img_light']+"')";
}

tile4.onmouseover = function () {
    header.innerHTML = data[3]["path"];
    arrow4.style.opacity = 1;
    tile4.style.backgroundImage = "url('/static/"+data[3]['img_dark']+"')";
}

tile4.onmouseout = function () {
    header.innerHTML = "here";
    arrow4.style.opacity = 0;
    tile4.style.backgroundImage =  "url('/static/"+data[3]['img_light']+"')";
}

// tile5.onmouseover = function () {
//     header.innerHTML = "dahlia.is/learning";
//     arrow5.style.opacity = 1;
//     tile5.style.backgroundImage =  "url('/static/media/IMG_0631 2.png')";
// }

// tile5.onmouseout = function () {
//     header.innerHTML = "dahlia.is/here";
//     arrow5.style.opacity = 0;
//     tile5.style.backgroundImage = "url('/static/media/IMG_0631.png')";
// }

tile6.onmouseover = function () {
    header.innerHTML = data[4]["path"];
    arrow6.style.opacity = 1;
    tile6.style.backgroundImage = "url('/static/"+data[4]['img_dark']+"')";
}

tile6.onmouseout = function () {
    header.innerHTML = "here";
    arrow6.style.opacity = 0;
    tile6.style.backgroundImage = "url('/static/"+data[4]['img_light']+"')";
}

tile7.onmouseover = function () {
    header.innerHTML = data[5]["path"];
    arrow7.style.opacity = 1;
    tile7.style.backgroundImage = "url('/static/"+data[5]['img_dark']+"')";
}

tile7.onmouseout = function () {
    header.innerHTML = "here";
    arrow7.style.opacity = 0;
    tile7.style.backgroundImage =  "url('/static/"+data[5]['img_light']+"')";
}

tile8.onmouseover = function () {
    header.innerHTML = data[6]["path"];
    arrow8.style.opacity = 1;
    tile8.style.backgroundImage = "url('/static/"+data[6]['img_dark']+"')";
}

tile8.onmouseout = function () {
    header.innerHTML = "here";
    arrow8.style.opacity = 0;
    tile8.style.backgroundImage =  "url('/static/"+data[6]['img_light']+"')";
}

tile9.onmouseover = function () {
    header.innerHTML = data[7]["path"];
    arrow9.style.opacity = 1;
    tile9.style.backgroundImage = "url('/static/"+data[7]['img_dark']+"')";
}

tile9.onmouseout = function () {
    header.innerHTML = "here";
    arrow9.style.opacity = 0;
    tile9.style.backgroundImage =  "url('/static/"+data[7]['img_light']+"')";
}

map.onmouseover = function () {
    header.innerHTML = "dahlia.is/where?";
}

map.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
}