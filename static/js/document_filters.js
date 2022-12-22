
function filter_documents(date){
    const search_value = document.getElementById('documents-search-field').value
    const urlParams = new URLSearchParams('')
    start_date = document.getElementById('documents-search-start-date').value
    end_date = document.getElementById('documents-search-end-date').value

    if (start_date !== '' && end_date !== ''){
      date = `${start_date}+${end_date}`
    }else{
      date = document.getElementById('search-date-select').value
    }
    
    urlParams.set('search', search_value)
    urlParams.set('period', date)
    
    window.location.search = urlParams

}



  