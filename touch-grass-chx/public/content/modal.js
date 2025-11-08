(() => {
  const Z = "2147483647";

  /** Modal factory: lets you inject custom body content + actions. */
  function showModalStep({
    id,
    title,
    subtitle,
    message,
    bg = "#FFD7DF",
    bodyBuilder,
    actions,
  }) {
    return new Promise((resolve) => {
      if (document.getElementById(id)) return;

      const overlay = document.createElement("div");
      overlay.id = id;
      Object.assign(overlay.style, {
        position: "fixed",
        inset: "0",
        background: "rgba(0,0,0,0.5)",
        zIndex: Z,
        display: "grid",
        placeItems: "center",
        fontFamily: "Inter, system-ui, Arial, sans-serif",
      });

      const box = document.createElement("div");
      Object.assign(box.style, {
        width: "min(95vw, 480px)",
        background: bg,
        color: "#111",
        borderRadius: "16px",
        padding: "20px",
        boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
        textAlign: "center",
      });

      const h = document.createElement("h3");
      h.textContent = title;
      Object.assign(h.style, { margin: "0 0 8px", fontSize: "20px" });

      const sh = document.createElement("h3");
      h.textContent = subtitle;
      Object.assign(h.style, { margin: "0 0 8px", fontSize: "20px" });

      const p = document.createElement("p");
      p.textContent = message;
      Object.assign(p.style, { margin: "0 0 16px", lineHeight: "1.4" });

      /** custom body area (optional) */
      const body = document.createElement("div");

      const row = document.createElement("div");
      Object.assign(row.style, {
        display: "flex",
        gap: "10px",
        justifyContent: "center",
        flexWrap: "wrap",
        marginTop: "12px",
      });

      /** Build custom body (webcam / slider, etc.) */
      let cleanup = null;
      let payloadRef = {}; // for returning data (photo/rating)
      if (typeof bodyBuilder === "function") {
        const { node, onCleanup, payload } = bodyBuilder();
        if (node) body.appendChild(node);
        if (onCleanup) cleanup = onCleanup;
        if (payload) payloadRef = payload;
      }

      actions.forEach(({ id: actionId, label, color, onClick }) => {
        const btn = document.createElement("button");
        btn.textContent = label;
        Object.assign(btn.style, {
          border: "none",
          borderRadius: "10px",
          padding: "10px 14px",
          cursor: "pointer",
          fontSize: "14px",
          fontWeight: 600,
          background: color,
          color: "white",
        });
        btn.addEventListener("click", async () => {
          try {
            if (typeof onClick === "function") await onClick(payloadRef);
          } catch {}
          if (typeof cleanup === "function") {
            try {
              cleanup();
            } catch {}
          }
          overlay.remove();
          resolve({ action: actionId, payload: payloadRef });
        });
        row.append(btn);
      });

      box.append(h, sh, p, body, row);
      overlay.append(box);
      document.documentElement.appendChild(overlay);

      setTimeout(() => row.querySelector("button")?.focus(), 0);

      overlay.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
          if (typeof cleanup === "function") {
            try {
              cleanup();
            } catch {}
          }
          overlay.remove();
          resolve({ action: "dismiss" });
        }
      });
    });
  }

  /** STEP 0: should we show for this host? */
  async function shouldShowForThisHost() {
    const host = location.hostname.replace(/^www\./, "").toLowerCase();
    const { blocked = [] } = await chrome.storage.sync.get("blocked");
    return blocked.some((b) => host === b || host.endsWith("." + b));
  }

  /** STEP 1: original confirm */
  async function step1_confirm() {
    return showModalStep({
      id: "__tg_focus_step1__",
      title: "Touch Grass!",
      subtitle: "Puzzle Solving - Analytical",
      message:
        "Grab a puzzle or create your own! You can draw a simple picture on a piece of cardboard and cut it into different shapes. Then, mix up the pieces and challenge yourself or a friend to put it back together! Don't forget to take a photo of your completed puzzle masterpiece!",
      actions: [
        {
          id: "leave",
          label: "Leave",
          color: "#ef4444",
          onClick: () => {
            if (history.length > 1) history.back();
            else location.href = "about:blank";
          },
        },
        { id: "continue", label: "Continue", color: "#3b82f6" },
      ],
    });
  }

  /** STEP 2: webcam capture */
  function buildWebcamBody() {
    const container = document.createElement("div");
    Object.assign(container.style, {
      display: "grid",
      gap: "8px",
      justifyItems: "center",
    });

    const status = document.createElement("div");
    Object.assign(status.style, { fontSize: "12px", opacity: 0.8 });

    const video = document.createElement("video");
    Object.assign(video.style, {
      width: "100%",
      maxWidth: "360px",
      borderRadius: "12px",
      background: "#000",
    });
    video.autoplay = true;
    video.playsInline = true;
    video.muted = true;

    const canvas = document.createElement("canvas"); // hidden, used for capture
    canvas.style.display = "none";

    container.append(status, video, canvas);

    let stream = null;
    const payload = { photoDataUrl: null };

    (async () => {
      try {
        status.textContent = "Requesting camera…";
        stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });
        video.srcObject = stream;
        status.textContent = 'Camera on. Click "Capture" to take a photo.';
      } catch (e) {
        status.textContent =
          "Could not access camera (permission denied or not supported).";
      }
    })();

    function captureFrame() {
      if (!video.videoWidth || !video.videoHeight) return;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);
      payload.photoDataUrl = canvas.toDataURL("image/png");
      status.textContent = "Captured ✔";
    }

    function cleanup() {
      if (stream) stream.getTracks().forEach((t) => t.stop());
    }

    return {
      node: container,
      onCleanup: cleanup,
      payload,
      captureFrame,
    };
  }

  async function step2_webcam() {
    let bodyApi; // to call capture from the action
    return showModalStep({
      id: "__tg_focus_step2__",
      title: "Quick Check-in 📷",
      message: "Take a picture of you solving a puzzle!",
      bodyBuilder: () => {
        bodyApi = buildWebcamBody();
        return bodyApi;
      },
      actions: [
        {
          id: "capture",
          label: "Capture",
          color: "#a855f7",
          onClick: (payload) => {
            bodyApi.captureFrame();
          },
        },
        {
          id: "skip",
          label: "Skip",
          color: "#6b7280", // gray
        },
        {
          id: "continue",
          label: "Continue",
          color: "#3b82f6",
          onClick: async (payload) => {
            // save snapshot (if any)
            const host = location.hostname.replace(/^www\./, "").toLowerCase();
            if (payload.photoDataUrl) {
              await chrome.runtime.sendMessage({
                type: "SAVE_SNAPSHOT",
                host,
                when: Date.now(),
                dataUrl: payload.photoDataUrl,
              });
            }
          },
        },
      ],
    });
  }

  /** STEP 3: mood slider 1–5 */
  function buildSliderBody() {
    const wrap = document.createElement("div");
    Object.assign(wrap.style, {
      display: "grid",
      gap: "10px",
      justifyItems: "center",
    });

    const value = document.createElement("div");
    value.textContent = "How interested are you in this activity? 3 / 5";
    Object.assign(value.style, { fontSize: "14px" });

    const range = document.createElement("input");
    range.type = "range";
    range.min = "1";
    range.max = "5";
    range.step = "1";
    range.value = "3";
    Object.assign(range.style, { width: "80%" });

    range.addEventListener("input", () => {
      value.textContent = `How interested are you in this activity? ${range.value} / 5`;
    });

    wrap.append(value, range);

    const payload = { rating: 3 };
    range.addEventListener(
      "input",
      () => (payload.rating = Number(range.value))
    );

    return {
      node: wrap,
      payload,
    };
  }

  async function step3_mood() {
    return showModalStep({
      id: "__tg_focus_step3__",
      title: "Last thing 💬",
      message: "From 1 to 5, How interested are you in this activity?",
      bodyBuilder: buildSliderBody,
      actions: [
        { id: "cancel", label: "Cancel", color: "#6b7280" },
        {
          id: "submit",
          label: "Submit",
          color: "#10b981",
          onClick: async (payload) => {
            const host = location.hostname.replace(/^www\./, "").toLowerCase();
            await chrome.runtime.sendMessage({
              type: "SAVE_MOOD",
              host,
              when: Date.now(),
              rating: payload.rating,
            });
          },
        },
      ],
    });
  }

  /** Main flow */
  async function runFlow() {
    const show = await shouldShowForThisHost();
    if (!show) return;

    const s1 = await step1_confirm();
    if (s1.action !== "continue") return;

    await step2_webcam(); // user can capture or skip; we store if captured
    await step3_mood(); // store rating
  }

  // initial + SPA navigations
  const run = () => runFlow();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run, { once: true });
  } else {
    run();
  }
  const origPush = history.pushState,
    origReplace = history.replaceState;
  const tick = () => setTimeout(run, 0);
  history.pushState = function (...a) {
    const r = origPush.apply(this, a);
    tick();
    return r;
  };
  history.replaceState = function (...a) {
    const r = origReplace.apply(this, a);
    tick();
    return r;
  };
  window.addEventListener("popstate", tick);
})();
