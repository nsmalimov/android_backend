function getDataToSent()
{
    var newURL = window.location.pathname;
    newURL = newURL.split("|")[1];
    var split_url = newURL.split("+");
    var json_create = {};
    for (var i = 0; i < split_url.length; i++)
    {
        var split_key = split_url[i].split("=");
        switch(split_key[0])
        {
            case "id":
                json_create.id = split_key[1];
                break;
            case "date":
                json_create.date = split_key[1];
                break;
            case "time_to":
                json_create.time_to = split_key[1];
                break;
            case "time_from":
                json_create.time_from = split_key[1];
                break;
            case "in_place":
                json_create.in_place = split_key[1];
                break;
            case "out_place":
                json_create.out_place = split_key[1];
                break;
        }
    }
    return json_create;
}

function getValue(dataToSent, serverUrl){
   var value= $.ajax({
       type: "POST",
       data: dataToSent,
       url: serverUrl + "build_route",
       async: false
   }).responseText;
   return value;
}

function assesPost(dataToSent, serverUrl){
   var value= $.ajax({
       type: "POST",
       data: dataToSent,
       url: serverUrl + "assesment",
       async: false
   }).responseText;
   return value;
}

function geocoderYandex(latitude, longitude){
   var value= $.ajax({
      url: "http://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + longitude + "," + latitude,
      async: false
   }).responseText;
   //value = value['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["metaDataProperty"]['GeocoderMetaData']['text'];
    var address = JSON.parse(value);
    address = address['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["metaDataProperty"]['GeocoderMetaData']['text'];

    address = address.replace("Россия, ", "")
    return address;
}

$(document).ready(
  function () {
      var serverHostName = window.location.hostname;

      var serverProtocolName = window.location.protocol;

      var portName = window.location.port;      
     if (portName.length == 0){portName = "80"; }
      var serverPath = serverProtocolName + "//" + serverHostName + ":" + portName + "/";

     var jsonDataSent = getDataToSent();
     var dataFromServer = getValue(jsonDataSent, serverPath);
     var jsonDataGet = JSON.parse(dataFromServer);

     var first_place = jsonDataGet['first_place'];
     var address_first = geocoderYandex(first_place['latitude'], first_place['longitude']);
      $('#firstPlaceTimeStart').text(first_place['time_start']);
      $('#firstPlaceAddress').text(address_first);
      $('#firstPlaceTimeNext').text("Время в пути до следующей точки (минут): " + first_place['time_road_next']);

     var array = jsonDataGet['medium_place'];

     var lenMediumPlace = array.length;

     for (var i = 0; i < array.length; i++)
     {
         $('#mainContainer').append("<div class='row'>" +
         "<p>" + array[i]['time_start'] + "-" + array[i]['time_end'] + "</p>" +
         "<p>" + array[i]['title'] +"</p>" +
         "<button type='button' class='btn btn-default' id='additbutton_" + i + "'>Подробнее</button>" +
         "<select class='form-control' id='assesform_" + i + "'>" +
         "<option>1</option>" +
         "<option>2</option>" +
         "<option>3</option>" +
         "<option>4</option>" +
         "<option>5</option>" +
         "</select>" +
         "<button type='button' class='btn btn-default' id='assesbutton_" + i + "'>Оценить</button>" +
         "<p>" + "Время в пути до следующей точки (минут): " + array[i]['time_road_next'] + "</p></div>");
     }

     $('#mainContainer').append("<div class='row'><p id='lastPlaceTimeStart'></p><p id='lastPlaceAddress'></p></div>");

      $('#mainContainer').append("<button type='button' class='btn btn-default' id='button_map'>Карта</button>");

      var last_place = jsonDataGet['last_place'];
      var address_last = geocoderYandex(last_place['latitude'], last_place['longitude']);
      $('#lastPlaceTimeStart').text(last_place['time_end']);
      $('#lastPlaceAddress').text(address_last);

      $("#button_map").click(function() {
         var strMap = serverPath + "geo_map|";
         strMap = strMap + first_place['latitude'] + "," + first_place['longitude'] + "+";

         for (var i = 0; i < array.length; i++)
         {
             strMap = strMap + array[i]['latitude'] + "," + array[i]['longitude'] + "+";
         }
         strMap = strMap + last_place['latitude'] + "," + last_place['longitude'];
         window.location.href  = strMap;

      });

      $(".btn-default").click(function() {
          var btnId = this.id;

          var split_btnId = btnId.split("_");
          var idNum = parseInt(split_btnId[1]);

          if (split_btnId[0] == "additbutton")
          {
              array[idNum]['phone'] = array[idNum]['phone'].replace("+7", "8");
              var str = serverPath + "addition|" +
              "title=" + array[idNum]['title'] + "+" + "description=" + array[idNum]['description'] + "+" +
              "address=" + array[idNum]['address'] + "+" + "phone=" + array[idNum]['phone'] + "+" +
              "categories=" + array[idNum]['categories'] + "+" + "site_url=" + array[idNum]['site_url'] + "+" +
              "ticket=" + array[idNum]['ticket'];
              window.location.href  = str;
          }
          else
          {
              var assesSentData = {};

              var assesFromForm = $('#assesform_' + idNum).val();
              assesFromForm = parseInt(assesFromForm);

              assesSentData.id = jsonDataSent['id'];
              assesSentData.asses = assesFromForm;
              assesSentData.event_name = array[idNum]['title'];
              var serverSent = assesPost(assesSentData, serverPath);

              $('#assesbutton_' + idNum).hide();
              $('#assesform_' + idNum).hide();
          }
     });
  }
);
