var check = document.querySelector('#check')
var box = document.querySelector('.box')
var ball = document.querySelector('.ball')
var lightmode = getCookie('lightmode')


function delay(time) {
  return new Promise(resolve => setTimeout(resolve, time));
}


async function lightmodeChanger(){

  if(lightmode === 'true' ){
    box.setAttribute('style','background-color:black;')
    ball.setAttribute('style','transform:translatex(0%);')
    await delay(100)
    box.setAttribute('style','background-color:black;')
    ball.setAttribute('style','transform:translatex(32px);')

  }else{
    box.setAttribute('style','background-color:white; color:black;')
    ball.setAttribute('style','transform:translatex(0%);')
  }
}
lightmodeChanger()


function setCookie(name, value, daysToLive){
  const date = new Date();
  date.setTime(date.getTime() +  (daysToLive * 24 * 60 * 60 * 1000));
  let expires = "expires=" + date.toUTCString();
  document.cookie = `${name}=${value}; ${expires}; path=/`
}

function getCookie(name){
  const cDecoded = decodeURIComponent(document.cookie);
  const cArray = cDecoded.split("; ");
  let result = null;
  
  cArray.forEach(element => {
      if(element.indexOf(name) == 0){
          result = element.substring(name.length + 1)
      }
  })
  return result;
}


check.addEventListener('click',async function(){
  if(lightmode === 'true'){
    setCookie("lightmode", false, 365);
    box.setAttribute('style','background-color:white; color:black;')
    ball.setAttribute('style','transform:translatex(0%);')
    await delay(300)
    location.reload()
  }
  else{
    setCookie("lightmode", true, 365);
    location.reload()
  }
})




var purecookieTitle = "Cookies."; 
var purecookieDesc = "By using this website, you automatically accept that we use cookies."; 
var purecookieLink = '<a href="https://www.cssscript.com/privacy-policy/" target="_blank">What for?</a>'; 
var purecookieButton = "FINE"; 


function pureFadeIn(elem, display){
  var el = document.getElementById(elem);
  el.style.opacity = 0;
  el.style.display = display || "block";

  (function fade() {
    var val = parseFloat(el.style.opacity);
    if (!((val += .02) > 1)) {
      el.style.opacity = val;
      requestAnimationFrame(fade);
    }
  })();
};
function pureFadeOut(elem){
  var el = document.getElementById(elem);
  el.style.opacity = 1;

  (function fade() {
    if ((el.style.opacity -= .02) < 0) {
      el.style.display = "none";
    } else {
      requestAnimationFrame(fade);
    }
  })();
};


function eraseCookie(name) {
    document.cookie = name+'=; Max-Age=-99999999;';
}

function cookieConsent() {
  if (!getCookie('purecookieDismiss')) {
    document.getElementById('cookie').innerHTML += '<div class="cookieConsentContainer" id="cookieConsentContainer"><div class="cookieTitle"><p>' + purecookieTitle + '</p></div><div class="cookieDesc"><p>' + purecookieDesc + ' ' + purecookieLink + '</p></div><div class="cookieButton"><a onClick="purecookieDismiss();">' + purecookieButton + '</a></div></div>';
	pureFadeIn("cookieConsentContainer");
  }
}

function purecookieDismiss() {
  setCookie('purecookieDismiss','1',7);
  pureFadeOut("cookieConsentContainer");
}

window.onload = function() { cookieConsent(); };



