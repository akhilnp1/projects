const droparea=document.getElementById("droparea")
const inputfile=document.getElementById("inputfile")
const imageview=document.getElementById("imgview")

inputfile.addEventListener("change",uploadimg);
 function uploadimg(){
    let imglink=URL.createObjectURL(inputfile.files[0]);
    imageview.style.backgroundImage= `url(${imglink})`;
    imageview.textContent="";
 }
 droparea.addEventListener("dragover",function(e){
    e.preventDefault();
 });
 droparea.addEventListener("drop",function(e){
    e.preventDefault();
    inputfile.files=e.dataTransfer.files;
    uploadimg();
 });

 


