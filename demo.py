#!/usr/bin/env python3
"""
Demo script for Alphabet Learning App
This script demonstrates the app's features and provides usage examples
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def show_demo_info():
    """Show demo information about the app"""
    info = """
🎓 ALPHABET LEARNING APP - DEMO

🌟 FEATURES DEMONSTRATED:

📚 Learning Mode:
• Large letter display (A-Z)
• Word associations (A for Apple)
• Emoji visuals (🍎, ⚽, 🐱)
• Text-to-speech pronunciation
• Navigation with buttons/keys
• Progress tracking

🎯 Quiz Mode:
• Interactive multiple choice questions
• 3 question types:
  - Letter to word matching
  - Word to letter matching  
  - Emoji to letter matching
• Real-time scoring
• Encouraging feedback
• Auto-advance through alphabet

🖼️ Image Support:
• Custom images for each letter
• Automatic image loading
• Fallback to emojis
• Auto-resize functionality

⌨️ Controls:
• Arrow keys: Navigate
• Spacebar: Hear pronunciation
• Q key: Toggle quiz mode
• Mouse: Click buttons

🚀 GETTING STARTED:
1. Run: python main.py
2. Try Learning Mode first
3. Press 'Q' to try Quiz Mode
4. Add images to 'images/' folder
5. Explore all features!

💡 TIPS:
• Use arrow keys for quick navigation
• Press spacebar to hear pronunciation
• Try quiz mode to test knowledge
• Add your own images for customization
"""
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create a custom dialog
    dialog = tk.Toplevel(root)
    dialog.title("🎓 Alphabet Learning App - Demo")
    dialog.geometry("600x500")
    dialog.configure(bg="#FFE5E5")
    
    # Center the dialog
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
    y = (dialog.winfo_screenheight() // 2) - (500 // 2)
    dialog.geometry(f"600x500+{x}+{y}")
    
    # Make dialog modal
    dialog.transient(root)
    dialog.grab_set()
    
    # Title
    title_label = tk.Label(
        dialog,
        text="🎓 Alphabet Learning App - Demo",
        font=("Comic Sans MS", 18, "bold"),
        bg="#FFE5E5",
        fg="#FF6B9D"
    )
    title_label.pack(pady=20)
    
    # Info text
    text_widget = tk.Text(
        dialog,
        wrap=tk.WORD,
        font=("Consolas", 10),
        bg="white",
        fg="#333333",
        relief="solid",
        borderwidth=1,
        padx=10,
        pady=10
    )
    text_widget.pack(expand=True, fill="both", padx=20, pady=10)
    text_widget.insert("1.0", info)
    text_widget.config(state="disabled")  # Make read-only
    
    # Buttons frame
    button_frame = tk.Frame(dialog, bg="#FFE5E5")
    button_frame.pack(pady=20)
    
    def launch_app():
        dialog.destroy()
        root.destroy()
        try:
            import main
            main.main()
        except ImportError:
            messagebox.showerror("Error", "Could not launch the main app. Make sure main.py is in the same directory.")
    
    def close_demo():
        dialog.destroy()
        root.destroy()
    
    # Launch button
    launch_button = tk.Button(
        button_frame,
        text="🚀 Launch App",
        font=("Comic Sans MS", 14, "bold"),
        bg="#4A90E2",
        fg="white",
        relief="raised",
        borderwidth=3,
        padx=20,
        pady=10,
        cursor="hand2",
        command=launch_app
    )
    launch_button.pack(side="left", padx=10)
    
    # Close button
    close_button = tk.Button(
        button_frame,
        text="❌ Close",
        font=("Comic Sans MS", 14, "bold"),
        bg="#FF6B9D",
        fg="white",
        relief="raised",
        borderwidth=3,
        padx=20,
        pady=10,
        cursor="hand2",
        command=close_demo
    )
    close_button.pack(side="left", padx=10)
    
    # Bind Enter key to launch
    dialog.bind("<Return>", lambda e: launch_app())
    dialog.bind("<Escape>", lambda e: close_demo())
    
    # Focus on dialog
    dialog.focus_set()
    
    # Start the dialog
    dialog.mainloop()

def check_dependencies():
    """Check if all dependencies are available"""
    missing = []
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter")
    
    try:
        import PIL
    except ImportError:
        missing.append("Pillow")
    
    try:
        import pyttsx3
    except ImportError:
        missing.append("pyttsx3")
    
    if missing:
        print("❌ Missing dependencies:", ", ".join(missing))
        print("💡 Run: python install.py")
        return False
    
    return True

def main():
    """Main demo function"""
    print("🎓 Alphabet Learning App - Demo")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py not found in current directory")
        return
    
    print("✅ All dependencies found!")
    print("🚀 Launching demo...")
    
    # Show demo info
    show_demo_info()

if __name__ == "__main__":
    main() 