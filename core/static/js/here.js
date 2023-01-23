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
    header.innerHTML = "dahlia.is/currently";
    arrow1.style.opacity = 1;
    tile1.style.backgroundImage = "url('/static/media/IMG_0475 2.JPG')";
}

tile1.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
    arrow1.style.opacity = 0;
    tile1.style.backgroundImage = "url('/static/media/IMG_0475.JPG')";
}

tile2.onmouseover = function () {
    header.innerHTML = "dahlia.is/taking-notes";
    arrow2.style.opacity = 1;
    tile2.style.backgroundImage ="url('/static/media/IMG_0631 2.png')";
}

tile2.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
    arrow2.style.opacity = 0;
    tile2.style.backgroundImage = "url('/static/media/IMG_0631.png')";
}

tile3.onmouseover = function () {
    header.innerHTML = "dahlia.is/in-new-places";
    arrow3.style.opacity = 1;
    tile3.style.backgroundImage = "url('/static/media/DSC_0474 2.jpg')";
}

tile3.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
    arrow3.style.opacity = 0;
    tile3.style.backgroundImage = "url('/static/media/DSC_0474.jpg')";
}

tile4.onmouseover = function () {
    header.innerHTML = "dahlia.is/thinking";
    arrow4.style.opacity = 1;
    tile4.style.backgroundImage = "url('/static/media/82349A5F-C38C-42E1-86E5-3ECE762EFDED 2.JPG')";
}

tile4.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
    arrow4.style.opacity = 0;
    tile4.style.backgroundImage = "url('/static/media/82349A5F-C38C-42E1-86E5-3ECE762EFDED.JPG')";
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
    header.innerHTML = "dahlia.is/lost-in-space";
    arrow6.style.opacity = 1;
    tile6.style.backgroundImage = "url('/static/media/m27-colorized-sharpened 2.JPG')";
}

tile6.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
    arrow6.style.opacity = 0;
    tile6.style.backgroundImage ="url('/static/media/m27-colorized-sharpened.JPG')";
}

tile7.onmouseover = function () {
    header.innerHTML = "dahlia.is/outside";
    arrow7.style.opacity = 1;
    tile7.style.backgroundImage = "url('/static/media/F48E1EF1-3007-4E74-9CAA-2AA379AC99BE 2.jpg')";
}

tile7.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
    arrow7.style.opacity = 0;
    tile7.style.backgroundImage = "url('/static/media/F48E1EF1-3007-4E74-9CAA-2AA379AC99BE.jpg')";
}

tile8.onmouseover = function () {
    header.innerHTML = "dahlia.is/busy";
    arrow8.style.opacity = 1;
    tile8.style.backgroundImage = "url('/static/media/IMG_1575 2.jpg')";
}

tile8.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
    arrow8.style.opacity = 0;
    tile8.style.backgroundImage = "url('/static/media/IMG_1575.jpg')";
}

tile9.onmouseover = function () {
    header.innerHTML = "dahlia.is/employable";
    arrow9.style.opacity = 1;
    tile9.style.backgroundImage = "url('/static/media/IMG_2011 2.jpg')";
}

tile9.onmouseout = function () {
    header.innerHTML = "dahlia.is/here";
    arrow9.style.opacity = 0;
    tile9.style.backgroundImage = "url('/static/media/IMG_2011.jpg')";
}
