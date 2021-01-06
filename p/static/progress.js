const intervalAction = () => {
    $.get(
        "/progress",
        (data) => {
            if (data.progress === 100) {
                clearInterval(myInterval);
                document.getElementById('change-view').submit()
            }
            const done = document.getElementById("done");
            done.style.width = data.progress + "%";
        }
    )
}

var myInterval = setInterval(intervalAction, 10)