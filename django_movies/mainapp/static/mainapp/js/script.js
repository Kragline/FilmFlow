function findMovieByYear() {
    const movieYearElement = document.getElementById("movieYear");
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

function findMovieByCountry() {
    const movieCountryElement = document.getElementById("movieCountry");
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