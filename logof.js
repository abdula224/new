const button=document.getElementById("submit");
button.addEventListener("click",(e)=>{
    e.preventDefault();
    console.log("submitted");
    alert("your response has been submitted");
});


