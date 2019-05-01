var deleteButton = document.getElementById('delete_note_button');
document.addEventListener('click', function (event) {
    var confirm = confirm('Are you sure you want to delete?');
    if(!confirm){
        event.preventDefault()
    }
});