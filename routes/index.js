var express = require('express');
var router = express.Router();
var fileupload = require('./fileupload');
var mysql = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '123456',
    database : 'album'
});


/* GET home page. */
router.get('/', function(req, res, next) {
  // res.render('index', { title: 'Express' });
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
});

router.use('/fileupload',fileupload);

module.exports = router;
