  // saving document id to variable
  var document
  $(window).on('click', function(e){
    if ($(e.target).hasClass('dropdown-document-sign-button')){
      document_to_sign_pk = e.target.id.split('-')[1]
    }
  })