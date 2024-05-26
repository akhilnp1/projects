let result=document.getElementById("result");

function appendvalue(value){
    result.value +=value;
}
function calculate(){
    try{
        result.value=eval(result.value);
    }catch(error){
        result.value="Error";
    }
}
function clearresult(){
    result.value="";

}
function deletechar(){
    result.value=result.value.slice(0,-1);
}
