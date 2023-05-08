function validateForm() {
    var emailRegex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var valid = true
    function containsNumbers(str) {
        return /\d/.test(str);
      }
    if(!document.getElementById('email').value.match(emailRegex)){
        document.getElementById('email').style.border='1px solid red'
        valid = false
    }else{
        document.getElementById('email').style.border='none'
    }
    if((document.getElementById('pass').value !== document.getElementById('conf-pass').value) || ((document.getElementById('pass').value).length<=5)){
        document.getElementById('pass').style.border='1px solid red'
        document.getElementById('conf-pass').style.border = '1px solid red'
        valid = false
    }else{
        document.getElementById('pass').style.border='none'
        document.getElementById('conf-pass').style.border='none'
    }
    if(containsNumbers(document.getElementById('first-name').value)){
        document.getElementById('first-name').style.border='1px solid red'
        valid = false
    }else{
        document.getElementById('first-name').style.border='none'

    }
    if(containsNumbers(document.getElementById('last-name').value)){
        document.getElementById('last-name').style.border='1px solid red'
        valid = false
    }else{
        document.getElementById('last-name').style.border='none'
    }
    return valid
  }