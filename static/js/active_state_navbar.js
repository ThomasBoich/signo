
  // active state for menu buttons
  page_name = window.location.pathname
  if (page_name == '/'){
    document.getElementById('nav-button-index').classList.add('active')
  }else if (page_name.includes('/alldocuments/')){
    document.getElementById('nav-button-alldocuments').classList.add('active')
  }else if (page_name.includes('/staff/')){
    document.getElementById('nav-button-staff').classList.add('active')
  }else if (page_name.includes('allclients/')){
    document.getElementById('nav-button-allclients').classList.add('active')
  }else if (page_name.includes('/myclients/')){
    document.getElementById('nav-button-myclients').classList.add('active')
  }else if (page_name.includes('/logs/')){
    document.getElementById('nav-button-logs').classList.add('active')
  }
