const all_btn = document.getElementById("btn-all")
const artist_btn = document.getElementById("btn-artist-alone")
const song_btn = document.getElementById("btn-songs-alone")
const album_btn = document.getElementById("btn-album-alone")

function change_btn_type(type) {
    const clicked_btn = document.getElementById("btn-"+type)
    const all_sections_btn = document.querySelectorAll(".type > button")

    for (const btn of all_sections_btn) {
        if (btn != clicked_btn) {
            btn.style.backgroundColor = "#2e2e2e"
            btn.style.color = "#ffffff"
        }
    }

    clicked_btn.style.backgroundColor = "#ffffff"
    clicked_btn.style.color = "#2e2e2e"
    
}

function change_type(type) {
    const section1 = document.getElementById(type)
    const all_sections = document.querySelectorAll(".all, .artist, .songs-alone, .album-alone")

    for (const section of all_sections) {
        if (section != section1) {
            section.style.display = "none" 
        }
        
    }

    section1.style.display = "block"
    change_btn_type(type)
}


all_btn.addEventListener("click", function(){change_type("all")})
artist_btn.addEventListener("click", function(){change_type("artist-alone")})
song_btn.addEventListener("click", function(){change_type("songs-alone")})
album_btn.addEventListener("click", function(){change_type("album-alone")})