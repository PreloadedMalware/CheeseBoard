function showDeleteAccount() {
    document.getElementById("delete-account").style.display = "block";
    document.getElementById("account-settings").style.display = "none";
    document.getElementById("user-posts-hidden").style.display = "none";
}
function showAccountSettings() {
    document.getElementById("delete-account").style.display = "none";
    document.getElementById("account-settings").style.display = "block";
    document.getElementById("user-posts-hidden").style.display = "none";
}
function showUserPosts() {
    document.getElementById("delete-account").style.display = "none";
    document.getElementById("account-settings").style.display = "none";
    document.getElementById("user-posts-hidden").style.display = "block";
}