const button = document.getElementById("button")
const back_button = document.getElementById("back-button")

function change_stage() {
    const stage1 = document.getElementById("email")
    const stage2 = document.getElementById("password")
    const stage3 = document.getElementById("user-details")
    const stage4 = document.getElementById("tandc")
    const stageHeader = document.getElementById("stage_header")
    const progress = document.getElementById("progress-bar")

    if (stage1.style.display != "none") {
        stage1.style.display = "none"
        stage2.style.display = "block"
        stageHeader.style.display = "block"
        document.getElementById("first").style.display = "none"
        document.getElementById("progress").style.display = "block"
        back_button.style.display = "block"
    }
    
    else if (stage2.style.display == "block") {
        stage2.style.display = "none"
        stage3.style.display = "block"
        stageHeader.innerHTML = "<p>Step 2 of 3</p> <h3>Tell us about yourself</h3>"
        progress.style.width = "66.6667%"
    }

    else if(stage3.style.display == "block") {
        stage3.style.display = "none"
        stage4.style.display = "block"
        stageHeader.innerHTML = "<p>Step 3 of 3</p> <h3>Terms & Conditions</h3>"
        progress.style.width = "100%"
        button.innerHTML = "Sign up"
    }

    else if(stage4.style.display == "block") {
        button.type = "submit"
    }
}

function change_stage_reverse() {
    const stage1 = document.getElementById("email")
    const stage2 = document.getElementById("password")
    const stage3 = document.getElementById("user-details")
    const stage4 = document.getElementById("tandc")
    const stageHeader = document.getElementById("stage_header")
    const progress = document.getElementById("progress-bar")

    if(stage4.style.display == "block") {
        stage4.style.display = "none"
        stage3.style.display = "block"
        stageHeader.innerHTML = "<p>Step 2 of 3</p> <h3>Tell us about yourself</h3>"
        progress.style.width = "66.6667%"
        button.type = "button"
        button.innerHTML = "Next"
    }

    else if(stage3.style.display == "block") {
        stage3.style.display = "none"
        stage2.style.display = "block"
        stageHeader.innerHTML = "<p>Step 1 of 3</p> <h3>Create a password</h3>"
        progress.style.width = "33.3333%"
    }

    else if (stage2.style.display == "block") {
        stage2.style.display = "none"
        stage1.style.display = "block"
        stageHeader.style.display = "none"
        document.getElementById("first").style.display = "block"
        document.getElementById("progress").style.display = "none"
        back_button.style.display = "none"
    }
}

button.addEventListener("click", change_stage)
back_button.addEventListener("click", change_stage_reverse)