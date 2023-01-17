  // saving document id to variable
  var document
  $(window).on('click', function(e){
    if ($(e.target).hasClass('dropdown-document-action-button')){
      document_pk = e.target.id.split('-')[2]
      console.log(document_pk)
    }
  })