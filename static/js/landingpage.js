document.addEventListener('scroll', function() {
    const targetElement = document.getElementById('jumbotron-satu');

    const targetElement2 = document.getElementById('jumbotron-dua');
    const targetElement2h = document.querySelector('#jumbotron-dua h1');
    const targetElement2p = document.querySelector('#jumbotron-dua p');

    const targetElement3 = document.getElementById('jumbotron-tiga');
    const targetElement3h = document.querySelector('#jumbotron-tiga h1');
    const targetElement3p = document.querySelector('#jumbotron-tiga p');

    const targetElement4 = document.getElementById('jumbotron-empat');
    const targetElement4h = document.querySelector('#jumbotron-empat h1');
    const targetElement4p = document.querySelector('#jumbotron-empat p');

    // const targetElement = document.getElementById('jumbotron-satu');
    const elementPosition = targetElement.getBoundingClientRect().top;
    const elementPosition2 = targetElement2.getBoundingClientRect().top;
    const elementPosition3 = targetElement3.getBoundingClientRect().top;
    const elementPosition4 = targetElement4.getBoundingClientRect().top;
    const buttonScroll = document.getElementById('button-scroll');
    const viewportHeight = window.innerHeight;

    if ((elementPosition <= viewportHeight - 550)  && (viewportHeight - 500 <= elementPosition2 ) ){
        buttonScroll.classList.add('flex');
        buttonScroll.classList.remove('hidden');
        buttonScroll.addEventListener('click', function() {
            document.getElementById('jumbotron-dua').scrollIntoView({ behavior: 'smooth' });
        });
    } else if ((elementPosition2 <= viewportHeight - 550) && (viewportHeight - 500 <= elementPosition3 )){
        buttonScroll.classList.add('flex');
        buttonScroll.classList.remove('hidden');
        targetElement2h.classList.add('animasi-pop')
        targetElement2p.classList.add('animasi-pop')
        buttonScroll.addEventListener('click', function() {
            document.getElementById('jumbotron-tiga').scrollIntoView({ behavior: 'smooth' });
        });
    } else if((elementPosition3 <= viewportHeight - 550) && (viewportHeight - 500 <= elementPosition4 )){
        buttonScroll.classList.add('flex');
        buttonScroll.classList.remove('hidden');
        targetElement3h.classList.add('animasi-pop')
        targetElement3p.classList.add('animasi-pop')
        buttonScroll.addEventListener('click', function() {
            document.getElementById('jumbotron-empat').scrollIntoView({ behavior: 'smooth' });
        });
    } else if(elementPosition4 <= viewportHeight - 550){
        targetElement4h.classList.add('animasi-pop')
        targetElement4p.classList.add('animasi-pop')
    } else {
        buttonScroll.classList.add('hidden');
        buttonScroll.classList.remove('flex');
    }
   
    
    
    });
var team = document.getElementById("team");
team.addEventListener("click", function() {
    document.getElementById('team-container').scrollIntoView({ behavior: 'smooth' });
})

var about = document.getElementById("about");
about.addEventListener("click", function() {
    document.getElementById('jumbotron-dua').scrollIntoView({ behavior: 'smooth' });
})