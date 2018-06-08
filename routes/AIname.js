var express = require('express');
var router = express.Router();

var mysql = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '123456',
    database : 'album'
});

router.all('/',function (req, res, next) {
    connection.query('SELECT namelabel FROM picture',function (err, resuts) {
        if(err){
            console.log('[SELECT ERROR] - ',err.message);
        }else{
            out = [];
            for(var i=0;i<resuts.length;i++){
                resu = resuts[i];
                if(resu == null)continue;
                // data[resu['picturename']]=resu['pictureid'];
                a = resu['namelabel'].split(",");
                out.push(a);
            }
            data = {};
            keys = [];
            for(var a in out[0]){
                keys.push(out[0][a]);
            }
            (function iterator(index){
                console.log(index);
                if (index === keys.length) {
                    res.render('AIphoto',{'lables':data});
                    return;
                }
                connection.query('SELECT picturename,pictureid FROM picture WHERE namelabel like "%'+out[0][index]+'%" limit 1',function (err, result) {
                    if(err){
                        console.log('[SELECT ERROR] - ',err.message);
                    }else{
                        data[out[0][index]] = [result[0]['picturename'],result[0]['pictureid']];
                        iterator(++index);
                    }
                });
            })(0);
        }
    });
});

module.exports = router;
