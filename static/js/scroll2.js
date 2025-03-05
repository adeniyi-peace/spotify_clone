
const scrollableContent2 = document.querySelector('.scrollable-content2');
const customScrollbar2 = document.querySelector('.custom-scrollbar2');
const scrollThumb2 = document.querySelector('.scroll-thumb2');
console.log(scrollableContent2.scrollTop2)

function updateScrollThumb2() {
  const scrollPercentage = scrollableContent2.scrollTop / (scrollableContent2.scrollHeight - scrollableContent2.clientHeight);
  scrollThumb2.style.height = `${(scrollableContent2.clientHeight / scrollableContent2.scrollHeight) * customScrollbar2.clientHeight}px`;
  scrollThumb2.style.top = `${scrollPercentage * (customScrollbar2.clientHeight - scrollThumb2.clientHeight)}px`;
}

scrollableContent2.addEventListener('scroll', updateScrollThumb2);
updateScrollThumb2(); // Initial update

// Dragging functionality
let isDragging2 = false;
let startYd = 0;

scrollThumb2.addEventListener('mousedown', (e) => {
  isDragging2 = true;
  startYd = e.clientY - scrollThumb2.offsetTop;
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
});

function handleMouseMove(e) {
  if (!isDragging2) return;
  const newThumbPosition = e.clientY - startYd;
  const maxThumbPosition = customScrollbar2.clientHeight - scrollThumb2.clientHeight;
  const clampedThumbPosition = Math.max(0, Math.min(newThumbPosition, maxThumbPosition));
  scrollThumb2.style.top = `${clampedThumbPosition}px`;
  const scrollPercentage = clampedThumbPosition / maxThumbPosition;
  scrollableContent2.scrollTop = scrollPercentage * (scrollableContent2.scrollHeight - scrollableContent2.clientHeight);
}

function handleMouseUp() {
  isDragging2 = false;
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
}

window.addEventListener('resize',updateScrollThumb2);