$(document).ready(function(){
    var my_data = {};
    my_data[0] = 
    {
        "model":"Jogador", 
        "fields": 
        {
            "ue4guid": "8ee13f2222944779b1d53aac01fd3700",
            "idade": 24, 
            "sexo": "M", 
            "localidade": "Recife", 
            "escola": 1
        }
    };
    my_data[1] =
    {
        "model":"Partida",
        "fields":
        {
            "ue4guid": "4b8d3f5820874ae3846ea2888dc74998",
            "numero_rodadas": 2, 
            "dificuldade": 0, 
            "estrategia": 1, 
            "jogador1": "8ee13f2222944779b1d53aac01fd3700", 
            "jogador2": null
        } 
    };
    my_data[2] = 
    {
        "model":"Rodada",
        "fields":
        {
            "ue4guid_partida": "4b8d3f5820874ae3846ea2888dc74998", 
            "rodada": 0, 
            "pontuacao_jogador1": 2, 
            "pontuacao_jogador2": 2, 
            "cooperacao_jogador1": 1, 
            "cooperacao_jogador2": 1
        }
    };
    my_data[3] = 
    {
        "model":"Rodada",
        "fields":
        {
            "ue4guid_partida": "4b8d3f5820874ae3846ea2888dc74998",
            "rodada": 1,     
            "pontuacao_jogador1": 2, 
            "pontuacao_jogador2": 0, 
            "cooperacao_jogador1": 0, 
            "cooperacao_jogador2": 1
        }
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
    
});