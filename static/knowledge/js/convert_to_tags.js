let textField = document.getElementsByClassName("textArea")[0];

function get_exist_tags_list(){
//  console.log("update tag list")
  childNodes = tagSection.getElementsByClassName("tag_text")
  res = []
  for(let i = 0; i<childNodes.length; i++){
  res.push(childNodes[i].value)
  }
  return res
}

function add_tag_in_tags_field(target){
//  console.log("add tag")
  input_for_new_tag.before(target)
  return 
}

function transfer_tags_from_convert_field_to_tagSection(event){

let target = event.target;
console.log(target)
if (target.tagName == 'INPUT'){
  var tag_list = get_exist_tags_list()
  if (!(target.value in tag_list)){
    while(target.className!="tag_block")
          target= target.parentNode
    add_tag_in_tags_field(target)
    if(converted_tags_field.getElementsByClassName("tag_text").length==0)
        converted_tags_field.style.display="none"
  }
//  convertTagsField.removeChild(target)
}
}



converted_tags_field.addEventListener("click", transfer_tags_from_convert_field_to_tagSection)