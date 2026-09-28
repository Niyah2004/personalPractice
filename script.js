// Shared storage helpers.
// Everything is kept in localStorage so the input page and the display
// page can share data purely in the browser, with no backend/server.
const STORAGE_KEYS = {
  title: "namesSite.title",
  names: "namesSite.names",
};

function getTitle() {
  return localStorage.getItem(STORAGE_KEYS.title) || "";
}

function setTitle(title) {
  localStorage.setItem(STORAGE_KEYS.title, title);
}

function getNames() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.names);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch (err) {
    return [];
  }
}

function saveNames(names) {
  localStorage.setItem(STORAGE_KEYS.names, JSON.stringify(names));
}

function addName(name) {
  const names = getNames();
  names.push(name);
  saveNames(names);
  return names;
}

function removeNameAt(index) {
  const names = getNames();
  names.splice(index, 1);
  saveNames(names);
  return names;
}

/* ---------------- Input page ---------------- */
function initInputPage() {
  const form = document.getElementById("entry-form");
  if (!form) return;

  const titleInput = document.getElementById("title-input");
  const nameInput = document.getElementById("name-input");
  const status = document.getElementById("status");
  const previewList = document.getElementById("preview-list");
  const emptyMsg = document.getElementById("preview-empty");

  // Restore whatever was already saved (e.g. a page refresh).
  titleInput.value = getTitle();

  function renderPreview() {
    const names = getNames();
    previewList.innerHTML = "";

    if (names.length === 0) {
      emptyMsg.style.display = "block";
      return;
    }
    emptyMsg.style.display = "none";

    names.forEach((name, index) => {
      const li = document.createElement("li");

      const span = document.createElement("span");
      span.textContent = name;
      li.appendChild(span);

      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "remove";
      removeBtn.setAttribute("aria-label", `Remove ${name}`);
      removeBtn.textContent = "✕";
      removeBtn.addEventListener("click", () => {
        removeNameAt(index);
        renderPreview();
      });
      li.appendChild(removeBtn);

      previewList.appendChild(li);
    });
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const title = titleInput.value.trim();
    const name = nameInput.value.trim();

    if (!name) {
      status.textContent = "Type a name first.";
      nameInput.focus();
      return;
    }

    setTitle(title);
    addName(name);

    nameInput.value = "";
    nameInput.focus();
    status.textContent = `Added "${name}" — check the display page to see it.`;
    renderPreview();
  });

  renderPreview();
}

/* ---------------- Display page ---------------- */
function initDisplayPage() {
  const heading = document.getElementById("display-title");
  const list = document.getElementById("display-list");
  const emptyMsg = document.getElementById("display-empty");
  const count = document.getElementById("display-count");
  if (!heading || !list) return;

  function render() {
    const title = getTitle();
    const names = getNames();

    heading.textContent = title || "Names";

    list.innerHTML = "";
    if (names.length === 0) {
      emptyMsg.style.display = "block";
    } else {
      emptyMsg.style.display = "none";
      names.forEach((name) => {
        const li = document.createElement("li");
        li.textContent = name;
        list.appendChild(li);
      });
    }

    count.textContent =
      names.length === 0
        ? "No names yet"
        : `${names.length} name${names.length === 1 ? "" : "s"}`;
  }

  render();

  // If names are added on the input page in another tab, update live.
  window.addEventListener("storage", (event) => {
    if (event.key === STORAGE_KEYS.names || event.key === STORAGE_KEYS.title) {
      render();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initInputPage();
  initDisplayPage();
});
