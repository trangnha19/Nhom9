// Mở form
document.getElementById("open-form").addEventListener("click", function () {
  document.getElementById("form-container").classList.remove("d-none");
  this.style.display = "none";
});

// Đóng form
document.getElementById("close-form").addEventListener("click", function () {
  document.getElementById("form-container").classList.add("d-none");
  document.getElementById("open-form").style.display = "inline-block";
});