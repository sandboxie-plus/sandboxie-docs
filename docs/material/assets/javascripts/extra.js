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
// Replace search links zh to zh-CN
document.addEventListener("DOMContentLoaded", function() {
  const DIR_ZH = '/zh/';
  const DIR_ZHCN = '/zh-CN/';
  const SEARCH_SELECTOR = '[data-md-component="search"]';
  const RESULTS_SELECTOR = '.md-search-result';
  const TARGET_LINKS = `.md-search-result__link[href*="${DIR_ZH}"]`;

  // Check if search exists
  const searchComponent = document.querySelector(SEARCH_SELECTOR);
  if (!searchComponent) return;

  // Optimized URL replacement function
  const replaceZhUrls = () => {
    const links = document.querySelectorAll(TARGET_LINKS);
    links.forEach(link => {
      if (!link.href.includes(DIR_ZHCN)) { // Avoid double-processing
        link.href = link.href.replace(DIR_ZH, DIR_ZHCN);
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

// AI
// Fixes broken search result highlights
document$.subscribe(function() {
  // Debounce with cleanup tracking
  let debounceTimer;
  let observer;
  const processedNodes = new WeakSet();

  function processMark(mark) {
    if (processedNodes.has(mark)) return;

    const cleanText = mark.textContent.replace(/r?k?(>|&gt;)/g, '');
    if (cleanText !== mark.textContent) {
      const newMark = document.createElement('mark');
      newMark.textContent = cleanText;
      mark.replaceWith(newMark);
      processedNodes.add(newMark);
    }
    processedNodes.add(mark);
  }

  function processMarks(mutations) {
    // Clear any pending debounce
    clearTimeout(debounceTimer);

    // Process either all marks or just mutations
    if (!mutations) {
      document.querySelectorAll('mark').forEach(processMark);
    } else {
      mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.matches('mark')) {
              processMark(node);
            }
            node.querySelectorAll('mark').forEach(processMark);
          }
        });
      });
    }
  }

  // Optimized search result handler
  function setupSearchObserver() {
    const searchContainer = document.querySelector('.md-search-result');
    if (!searchContainer) return;

    // Cleanup previous observer if exists
    if (observer) observer.disconnect();

    observer = new MutationObserver(mutations => {
      // Use idle callback if available
      if ('requestIdleCallback' in window) {
        window.requestIdleCallback(
          () => processMarks(mutations),
          { timeout: 200 }
        );
      } else {
        debounceTimer = setTimeout(
          () => processMarks(mutations),
          300
        );
      }
    });

    observer.observe(searchContainer, {
      childList: true,
      subtree: true
    });
  }

  // Initial setup
  setupSearchObserver();
  processMarks();

  // Re-setup observer when search is reopened
  document.addEventListener('search', setupSearchObserver);
});
