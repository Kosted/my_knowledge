
//<div class="tag_block">
//<input type="button" class="tag_text" value="Example TAG">
//    <div class="tag_counter">156</div>
//<img class="close_button" src="{% static '/knowledge/img/delete_icon.png' %}" height = "24px" align="center">
//
//</div>



var convert_button = document.getElementsByName("convert_text_to_tags")[0]
var converted_tags_field = document.getElementsByClassName("converted_tags")[0]

function get_all_existing_tags(){

 let converted_tag_elements = converted_tags_field.getElementsByClassName("tag_text");
 let existing_tags = document.getElementsByClassName("tagSection")[0].getElementsByClassName("tag_text");

// let converted_tag_elements = document.getElementsByClassName("tagSection").getElementsByClassName("tag_text");

 let res = []
 for(let i = 0; i< converted_tag_elements.length; i++)
    res.push(converted_tag_elements[i].value)
 for(let i = 0; i< existing_tags.length; i++)
    res.push(existing_tags[i].value)
 return res;
}

function create_tag_elem(tag_text){

let div_block = document.createElement("div")
div_block.className = "tag_block"

let input = document.createElement("input")
input.type="button"
input.className="tag_text"

let div_counter = document.createElement("div")
div_counter.className= "tag_counter"

let img = document.createElement("img")
img.className = "close_button"
img.src = delete_icon
img.height = 24
img.align = "center"

let converted_tags = document.getElementsByClassName("converted_tags")[0]
//converted_tags.style.display="block"

div_block.append(input)
div_block.append(div_counter)
div_block.append(img)

input.value=tag_text;
div_counter.innerText=0

get_and_update_single_tag_counter(div_counter, tag_text)
//console.log(div_counter.innerText)

//функция получения колва использования этого тега
return div_block
}

function add_tags_to_converted_tags_field(tags_json){

let div_block = document.createElement("div")
div_block.className = "tag_block"

let input = document.createElement("input")
input.type="button"
input.className="tag_text"

let div_counter = document.createElement("div")
div_counter.className= "tag_counter"

let img = document.createElement("img")
img.className = "close_button"
img.src = delete_icon
img.height = 24
img.align = "center"

console.log(tags_json)
tags_json = JSON.parse(tags_json)

console.log(tags_json)
tags_json=tags_json["tags"]

console.log(tags_json)
let converted_tags = document.getElementsByClassName("converted_tags")[0]
converted_tags.style.display="block"

div_block.append(input)
div_block.append(div_counter)
div_block.append(img)
//temp
for(let i = 0; i <tags_json.length; i++){
input.value=tags_json[i][0]
div_counter.innerText=tags_json[i][1]

let clone_for_add = div_block.cloneNode(deep=true)
converted_tags.append(clone_for_add)
}

return "final"
}


async function convert_text_to_tags(){

//let existing_tags = []

let json_request_data = {
"text": document.getElementsByClassName("textArea")[0].innerText,
"existing_tags": get_all_existing_tags()
}

token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

await fetch(url_convert_text_to_tags, {

  method: 'POST',
  headers: {
          "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
          'Content-Type': 'application/x-www-form-urlencoded',
//          'Content-Type': 'application/json; charset=UTF-8',
    "X-CSRFToken": token,
//    Authorization: "Token "+token
//    "X-CSRFToken": getCookie("csrftoken"),
//    'X-Requested-With': 'XMLHttpRequest'
  },
  'credentials': 'include',
  body: JSON.stringify(json_request_data)
})
.then(res => res.json())
.then(response => console.log('Успех:', add_tags_to_converted_tags_field(JSON.stringify(response))))
.catch(error => console.error('Ошибка:', error))
}


convert_button.addEventListener("click" , convert_text_to_tags)

converted_tags_field.addEventListener("click", function(event){
let target_button = event.target;
if(target_button.className == "close_button"){
        while(target_button.className!="tag_block")

               target_button= target_button.parentNode

    target_button.remove()
    if(converted_tags_field.getElementsByClassName("tag_text").length==0)
    converted_tags_field.style.display="none"
    }
})

async function get_and_update_single_tag_counter(counter_elem, tag_text){

token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
//console.log(url_get_single_tag_counter)
await fetch(url_get_single_tag_counter.replace("null",tag_text), {

  method: 'GET',
  headers: {
    "X-CSRFToken": token,

  },
  'credentials': 'include',

})
.then(res => res.text())
//.then(response => console.log( response))
.then(response => counter_elem.innerText = response)

}

var input_for_new_tag = document.getElementsByName("input_for_new_tag")[0]
var tagSection = document.getElementsByClassName("tagSection")[0];

var global_input_value = ""

function convert_input_for_new_tag(){

if(global_input_value != ""){
//    if(full){
     var new_tag_for_input = create_tag_elem(global_input_value)
    input_for_new_tag.innerText = ""
    input_for_new_tag.before(new_tag_for_input)
    global_input_value = ""
//    }
//    else{
//
//
//    }
}
}

input_for_new_tag.addEventListener("blur", convert_input_for_new_tag)

function update_input_for_new_tag(){
if(global_input_value != ""){
    let input = document.createElement("input")
    input.type="button"
    input.className="tag_text"
    input.value= global_input_value
    editable_div_for_update_tags.replaceWith(input)

    //поиск счетчика для его редактирования
    let counter_field = input.parentNode.getElementsByClassName("tag_counter")[0];
    counter_field.innerText = 0;
    get_and_update_single_tag_counter(counter_field, global_input_value)

    global_input_value=""

}
}



// отлавливание события нажатия клавишь в передовом инпуте
input_for_new_tag.addEventListener("keyup", function(event){
    if(event.key=="," || event.code=="Enter")
      convert_input_for_new_tag()
    else
        global_input_value = input_for_new_tag.innerText
})

// заранее созданный див для замены редактируемого инпута. уже имеет лисенеры
let editable_div_for_update_tags = document.createElement("div")
editable_div_for_update_tags.className="tag_input"
editable_div_for_update_tags.contentEditable=true


//
editable_div_for_update_tags.addEventListener("blur",update_input_for_new_tag)
editable_div_for_update_tags.addEventListener("keyup", function(event){
    if(event.key=="," || event.code=="Enter")
      update_input_for_new_tag()
    else
        global_input_value = editable_div_for_update_tags.innerText
})





//делегирование события клика на область с текущими тегами
tagSection.addEventListener("click", function(event){

    let target_button = event.target;
    console.log(target_button)
    if (target_button.className == "tagSection")
        input_for_new_tag.focus()
    else
    if(target_button.className == "close_button"){
        while(target_button.className!="tag_block")

               target_button= target_button.parentNode

    target_button.remove()
    }
     else
     if(target_button.tagName =="INPUT"){
//    let default_input_value = target_button.value
        global_input_value = target_button.value
        editable_div_for_update_tags.innerText= global_input_value
//    let div = document.createElement("div")
//    div.className="tag_input"
//    div.contentEditable=true

//    div.innerText="67284564sdfasdf";
        target_button.replaceWith(editable_div_for_update_tags);
//    editable_div_for_update_tags.focus()
//    editable_div_for_update_tags.selectionStart = editable_div_for_update_tags.innerText.length
        setCursorToEnd(editable_div_for_update_tags)

//    console.log("text")
    }

    })

function setCursorToEnd(ele){
    var range = document.createRange();
    var sel = window.getSelection();
    range.setStart(ele, 1);
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);
    ele.focus();
  }





