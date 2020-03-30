function switchVisibleSafteyTraining(){
  document.getElementById('divSafteyTraining').style.display = 'block';
  document.getElementById('divOther').style.display = 'none';
  document.getElementById('divBespoke').style.display = 'none';
  document.getElementById('divWorkshopSkills').style.display = 'none';
  document.getElementById('divFirstAid').style.display = 'none';
  document.getElementById('divForkliftAndPlant').style.display = 'none';
}

function switchVisibleForkliftAndPlant(){
  document.getElementById('divSafteyTraining').style.display = 'block';
  document.getElementById('divOther').style.display = 'none';
  document.getElementById('divBespoke').style.display = 'none';
  document.getElementById('divWorkshopSkills').style.display = 'none';
  document.getElementById('divFirstAid').style.display = 'none';
  document.getElementById('divForkliftAndPlant').style.display = 'none';
}

function switchVisibleFirstAid(){
  document.getElementById('divFirstAid').style.display = 'block';
  document.getElementById('divOther').style.display = 'none';
  document.getElementById('divBespoke').style.display = 'none';
  document.getElementById('divWorkshopSkills').style.display = 'none';
  document.getElementById('divSafteyTraining').style.display = 'none';
  document.getElementById('divForkliftAndPlant').style.display = 'none';
}

function switchVisibleWorkshopSkills(){
  document.getElementById('divWorkshopSkills').style.display = 'block';
  document.getElementById('divOther').style.display = 'none';
  document.getElementById('divBespoke').style.display = 'none';
  document.getElementById('divSafteytraining').style.display = 'none';
  document.getElementById('divFirstAid').style.display = 'none';
  document.getElementById('divForkliftAndPlant').style.display = 'none';
}

function switchVisibleBespoke(){
  document.getElementById('divBespoke').style.display = 'block';
  document.getElementById('divOther').style.display = 'none';
  document.getElementById('divSafteyTraining').style.display = 'none';
  document.getElementById('divWorkshopSkills').style.display = 'none';
  document.getElementById('divFirstAid').style.display = 'none';
  document.getElementById('divForkliftAndPlant').style.display = 'none';
}

function switchVisibleOther(){
  document.getElementById('divOther').style.display = 'block';
  document.getElementById('divSafteyTraining').style.display = 'none';
  document.getElementById('divBespoke').style.display = 'none';
  document.getElementById('divWorkshopSkills').style.display = 'none';
  document.getElementById('divFirstAid').style.display = 'none';
  document.getElementById('divForkliftAndPlant').style.display = 'none';
}

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