const salaryTable = document.querySelector('.table-salary')
const selectExport = document.querySelector('#select-export')
const salaryMonth = document.querySelector('#select-month').value
const salaryYear = document.querySelector('#select-year').value
const salaryDpm = document.querySelector('#select-dpm').value
const currentDateTimeISO = new Date().toISOString();

selectExport.addEventListener('change', () => {
  if (salaryTable.querySelectorAll('td').length === 0) {
    alert('Không có dữ liệu để xuất file')
    selectExport.selectedIndex = 0
    return 
  } else {
    const confirmExport = confirm("Bạn muốn xuất file bảng lương chứ?")
    if (confirmExport) {
      const slugDpm = (str) => {
        return str
          .toLowerCase()                 
          .normalize('NFD').replace(/[\u0300-\u036f]/g, '') 
          .replace(/[^a-z0-9\s-]/g, '')              
          .trim()                                   
          .replace(/\s+/g, '-')                     
          .replace(/-+/g, '-');     
      }
      let fileName = `${slugDpm(salaryDpm)}_month-${salaryMonth}_year-${salaryYear}_export_time_${currentDateTimeISO}`

      if (selectExport.value === 'csv') {
        let csvContent = ""
        const rowTables = salaryTable.querySelectorAll('tr')
    
        rowTables.forEach((row, index) => {
          const cellRows = row.querySelectorAll('th, td')
          let rowData = []
    
          cellRows.forEach((cell) => {
            rowData.push(cell.textContent.trim())
          })
    
          csvContent += rowData.join(',') + (index < rowTables.length - 1 ? '\n' : '')
        })
    
        const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
    
        a.href = url
        a.download = `${fileName}.csv`
        a.click()    
        URL.revokeObjectURL(url)

      } else if (selectExport.value === 'json') {
        let jsonData = []
        const rowTables = salaryTable.querySelectorAll('tr')

        rowTables.forEach((row, index) => {
          if (index === 0) return 
          const cellRows = row.querySelectorAll('td')
          let rowData = {}
      
          cellRows.forEach((cell, idx) => {
            const header = salaryTable.querySelectorAll('th')[idx].textContent.trim()
            rowData[header] = cell.textContent.trim()
          })
      
          jsonData.push(rowData)
        })

        const jsonBlob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(jsonBlob)
        const a = document.createElement('a')
      
        a.href = url
        a.download = `${fileName}.json`
        a.click()     
        URL.revokeObjectURL(url)

      } else {
        let textContent = ""
        const rowTables = salaryTable.querySelectorAll('tr')

        rowTables.forEach((row) => {
          const cellRows = row.querySelectorAll('th, td')
          let rowData = []
      
          cellRows.forEach((cell) => {
            rowData.push(cell.textContent.trim())
          })
      
          textContent += rowData.join('\t') + '\n'
        })

        const textBlob = new Blob([textContent], { type: 'text/plain' })
        const url = URL.createObjectURL(textBlob)
        const a = document.createElement('a')
      
        a.href = url
        a.download = `${fileName}.txt`
        a.click()     
        URL.revokeObjectURL(url)

      }
    }
    selectExport.selectedIndex = 0
  }
})