    // Infinite scroll
function infi_scroll(target, item){
  let elem2 = document.querySelector(target);
  let infScroll = new InfiniteScroll( elem2, {
  // options
  path: '.pagination__next',
  append: item,
  history: false,
  status: '.page-load-status'
});
}