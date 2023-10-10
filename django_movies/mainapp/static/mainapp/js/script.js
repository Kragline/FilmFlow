function fineMovieByYear() {
    const movieYearElemet = document.getElementById("movieYear");
    const movieYear = movieYearElemet.textContent;
    console.log(movieYear);

    const formElement = document.getElementById("movieSearchForm");
    const checkboxes = document.querySelectorAll('input[type="checkbox"]')    

    checkboxes.forEach(checkbox => {
        if (checkbox.value === movieYear) {
            checkbox.checked = true;
        }
    });

    formElement.submit();
}