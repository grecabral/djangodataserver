$(document).ready(function(){
    my_data = {
        "players":[
            {
                "age": 24, 
                "sex": "M", 
                "locality": "Recife", 
                "school": 1
            }
        ],       
        "gameFlag": 0, 
        "number_of_rounds": 2, 
        "coop_points": 4, 
        "no_coop_points": 2, 
        "difficulty": 0, 
        "strategy": 1,
        "rounds":[
            {
                "round": 0,     
                "player1Score": 2, 
                "player2Score": 2, 
                "player1Coop": 0, 
                "player2Coop": 0
            },
            {
                "round": 1,     
                "player1Score": 0, 
                "player2Score": 4, 
                "player1Coop": 1, 
                "player2Coop": 0
            }
        ]
    };
    $("#new_entry").click(function(){
        $.ajax({
            url: '/json_post/',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            processData: false,
            data: JSON.stringify(my_data),
            success: function(data){
                alert(data);
            }
        });
    });
    
    $('#submitBtn').click(function() {
      checked = $("input[type=radio]:checked").length;

      if(!checked) {
        alert("Você precisa selecionar uma opção");
        return false;
      }

    });

});