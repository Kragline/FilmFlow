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
                var countDifference = avgRatingStars.length - newAvgRating;

                if (countDifference > 0) {
                    for (let index = 0; index < countDifference; index++) {
                        avgRatingStars[index].remove();                        
                    }
                } else if (countDifference < 0) {
                    for (let index = 0; index < Math.floor(Math.abs(countDifference)); index++) {
                        var cloneStar = avgRatingStars[0].cloneNode(true);
                        document.getElementById('avgRatingBlock').appendChild(cloneStar);
                    }
                }
            }
        })
    })
});
