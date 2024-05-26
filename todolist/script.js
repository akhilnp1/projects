

const inputbox = document.getElementById("inputbox");
const listcontainer = document.getElementById("listcontainer");

function addtask() {
    if (inputbox.value === "") {
        alert("You must write something");
    } else {
        let li = document.createElement("li");
        li.innerHTML = inputbox.value;
        listcontainer.appendChild(li);
        let span = document.createElement("span");
        span.innerHTML = "\u00d7";
        li.appendChild(span);
    }
    inputbox.value = "";
    savedata();
}

listcontainer.addEventListener("click", function(e) {
    if (e.target.tagName === "LI") {
        e.target.classList.toggle("checked");
    } else if (e.target.tagName === "SPAN") {
        e.target.parentElement.remove();
        savedata(); // Ensure data is saved after removing an item
    }
}, false);

function savedata() {
    localStorage.setItem("data", listcontainer.innerHTML);
}

function showtask() {
    let savedData = localStorage.getItem("data");
    if (savedData) {
        listcontainer.innerHTML = savedData;
    }
}

showtask();
