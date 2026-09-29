/**
 * Small progressive enhancements for the portfolio.
 * The site works without JavaScript; this only adds convenience.
 */

/**
 * Writes the current year into every element with id "year".
 * Keeps the footer copyright from going stale.
 */
function stampCurrentYear() {
  const target = document.getElementById("year");
  if (target) {
    target.textContent = String(new Date().getFullYear());
  }
}

/**
 * Marks the navigation link matching the current page as active,
 * so the header reflects where the visitor is.
 */
function highlightCurrentPage() {
  const current = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".site-nav a").forEach((link) => {
    if (link.getAttribute("href") === current) {
      link.setAttribute("aria-current", "page");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  stampCurrentYear();
  highlightCurrentPage();
});
