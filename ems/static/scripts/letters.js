const divForm = document.querySelector('.div-form')
const buttonClose = divForm.querySelector('.close')
const buttonLetter = document.querySelector('.btn-letter')
buttonLetter.addEventListener('click', () => {
  if (divForm.classList.contains('d-none')) {
    divForm.classList.remove('d-none')
  }
})

buttonClose.addEventListener('click', () => {
  if (!divForm.classList.contains('d-none')) {
    divForm.classList.add('d-none')
  }
})
