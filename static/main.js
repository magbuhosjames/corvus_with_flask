var listen_btn = document.getElementsByClassName("listen_btn")[0]

var listen_form_btn = document.getElementById("listen_form_btn")
var listen_form_text = document.getElementById("listen_form_text")





console.log(listening)

if (listening == true) {
    listen_btn.innerText = "Stop listening";
    listen_btn.classList.add("listen_btn_stop")
}



listen_btn.addEventListener("click", function () {
    listen_form_text.value = listen_btn.innerText;
    listen_form_btn.click()
    if (listen_btn.innerText == "Start listening") {
        listen_btn.innerText = "Stop listening";
        listen_btn.classList.add("listen_btn_stop")
    } else {
        listen_btn.innerText = "Start listening";
        listen_btn.classList.remove("listen_btn_stop")
    }
})