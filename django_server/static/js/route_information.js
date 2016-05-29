function createJson() {
    var json_create = new Object();
    var date = getDatafromDate();
    json_create.date = rewriteDate(date);
    json_create.time_to = getDatafromTimeTo();
    json_create.time_from = getDatafromTimeFrom();
    json_create.in_place = getDatafromInPlace();
    json_create.out_place = getDatafromOutPlace();

    return json_create
}
var sortObjectByKey = function (obj) {
    var keys = [];
    var sorted_obj = {};

    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            keys.push(key);
        }
    }
    keys.sort();

    jQuery.each(keys, function (i, key) {
        sorted_obj[key] = obj[key];
    });

    return sorted_obj;
};

function getDatafromDate() {
    var text = $("#date").val();
    var textSplit = text.split('/');
    return textSplit[0] + "-" + textSplit[1] + "-" + textSplit[2]
}

function getDatafromTimeTo() {
    var text = $("#time_in").val();
    return text
}

function getDatafromTimeFrom() {
    var text = $("#time_from").val();
    return text
}

function getValue(address) {
    var value = $.ajax({
        url: "http://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + address,
        async: false
    }).responseText;
    return value;
}

function geokoderData(address) {
    var url = "http://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + address;
    var data_get = getValue(address);
    data_get = JSON.parse(data_get);
    var newData = data_get['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']["pos"];
    var answer = newData.split(" ")[1] + "," + newData.split(" ")[0];

    return answer;
}

function getDatafromInPlace() {
    text = "";
    if ($('#checkbox_1').is(':checked')) {
        var text = $("#edit_1").val();
    }
    else {
        var text = $("#form_1 option:selected").text();
        var textSplit = text.split(':');
        text = textSplit.splice(1, textSplit.length)
    }

    var answerTextIn = geokoderData(text[0]);
    return answerTextIn
}

function getDatafromOutPlace() {
    text = "";
    if ($('#checkbox_1').is(':checked')) {
        var text = $("#edit_2").val();
    }
    else {
        var text = $("#form_2 option:selected").text();
        var textSplit = text.split(':');
        text = textSplit.splice(1, textSplit.length)
    }

    var answerTextOut = geokoderData(text[0]);
    return answerTextOut
}

function rewriteDate(oldDate) {
    var prettyDateSplit = oldDate.split('-');

    if (prettyDateSplit[0].length != 2) {
        prettyDateSplit[0] = '0' + prettyDateSplit[0];
    }

    if (prettyDateSplit[1].length != 2) {
        prettyDateSplit[1] = '0' + prettyDateSplit[1];
    }

    var prettyDate = prettyDateSplit[1] + '-' + prettyDateSplit[0] + '-' + prettyDateSplit[2];

    return prettyDate;
}

function getDataValue(serverUrl) {
    var value = $.ajax({
        url: serverUrl + "wich_days",
        async: false
    }).responseText;
    return value;
}

//var disabledSpecificDays = ["6-18-2015", "6-19-2015", "6-20-2015", "6-21-2015"];

var serverHostName = window.location.hostname;

var serverProtocolName = window.location.protocol;

var portName = window.location.port;
if (portName.length == 0) {
    portName = "80";
}
var serverPath = serverProtocolName + "//" + serverHostName + ":" + portName + "/";

var disabledSpecificDays = getDataValue(serverPath);
disabledSpecificDays = JSON.parse(disabledSpecificDays);

function disableSpecificDaysAndWeekends(date) {
    var m = date.getMonth();
    var d = date.getDate();
    var y = date.getFullYear();

    var now_date = new Date();
    var checker = false;
    if (new Date().getMonth() == date.getMonth() && (new Date().getDate() == date.getDate())) {
        for (var i = 0; i < disabledSpecificDays.length; i++) {
            if ($.inArray(((now_date.getMonth() + 1) + '-' + now_date.getDate() + '-' + now_date.getFullYear()), disabledSpecificDays) != -1) {
                checker = true;
            }
        }
        if (checker) {
            return [true];
        }
        else {
            return [false];
        }
    }


    for (var i = 0; i < disabledSpecificDays.length; i++) {
        if ($.inArray((m + 1) + '-' + d + '-' + y, disabledSpecificDays) != -1 || new Date() >= date) {
            return [true];
        }
        else {
            return [false];
        }
    }
    return [false];
}

$(document).ready(
    function () {

        var serverHostName = window.location.hostname;

        var serverProtocolName = window.location.protocol;

        var portName = window.location.port;
        if (portName.length == 0) {
            portName = "80";
        }
        var serverPath = serverProtocolName + "//" + serverHostName + ":" + portName + "/";
        $('.form-group').hide();

        $(".datepicker").datepicker({
            minDate: 0,
            beforeShowDay: disableSpecificDaysAndWeekends
        });

        var myDate = new Date();
        var prettyDate = (myDate.getMonth() + 1) + '/' + myDate.getDate() + '/' +
            myDate.getFullYear();

        var prettyDateSplit = prettyDate.split('/');

        if (prettyDateSplit[0].length != 2) {
            prettyDateSplit[0] = '0' + prettyDateSplit[0];
        }

        if (prettyDateSplit[1].length != 2) {
            prettyDateSplit[1] = '0' + prettyDateSplit[1];
        }

        var prettyDate = prettyDateSplit[0] + '/' + prettyDateSplit[1] + '/' + prettyDateSplit[2];

        $("#date").val(prettyDate);

        var time_in = "08:00";
        var time_out = "22:00";
        $('#time_in').timepicker({
            hour: '08',
            minute: '00'
        });
        $('#time_in').val(time_in);
        $('#time_from').timepicker({
            hour: '08',
            minute: '00'
        });

        $('#time_from').val(time_out);

        $('#checkbox_1').attr('checked', false);
        $('#checkbox_1').click(function () {
            if ($(this).is(':checked')) {
                $('.form-group').show();
                $('#edit_1').val("Санкт-Петербург,");
                $('#edit_2').val("Санкт-Петербург,");
                $('#form_1').hide();
                $('#form_2').hide();
                $('#text_1').hide();
                $('#text_2').hide();
            }
            else {
                $('.form-group').hide();
                $('#form_1').show();
                $('#form_2').show();
                $('#text_1').show();
                $('#text_2').show();
            }

        });

        $('#button_build').click(function () {
            var json_data = createJson();
            var newURL = window.location.pathname;
            var vkID = newURL.split("_")[1];
            var sent_string = "id=" + vkID + "+";
            for (key in json_data) {
                var new_str = key + "=" + json_data[key];
                sent_string += new_str + '+';
            }
            sent_string = sent_string.substring(0, sent_string.length - 1);

            window.location.href = serverPath + "list_route|" + sent_string;
        });
    }
);
