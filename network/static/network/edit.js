

function save_edit(id){
    
    fetch(`/edit/${id}`)
.then(response => response.json())
.then(post => {
    // Print email
    cardbody = document.querySelector(`#card-body-${id}`);
    cardbody.innerHTML = `<form id="editform-${post.id}"><div class="form-group"><label for="textarea">Edit your post:</label>
    <textarea class="form-control" id="textarea-${post.id}" rows="5">${post.txt}</textarea><br><button class="btn btn-primary" type="submit">Save</button></form>`;
    // ... do something else with email ...
    const form = document.querySelector(`#editform-${post.id}`);
    form.onsubmit = () => {
        const textarea = document.querySelector(`#textarea-${post.id}`).value;
        console.log(textarea)
        fetch(`/edit/${post.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                txt: textarea,
                usr: post.usr
                
            })
          })
        showcontent(`${post.id}`);
        return false;
    }
});
}

function showcontent(id){
   
    cardbody = document.querySelector(`#card-body-${id}`);
    fetch(`/edit/${id}`)
.then(response => response.json())
.then(post => {
    // Print email
     cardbody.innerHTML = `<p>${post.txt}</p>`;
    // ... do something else with email ...
});
}

function like(id1,usrn){

   fetch(`/likedby/${id1}/${usrn}`)
.then(response => response.json())
.then(likepost => {
      lik=document.querySelector(`lik-${id1}`)
    
        fetch(`/likedby/${id1}/${usrn}`, {
            method: 'POST',
            body: JSON.stringify({
                by:usrn,
                pid:id1
                
            })
          })
         showcontent1(id1,usrn);
        return false;

        
        
    });
}
function showcontent1(id1,usrn){
    v=1
    lik=document.querySelector(`#lik-${id1}`)

    fetch(`/likedby/${id1}/${usrn}`)
.then(response => response.json())
.then(likepost => {
     for(i=0;i<likepost.length;i++){
      v=v+1;
     }
     lik.innerHTML = `${v}<br> <button id="ulk-${ id1 }" >❤️</button>`;
     rev=document.querySelector(`#lk-${id1}`)
     if(rev !=null){
      rev.style.display="none";
     }
     ukl=document.querySelector(`#ulk-${id1}`)
     ukl.onclick=() =>{
      unlike(id1,usrn)
     } 
   });
    
}





function unlike(id2,usrn2){
  
   fetch(`/unlike/${id2}/${usrn2}`)
.then(response => response.json())
.then(likepost1 => {
      lik=document.querySelector(`lik-${id2}`)
    
        fetch(`/unlike/${id2}/${usrn2}`, {
            method: 'DELETE',
            body: JSON.stringify({
                by:usrn2,
                pid:id2
                
            })
          })
         showcontent2(id2,usrn2);
        return false;

        
        
    });
}
function showcontent2(id2,usrn2){
    v=0
    lik=document.querySelector(`#lik-${id2}`)

    fetch(`/unlike/${id2}/${usrn2}`)
.then(response => response.json())
.then(likepost1 => {
     for(i=0;i<likepost1.length;i++){
      v=v+1;
     }
     lik.innerHTML = `${v} <br><button id="lk-${id2}">🤍</button>`;
     rev1=document.querySelector(`#ulk-${id2}`)
     if(rev1 !=null){
      rev1.style.display="none";
     }
     lkl=document.querySelector(`#lk-${id2}`)
     lkl.onclick=()=>{
      like(id2,usrn2)
     }
   });
    
}




