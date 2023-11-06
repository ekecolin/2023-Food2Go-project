// Setting our variables from html into javascript
var age = document.getElementById("age");
var height = document.getElementById("height");
var weight = document.getElementById("weight");
var male = document.getElementById("m");
var female = document.getElementById("f");
var form = document.getElementById("form");
let resultArea = document.querySelector(".comment");

modalContent = document.querySelector(".modal-content");
modalText = document.querySelector("#modalText");
var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

/* Runs by pressing the calculate function in the bmi calculator */
function calculate(){
  
  /* Checks if values of age, weight and height are not empty and checks if male or female are not checked
     if its empty then this message below will pop up on the screen */
  if(age.value=='' || height.value=='' || weight.value=='' || (male.checked==false && female.checked==false)){
    modal.style.display = "block";
    modalText.innerHTML = `All fields must be filled!`;

  /* If its ok and everything is fill we run countBmi function*/
  }else{
    countBmi();
  }
}


/* Counts BMI for us and prints the output */
function countBmi(){
    /* Put the information in a array and then check if either male or female was selected by the user, we use push to put the M or F in the array */
    var p = [age.value, height.value, weight.value];
    if(male.checked){
      p.push("male");
    }else if(female.checked){
      p.push("female");
}

/* BMI calculation formula, select weight and divide by the height and then divide everything by height */
var bmi = Number(p[2])/(Number(p[1])/100*Number(p[1])/100);

/* Made a variable 'result' so depending on which weight you fall under then this will produce your result */
var result = '';
if(bmi<18.5){
    result = 'Underweight';
    }else if(18.5<=bmi&&bmi<=24.99){
    result = 'Healthy';
    }else if(25<=bmi&&bmi<=29.99){
    result = 'Overweight';
    }else if(30<=bmi&&bmi<=34.99){
    result = 'Obese';
    }else if(35<=bmi){
    result = 'Extremely obese';
}
  
  
/* Displays the result on screen */
resultArea.style.display = "block";
document.querySelector(".comment").innerHTML = `You are <span id="comment">${result}</span>`;
document.querySelector("#result").innerHTML = bmi.toFixed(2);
}
  
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}
  
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
