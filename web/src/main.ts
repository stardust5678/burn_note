import { renderHomeView } from "./views/HomeView";
import { renderNotFoundView } from "./views/NotFoundView";
import { renderSecretView } from "./views/SecretView";

const path = window.location.pathname;
const hash = window.location.hash;

if (path === "/") {
  renderHomeView();
} else if (path.startsWith("/s/")) {
  const token = path.split("/s/")[1];
  const aesKeyHex = hash.slice(1);
  renderSecretView(token, aesKeyHex);
} else {
  renderNotFoundView();
}
