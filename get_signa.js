var express = require('express');
var app = express();
var get_keys = require('./douyin_signature')

// 获取抖音 _signature 参数
app.get('/douyin', function (req, res) {
    var uid = req.query["user_id"].toString();
    var tac = req.query["tac"].toString();
    keys = get_keys.get_signature(uid, tac);
    if (keys) {
        res.send(keys);
        console.log(keys.toString());
    } else {
        res.send('keys未生成!');
    }
});

var server = app.listen(8000);
console.log("server running http://127.0.0.1:8000");
