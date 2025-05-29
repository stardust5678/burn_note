import notFoundTemplate from "./templates/not-found.html?raw";

export function renderNotFoundView() {
  const container = document.getElementById("app")!;
  container.innerHTML = notFoundTemplate;
}
