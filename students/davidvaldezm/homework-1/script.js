const year = document.querySelector("#year");
const navigationLinks = document.querySelectorAll("nav a[href^='#']");
const sections = document.querySelectorAll("main section[id]");

year.textContent = new Date().getFullYear();

const observer = new IntersectionObserver(
  (entries) => {
    const visibleSection = entries.find((entry) => entry.isIntersecting);

    if (!visibleSection) return;

    navigationLinks.forEach((link) => {
      const isCurrent = link.hash === `#${visibleSection.target.id}`;
      link.toggleAttribute("aria-current", isCurrent);
    });
  },
  { rootMargin: "-30% 0px -60%", threshold: 0 }
);

sections.forEach((section) => observer.observe(section));
