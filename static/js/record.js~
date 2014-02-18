$(document).ready( function() {
    var nBatter = 2;
    var nPA = 3; 
    $("#send").click( function() {
        var b1 = {
            order: '1', 
            no: $("#B1-no").val(),
            PA: [ 
                    $("#B1-PA1").val(),
                    $("#B1-PA2").val()
                ]
        };
        var b2 = {
            order: '2', 
            no: $("#B2-no").val(),
            PA: [ 
                    $("#B2-PA1").val(),
                    $("#B2-PA2").val()
                ]
        };
        //var dat = [1, 2, 3];
        //var dat = {'a':[1, 2, 'aaa'], 'b':[4, 5, 'bbb']};
        var dat = [];
        dat.push(b1);
        dat.push(b2);
        $.post( '/record.json', {data: dat, nPlayer: nBatter}, 
                function(data) {
                    $("#output").val(data.result);
                }  
        );
    })
        
    $("#add_player").click( function() {
        var content = '<tr>';
        nBatter += 1;
        content += '<th>' + nBatter.toString() + '.</th>';
        var id = 'B' + nBatter.toString();
        content += '<th><input type="text" size="5" id="' + id + '"> </th>';
        var nCols = $('#record_table tbody tr th').length / (nBatter-1) - 2;
        for (var i=0 ; i<nCols ; i++) {
            content += '<th><input type="text" id="' + id + '-PA' + i.toString() + '"></th>';
        }
        content += '</tr>';
        $(content).hide().appendTo('#record_table').fadeIn(750);
    });

    $('#add_PA').click( function() {
        nPA += 1;
        var pa = nPA.toString();

        // header
        var content = '<th>PA' + pa + '</th>';
        $(content).hide().appendTo('#record_table thead tr').fadeIn(750);

        // body
        var rows = $('#record_table tbody tr');
        for (var i=0 ; i<rows.length ; i++) {
            content = '<th><input type="text" id="B' + i.toString() + '-PA' + pa + '"></th>';
            $(content).hide().appendTo(rows[i]).fadeIn();
        }
    });


});
