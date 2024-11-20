document.querySelectorAll('.helptext').forEach((ht) => {
  ht.remove()
})
const passwordSignUp = document.querySelector('#id_usable_password')
if (passwordSignUp) {
  passwordSignUp.remove()
}

const pTags = document.querySelectorAll('p')
if (pTags.length > 8) {
  pTags[7].remove()
}
