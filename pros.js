const btn=document.getElementById("images");
btn.addEventListener("click",()=>{
    console.log("click on image");
});
let mode=document.querySelector("#mode");
let currmode="light";
mode.addEventListener("click",()=>{
    if(currmode==="light"){
        currmode="dark";
        document.querySelector("body").style.backgroundColor="#80ed45";
    }else{
        currmode="light";
        document.querySelector("body").style.backgroundColor="#80ed99";
    }
    console.log(currmode);
})