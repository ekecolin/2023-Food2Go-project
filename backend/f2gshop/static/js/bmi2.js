function Calo()
{
    // setting our variable that will help use calculate the height, age and weight of the user
    var h=document.getElementById('hi').value;
    var w=document.getElementById('we').value;
    var age=document.getElementById('age').value;
    var activity_level = document.getElementById('activity-level').value;

    // CHecking which gender was selected by the user and if no gender is selected then an error message will come up
    var selectedGender = document.querySelector('input[name="gender"]:checked');
    var gender = selectedGender ? selectedGender.value : null;
    if(!gender){
        alert("Please select your gender & fill in all the inputs");
        return;
    }
    
    // BMR calculation formula - Mifflin-St Jeor equation, considered to be more accurate than Harris-Benedict equation
    if (gender == "m") {
        calom = (10 * w) + (6.25 * h) - (5 * age) + 5;
    } else if (gender == "f") {
        calom = (10 * w) + (6.25 * h) - (5 * age) - 161;
    }

     // Displays the message and the result of user input (Total Daily Energy Expenditure)
    var TDEE = calom * activity_level;
    document.getElementById("resultcal").innerHTML="You require "+TDEE.toFixed(2)+" calories to maintain your current weight";
  
    // calculate protein, fats, and carbs intake based on TDEE
    const proteinsG = TDEE * 0.12;
    const fatsG = TDEE * 0.60;
    const carbsG = TDEE * 0.27;

    // conversion factor to grams from nutritional intake
    const proteinCaloriesPerGram = 4;
    const fatsCaloriesPerGram = 9;
    const carbsCaloriesPerGram = 4;
    
    // calculate protein, fats, and carbs intake in grams
    const protein = proteinsG / proteinCaloriesPerGram;
    const fats = fatsG / fatsCaloriesPerGram;
    const carbs = carbsG / carbsCaloriesPerGram;

    // https://www.chartjs.org/docs/latest/getting-started/ source to where I got the code for the chart + set up labels and colors for chart
    let data2 = [protein, fats, carbs];
    const ctx = document.getElementById("myChart").getContext("2d");
    let myChart = new Chart(ctx,{
        type:'doughnut' , 
        data:{
            // Labeling contents we want to display on our pie chart
            labels: ['Protein', 'Fat', 'Carbs'],
            datasets: [
                {
                    label : 'Number of grams you consume',
                    data : data2,
                    backgroundColor: ['#4e691a', '#7cb896', '#b6d4ae'],
                    borderWidth: 1
                }
            ]
        }
    });
}

// Clears result of calories when 'Clear' button is selected
function Clear()
{
    document.getElementById("resultcal").innerHTML="";
}