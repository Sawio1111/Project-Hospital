window.onload = () => {
    let timeOpen = new Date()
    document.querySelector('#currentTime').innerHTML =
        timeOpen.getHours() + ':' +
        timeOpen.getMinutes() + ':' +
        timeOpen.getSeconds();

    document.querySelector('#currentDate').innerHTML =
        timeOpen.getFullYear() + '/' +
        (timeOpen.getMonth() + 1) + '/' +
        timeOpen.getDate();

    setInterval(function() {
    let time = new Date()
    document.querySelector('#currentTime').innerHTML =
        time.getHours() + ':' +
        time.getMinutes() + ':' +
        time.getSeconds();
}, 1000);
    
}

