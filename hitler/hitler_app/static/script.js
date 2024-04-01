function isValidLink(link){
    if (link.includes("https://en.wikipedia.org/wiki/")){
        return true
    }
    return false
}

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? decodeURIComponent(cookieValue[2]) : null;
}

const button = document.getElementsByClassName("send-button")[0]
const label = document.getElementsByClassName("text-label")[0]
const table = document.getElementsByClassName("result-table")[0]

button.addEventListener("click", async () => {
    const link_input = document.getElementsByClassName("link-input")[0]
    const checkbox_input = document.getElementsByClassName("database-input")[0]

    const link = link_input.value
    const isActive = checkbox_input.checked

    if (!isValidLink(link)) {
        alert("Link isn`t valid")
        return
    }
    label.innerHTML = "Waiting for result..."
    button.value = "Waiting..."
    button.disabled = true
    let request = {
        "link": link,
        "isDB": isActive,
    }
    const csrftoken = getCookie('csrftoken');

    const response = await fetch('/heil', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(request)
    });

    jsonData = await response.json()
    
    button.disabled = false
    button.value = "Try another"
    console.log(jsonData)

    path = jsonData.path
    el_time = jsonData.elapsed_time
    label.innerHTML = `Elapsed time ${el_time - el_time%0.01}s`

    var rowCount = table.rows.length;
    for (var i = rowCount - 1; i >= 0; i--) {
        table.deleteRow(i);
    }

    for (var i = 0;i < path.length; i++){
        var row = table.insertRow()
        var cell = row.insertCell(0)
        cell.innerHTML = path[i] 
    }

})