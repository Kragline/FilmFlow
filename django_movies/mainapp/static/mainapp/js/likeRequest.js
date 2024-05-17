$(document).ready(function () {
    $(document).on('click', '.like-comm-btn', function (e) {
        e.preventDefault();

        var url = $(this).attr('href');
        
        var movieID = $(this).data('moive-id');
        var commentID = $(this).data('comment-id');
        
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                movie_id: movieID,
                comment_id: commentID,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                var newLikesCount = data.newLikesCount;
                var newButtonText = data.newButtonText;

                $('#commentLikesCount_' + String(commentID)).html(newLikesCount);
                $('#commentBtnText_' + String(commentID)).html(newButtonText);
            }
        })
    })
});