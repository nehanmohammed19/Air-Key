// server.js

const express = require('express');
const path = require('path');
const app = express();
const mongoose = require('mongoose');
const { access } = require('fs');
const port = process.env.PORT || 3000;


// Serve static files from the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// Route to serve the HTML file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/data', async (req, res) => {
  try {
      const users = await User.find({}, { _id: 0, name: 1, passwordSequence: 1 });
      res.json(users);
  } catch (err) {
      res.status(500).json({ error: err.message });
  }
});


const mongoURI = 'mongodb+srv://thecargaming:notpassword@cluster0.jepcu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';

mongoose.connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));


const UserSchema = new mongoose.Schema({
    name: String,
    passwordSequence: [Number]
});

const User = mongoose.model('User', UserSchema);

// API endpoint to register a user
app.use(express.json());  // This line must be above route handlers

// Debugging middleware to log the request body
app.use((req, res, next) => {
    console.log('Request Body:', req.body);  // Log the parsed request body
    next();  // Proceed to the next middleware or route
});

// Your POST route
app.post('/api/register', async (req, res) => {
    const {name, passwordSequence } = req.body;  // Extract passwordSequence from req.body
    console.log('passwordSequence:', passwordSequence);  // Log the passwordSequence

    if (!passwordSequence) {
        return res.status(400).json({ message: 'Password sequence is required' });
    }

    try {
        // Save the password sequence to the database
        const newUser = new User({name, passwordSequence });
        await newUser.save();
        res.status(201).json({ message: 'Password saved successfully!' });
    } catch (error) {
        res.status(500).json({ message: 'Error saving user', error });
    }
});




// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
