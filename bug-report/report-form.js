"use strict";

const MAX_LOG_BYTES = 1024 * 1024;

class Refused extends Error {}

function show(container, name, slots = {}) {
  let shown;
  for (const message of container.querySelectorAll("[data-message]")) {
    message.hidden = message.dataset.message !== name;
    if (!message.hidden) shown = message;
  }
  if (!shown) return;
  for (const [slot, text] of Object.entries(slots)) {
    const target = shown.dataset.slot === slot ? shown : shown.querySelector(`[data-slot="${slot}"]`);
    if (target) target.textContent = text;
  }
}

function setUpCopyButtons() {
  for (const button of document.querySelectorAll("[data-copy]")) {
    const row = button.closest(".copy-row");
    const copied = row.querySelector("[data-copied]");
    const failed = row.querySelector("[data-copy-failed]");
    row.hidden = false;
    button.addEventListener("click", async () => {
      copied.hidden = failed.hidden = true;
      let ok = false;
      try {
        await navigator.clipboard.writeText(document.getElementById(button.dataset.copy).textContent);
        ok = true;
      } catch {}
      setTimeout(() => {
        (ok ? copied : failed).hidden = false;
      }, 50);
    });
  }
}

function glob(pattern, name) {
  const source = pattern
    .split("*")
    .map((part) => part.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
    .join("[^/\\\\]*");
  return new RegExp(`^${source}$`, "i").test(name);
}

function fileNamePattern(mod) {
  return mod.run_log_pattern.slice(mod.run_log_pattern.lastIndexOf("/") + 1);
}

function startsLikeRunLog(mod, text) {
  const body = text.startsWith("﻿") ? text.slice(1) : text;
  return body.startsWith(`${mod.run_log_first_line}\n`) || body.startsWith(`${mod.run_log_first_line}\r\n`);
}

function fitsPattern(mod, segments) {
  const pattern = mod.run_log_pattern.split("/");
  const places = [[fileNamePattern(mod)], pattern];
  if (mod.install_folder) places.push(["Mods", "Data", mod.install_folder, ...pattern]);
  return places.some(
    (place) => place.length === segments.length && place.every((part, i) => glob(part, segments[i])),
  );
}

async function firstLineMod(file, mods) {
  const longest = Math.max(...mods.map((mod) => new TextEncoder().encode(mod.run_log_first_line).length));
  try {
    const head = new TextDecoder().decode(await file.slice(0, longest + 5).arrayBuffer());
    return mods.find((mod) => startsLikeRunLog(mod, head));
  } catch {
    return undefined;
  }
}

async function readRunLog(file, mods) {
  const named = mods.filter((mod) => glob(fileNamePattern(mod), file.name));
  if (!named.length) throw new Refused("not-run-log");
  if (file.size === 0) throw new Refused("empty");
  if (file.size > MAX_LOG_BYTES) throw new Refused("too-large");
  let bytes;
  try {
    bytes = await file.arrayBuffer();
  } catch {
    throw new Refused("unreadable");
  }
  let log;
  try {
    log = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
  } catch {
    throw new Refused("not-text");
  }
  if (log.includes("\0")) throw new Refused("not-text");
  const mod = named.find((candidate) => startsLikeRunLog(candidate, log));
  if (!mod) throw new Refused("not-run-log");
  return { mod, log };
}

async function loadMods(url) {
  const response = await fetch(url, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(`mods: ${response.status}`);
  const { mods } = await response.json();
  const usable = (mods ?? []).filter(
    (mod) =>
      typeof mod?.id === "string" &&
      typeof mod.run_log_pattern === "string" &&
      typeof mod.run_log_first_line === "string" &&
      mod.run_log_first_line !== "",
  );
  if (!usable.length) throw new Error("mods: none listed");
  return usable;
}

function setUpForm(form, mods) {
  const pick = form.querySelector("#pick");
  const pickStatus = form.querySelector(".pick-status");
  const sendStatus = form.querySelector(".send-status");
  const runsBox = form.querySelector("#runs");
  const runList = form.querySelector("#run-list");
  const folderInput = form.querySelector("#folder-input");
  const fileInput = form.querySelector("#file-input");
  const description = form.querySelector("#description");
  const send = form.querySelector("#send");
  const dateFormat = new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" });

  let runs = [];
  let chosen = null;

  function choose(newRuns) {
    runs = newRuns;
    chosen = runs[0] ?? null;
    runList.replaceChildren(
      ...runs.map((file, i) => {
        const item = document.createElement("li");
        const label = document.createElement("label");
        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "run";
        radio.value = String(i);
        radio.checked = i === 0;
        const name = document.createElement("span");
        name.className = "run-name";
        name.textContent = file.name;
        const when = document.createElement("time");
        when.dateTime = new Date(file.lastModified).toISOString();
        when.textContent = dateFormat.format(file.lastModified);
        label.append(radio, name, when);
        item.append(label);
        return item;
      }),
    );
  }

  async function listFolder(files, segmentsOf) {
    const listed = [];
    for (const file of files) {
      const segments = segmentsOf(file);
      const fitting = mods.filter((mod) => fitsPattern(mod, segments));
      if (fitting.length && (await firstLineMod(file, fitting))) listed.push(file);
    }
    listed.sort((a, b) => b.lastModified - a.lastModified);
    choose(listed);
    runsBox.hidden = listed.length < 2;
    show(sendStatus, null);
    if (!listed.length) show(pickStatus, "no-runs");
    else if (listed.length === 1) show(pickStatus, "chosen", { name: listed[0].name });
    else show(pickStatus, "listed", { count: String(listed.length) });
  }

  async function chooseFile(file) {
    show(sendStatus, null);
    runsBox.hidden = true;
    try {
      await readRunLog(file, mods);
      choose([file]);
      show(pickStatus, "chosen", { name: file.name });
    } catch (error) {
      if (!(error instanceof Refused)) throw error;
      choose([]);
      show(pickStatus, error.message, { name: file.name });
    }
  }

  async function chooseFiles(files) {
    if (files.length === 1) await chooseFile(files[0]);
    else if (files.length > 1) await listFolder(files, (file) => [file.name]);
  }

  form.querySelector('[data-pick="folder"]').addEventListener("click", () => folderInput.click());
  form.querySelector('[data-pick="file"]').addEventListener("click", () => fileInput.click());

  folderInput.addEventListener("change", async () => {
    const files = [...folderInput.files];
    folderInput.value = "";
    await listFolder(files, (file) => file.webkitRelativePath.split("/").slice(1));
  });

  fileInput.addEventListener("change", async () => {
    const [file] = fileInput.files;
    fileInput.value = "";
    if (file) await chooseFile(file);
  });

  runList.addEventListener("change", (event) => {
    chosen = runs[Number(event.target.value)] ?? null;
  });

  form.addEventListener("dragover", (event) => {
    if (!event.dataTransfer.types.includes("Files")) return;
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
    pick.classList.add("pick--dragging");
  });
  form.addEventListener("dragleave", (event) => {
    if (!form.contains(event.relatedTarget)) pick.classList.remove("pick--dragging");
  });
  form.addEventListener("drop", async (event) => {
    if (!event.dataTransfer.types.includes("Files")) return;
    event.preventDefault();
    pick.classList.remove("pick--dragging");
    await chooseFiles([...event.dataTransfer.files]);
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (send.disabled) return;
    if (!chosen) {
      show(sendStatus, "no-run");
      form.querySelector('[data-pick="folder"]').focus();
      return;
    }
    if (!description.value.trim()) {
      show(sendStatus, "no-description");
      description.focus();
      return;
    }

    const file = chosen;
    let run;
    try {
      run = await readRunLog(file, mods);
    } catch (error) {
      if (!(error instanceof Refused)) throw error;
      show(sendStatus, null);
      show(pickStatus, error.message, { name: file.name });
      return;
    }

    send.disabled = true;
    show(sendStatus, "sending");
    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mod_id: run.mod.id, description: description.value, log_name: file.name, log: run.log }),
      });
      const answer = await response.json().catch(() => ({}));
      if (response.status === 201 && typeof answer.reference === "string" && answer.reference) {
        show(sendStatus, "sent", { reference: answer.reference });
      } else if (response.status !== 201 && typeof answer.error === "string" && answer.error.trim()) {
        show(sendStatus, "refused", { error: answer.error });
      } else {
        show(sendStatus, "no-reason");
      }
    } catch {
      show(sendStatus, "no-answer");
    } finally {
      send.disabled = false;
    }
  });
}

async function setUp() {
  setUpCopyButtons();

  const form = document.getElementById("report-form");
  const loading = document.getElementById("form-loading");
  document.getElementById("form-needs-js").hidden = true;
  loading.hidden = false;

  let mods;
  try {
    mods = await loadMods(form.dataset.mods);
  } catch {
    loading.hidden = true;
    document.getElementById("form-unavailable").hidden = false;
    return;
  }
  loading.hidden = true;
  setUpForm(form, mods);
  form.hidden = false;
}

setUp();
