function filter_logs(){
    const search_value = document.getElementById('table-search-field').value
    
    const urlParams = new URLSearchParams('')
    start_date = document.getElementById('search-start-date').value
    end_date = document.getElementById('search-end-date').value
    if (start_date !== '' && end_date !== ''){
      date = `${start_date}+${end_date}`
      urlParams.set('period', date)
    }
    
    urlParams.set('search', search_value)
    
    window.location.search = urlParams

}



// prefilling search fields
document.addEventListener("DOMContentLoaded", function() {
  fill_search_fields()

})

function fill_search_fields(){
  
  if(getParameterByName('search') != null){
    document.getElementById('table-search-field').value = getParameterByName('search')
  }

  if(getParameterByName('period') != null){
    period = getParameterByName('period')
    
    // we don't have a way to reset date here rather than manually delete field value
    // document.getElementById('search-start-date').value = period.split('+')[0]
    document.getElementById('search-end-date').value = period.split('+')[1]
    }
  }


