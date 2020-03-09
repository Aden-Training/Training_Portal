function switchVisibleHGV(){
    document.getElementById('divOffshore').style.display = 'none';
    document.getElementById('divHGV').style.display = 'block';
}

function switchVisibleOffshore(){
    document.getElementById('divHGV').style.display = 'none';
    document.getElementById('divOffshore').style.display = 'block';
}

// Resizes navigation bar if screen is less that 600px
function navbarChange()
{
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") 
  {
    x.className += " responsive";
  } 
  else
  {
    x.className = "topnav";
  }
}