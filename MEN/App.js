const express = require('express')
const morgan = require('morgan')
const app= express()
const dbConnection = require('./config/db')
const userModel = require('./models/user')

app.use(morgan('dev'))

//build in middleware

app.use(express.json())
app.use(express.urlencoded({extended:true}))
app.use(express.static('public'))
app.set('view engine','ejs')


app.get('/',(req,res)=>{
    res.render('index')
})

app.get('/about',(req,res)=>{
    res.send("about page")
})

app.get('/profile',(req,res)=>{
    res.send("Profile page")
})

app.get('/register', (req,res)=>{
    res.render('register')
    
})
// CRUD =>{
// C-Create
// R-Read
// U-Update
// D-Delete}

//1-Create
app.post('/register', async(req,res)=>{
    
    const{username,email,password} = req.body

    const newUser = await userModel.create({
        username:username,
        email:email,
        password:password
    })
    
    res.send(newUser)
})


//2-Read
app.get('/get-users',(req,res)=>{
    userModel.find({a}).then((user)=>{
        res.send(user)
    })
})
//3-Update
app.get('/update-user',async(req,res)=>{
    await userModel.findOneAndUpdate({
        username:'a'
    },{
        email:'b@b.com'
    })
    res.send('user updated')
})
//4-Delete
app.get('/delete-user',async(req,res)=>{
    await userModel.findOneAndDelete({
        username:'a'
    })
    res.send("User Deleted")
})

app.post('/get-form-data',(req,res)=>{
    console.log(req.body);
    res.send('data recieved')
})
app.listen(3000)