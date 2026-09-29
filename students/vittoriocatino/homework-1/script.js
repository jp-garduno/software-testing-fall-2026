const projects = [
  {
    name: "Git Workflow Practice",
    description: "A portfolio created with focused branches and conventional commits.",
    tags: ["Git", "HTML", "CSS"],
  },
  {
    name: "Testing Notes",
    description: "A growing collection of software-testing concepts and techniques.",
    tags: ["Quality", "Learning"],
  },
];

const projectList = document.querySelector("#project-list");

projectList.innerHTML = projects
  .map(
    ({ name, description, tags }) => `
      <article class="project-card">
        <h3>${name}</h3>
        <p>${description}</p>
        <p class="tags">${tags.map((tag) => `<span>${tag}</span>`).join("")}</p>
      </article>
    `,
  )
  .join("");
