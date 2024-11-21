const formStatus = document.querySelector('[form-status]')
const btnStatus = formStatus.querySelector('button')
btnStatus.addEventListener('click', () => {
  const confirmStatus = confirm('Xác nhận đã xử lý tình trạng này?')
  if (confirmStatus) {
    formStatus.submit()
  }
})