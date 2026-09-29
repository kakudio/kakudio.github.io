(function () {
  const config = window.KAKUDIO_CONFIG;
  if (!config) return;

  const isLive = (url) => typeof url === "string" && url.startsWith("https://");

  document.querySelectorAll("[data-field]").forEach((el) => {
    const value = config.randomizer[el.dataset.field];
    if (value) el.textContent = value;
    else el.hidden = true;
  });

  document.querySelectorAll("[data-link]").forEach((el) => {
    const url = config.links[el.dataset.link];
    if (isLive(url)) {
      const link = document.createElement("a");
      link.className = el.className;
      link.href = url;
      link.innerHTML = el.innerHTML;
      el.replaceWith(link);
    } else {
      el.classList.add("is-soon");
      const note = document.createElement("span");
      note.className = "soon-note";
      note.textContent = "coming soon";
      el.append(" ", note);
    }
  });

  const slots = document.querySelectorAll("[data-media-slot]");
  (config.media || []).slice(0, slots.length).forEach((item, i) => {
    const img = document.createElement("img");
    img.src = item.src;
    img.alt = item.alt || "";
    img.loading = "lazy";
    img.decoding = "async";
    slots[i].replaceChildren(img);
    slots[i].classList.add("is-filled");
  });
})();
