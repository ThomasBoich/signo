    // Infinite scroll
function infi_scroll(target, item){
    console.log('!', target)
  let elem2 = document.querySelector(target);
  console.log(elem2)
  let infScroll = new InfiniteScroll( elem2, {
  // options
  path: '.pagination__next',
  append: item,
  history: false,
  status: '.page-load-status'
});
}