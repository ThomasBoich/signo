btn_up = document.getElementById('btn-up')
window.addEventListener("scroll", (event) => {
    let scroll = this.scrollY;
    if (scroll > 400){
        btn_up.hidden = false
    }else{
        btn_up.hidden = true
    }
})
    
$(btn_up).on('click', function(){
    window.scrollTo(0, 0)
})