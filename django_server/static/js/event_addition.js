$(document).ready(
  function () {
      var newURL = window.location.pathname;
      newURL = decodeURIComponent(newURL);
      newURL = newURL.replace("/addition|", "");
      splitUrl = newURL.split("+");

      var json_create = {};
      for (var i = 0; i < splitUrl.length; i++)
      {
        var splitKey = splitUrl[i].split("=");
        switch(splitKey[0])
        {
            case "title":
                json_create.title = splitKey[1];
                break;
            case "phone":
                json_create.phone = splitKey[1];
                break;
            case "description":
                json_create.description = splitKey[1];
                break;
            case "site_url":
                json_create.site_url = splitKey[1];
                break;
            case "address":
                json_create.address = splitKey[1];
                break;
            case "ticket":
                json_create.ticket = splitKey[1];
                break;
            case "categories":
                json_create.categories = splitKey[1];
                break;
        }
      }
      $('#categories').text(json_create['categories']);

      //alert(json_create['phone']);
      if (json_create['phone'] == "no"){
          $('#phone').hide();
      }
      else
      {
          $('#phone').text(json_create['phone']);
      }


      $('#address').text(json_create['address']);

      if (json_create['description'] == "no"){
          $('#description').hide();
      }
      else
      {
          $('#description').text(json_create['description']);
      }

      $('#title').text(json_create['title']);

      if (json_create['ticket'] == "no"){
          $('#ticketHref').hide();
      }
      else
      {
          $('#ticketHref').attr('href',json_create['ticket']);
      }

      if (json_create['site_url'] == "no"){
          $('#siteHref').hide();
      }
      else
      {
          $('#siteHref').attr('href',json_create['site_url']);
      }
      //alert("111");
  }
);