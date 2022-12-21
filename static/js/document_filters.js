
function filter_documents(){
    const search_value = document.getElementById('documents-search-field').value
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has(`search`)){
      urlParams.delete(`search`)
    }
    urlParams.append('search', search_value)

    window.location.search = urlParams;

}





  