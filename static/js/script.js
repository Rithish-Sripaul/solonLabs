let shortDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
let datetime = document.getElementById("date");
let time_ = document.getElementById("time");

function updateTime() {
  let now = new Date();
  let day = now.getDay();
  datetime.textContent = `${shortDays[day]} - ${now.getDate()}/${
    now.getMonth() + 1
  }/${now.getFullYear() % 2000}`;
  if (now.getHours() >= 12) {
    time_.textContent = `${now.getHours() % 12}:${now.getMinutes()} PM`;
  } else {
    time_.textContent = `${now.getHours() % 12}:${now.getMinutes()} AM`;
  }
}

setInterval(updateTime, 1000);

// Getting the uploaded image
function upload() {
  const fileUploadInput = document.querySelector(".file-uploader");
  const image = fileUploadInput.files[0];

  const fileReader = new FileReader();
  fileReader.readAsDataURL(image);
  fileReader.onload = (fileReaderEvent) => {
    const scanImage = document.querySelector(".scanImage");
    scanImage.style.backgroundImage = `url(${fileReaderEvent.target.result})`;
  };
}

let download = document.querySelector(".download");
download.addEventListener("click", downloadPDF);
function downloadPDF() {
  let element = document.getElementById("element-to-print");
  let patientId = document.querySelector(".patientId");
  let patientName = document.querySelector(".patientName");
  let opt = {
    margin: 0,
    filename: `${patientId.textContent}_${patientName.textContent}.pdf`,
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
  };
  html2pdf().from(element).set(opt).save();
}
