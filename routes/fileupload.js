var express = require('express');
var router = express.Router();
var fs = require('fs');
var multiparty = require('multiparty');
var mysql = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '123456',
    database : 'album'
});

/* GET home page. */
router.all('/', function(req, res, next) {
    //配置上传目录
    var form = new multiparty.Form({uploadDir:'./public/photos'});
    //上传完成的后台处理
    form.parse(req, function(err, fields, files){
        // res.end(files.upload[0].originalFilename);
        if(err){
            res.end(err.message);
        }else {
            // console.log(files.upload[0].path);
            var Mfile = files.upload[0];
            connection.connect();
            //TODO:打上标签
            connection.query("INSERT INTO picture VALUES('"+Mfile.originalFilename+"','123456','"+Mfile.path.replace(/\\/g,"/").replace("public/","")+"','aaa,bb','person 1')",function (error, results, fields) {
                if (error) throw error;
            });
            connection.query('SELECT picturename,pictureid FROM picture',function (err, resuts) {
                if(err){
                    console.log('[SELECT ERROR] - ',err.message);
                }else{
                    data = {};
                    for(var i=0;i<resuts.length;i++){
                        resu = resuts[i];
                        data[resu['picturename']]=resu['pictureid'];
                    }
                    res.render('index',{'pictures':data});
                }
            });
            connection.end();
        }
    });
});

module.exports = router;