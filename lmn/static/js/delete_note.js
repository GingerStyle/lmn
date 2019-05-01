var deleteButton = document.getElementById('delete_note_button');
if(deleteButton){
   deleteButton.addEventListener('click', function (event) {
    let confirmation = confirm('Are you sure you want to delete?');
    if(!confirmation){
        event.preventDefault();
    }
});
}
