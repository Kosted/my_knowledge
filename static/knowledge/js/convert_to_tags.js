let textField = document.getElementsByClassName("textArea")[0];
let tagsField = document.getElementsByClassName("tagSection")[0];
let convertTagsField = document.getElementsByClassName("converted_tags")[0];

function updateTagList(){
  console.log("update tag list")
  childNodes = tagsField.getElementsByClassName("tag_text")
  res = []
  for(let i = 0; i<childNodes.length; i++){
  res.push(childNodes[i].value)
  }
  return res
}

function add_tag_in_tags_field(target_button){
  console.log("add tag")
  input_for_new_tag.before(target_button)
  return 
}

function addTagToTagsField(event){

let target_button =event.target;
console.log(target_button)
if (target_button.tagName == 'INPUT'){
  var tag_list = updateTagList()
  if (!(target_button.value in tag_list)){
    while(target_button.className!="tag_block")
          target_button= target_button.parentNode
    add_tag_in_tags_field(target_button)
    if(converted_tags_field.getElementsByClassName("tag_text").length==0)
    converted_tags_field.style.display="none"
  }
//  convertTagsField.removeChild(target_button)
}
}



convertTagsField.addEventListener("click", addTagToTagsField)