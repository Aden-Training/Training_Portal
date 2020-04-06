// Resizes navigation bar if screen is less that 600px
function navbarChange(){
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav"){
    x.className += " responsive";
  }else{
    x.className = "topnav";
  }
}

// Search bar for courses
function searchCourses(){
    let search = document.getElementById('searchBar').value
    search = search.toLowerCase();
    let x = document.getElementsByClassName('card')
    let y = document.getElementsByClassName('card-title');

    for(i = 0; i < x.length; i++){
        if(!y[i].innerHTML.toLowerCase().includes(search)){
            x[i].style.display="none";
        }else{
            x[i].style.display="inline-block";
        }
    }
}

// function showSubCatSaftey(){
//   document.getElementById('divSubCatSafety').style.display = 'block';
//   document.getElementById('divSubCatWorkshop').style.display = 'none';
// }

// function showSubCatWorkshop(){
//   document.getElementById('divSubCatSafety').style.display = 'none';
//   document.getElementById('divSubCatWorkshop').style.display = 'block';
// }