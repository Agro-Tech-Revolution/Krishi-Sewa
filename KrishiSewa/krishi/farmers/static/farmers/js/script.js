"use strict";

// ---------- This part is for Image testing-------------------------------*//

const dropArea = document.querySelector(".drag-area"),
  dragText = dropArea.querySelector("header"),
  button = dropArea.querySelector("button"),
  input = dropArea.querySelector("input");

let file;

button.onclick = () => {
  input.click(); //
};

input.addEventListener("change", function () {
  file = this.files[0];
  dropArea.classList.add("active");
  showFile();
});

//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
  event.preventDefault(); // preventing from default behaviors
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload Files";
});

//If user leave dragged file frim DropArea
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop Your Soil image";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
  event.preventDefault(); // preventing from default behaviors
  file = event.dataTransfer.files[0]; // making user select file
  showFile();
});

function showFile() {
  let fileType = file.type;
  let validExtensions = ["image/png", "image/jpg", "image/jpeg"]; //adding some valid image extensions in array
  if (validExtensions.includes(fileType)) {
    //if user selects image file
    let fileReader = new FileReader(); //creating new FileReader Object
    fileReader.onload = () => {
      let fileURL = fileReader.result; // passing user file source in fileURL variable
      // console.log(fileURL);
      let imgTag = `<img src="${fileURL}" alt="">`; //creating an img tag and passing user selected file source insidee src attribute
      dropArea.innerHTML = imgTag; // addding that created img tag inside dropArea container
    };
    fileReader.readAsDataURL(file);
  } else {
    alert("This is not an image file!");
    dropArea.classList.remove("active");
    dragText.textContent = "Release to Upload Files";
  }
}
