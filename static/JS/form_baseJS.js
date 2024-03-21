function displayError(){
    try {
        alert(document.getElementsByClassName("errorlist nonfield").item(0).childNodes.item(0).firstChild.nodeValue);
    } catch (e) {
    }
}