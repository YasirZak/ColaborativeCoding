const express=require("express")
const app=express()
const bodyP=require("body-parser")
app.use(bodyP.json())
app.use("static/js/codemirror",express.static("E:/ColaborativeCoding/static/js/codemirror"))
app.get("/",function(req,res){
    res.sendFile("E:/ColaborativeCoding/templates/index.html")
})
app.listen(8000)

    

