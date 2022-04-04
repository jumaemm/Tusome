function modal_show(document){
    let inputBtn = document.getElementById("input_btn");
    let modal_class = document.getElementById("myModal").className.toString();
    console.log(modal_class);
    inputBtn.addEventListener('click', () => {
       // ('#' + modal_class).modal('show');
    })
}