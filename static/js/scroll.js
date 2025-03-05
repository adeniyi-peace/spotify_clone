// script.js
const scrollableContent = document.querySelector('.scrollable-content');
const customScrollbar = document.querySelector('.custom-scrollbar');
const scrollThumb = document.querySelector('.scroll-thumb');
console.log(scrollableContent.scrollTop)

function updateScrollThumb() {
  const scrollPercentage = scrollableContent.scrollTop / (scrollableContent.scrollHeight - scrollableContent.clientHeight);
  scrollThumb.style.height = `${(scrollableContent.clientHeight / scrollableContent.scrollHeight) * customScrollbar.clientHeight}px`;
  scrollThumb.style.top = `${scrollPercentage * (customScrollbar.clientHeight - scrollThumb.clientHeight)}px`;
}

scrollableContent.addEventListener('scroll', updateScrollThumb);
updateScrollThumb(); // Initial update

// Dragging functionality
let isDragging = false;
let startY = 0;

scrollThumb.addEventListener('mousedown', (e) => {
  isDragging = true;
  startY = e.clientY - scrollThumb.offsetTop;
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
});

function handleMouseMove(e) {
  if (!isDragging) return;
  const newThumbPosition = e.clientY - startY;
  const maxThumbPosition = customScrollbar.clientHeight - scrollThumb.clientHeight;
  const clampedThumbPosition = Math.max(0, Math.min(newThumbPosition, maxThumbPosition));
  scrollThumb.style.top = `${clampedThumbPosition}px`;
  const scrollPercentage = clampedThumbPosition / maxThumbPosition;
  scrollableContent.scrollTop = scrollPercentage * (scrollableContent.scrollHeight - scrollableContent.clientHeight);
}

function handleMouseUp() {
  isDragging = false;
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
}

window.addEventListener('resize',updateScrollThumb);