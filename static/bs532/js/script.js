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


const createEl = (tag) => document.createElement(tag);

const inputs = document.querySelectorAll(".upload-img");

let imgUsuario = null; // guardamos la respuesta una sola vez

// 🔥 1 sola petición al servidor
async function cargarImagenServidor() {
  try {
    const response = await fetch("");
    console.log(response);
    const data = await response.json();
    imgUsuario = data.img_usuario || [];
  } catch (error) {
    console.error("Error cargando imagen:", error);
    imgUsuario = [];
  }
}

function crearUIInputFile(f) {
  const label = createEl("label");
  const spanText = createEl("span");
  const spanName = createEl("span");
  const spanButton = createEl("span");

  label.htmlFor = f.id;

  spanText.className = "upload-img__upload-img-name";
  spanButton.className = "upload-img__upload-img-button";

  // 🔹 Texto inicial
  if (imgUsuario.length === 0) {
    spanName.textContent = f.dataset.empty || "Cargue una foto";
  } else {
    spanName.textContent = imgUsuario[0].nameimg;
  }

  spanButton.textContent = f.dataset.button || "Subir";

  spanText.appendChild(spanName);
  label.appendChild(spanText);
  label.appendChild(spanButton);
  f.parentNode.appendChild(label);

  // 🔹 Ajustar ancho correctamente cuando el DOM ya pintó
  requestAnimationFrame(() => {
    spanName.style.width = spanText.clientWidth - 20 + "px";
  });

  // 🔹 Evento cambio de archivo
  f.addEventListener("change", () => {
    spanName.textContent = f.files.length
      ? f.files[0].name
      : (f.dataset.empty || "Cargar foto");
  });
}

// // 🚀 Flujo principal
// (async () => {
//   await cargarImagenServidor(); // solo una vez
//   inputs.forEach(crearUIInputFile);
// })();




// const imgFoto = async () => {
//   var idimgfot = document.getElementById("idimgfot");
//   var fotomodal = document.getElementById("fotomodal");

//   try {
//     const response = await fetch("./get_phot");
//     const datsfots = await response.json();

//     var estadtupla = Object.entries(datsfots.img_usuario).length;

//     if (estadtupla == 0) {
//       idimgfot.innerHTML = `<img class="clsimg" src='/static/bs532/img/einstein_883032.png' style="position: relative; width: 100%;" alt="My image">`;
//       fotomodal.innerHTML = `<img  src='/static/bs532/img/einstein_883032.png' style="position: relative;  width: 10cm; height:10cm;transform: scale(1)"" alt="My image">`;
//     } else {
//       idimgfot.innerHTML = `<img src='/media/${datsfots.img_usuario[0].fotoperfil}'
//                             class="clsimg my_img_html" style="width: 100%;  ;" alt="My image">`;
//       fotomodal.innerHTML = `<img src='/media/${datsfots.img_usuario[0].fotoperfil}'
//                             class="clsimg my_img_html" style="width: 10cm; height:10cm;transform: scale(1)" alt="My image">`;
//     }
//   } catch (error) {
//     console.log(error);
//   }
// };

// window.addEventListener("load", async () => {
//   await imgFoto();
// });

// MathJax = {
//   tex: {
//     inlineMath: [
//       ["$", "$"],
//       ["\\(", "\\)"],
//     ],
//   },
//   svg: {
//     fontCache: "global",
//   },
// };
