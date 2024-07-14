var mysql = require('mysql2');
var express = require('express');
var bodyParser = require("body-parser");
var {faker} = require('@faker-js/faker');

var app = express();
app.set("view engine", "ejs");


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));


var connection = mysql.createConnection({
    host: 'xxx',
    user: 'xxx',
    password: 'xxx',
    database: 'xxx'
  });


app.get("/home", function(req, res){
    var q = "SELECT COUNT(*) AS count FROM users";
    var q2= "SELECT user_name FROM users order by created_at desc limit 1";
    connection.query(q, function(error, results){
        if (error) throw error;
        var count = results[0].count;
        connection.query(q2, function(error, results){
            if (error) throw error;
            var lastestUser = results[0].user_name;
        res.render("home", {data: count, lastestUser: lastestUser});
        });
    });
});


app.post('/add_user', function(req,res){
    var person = {user_name: req.body.username}; // user_name = column name in mysql
    connection.query('INSERT INTO users SET ?', person, function(err, result) {
    res.redirect("/home");
    });
});


app.post('/add_random_user', function(req,res){
    var person = {user_name: faker.internet.userName()}; 
    connection.query('INSERT INTO users SET ?', person, function(err, result) {
    res.redirect("/home");
    });
});





app.listen(8080, function (){
    console.log("App listening on port 8080");
});
