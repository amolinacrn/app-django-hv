const create_files = (str) => document.createElement(str);
const var_files = document.querySelectorAll(".fancy-file");
Array.from(var_files).forEach(async (f) => {
  const label = create_files("label");
  const span_text = create_files("span");
  const span_name = create_files("span");
  const span_button = create_files("span");
  label.htmlFor = f.id;
  span_text.className = "fancy-file__fancy-file-name";
  span_button.className = "fancy-file__fancy-file-button";
  try {
    const response = await fetch("./fjspdf");
    const dafpdf = await response.json();
    var filetupla = Object.entries(dafpdf.file_usuario).length;
    if (filetupla == 0) {
      span_name.innerHTML = f.dataset.empty || "Subir archivo ...";
    } else {
      span_name.innerHTML = f.dataset.empty || dafpdf.file_usuario[0].filepdf;
    }
  } catch (error) {
    console.log(error);
  }
  span_button.innerHTML = f.dataset.button || "";
  label.appendChild(span_text);
  label.appendChild(span_button);
  span_text.appendChild(span_name);
  f.parentNode.appendChild(label);
  span_name.style.width = span_text.clientWidth - 20 + "px";
  f.addEventListener("change", (e) => {
    if (f.files.length == 0) {
      span_name.innerHTML = f.dataset.empty || "Subir archivo ...";
    } else {
      span_name.innerHTML = f.files[0].name;
    }
  });
});

const create_img = (str) => document.createElement(str);
const var_img = document.querySelectorAll(".upload-img");
Array.from(var_img).forEach(async (f) => {
  const label = create_img("label");
  const span_text = create_img("span");
  const span_name = create_img("span");
  const span_button = create_img("span");

  label.htmlFor = f.id;

  span_text.className = "upload-img__upload-img-name";
  span_button.className = "upload-img__upload-img-button";

  try {
    const response = await fetch("./get_phot");
    const dafots = await response.json();
    var estadtupla = Object.entries(dafots.img_usuario).length;
    if (estadtupla == 0) {
      span_name.innerHTML = f.dataset.empty || "Cargue una foto";
    } else {
      span_name.innerHTML = f.dataset.empty || dafots.img_usuario[0].nameimg;
    }
  } catch (error) {
    console.log(error);
  }

  span_button.innerHTML = f.dataset.button || "";

  label.appendChild(span_text);
  label.appendChild(span_button);
  span_text.appendChild(span_name);
  f.parentNode.appendChild(label);

  span_name.style.width = span_text.clientWidth - 20 + "px";

  f.addEventListener("change", async (e) => {
    if (f.files.length == 0) {
      span_name.innerHTML = f.dataset.empty || "Cargar foto";
    } else {
      span_name.innerHTML = f.files[0].name;
    }
  });
});

window.addEventListener("load", async () => {
  await imgFoto();
});

MathJax = {
  tex: {
    inlineMath: [
      ["$", "$"],
      ["\\(", "\\)"],
    ],
  },
  svg: {
    fontCache: "global",
  },
};

