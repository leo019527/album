var express = require('express');
var router = express.Router();

var sepPhoto = require('./sepPhoto');

var mysql = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '123456',
    database : 'album'
});

router.all('/',function (req, res, next) {
    connection.query('SELECT DISTINCT label FROM picture',function (err, resuts) {
        if(err){
            console.log('[SELECT ERROR] - ',err.message);
        }else{
            out = [];
            for(var i=0;i<resuts.length;i++){
                resu = resuts[i];
                // data[resu['picturename']]=resu['pictureid'];
                a = resu['label'].split(",");
                if(a[0]!=''){
                    out.push(a);
                }
            }
            data = {};
            keys = [];
            for(var a in out){
                keys.push(out[a][0]);
            }
            (function iterator(index){
                if (index === keys.length) {
                    //console.log(data);
                    res.render('AIphoto',{'lables':data});
                    return;
                }
                connection.query('SELECT picturename,pictureid FROM picture WHERE label like "%'+out[index][0]+'%" limit 1',function (err, result) {
                    if(err){
                        console.log('[SELECT ERROR] - ',err.message);
                    }else{
                        data[out[index][0]] = [result[0]['picturename'],result[0]['pictureid']];
                        iterator(++index);
                    }
                });
            })(0);
        }
    });
});

router.use('/sepPhoto',sepPhoto);

module.exports = router;
