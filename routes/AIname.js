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
    connection.query('SELECT DISTINCT namelabel FROM picture',function (err, resuts) {
        if(err){
            console.log('[SELECT ERROR] - ',err.message);
        }else{
            out = [];
            for(var i=0;i<resuts.length;i++){
                resu = resuts[i];
                if(resu == null)continue;
                // data[resu['picturename']]=resu['pictureid'];
                a = resu['namelabel'].split(",");
                if(a[0] != '') {
                    out.push(a);
                }
            }
            data = {};
            keys = [];
            //for(var a in out[0]){
            //    keys.push(out[0][a]);
            //}
            for(var a in out){
                keys.push(out[a][0]);
            }
            (function iterator(index){
                //console.log(index);
                if (index === keys.length) {
                    //console.log(data);
                    res.render('AIphoto2',{'lables':data});
                    return;
                }
                //console.log('SELECT picturename,pictureid FROM picture WHERE           namelabel like "%'+out[index][0]+'%" limit 1');
                connection.query('SELECT picturename,pictureid FROM picture WHERE namelabel like "%'+out[index][0]+'%" limit 1',function (err, result) {
                    if(err){
                        console.log('[SELECT ERROR] - ',err.message);
                    }else{
                        data[out[index][0]] = [result[0]['picturename'],result[0]['pictureid']];
                        //console.log(data);
                        iterator(++index);
                    }
                });
            })(0);
        }
    });
});

module.exports = router;
