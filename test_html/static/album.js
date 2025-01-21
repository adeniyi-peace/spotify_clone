
const albumImage = document.getElementById('album-image');
const image = document.querySelector('.album-img > img');

window.onload = () => {
    // Create an off-screen canvas
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = image.width;
    canvas.height = image.height;
    context.drawImage(image, 0, 0);
  
    // Get image data
    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const pixels = imageData.data;
  
    // Calculate color frequencies
    const colorCounts = {};
    for (let i = 0; i < pixels.length; i += 4) {
      const r = pixels[i];
      const g = pixels[i + 1];
      const b = pixels[i + 2];
      const colorKey = `rgb(${r},${g},${b})`;
      colorCounts[colorKey] = (colorCounts[colorKey] || 0) + 1;
    }
  
    // Find most frequent color
    let mostFrequentColor = null;
    let maxCount = 0;
    for (const color in colorCounts) {
      if (colorCounts[color] > maxCount) {
        mostFrequentColor = color;
        maxCount = colorCounts[color];
      }
    }
  
    // Set album-image background color
    if (mostFrequentColor) {
      albumImage.style.backgroundColor = mostFrequentColor;
    }
  };