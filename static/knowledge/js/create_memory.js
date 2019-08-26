var create_memory_button = document.getElementsByName("create_memory_button")[0];

create_memory_button.addEventListener("click", function()
{
text = document.getElementsByClassName("textArea")[0].textContent;
if(text =="")
return

tagElements = document.getElementsByClassName("tagSection")[0].getElementsByClassName("tag_text")
tags = []
  for(let i = 0; i<tagElements.length; i++){
  tags.push(tagElements[i].value)
  }

priority = document.getElementsByClassName("priority_section")[0].textContent;
if(priority=="")
    priority=8;

var form = document.createElement("form");
form.method = "POST";
form.action = url_create_memory;
var input = document.createElement("input");
input.value= tags;
input.name="tags"


console.log(tags)
console.log(text)

form.appendChild(input)

 input = document.createElement("input");
input.value= text;
input.name="text"

form.appendChild(input)

 input = document.createElement("input");
input.value= priority;
input.name="priority"

form.appendChild(input)

 input = document.createElement("input");
 input.name="csrfmiddlewaretoken"
input.value= document.getElementsByName("csrfmiddlewaretoken")[0].value;
form.appendChild(input)
form.hidden = true;
document.body.appendChild(form);
form.submit()

});