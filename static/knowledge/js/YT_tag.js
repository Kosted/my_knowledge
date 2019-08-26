
//<div class="tag_block">
//<input type="button" class="tag_text" value="Example TAG">
//    <div class="tag_counter">156</div>
//<img class="close_button" src="{% static '/knowledge/img/delete_icon.png' %}" height = "24px" align="center">
//
//</div>



var convert_button = document.getElementsByName("convert_text_to_tags")[0]

function get_all_existing_tags(){

 let tag_elements = document.getElementsByClassName("converted_tags")[0].getElementsByClassName("tag_text");
// let tag_elements = document.getElementsByClassName("tagSection").getElementsByClassName("tag_text");

 let res = []
 for(let i = 0; i< tag_elements.length; i++)
    res.push(tag_elements[i].value)
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
div_counter.innerText=99

//функция получения колва использования этого тега
return div_block
}

function add_tags_in_tags_field(tags_json){

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
.then(response => console.log('Успех:', add_tags_in_tags_field(JSON.stringify(response))))
.catch(error => console.error('Ошибка:', error))
}


convert_button.addEventListener("click" , convert_text_to_tags)



