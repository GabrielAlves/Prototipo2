// const API_KEY = "SUA_API_KEY";

const gallery = document.getElementById("gallery");
const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");

uploadBtn.addEventListener("click", async () => {

  const files = fileInput.files;

  if (!files.length) {
    alert("Selecione arquivos");
    return;
  }

  for (const file of files) {

    const formData = new FormData();
    formData.append("file", file);

    try {

      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        // headers: {
        //   "X-API-Key": API_KEY
        // },
        body: formData
      });

      if (!response.ok) {
        throw new Error("Erro upload");
      }

    } catch (err) {
      console.error(err);
      alert(`Erro ao enviar ${file.name}`);
    }
  }

  fileInput.value = "";

  loadFiles();
});

async function loadFiles() {

  gallery.innerHTML = "";

  try {

    const response = await fetch(`${API_BASE}/list`);

    const files = await response.json();

    files.forEach(file => {

      const card = document.createElement("div");
      card.classList.add("card");

      let previewElement;
      const mediaType = (file.file_type || "").toLowerCase();
      console.log("src:", file.file_url);

      if (mediaType.startsWith("image")) {

        previewElement = document.createElement("img");

        previewElement.src = file.file_url;

        previewElement.classList.add("preview");
      }

      else if (mediaType.startsWith("video")) {

        previewElement = document.createElement("video");

        previewElement.src = file.file_url;
        previewElement.preload = "metadata";
        previewElement.controls = true;
        previewElement.muted = false;
        previewElement.defaultMuted = false;
        previewElement.volume = 1;
        previewElement.playsInline = true;
        previewElement.autoplay = false;
        previewElement.load();

        previewElement.classList.add("preview");
      }

      else if (mediaType.startsWith("audio")) {

        previewElement = document.createElement("audio");

        previewElement.src = file.file_url;
        previewElement.preload = "auto";
        previewElement.controls = true;
        previewElement.controlsList = "nodownload";

        previewElement.classList.add("preview", "preview-audio");
      }

      else if (mediaType === "application/pdf") {

        previewElement = document.createElement("iframe");

        previewElement.src = file.file_url;


        previewElement.width = "100%";

        previewElement.height = "500";

        previewElement.classList.add("preview");
      }

      else {

        previewElement = document.createElement("div");

        previewElement.classList.add("preview");

        previewElement.innerHTML = `
          <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            height:100%;
            gap:10px;
            font-size:18px;
          ">
            <div style="font-size:50px;">
              ??
            </div>

            <a
              href="${file.file_url}"
              target="_blank"
            >
              Abrir arquivo
            </a>
          </div>
        `;
      }

      const info = document.createElement("div");

      info.classList.add("file-info");

      const createdAt = file.created_at
        ? new Date(file.created_at).toLocaleString("pt-BR")
        : "Sem data";

      info.innerHTML = `
        <div class="file-name">${file.file_name}</div>
        <div class="file-meta">Tipo: ${file.file_type || "Desconhecido"}</div>
        <div class="file-meta">Enviado em: ${createdAt}</div>
      `;

      const deleteBtn = document.createElement("button");

      deleteBtn.innerText = "Excluir";

      deleteBtn.classList.add("delete-btn");

      deleteBtn.addEventListener("click", () => {
        deleteFile(file.id);
      });

      card.appendChild(previewElement);
      card.appendChild(info);
      card.appendChild(deleteBtn);

      gallery.appendChild(card);

    });

  } catch (err) {

    console.error(err);

  }
}

async function deleteFile(id) {

  if (!confirm("Deseja excluir?")) {
    return;
  }

  try {

    const response = await fetch(`${API_BASE}/delete/${id}`, {
      method: "DELETE"
      // headers: {
      //   "X-API-Key": API_KEY
      // }
    });

    if (!response.ok) {
      console.error(`HTTP Error: ${response.status} - ${response.statusText}`)
      throw new Error("Erro delete");
    }

    loadFiles();

  } catch (err) {

    console.error(err);
    alert("Erro ao excluir");

  }
}

loadFiles();