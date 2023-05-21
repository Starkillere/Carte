let login = document.getElementsByClassName("login");
let singin = document.getElementsByClassName("sigin");

let h2login = document.getElementsByClassName("h2login");
let h2singin = document.getElementsByClassName("h2singin");

function printlogin(){
    singin[0].classList.remove('active');
    login[0].classList.add('active');

    h2singin[0].classList.remove('activeh2');
    h2login[0].classList.add('activeh2');
}

function printsigin(){
    singin[0].classList.add('active');
    login[0].classList.remove('active');

    h2singin[0].classList.add('activeh2');
    h2login[0].classList.remove('activeh2');
}