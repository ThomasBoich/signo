// sorting
function filterByField(value) {
  
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('sort')){
    if (urlParams.get('sort').includes(value) & urlParams.get('sort').includes('-')){
      value = urlParams.get('sort').replace('-', '')
    }else if (urlParams.get('sort').includes(value)){
      value = '-' + urlParams.get('sort')
    }
    urlParams.delete('sort')
  }
  urlParams.append('sort', value);
  

  // if (field === 'sort' && urlParams.has('page')){
  //   urlParams.delete('page')
  //   urlParams.append('page', '1')
  // }

  window.location.search = urlParams;
}

function clear_date(){
  document.getElementById('users-search-start-date').value = ''
}

function filter_users(){
    const search_value = document.getElementById('table-search-field').value
    const urlParams = new URLSearchParams('')
    start_date = document.getElementById('users-search-start-date').value
    end_date = document.getElementById('users-search-end-date').value

    user_type_field = document.getElementById('table-search-user-type')
    if (user_type_field){
      urlParams.set('user_type', user_type_field.value)
    }
    console.log(start_date)
    if (start_date !== '' && end_date !== ''){
      date = `${start_date}+${end_date}`
    }else{
      date = document.getElementById('search-date-select').value
    }
    
    urlParams.set('search', search_value)
    urlParams.set('period', date)
    
    window.location.search = urlParams

}



// prefilling search fields
document.addEventListener("DOMContentLoaded", function() {
  fill_user_search_fields()
  highlight_table_header()
})

function highlight_table_header(){
  const urlParams = new URLSearchParams(window.location.search); 
  if (urlParams.get('sort')){

  document.getElementById('th-'+urlParams.get('sort').replace('-', '')).style.color = 'orange'
  }
}

function fill_user_search_fields(){
  
  if(getParameterByName('search') != null){
    document.getElementById('table-search-field').value = getParameterByName('search')
  }

  if(getParameterByName('period') != null){
    period = getParameterByName('period')
    if (['', '7', '30', '60'].includes(period)){
    document.getElementById('search-date-select').value = getParameterByName('period')
    }else{
      document.getElementById('users-search-start-date').value = period.split('+')[0]
      document.getElementById('users-search-end-date').value = period.split('+')[1]
    }
  }

  if (getParameterByName('user_type') != null){
    document.getElementById('table-search-user-type').value = getParameterByName('user_type')
  }

} 

