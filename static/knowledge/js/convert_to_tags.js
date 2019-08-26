let textField = document.getElementsByClassName("textArea")[0];
let tagsField = document.getElementsByClassName("tagSection")[0];
let convertTagsField = document.getElementsByClassName("converted_tags")[0];

function updateTagList(){
  console.log("update tag list")
  childNodes = tagsField.getElementsByClassName("tag_text")
  res = []
  for(let i = 0; i<childNodes; i++){
  res.push(childNodes[i].value)
  }
  return res
}

function add_tag_in_tags_field(){
  console.log("add tag")
//  input_for_new_tag.before(target_button)
  return 
}

function addTagToTagsField(event){

let target_button =event.target;
console.log(target_button)
if (target_button.tagName == 'INPUT'){
  var tag_list = updateTagList()
  if (!(target_button.value in tag_list)){
    add_tag_in_tags_field()
  }
  convertTagsField.removeChild(target_button)
}
}



convertTagsField.addEventListener("click", addTagToTagsField)