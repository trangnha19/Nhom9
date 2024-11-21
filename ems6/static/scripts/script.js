const xIcon = document.querySelector('[x-icon]')
if (xIcon) {
  const alertDiv = document.querySelector('[mess-div]')
  xIcon.addEventListener('click', () => {
    alertDiv.remove()
  })
  setTimeout (() => {
    alertDiv.remove()
  }, 5000)
}