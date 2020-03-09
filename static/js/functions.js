function switchVisibleHGV(){
    document.getElementById('divOffshore').style.display = 'none';
    document.getElementById('divHGV').style.display = 'block';
}

function switchVisibleOffshore(){
    document.getElementById('divHGV').style.display = 'none';
    document.getElementById('divOffshore').style.display = 'block';
}

function searchCourses(){
    
    // document.getElementById('divHGV').style.display = 'none';
    // document.getElementById('divOffshore').style.display = 'none';

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