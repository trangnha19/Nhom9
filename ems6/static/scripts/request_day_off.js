const formRequest = document.querySelector('.form-request')
formRequest.querySelectorAll('label').forEach((label) => {
  label.classList.add('label-request')
})

const selectStartDate = document.querySelector('#id_start_date')
const selectEndDate = document.querySelector('#id_end_date')
const maxEndDate = formRequest.getAttribute('max_end_date')

const today = new Date();
const formattedToday = today.toISOString().split('T')[0];

let minStartDate = formattedToday
if (maxEndDate && maxEndDate > minStartDate) { 
  minStartDate = maxEndDate
}

selectStartDate.min = minStartDate
selectEndDate.min = minStartDate

selectStartDate.addEventListener('change', () => {
  const startDateValue = selectStartDate.value;
  if (startDateValue) {
    const startDate = new Date(startDateValue);
    const endDateMinValue = new Date(startDate);
    endDateMinValue.setDate(endDateMinValue.getDate());
    const formattedEndDateMin = endDateMinValue.toISOString().split('T')[0];
    selectEndDate.min = formattedEndDateMin;
    if (new Date(selectEndDate.value) < new Date(startDateValue)) {
      selectEndDate.value = '';
    }
  }
});
