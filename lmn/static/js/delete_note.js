$("#delete_note_button").click(function(event){
    var confirm = confirm('Are you sure you want to delete?')
    if(!confirm){
        event.preventDefault()
    }
}
);