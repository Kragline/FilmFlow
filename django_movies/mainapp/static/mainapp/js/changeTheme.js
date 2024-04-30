const doc = document.getElementById('html');

window.addEventListener('load', checkThemeOnLoad);
function checkThemeOnLoad() {
    const storedTheme = JSON.parse(localStorage.getItem('theme'));
    if (!storedTheme) {
        localStorage.setItem('theme', JSON.stringify('light'));
    } else if (storedTheme == 'light') {
        setLightTheme();
    } else if (storedTheme == 'dark') {
        setDarkTheme();
    }
}

function checkThemeByBtn() {
    if (theme_btn.value == 'light') {
        setLightTheme();
    } else if (theme_btn.value == 'dark') {
        setDarkTheme();
    }
}

const theme_btn = document.getElementById('themeBtn');
theme_btn.addEventListener('click', setThemeByButton);

function setThemeByButton() {
    localStorage.setItem('theme', JSON.stringify(theme_btn.value));
    checkThemeByBtn();
}

function setDarkTheme() {
    doc.setAttribute("data-bs-theme", "dark");
    theme_btn.value = 'light';
    theme_btn.innerText = 'Light mode';
    
    document.getElementById('header-nav').classList.add('nav-dark-shadow');
    document.getElementById('footer').classList.add('footer-dark-shadow');
    
    const boldElements = document.getElementsByClassName('movie-bold');
    for (let index = 0; index < boldElements.length; index++) {
        boldElements[index].classList.add('movie-bold-dark');
    }

    const linkElements = document.getElementsByClassName('movie-link');
    for (let index = 0; index < linkElements.length; index++) {
        linkElements[index].classList.add('movie-link-dark');
    }

    const hoverLinkElements = document.getElementsByClassName('hover-movie-link');
    for (let index = 0; index < hoverLinkElements.length; index++) {
        hoverLinkElements[index].classList.add('hover-movie-link-dark');
    }

    
    localStorage.setItem('theme', JSON.stringify('dark'));
}

function setLightTheme() {
    doc.setAttribute("data-bs-theme", "light");
    theme_btn.value = 'dark';
    theme_btn.innerText = 'Dark mode';

    document.getElementById('header-nav').classList.remove('nav-dark-shadow');
    document.getElementById('footer').classList.remove('footer-dark-shadow');

    const boldElements = document.getElementsByClassName('movie-bold-dark');
    for (let index = 0; index < boldElements.length; index++) {
        boldElements[index].classList.remove('movie-bold-dark');
    }

    const linkElements = document.getElementsByClassName('movie-link');
    for (let index = 0; index < linkElements.length; index++) {
        linkElements[index].classList.remove('movie-link-dark');
    }

    const hoverLinkElements = document.getElementsByClassName('hover-movie-link');
    for (let index = 0; index < hoverLinkElements.length; index++) {
        hoverLinkElements[index].classList.remove('hover-movie-link-dark');
    }

    localStorage.setItem('theme', JSON.stringify('light'));
}