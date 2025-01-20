const image = document.getElementById("album-image")
const img_bg = document.querySelector(".album-image > img")

image.onload = () =>{
    // create off screen canvas
    const canvas = document.createElemen("canvas")
    const context = canvas.getContext("2d")
    canvas.width = image.width
    canvas.height = image.height
    context.drawImage(image, 0, 0)

    // get image data
    const image_data = context.getImageData(0,0,canvas.width,canvas.height)
    const pixels = image_data.data

    // ccalculate color frequency
    const colour_count = {}
    for (let i = 0; i < pixels.length; i++) {
        const r = pixels[i]
        const g = pixels[i + 1]
        const b = pixels[i + 2]
        const color_key = "rgb($(r),$(g),$(b))"
        colour_count[color_key] = (colour_count[color_key] || 0) + 1  
    }


    // find most frequent color
    let most_frequent_color = null
    let max_count = 0
    for (const colour in colour_count) {
        if(colour_count[colour] > max_count) {
            most_frequent_color = colour
            max_count = colour_count[colour]
        }
    }

    if (most_frequent_color) {
        img_bg.style.backgroundColor = most_frequent_color
    }
}