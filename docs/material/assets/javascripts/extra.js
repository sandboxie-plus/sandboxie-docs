// The script expands only the first level. Change the number 1 in the line with a comment for different levels, if desired.
// https://github.com/squidfunk/mkdocs-material/issues/2818#issuecomment-896084332
function load_navpane() {
  var width = window.innerWidth;
  if (width <= 1200)
    return;

  var nav = document.getElementsByClassName("md-nav__toggle");
  for (var i = 0; i < nav.length; i++) {
    if ((nav.item(i).id.match(/_\d/g) || []).length > 1)  // Here
      continue;
    nav.item(i).checked = true;
  }
}

document.addEventListener("DOMContentLoaded", load_navpane);

// AI
document.addEventListener("DOMContentLoaded", function() {
  const SEARCH_SELECTOR = '[data-md-component="search"]';
  const RESULTS_SELECTOR = '.md-search-result';
  const TARGET_LINKS = '.md-search-result__link[href*="/zh/"]';

  // Check if search exists
  const searchComponent = document.querySelector(SEARCH_SELECTOR);
  if (!searchComponent) return;

  // Optimized URL replacement function
  const replaceZhUrls = () => {
    const links = document.querySelectorAll(TARGET_LINKS);
    links.forEach(link => {
      if (!link.href.includes("/zh_CN/")) { // Avoid double-processing
        link.href = link.href.replace('/zh/', '/zh_CN/');
      }
    });
  };

  // Set up MutationObserver
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === 'childList') {
        replaceZhUrls();
      }
    }
  });

  // Start observing
  const searchResults = document.querySelector(RESULTS_SELECTOR);
  if (searchResults) {
    observer.observe(searchResults, {
      childList: true,
      subtree: true
    });

    // Cleanup on page navigation (for SPAs)
    document.addEventListener('click', (e) => {
      if (e.target.closest('a')) {
        observer.disconnect();
      }
    });
  }

  // Initial run (in case results exist before observer starts)
  replaceZhUrls();
});