
  // active state for menu buttons
  page_name = window.location.pathname
  if (page_name == '/'){
    document.getElementById('nav-button-index').classList.add('active')
  }else if (page_name.includes('/alldocuments/')){
    document.getElementById('nav-button-alldocuments').classList.add('active')
  }else if (page_name.includes('/mydocuments/')){
    document.getElementById('nav-button-mydocuments').classList.add('active')
  }else if (page_name.includes('/id/users/')){
    document.getElementById('nav-button-users').classList.add('active')
  }else if (page_name.includes('/myclients/')){
    document.getElementById('nav-button-myclients').classList.add('active')
  }
