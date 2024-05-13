$(document).ready(function () {
    $(document).on('click', '.rate-movie', function (e) {
        e.preventDefault();

        var url = $(this).attr('href');
        
        var movieID = $(this).data('moive-id');
        var ratingScore = $(this).data('ratingScore');
        
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                movie_id: movieID,
                rating_score: ratingScore,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                newAvgRating = data.newAvgRating;
                $('#avgRating').html(parseFloat(newAvgRating));

                var avgRatingStars = $('.avgRatingStar');
                if (avgRatingStars.length === 0) {
                    createStars(Math.floor(newAvgRating));
                    return;
                }

                var countDifference = avgRatingStars.length - newAvgRating;
                if (countDifference > 0) {
                    removeStars(countDifference, avgRatingStars);
                } else if (countDifference < 0) {
                    addStars(countDifference, avgRatingStars);
                }
            }
        })
    })
});

function removeStars(count, set) {
    for (let index = 0; index < count; index++) {
        set[index].remove();
    }
}

function addStars(count, set) {
    var avgRatingBlock = document.getElementById('ratingStarsDiv');

    for (let index = 0; index < Math.floor(Math.abs(count)); index++) {
        var cloneStar = set[0].cloneNode(true);
        avgRatingBlock.appendChild(cloneStar);
    }
}

function createStars(newStarsCount) {
    var avgRatingBlock = document.getElementById('ratingStarsDiv');

    for (let index = 0; index < newStarsCount; index++) {
        var starIcon = document.createElement('i');
        starIcon.className = 'bi bi-star-fill avgRatingStar';
        starIcon.style.fontSize = '2rem';
        starIcon.style.color = 'rgb(235, 192, 52)';
        avgRatingBlock.appendChild(starIcon);
    }

    addTextToBlock(avgRatingBlock, String(newStarsCount))
}

function addTextToBlock(block, text) {
    var themeBtn = document.getElementById('themeBtn');

    var textP = document.createElement('p');
    textP.className = 'card-text';

    var textB = document.createElement('b');
    textB.className = 'movie-bold';
    if (themeBtn.value === 'light') {
        textB.className += ' movie-bold-dark'
    } 

    textB.setAttribute('id', 'avgRating');
    textB.innerText = text;

    textP.appendChild(textB);
    textP.innerHTML += ' / 10';

    block.appendChild(textP);
}
