'use strict'
function getLocation(){
    if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(
            (position)=> {
                document.getElementById('latitude').value = position.coords.latitude
                document.getElementById('longitude').value = position.coords.longitude
            },
            (error) =>{
                document.getElementById('manual-location').style.display = 'block'
            }
        )
    }
}