const inputbox=document.getElementById("inputbox")
const listcontainer=document.getElementById("listcontainer")
function addtask(){
    if(inputbox.value=== ""){
        alert("you must write something")
    }
    else{
        let li=document.createElement("li");
        li.innerHTML= inputbox.value;
        listcontainer.appendChild(li);
        let span=document.createElement("span");
        span.innerHTML= "\u00d7";
        li.appendChild(span);
        }
        inputbox.value = "";
        savedata();
}

listcontainer.addEventListener("click",function(e){
    if(e.target.tagname === "li"){
        e.target.ClassList.toggle("checked");
    }
    else if(e.target.tagname === "span"){
        e.target.ParentElement.remove();
    }
},false);


function savedata(){
    localStorage.setItem("data",listcontainer.innerHTML);
}
function showtask(){
    listcontainer.innerHTML= localStorage.getItem("data")
}
showtask()
