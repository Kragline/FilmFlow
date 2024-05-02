const labels = document.querySelectorAll('.rate-movie');

labels.forEach(label => {
    label.addEventListener('mouseover', () => {
        const rating = parseInt(label.dataset.ratingScore);

        for (let i = 0; i <= rating - 1; i++) {
            const previousLabel = labels[i];
            const starIcon = previousLabel.querySelector('.bi-star');

            starIcon.classList.add('bi-star-fill');
            starIcon.classList.remove('bi-star');
        }
    });

    label.addEventListener('mouseout', () => {
        const rating = parseInt(label.dataset.ratingScore);

        for (let i = 0; i <= rating - 1; i++) {
            const previousLabel = labels[i];
            const starIcon = previousLabel.querySelector('.bi-star-fill');

            starIcon.classList.add('bi-star');
            starIcon.classList.remove('bi-star-fill');
        }
    });
});