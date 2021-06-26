var express = require('express');
var app = express();
var get_keys = require('./douyin_signature')
var get_keys2 = require('./douyin_signature2')

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

app.get('/douyin2', function (req, res) {
    var ua = req.query["ua"].toString();
    var user_id = req.query["user_id"].toString();
    keys = get_keys2.get_signature2(ua, user_id);
    if (keys) {
        res.send(keys);
        console.log(keys.toString());
    } else {
        res.send('');
    }
});

var server = app.listen(8000);
console.log("server running http://0.0.0.0:8000");
