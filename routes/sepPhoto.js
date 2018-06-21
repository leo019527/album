var express = require('express');
var router = express.Router();

var mysql = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '123456',
    database : 'album'
});

router.get('/',function (req, res, next) {
    var a = req.query.label;
    console.log(a);
    var sql = 'SELECT picturename,pictureid FROM picture WHERE label like "%'+a+'%" or namelabel  like "%'+a+'%"';
    console.log(sql);
    connection.query(sql,function (err, results) {
        if(err){
            console.log('[SELECT ERROR] - ',err.message);
        }else {
            data = {};
            for(var i=0;i<results.length;i++){
                resu = results[i];
                data[resu['picturename']]=resu['pictureid'];
            }
            res.render('sepPhoto',{'pictures':data,'label':a});
        }
    })
});

router.post('/',function(req,res,next){
    res.end("why hacking us?");
});


module.exports = router;