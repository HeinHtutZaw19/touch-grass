// Simple storage helpers
async function getBlocked() {
  const { blocked = [] } = await chrome.storage.sync.get("blocked");
  return blocked; // array of host strings like "youtube.com"
}
async function setBlocked(list) {
  await chrome.storage.sync.set({ blocked: list });
}

// Ensure default list on install
chrome.runtime.onInstalled.addListener(async () => {
  const current = await getBlocked();
  if (!current.length) {
    await setBlocked(["youtube.com", "twitter.com"]); // default examples
  }
});

// Listen for popup UI messages
chrome.runtime.onMessage.addListener((msg, _sender, send) => {
  (async () => {
    if (msg.type === "LIST_BLOCKED") {
      send({ ok: true, blocked: await getBlocked() });
    } else if (msg.type === "ADD_BLOCKED") {
      const list = await getBlocked();
      const host = (msg.host || "").trim().toLowerCase();
      if (host && !list.includes(host)) list.push(host);
      await setBlocked(list);
      send({ ok: true, blocked: list });
    } else if (msg.type === "REMOVE_BLOCKED") {
      const list = (await getBlocked()).filter((h) => h !== msg.host);
      await setBlocked(list);
      send({ ok: true, blocked: list });
    }
  })();
  return true; // keep channel open for async
});
