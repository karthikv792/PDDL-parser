# model_parser
MODEL PARSING OF PDDL FILES
     function onOpen(evt) {
      websocket.send('{"action": "start","content-type": "audio/wav"}');
      }
      function onMessage(evt) {
  console.log(evt.data);
}
    function downloadfile(){

        recorder.exportWAV(
        function (blob){
            var IBM_access_token = 'XP05-H02OVkI-xiVFDImibL9wIMtv7wPTrexaa48zsJG'
            var ws_url = 'wss://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/bb483480-b7e2-419c-9640-c48b7c000351/v1/recognize'
            var wsURI = ws_url+'/v1/recognize'+ '?access_token=' + IBM_access_token + '&model=en-US_BroadbandModel';
            var websocket = new WebSocket(wsURI);
              websocket.onopen = function(evt) { onOpen(evt) };
                websocket.onmessage = function(evt) { onMessage(evt) };
                websocket.send(blob);
                websocket.send(JSON.stringify({action: 'stop'}));
        }
        );
    }
