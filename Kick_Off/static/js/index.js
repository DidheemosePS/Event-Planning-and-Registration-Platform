const toggle_slider = () => {
    const toggle_slider = document.getElementById("toggle_slider");
    const slider = document.getElementById("slider");
    if (slider.style.top === "-100dvh" || slider.style.top === "") {
        slider.style.top = "4rem";
        toggle_slider.style.color = "rgb(223, 62, 62)";
        toggle_slider.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16"><path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" /></svg >'
    } else {
        slider.style.top = "-100dvh";
        toggle_slider.style.color = "black";
        toggle_slider.innerHTML = '<svg xmlns = "http://www.w3.org/2000/svg" width = "25" height = "25" fill = "currentColor" class="bi bi-list" viewBox = "0 0 16 16"><path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/></svg >'
    }
}