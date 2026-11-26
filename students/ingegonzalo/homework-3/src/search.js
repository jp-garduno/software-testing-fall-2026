// search.js
// Filters the project cards on the homepage based on the navbar search input.

function initProjectSearch() {
  var searchInput = document.getElementById('projectSearch');
  var searchButton = document.getElementById('searchButton');
  var cards = document.querySelectorAll('.project-card');
  var noResultsMsg = document.getElementById('noResultsMessage');

  if (!searchInput || cards.length == 0) {
    return;
  }

  function filterCards() {
    var query = searchInput.value.toLowerCase().trim();
    var matches = 0;

    cards.forEach(function (card) {
      var title = card.querySelector('.card-title').textContent.toLowerCase();
      var text = card.querySelector('.card-text').textContent.toLowerCase();
      var isMatch = title.indexOf(query) > -1 || text.indexOf(query) > -1;

      if (isMatch || query == '') {
        card.parentElement.style.display = '';
        matches = matches + 1;
      } else {
        card.parentElement.style.display = 'none';
      }
    });

    if (noResultsMsg) {
      if (matches == 0) {
        noResultsMsg.classList.remove('d-none');
      } else {
        noResultsMsg.classList.add('d-none');
      }
    }
  }

  searchInput.addEventListener('input', filterCards);

  if (searchButton) {
    searchButton.addEventListener('click', function (event) {
      event.preventDefault();
      filterCards();
    });
  }
}

document.addEventListener('DOMContentLoaded', initProjectSearch);
