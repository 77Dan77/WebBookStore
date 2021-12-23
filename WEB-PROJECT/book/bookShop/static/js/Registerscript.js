const form = document.querySelector("form");

uField = form.querySelector(".username"),
uInput = nField.querySelector("input");

lField = form.querySelector(".lname"),
lInput = lField.querySelector("input");

nField = form.querySelector(".fname"),
nInput = nField.querySelector("input");

eField = form.querySelector(".email"),
eInput = eField.querySelector("input");

pField = form.querySelector(".password"),
pInput = pField.querySelector("input");



form.onsubmit = (e)=>{
  e.preventDefault(); //preventing from form submitting
  //if email and password is blank then add shake class in it else call specified function
  (eInput.value == "") ? eField.classList.add("shake", "error") : checkEmail();
  (uInput.value == "") ? uField.classList.add("shake", "error") : checkUsername();
  (pInput.value == "") ? pField.classList.add("shake", "error") : checkPass();
  (nInput.value == "") ? nField.classList.add("shake", "error") : checkFName();
  (lInput.value == "") ? lField.classList.add("shake", "error") : checkLName();

  setTimeout(()=>{ //remove shake class after 500ms
    uField.classList.remove("shake");
    eField.classList.remove("shake");
    pField.classList.remove("shake");
    nField.classList.remove("shake");
    lField.classList.remove("shake");

  }, 500);
  eInput.onkeyup = ()=>{checkEmail();} //calling checkEmail function on email input keyup
  uInput.onkeyup = ()=>{checkUsername();} //calling checkEmail function on email input keyup
  pInput.onkeyup = ()=>{checkPass();} //calling checkPassword function on pass input keyup
  nInput.onkeyup = ()=>{checkFName();} //calling checkEmail function on email input keyup
  lInput.onkeyup = ()=>{checkLName();} //calling checkPassword function on pass input keyup

  function checkEmail(){ //checkEmail function
    let pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/; //pattern for validate email
    if(!eInput.value.match(pattern)){ //if pattern not matched then add error and remove valid class
      eField.classList.add("error");
      eField.classList.remove("valid");
      let errorTxt = eField.querySelector(".error-txt");
      //if email value is not empty then show please enter valid email else show Email can't be blank
      (eInput.value != "") ? errorTxt.innerText = "Enter a valid email address" : errorTxt.innerText = "Email can't be blank";
    }else{ //if pattern matched then remove error and add valid class
      eField.classList.remove("error");
      eField.classList.add("valid");
    }
  }
  function checkPass(){ //checkPass function
    if(pInput.value == ""){ //if pass is empty then add error and remove valid class
      pField.classList.add("error");
      pField.classList.remove("valid");
    }else{ //if pass is empty then remove error and add valid class
      pField.classList.remove("error");
      pField.classList.add("valid");
    }
  }
  function checkFName(){ //checkPass function
    var letters = /^[A-Za-z]+$/;
    if(!nInput.value.match(letters)){ //if pass is empty then add error and remove valid class
      nField.classList.add("error");
      nField.classList.remove("valid");
      let errorTxt = nField.querySelector(".error-txt");
      //if email value is not empty then show please enter valid email else show Email can't be blank
      (nInput.value != "") ? errorTxt.innerText = "Enter a valid Name" : errorTxt.innerText = "Name can't be blank";
    }else{ //if pass is empty then remove error and add valid class
      nField.classList.remove("error");
      nField.classList.add("valid");
    }
  }

  function checkUsername(){ //checkPass function
    var letters = /^[A-Za-z]+$/;
    if(!uInput.value.match(letters)){ //if pass is empty then add error and remove valid class
      uField.classList.add("error");
      uField.classList.remove("valid");
      let errorTxt = uField.querySelector(".error-txt");
      //if email value is not empty then show please enter valid email else show Email can't be blank
      (uInput.value != "") ? errorTxt.innerText = "Enter a valid Name" : errorTxt.innerText = "Name can't be blank";
    }else{ //if pass is empty then remove error and add valid class
      uField.classList.remove("error");
      uField.classList.add("valid");
    }
  }

  function checkLName(){ //checkPass function
    var letters = /^[A-Za-z]+$/;
    if(!lInput.value.match(letters)){ //if pass is empty then add error and remove valid class
      lField.classList.add("error");
      lField.classList.remove("valid");
      let errorTxt = lField.querySelector(".error-txt");
      //if email value is not empty then show please enter valid email else show Email can't be blank
      (lInput.value != "") ? errorTxt.innerText = "Enter a valid Name" : errorTxt.innerText = "Name can't be blank";
    }else{ //if pass is empty then remove error and add valid class
      lField.classList.remove("error");
      lField.classList.add("valid");
    }
  }

  //if eField and pField doesn't contains error class that mean user filled details properly
  if(!eField.classList.contains("error") && !pField.classList.contains("error")){
    //window.location.href = form.getAttribute("action"); //redirecting user to the specified url which is inside action attribute of form tag
  }
}