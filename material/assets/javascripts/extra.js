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
