document.querySelectorAll('label').forEach((label) => {
  if (label.textContent.trim() === 'Password-based authentication:') {
    label.remove()
  }
})

const pwHt = document.querySelector('#id_usable_password_helptext')
if (pwHt) {
  pwHt.remove()
}

const uPw = document.querySelector('#id_usable_password')
if (uPw) {
  uPw.remove()
}