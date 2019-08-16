let textField = document.getElementsByClassName("textArea")[0];
let tagsField = document.getElementsByClassName("tagSection")[0];
let convertTagsField = document.getElementsByClassName("converted_tags")[0];

function updateTagList(){
  console.log("update tag list")
  return ["tag1", "tag2"]
}

function add_tag_in_tags_field(){
  console.log("add tag")
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