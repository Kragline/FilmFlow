const movieYearElement = document.getElementById("movieYear");
movieYearElement.addEventListener("click", findMoviesByYear);

function findMoviesByYear() {
    const movieYear = movieYearElement.textContent;

    const formElement = document.getElementById("movieSearchForm");
    const checkboxes = document.getElementsByClassName('movie-year-checkbox');

    for (let index = 0; index < checkboxes.length; index++) {
        if (checkboxes[index].value === movieYear) {
            checkboxes[index].checked = true;
            break;        
        }
    }

    formElement.submit();
}

const movieCountryElement = document.getElementById("movieCountry");
movieCountryElement.addEventListener("click", findMoviesByCountry);

function findMoviesByCountry() {
    const movieCountry = movieCountryElement.textContent;

    const formElement = document.getElementById("movieSearchForm");
    const checkboxes = document.getElementsByClassName('movie-country-checkbox');

    for (let index = 0; index < checkboxes.length; index++) {
        if (checkboxes[index].value === movieCountry) {
            checkboxes[index].checked = true;
            break;        
        }
    }

    formElement.submit();
}