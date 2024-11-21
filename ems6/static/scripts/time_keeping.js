const formCheck = document.querySelector('form')
const checkIO = document.querySelector('[btn-check]')
const requiredLatitude = 16.0473935
const requiredLongitude = 108.2368985
const tolerance = 0.01

if (checkIO) {
  checkIO.addEventListener('click', () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const {latitude, longitude} = position.coords
        if (Math.abs(latitude - requiredLatitude) <= tolerance && Math.abs(longitude - requiredLongitude) <= tolerance) {
          const inputHidden = formCheck.querySelector('[hidden]')
          const buttonValue = checkIO.value 
          inputHidden.value = buttonValue
          formCheck.submit()
        } else {
          const inputHidden = formCheck.querySelector('[hidden]')
          const buttonValue = checkIO.value 
          inputHidden.value = buttonValue
          formCheck.submit() // Khi nào ấy thì xóa từ dòng 18 đến dòng 21 và bỏ comment dòng 22 đi là được
          // alert('Bạn đang không ở công ty')
        }
      }, (err) => {
        alert('Vui lòng cho phép vị trí để kiểm tra')
      })
    }
  })
}

setInterval(() => {
  const clockElement = document.querySelector('.clock')
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  clockElement.textContent = `${hours}:${minutes}:${seconds}`
}, 1000)
