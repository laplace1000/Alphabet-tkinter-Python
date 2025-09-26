# 🎓 Alphabet Learning App for Kids

A fun and interactive Python application designed to help children learn the alphabet through visual, audio, and interactive learning experiences!

## 🌟 Features

### 📚 Learning Mode
- **🎯 Single Letter Focus**: Each screen displays one letter in large, bold font
- **🖼️ Visual Learning**: Each letter paired with a word, emoji, and optional image
- **🔊 Audio Pronunciation**: Text-to-speech functionality says "A for Apple"
- **⏩ Easy Navigation**: Next and Previous buttons with keyboard support
- **🎨 Kid-Friendly UI**: Colorful design with large fonts and simple layout
- **📊 Progress Tracking**: Shows current position (e.g., "Letter 5 of 26")

### 🎯 Quiz Mode (NEW!)
- **🧠 Interactive Questions**: Multiple choice questions about letters and words
- **📝 Question Types**: 
  - "What word starts with letter A?"
  - "What letter does 'Apple' start with?"
  - "What letter does this emoji represent? 🍎"
- **🏆 Score Tracking**: Real-time score display and final results
- **🎉 Encouraging Feedback**: Positive messages for correct answers
- **🔄 Auto-Advance**: Automatically moves to next letter after answering

### 🖼️ Image Support (NEW!)
- **📁 Images Directory**: Automatically creates `images/` folder
- **🖼️ Custom Images**: Add PNG files named `a.png`, `b.png`, etc.
- **🔄 Fallback System**: Shows emoji if image not found
- **📐 Auto-Resize**: Images automatically resize to fit display

### ⌨️ Enhanced Controls
- **Arrow Keys**: Navigate between letters
- **Spacebar/Enter**: Hear pronunciation
- **Q Key**: Toggle between Learning and Quiz modes
- **Mouse**: Click buttons for easy interaction

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Quick Setup

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd Alphabet
   ```

2. **Run the installation script**
   ```bash
   python install.py
   ```

3. **Launch the application**
   ```bash
   python main.py
   ```

### Alternative Setup

1. **Install dependencies manually**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   python main.py
   ```

### Platform-Specific Launchers
- **Windows**: Double-click `run_app.bat`
- **macOS/Linux**: Run `./run_app.sh`

## 🎮 How to Use

### Learning Mode
- **Navigation**: Use Previous/Next buttons or arrow keys
- **Pronunciation**: Click "Say It!" or press spacebar
- **Auto-Speech**: Each letter is spoken when you navigate to it
- **Progress**: See your current position in the alphabet

### Quiz Mode
- **Toggle**: Click "🎯 Quiz Mode" button or press 'Q'
- **Answer**: Click on the correct answer from multiple choices
- **Feedback**: Get immediate feedback on your answers
- **Scoring**: Track your progress with real-time score
- **Completion**: Get final results when you finish all letters

### Adding Images
1. **Create images folder** (automatically created)
2. **Add PNG files** named `a.png`, `b.png`, `c.png`, etc.
3. **Restart the app** to see your images

## 📁 Project Structure

```
Alphabet/
├── main.py              # Main application with all features
├── requirements.txt     # Python dependencies
├── README.md           # This documentation
├── install.py          # Automated installation script
├── run_app.bat         # Windows launcher
├── run_app.sh          # macOS/Linux launcher
└── images/             # Custom images folder (auto-created)
    ├── a.png           # Apple image
    ├── b.png           # Ball image
    └── ...             # More images
```

## 🎨 Customization

### Adding Custom Images
1. **Find or create images** for each letter
2. **Name them correctly**: `a.png`, `b.png`, `c.png`, etc.
3. **Place in images folder**: The app will automatically load them
4. **Supported formats**: PNG, JPG, GIF (PNG recommended)

### Modifying Content
- **Change words**: Edit the `alphabet_data` list in `main.py`
- **Adjust speech rate**: Modify the `rate` property in `init_text_to_speech()`
- **Customize colors**: Change color codes in the UI setup
- **Add new question types**: Extend the quiz system

### Quiz Customization
- **Question types**: Modify `question_types` list in `generate_quiz_question()`
- **Scoring thresholds**: Adjust percentage thresholds in `check_answer()`
- **Feedback messages**: Customize success/failure messages

## 🔧 Troubleshooting

### Text-to-Speech Issues
- **Windows**: Should work out of the box
- **macOS**: May need to install additional speech synthesis
- **Linux**: Install `espeak` or `festival`:
  ```bash
  sudo apt-get install espeak  # Ubuntu/Debian
  ```

### Image Loading Issues
- **Check file names**: Must be lowercase (a.png, not A.png)
- **Verify format**: Use PNG format for best compatibility
- **Check permissions**: Ensure images are readable
- **Restart app**: Images are loaded when app starts

### Import Errors
If you get import errors, make sure all packages are installed:
```bash
pip install Pillow pyttsx3
```

## 🎯 Learning Objectives

This project teaches:
- **Tkinter GUI Development**: Creating complex user interfaces
- **Text-to-Speech**: Using `pyttsx3` for audio output
- **Event Handling**: Button clicks, keyboard events, and mode switching
- **Data Management**: Working with structured data and random selection
- **Image Processing**: Loading and displaying images with PIL
- **User Experience**: Designing engaging, educational interfaces
- **Error Handling**: Graceful fallbacks and user feedback

## 🚀 Future Enhancements

- [x] **Quiz Mode** - Interactive learning with questions
- [x] **Image Support** - Custom images for each letter
- [x] **Enhanced UI** - Better layout and visual design
- [ ] **Sound Effects** - Background music and audio feedback
- [ ] **Letter Tracing** - Interactive writing practice
- [ ] **Multiple Languages** - Support for different alphabets
- [ ] **Progress Saving** - Remember user progress
- [ ] **Difficulty Levels** - Easy, medium, hard quiz modes
- [ ] **Achievement System** - Badges and rewards
- [ ] **Parent Dashboard** - Track learning progress

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to contribute by:
- Adding new features and quiz types
- Improving the UI design and animations
- Adding more educational content
- Creating custom image sets
- Fixing bugs and improving performance
- Adding support for more languages

## 🎓 Educational Value

This app is designed to help children:
- **Learn letter recognition** through visual and audio cues
- **Build vocabulary** by associating letters with words
- **Practice memory** through interactive quiz questions
- **Develop confidence** with positive feedback and scoring
- **Engage with technology** in an educational way

---

**Happy Learning! 🎓✨** 