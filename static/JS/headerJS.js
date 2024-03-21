function search() {
    let search = document.getElementById("mainSearch").value;
    let encodedSearchTerm = encodeURIComponent(search);
    
    window.location.href = "/search/" + encodedSearchTerm;
}