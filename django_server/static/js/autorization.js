$(document).ready(
  function () {
      //alert("111");
      var serverHostName = window.location.hostname;

      var serverProtocolName = window.location.protocol;
      
      var portName = window.location.port;
      if (portName.length == 0){portName = "80"; }
      var serverPath = serverProtocolName + "//" + serverHostName + ":" + portName + "/";

     $("#vkIdInput").val("21747799");
     $('#button_sent').click(function() {
         window.location.href  = serverPath + "routeinfrom_" + $("#vkIdInput").val();
     });
  }
);
