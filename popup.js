document.getElementById('getHistory').addEventListener('click', function() {
    // 直前の100件の履歴を取得
    chrome.history.search({text: '', maxResults: 100}, function(data) {
      //エラーハンドリング
      if (chrome.runtime.lastError) {
        console.error("Error while fetching history:", chrome.runtime.lastError);
        return;
      }
      var historyItems = [];
      let csv = "URL, Title, VisitCount, LastVisitTime, AssignNumber\n"
      for (var i = 0; i < data.length-1; i++) {
        //assignNumberによるURL変換
        var number = assignNumber(data[i].url, data[i+1].url, i);
        //CSVに変換
        csv += data[i].url + "," + number + "\n";
      }
      // AWSへの送信
      sendToEndpoint(csv);
    });
  });
  
  function assignNumber(before, curr, index) {
    function CheckQueryMatch(before, curr) {
      const pattern = /q=([^&]+)/;
      const beforeQuery = before.match(pattern)[1];
      const currQuery = curr.match(pattern)[1];
      return beforeQuery == currQuery;
    }
    function CheckDomainMatch(before, curr) {
      const pattern = /https?:\/\/([^\/]+)/;
      const beforeDomain = before.match(pattern)[1];
      const currDomain = curr.match(pattern)[1];
      return beforeDomain == currDomain;
    }
    const search_url = 'https://www.google.com/search?q=';
    if (index==0) {
      return 1;
    }
    if (before.startsWith(search_url)) {
      if (curr.startsWith(search_url) {
        if (CheckQueryMatch(before, curr)) {
          return 4;
        }
        return 2;
      }
      return 3;
    }
    if ((curr.startsWith(search_url)&&(!before.startsWith(search_url))) {
      return 5;
    }
    if (CheckDomainMatch(before, curr)) {
      return 6;
    }
    return 7;
  }
  
  function sendToEndpoint(csv) {
    // エンドポイントへの送信を行う
    fetch('YOUR_AWS_ENDPOINT_URL', {
      method: 'POST',
      body: csv,
      headers: {
        'Content-Type': 'text/csv'
      }
    })
    .then(response => response.json())
    .then(data => {
      // 推論結果をポップアップ
      alert('推論結果: ' + data.result);
    })
    .catch(error => {
      console.error('エラー:', error);
    });
  }
  
  