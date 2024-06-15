document.addEventListener('DOMContentLoaded', function() {
    var starCheckbox = document.getElementById('id_is_favorite');
    var starLabel = document.querySelector('.star-label');

    if (starLabel) {
        starLabel.addEventListener('mouseover', function() {
            if (!starCheckbox.checked) {
                this.querySelector('.far.fa-star').style.color = '#ffc107';
            }
        });

        starLabel.addEventListener('mouseout', function() {
            if (!starCheckbox.checked) {
                this.querySelector('.far.fa-star').style.color = '#ccc';
            }
        });
    }
});