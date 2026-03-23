// ----- Helpers -----
const formatBytes = (bytes) => {
  if (bytes === 0 || bytes == null) return "—";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

const formatSeconds = (s) => {
  if (!s && s !== 0) return "—";
  const m = Math.floor(s / 60);
  const sec = Math.round(s % 60);
  return `${m}:${sec.toString().padStart(2, "0")}`;
};

// ----- Upload -----
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const progressContainer = document.getElementById("progressContainer");
const gallery = document.getElementById("gallery");
const filterButtons = document.querySelectorAll(".filter-button");

// 🔧 Em DEV (sem Nginx), defina API_BASE p/ "http://127.0.0.1:8000".
// Em PRODUÇÃO (com Nginx proxy), use "/api".
if (!window.API_BASE || typeof window.API_BASE !== "string" || window.API_BASE.trim() === "") {
  window.API_BASE = "/api"; // fallback seguro
}

let currentFilter = "all";

filterButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    filterButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = btn.dataset.filter;
    renderGallery(window.__files || []);
  });
});

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  const files = e.dataTransfer.files;
  if (files?.length) uploadFiles(files);
});

fileInput.addEventListener("change", (e) => {
  const files = e.target.files;
  if (files?.length) uploadFiles(files);
});

function uploadFiles(files) {
  const xhr = new XMLHttpRequest();
  const formData = new FormData();
  Array.from(files).forEach(f => formData.append("files", f)); // nome do campo = "files"

  const progressEl = document.createElement("div");
  progressEl.className = "progress";
  progressEl.innerHTML = `<div class="bar"></div>`;
  const bar = progressEl.querySelector(".bar");
  progressContainer.appendChild(progressEl);

  xhr.upload.addEventListener("progress", (e) => {
    if (e.lengthComputable) {
      const percent = (e.loaded / e.total) * 100;
      bar.style.width = `${percent}%`;
    }
  });

  xhr.onerror = () => {
    alert(window.API_BASE);
    alert("Falha de rede durante o upload. Verifique a API_BASE e o CORS.");
  };
  xhr.ontimeout = () => {
    alert("Tempo esgotado durante o upload.");
  };
  xhr.timeout = 0; // sem timeout (ajuste se quiser)

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      try {
        const data = JSON.parse(xhr.responseText);
        if (xhr.status >= 200 && xhr.status < 300) {
          window.__files = data || [];
          renderGallery(window.__files);
        } else {
          alert("Erro no upload: " + (data?.detail || xhr.statusText || "Tente novamente."));
        }
      } catch (err) {
        console.error("Upload parse error", err);
        if (xhr.status >= 200 && xhr.status < 300) {
          // API respondeu algo não-JSON?
          alert("Upload concluído, mas resposta inesperada do servidor.");
        } else {
          alert(window.API_BASE);
          alert("Erro no upload. Verifique o backend.");
        }
      } finally {
        setTimeout(() => progressEl.remove(), 600);
      }
    }
  };

  xhr.open("POST", `${API_BASE}/api/upload`);
  xhr.send(formData);
}

// ----- Gallery -----
async function fetchFiles() {
  try {
    const res = await fetch(`${API_BASE}/api/files`);
    const data = await res.json();
    window.__files = data || [];
    renderGallery(window.__files);
  } catch (err) {
    console.error("Erro ao buscar arquivos", err);
  }
}

function renderGallery(files) {
  const filtered = files.filter(f => currentFilter === "all" ? true : f.category === currentFilter);
  if (!filtered.length) {
    gallery.innerHTML = `<div style="opacity:.7">Nenhum arquivo encontrado.</div>`;
    return;
  }
  gallery.innerHTML = filtered.map(renderCard).join("");
}

function iconFor(f) {
  switch (f.category) {
    case "image": return "🖼️ Imagem";
    case "audio": return "🎧 Áudio";
    case "video": return "🎬 Vídeo";
    case "document": return "📄 Documento";
    default: return "📦 Arquivo";
  }
}

// --- helper: resolve a origem do backend e monta URL absoluta para /uploads ---
const __BACKEND_ORIGIN = (() => {
  try {
    // 1) honra window.API_BASE se definido no template
    let base = (window.API_BASE || "").trim();
    // 2) se vazio, heurística: dev (front :5001) -> back :8000; senão, mesma origem
    if (!base) base = (location.port === "5001") ? "http://127.0.0.1:8000" : location.origin;
    const u = new URL(base, location.origin);
    // remove /api do final, se presente
    u.pathname = u.pathname.replace(/\/+$/, "").replace(/\/api$/i, "");
    return u.origin; // ex.: http://127.0.0.1:8000
  } catch {
    return location.origin;
  }
})();

function fileUrl(u) {
  if (!u) return u;
  if (/^https?:\/\//i.test(u)) return u;        // já é absoluta
  if (u.startsWith("/")) return __BACKEND_ORIGIN + u; // /uploads/...
  return `${__BACKEND_ORIGIN}/${u.replace(/^\/+/, "")}`;
}


function renderPreview(f) {
  const url = fileUrl(f.file_url || "");
  const isPdf = (f.file_type === "application/pdf") || url.toLowerCase().endsWith(".pdf");

  if (f.category === "image") {
    return `<img class="preview" src="${url}" alt="${f.name}">`;
  } else if (f.category === "audio") {
    return `<audio class="preview" controls src="${url}"></audio>`;
  } else if (f.category === "video") {
    return `<video class="preview" controls src="${url}"></video>`;
  } else if (f.category === "document" && isPdf) {
    return `<iframe class="preview" src="${url}" title="${f.name}"></iframe>`;
  } else {
    return `<div class="preview" style="display:flex;align-items:center;justify-content:center;opacity:.6">Sem prévia</div>`;
  }
}

function renderCard(f) {
  const url = fileUrl(f.file_url || "");
  return `
    <div class="card">
      <div class="card-header">
        <span class="badge">${iconFor(f)}</span>
        <strong style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${f.name}</strong>
      </div>
      ${renderPreview(f)}
      <div class="card-body">
        <div class="meta">
          <div><strong>Tamanho:</strong> ${formatBytes(f.file_size)}</div>
          <div><strong>Tipo:</strong> ${f.file_type || "—"}</div>
          <div><strong>Dimensões:</strong> ${f.width && f.height ? `${f.width}×${f.height}` : "—"}</div>
          <div><strong>Duração:</strong> ${formatSeconds(f.duration)}</div>
          <div><strong>Páginas:</strong> ${f.pages ?? "—"}</div>
          <div><strong>Categoria:</strong> ${f.category}</div>
        </div>
      </div>
      <div class="card-actions">
        <a class="action" href="${url}" download>Baixar</a>
        <a class="action" href="${url}" target="_blank" rel="noopener">Abrir</a>
      </div>
    </div>
  `;
}

// Init
fetchFiles();