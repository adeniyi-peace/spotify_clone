$(document).ready( function (){
    $("#artistfollowingform").submit(function(event){
        event.preventDefault()

        const formData = new FormData(this)

        const url = $(this).attr("action")

        $.ajax({
            url:url,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response){
                $(".following").empty
                $(".following").html(response.follow)

                $("#sidebarartist").empty()

                for (let key in response.object) {
                    let temp = `<div class="artist-card">
                                    <a href="/artist-profile/${response.object[key].id}/">
                                        <img src="${response.object[key].image_url}" alt="${response.object[key].artist}" >
                                        
                                        <div class="artist-name">
                                            <h3>${response.object[key].artist}</h3>
                                            <p>artist</p>
                                        </div>
                                    </a>
                                </div>`
                    $("#sidebarartist").append(temp)
                }
            },

            error: function(error) {
                console.error("AJAX Error:", error);
            }
        })
    })
})