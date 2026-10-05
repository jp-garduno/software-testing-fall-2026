// smooth-scroll.js
// Smoothly scrolls to in-page sections when a nav link is clicked, and
// highlights the nav link corresponding to the section currently in view.

const NAVBAR_OFFSET = 70;

function scrollToSection(targetId) {
  const target = document.querySelector(targetId);
  if (target) {
    const top = target.getBoundingClientRect().top + window.scrollY - NAVBAR_OFFSET;
    window.scrollTo({ top: top, behavior: 'smooth' });
  }
}

function initSmoothScroll() {
  const navLinks = document.querySelectorAll('.nav-link[href^="#"], .dropdown-item[href^="#"]');

  navLinks.forEach(function (link) {
    link.addEventListener('click', function (event) {
      const href = link.getAttribute('href');
      if (href.length > 1) {
        event.preventDefault();
        scrollToSection(href);
        const collapseEl = document.getElementById('mynavbar');
        if (collapseEl && collapseEl.classList.contains('show'))
          collapseEl.classList.remove('show');
      }
    });
  });
}

function initActiveLinkHighlight() {
  const sections = document.querySelectorAll('main section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', function () {
    let currentSectionId = '';

    sections.forEach(function (section) {
      const sectionTop = section.offsetTop - NAVBAR_OFFSET - 10;
      if (window.scrollY >= sectionTop) currentSectionId = section.getAttribute('id');
    });

    navLinks.forEach(function (link) {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + currentSectionId) {
        link.classList.add('active');
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  initSmoothScroll();
  initActiveLinkHighlight();
});
