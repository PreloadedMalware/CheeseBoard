var isFullHeight = false;
function setGridSize(){
    document.querySelector(".grid").style.width = "100%";
}
function toggleListHeight(button) {
    let parentDiv = $(button).parent().find(".grid");
    parentDiv.toggleClass("list-full-height");
    
    isFullHeight = !isFullHeight;
    document.getElementById("showButton").innerText = isFullHeight ? "Show Less" : "Show More";
}