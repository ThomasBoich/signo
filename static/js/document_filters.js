
function filter_documents(){
    const search_value = document.getElementById('documents-search-field').value
    const signed = document.getElementById('search-signed-status-select').value
    const doc_type = document.getElementById('search-document-type-select').value
    const urlParams = new URLSearchParams('')
    start_date = document.getElementById('documents-search-start-date').value
    end_date = document.getElementById('documents-search-end-date').value

    if (start_date !== '' && end_date !== ''){
      date = `${start_date}+${end_date}`
    }else{
      date = document.getElementById('search-date-select').value
    }
    
    urlParams.set('doc_type', doc_type)
    urlParams.set('signed', signed)
    urlParams.set('search', search_value)
    urlParams.set('period', date)
    
    window.location.search = urlParams

}

// function to check if param exists
function getParameterByName(name, url = window.location.href) {
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// prefilling search fields
document.addEventListener("DOMContentLoaded", function() {
  fill_search_fields()

})

function fill_search_fields(){
  
  if(getParameterByName('search') != null){
    document.getElementById('documents-search-field').value = getParameterByName('search')
  }

  if(getParameterByName('doc_type') != null){
    document.getElementById('search-document-type-select').value = getParameterByName('doc_type')
    console.log(getParameterByName('doc_type'))
  }

  if(getParameterByName('period') != null){
    period = getParameterByName('period')
    if (['', '7', '30', '60'].includes(period)){
    document.getElementById('search-date-select').value = getParameterByName('period')
    }else{
      document.getElementById('documents-search-start-date').value = period.split('+')[0]
      document.getElementById('documents-search-end-date').value = period.split('+')[1]
    }
  }

  if(getParameterByName('signed') != null){
    console.log('!here')
    document.getElementById('search-signed-status-select').value = getParameterByName('signed')
  }
} 

