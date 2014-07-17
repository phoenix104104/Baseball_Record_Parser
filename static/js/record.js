$(document).ready( function() {

    $("#parse").click( function() {
        var content1 = $('#team1').val();
        var content2 = $('#team2').val();
        if( content1.length ) {
            $.post('convert.json', 
                { text1: content1, text2: content2 }, 
                function(data, textStatus) {
                    $('#output').val(data.result);
                });
        }
    });

});
