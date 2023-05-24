var count = 0;
const content =  document.getElementById('creat_option_zone');
let ident = "";
btndel = document.getElementById("sup");

function AddOptions() {
    var input = document.createElement('INPUT');
    input.setAttribute('type', 'text');
    input.setAttribute('id', 'creat_base_creat_content_zoneadd_options_input_option'+count.toString(10));
    input.setAttribute('class', 'creat_base_creat_content_zoneadd_options_input_option');
    input.setAttribute('placeholder', 'titre de l\'option'+count.toString(10));
    input.setAttribute('required', 'required');
    input.setAttribute("onclick", "printBtnDel(this.id)");
    input.setAttribute('name', "option"+count.toString(10));
    content.appendChild(input);
    count = count + 1;
}

function printBtnDel(id) {
    btndel.style.display = "block";
    ident =  id;
}

function del() {
    content.removeChild(document.getElementById(ident));
    btndel.style.display = "none";
}