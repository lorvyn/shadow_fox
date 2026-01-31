"""
User Interface Module
GUI for the autocorrect keyboard system using tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from spell_checker import AutocorrectEngine
import threading
import time

class AutocorrectUI:
    """Main GUI application for autocorrect keyboard"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Autocorrect Keyboard System")
        self.root.geometry("900x600")
        
        # Initialize spell checker engine
        self.engine = AutocorrectEngine()
        
        # UI state variables
        self.autocorrect_enabled = tk.BooleanVar(value=True)
        self.highlight_errors = tk.BooleanVar(value=True)
        self.last_check_time = 0
        self.check_delay = 0.3  # Delay in seconds before checking
        self.pending_check = None
        self.current_suggestions = []
        self.suggestion_window = None
        
        # Setup UI
        self.setup_ui()
        
        # Bind events
        self.bind_events()
    
    def setup_ui(self):
        """Setup the user interface components"""
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Text", command=self.clear_text)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_checkbutton(
            label="Enable Autocorrect",
            variable=self.autocorrect_enabled,
            command=self.toggle_autocorrect
        )
        settings_menu.add_checkbutton(
            label="Highlight Errors",
            variable=self.highlight_errors,
            command=self.refresh_highlighting
        )
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Top toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            toolbar,
            text="✓ Autocorrect: ON | Highlight: ON",
            foreground="green"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Add word button
        self.add_word_btn = ttk.Button(
            toolbar,
            text="Add Word to Dictionary",
            command=self.add_word_to_dict
        )
        self.add_word_btn.pack(side=tk.RIGHT, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(
            toolbar,
            text="Clear Text",
            command=self.clear_text
        )
        clear_btn.pack(side=tk.RIGHT)
        
        # Text editor frame
        editor_frame = ttk.Frame(main_frame)
        editor_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
        self.text_widget = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            undo=True,
            maxundo=-1
        )
        self.text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for highlighting
        self.text_widget.tag_config("misspelled", underline=True, foreground="red")
        self.text_widget.tag_config("corrected", background="lightgreen")
        
        # Bottom info panel
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.info_label = ttk.Label(
            info_frame,
            text="Start typing... Errors will be highlighted in red.",
            font=("Arial", 9),
            foreground="gray"
        )
        self.info_label.pack(side=tk.LEFT)
        
        # Word count label
        self.word_count_label = ttk.Label(
            info_frame,
            text="Words: 0",
            font=("Arial", 9)
        )
        self.word_count_label.pack(side=tk.RIGHT)
    
    def bind_events(self):
        """Bind keyboard and mouse events"""
        # Text change events
        self.text_widget.bind('<KeyRelease>', self.on_text_change)
        self.text_widget.bind('<Button-3>', self.show_context_menu)  # Right click
        
        # Keyboard shortcuts
        self.text_widget.bind('<Control-z>', lambda e: self.text_widget.edit_undo())
        self.text_widget.bind('<Control-y>', lambda e: self.text_widget.edit_redo())
    
    def on_text_change(self, event):
        """Handle text changes with debouncing"""
        # Cancel any pending check
        if self.pending_check:
            self.root.after_cancel(self.pending_check)
        
        # Schedule a new check after delay
        self.pending_check = self.root.after(
            int(self.check_delay * 1000),
            self.check_spelling
        )
        
        # Update word count
        self.update_word_count()
    
    def check_spelling(self):
        """Check spelling of the current text"""
        if not self.autocorrect_enabled.get():
            return
        
        # Get current text
        text = self.text_widget.get("1.0", tk.END)
        
        # Clear previous highlighting
        self.text_widget.tag_remove("misspelled", "1.0", tk.END)
        
        if not self.highlight_errors.get():
            return
        
        # Process text in background to avoid UI freeze
        def process():
            errors = self.engine.process_text(text)
            self.root.after(0, lambda: self.highlight_errors_ui(errors))
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def highlight_errors_ui(self, errors):
        """Highlight misspelled words in the text widget"""
        for error in errors:
            start_idx = f"1.0+{error['start']}c"
            end_idx = f"1.0+{error['end']}c"
            
            # Apply misspelled tag
            self.text_widget.tag_add("misspelled", start_idx, end_idx)
            
            # Auto-correct if enabled and confident
            if error['auto_correct'] and self.autocorrect_enabled.get():
                # Get current word to verify it hasn't changed
                current_word = self.text_widget.get(start_idx, end_idx)
                if current_word == error['word']:
                    self.auto_replace_word(start_idx, end_idx, error['correction'])
    
    def auto_replace_word(self, start_idx, end_idx, correction):
        """Automatically replace a misspelled word"""
        # Delete the misspelled word
        self.text_widget.delete(start_idx, end_idx)
        
        # Insert the correction
        self.text_widget.insert(start_idx, correction)
        
        # Highlight the correction briefly
        new_end_idx = f"{start_idx}+{len(correction)}c"
        self.text_widget.tag_add("corrected", start_idx, new_end_idx)
        
        # Remove highlight after 2 seconds
        self.root.after(2000, lambda: self.text_widget.tag_remove("corrected", start_idx, new_end_idx))
    
    def show_context_menu(self, event):
        """Show context menu with suggestions on right-click"""
        # Get the clicked position
        index = self.text_widget.index(f"@{event.x},{event.y}")
        
        # Get the word at that position
        line, col = map(int, index.split('.'))
        line_text = self.text_widget.get(f"{line}.0", f"{line}.end")
        
        # Find word boundaries
        word, start, end = self.get_word_at_position(line_text, col)
        
        if not word:
            return
        
        # Check if word is misspelled
        if self.engine.is_valid_word(word):
            return
        
        # Get suggestions
        suggestions = self.engine.get_suggestions(word, max_suggestions=5)
        
        if not suggestions:
            return
        
        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        
        # Add suggestions
        for suggestion in suggestions:
            context_menu.add_command(
                label=suggestion,
                command=lambda s=suggestion, w=word, l=line, st=start, e=end: 
                    self.replace_word(l, st, e, s, w)
            )
        
        context_menu.add_separator()
        context_menu.add_command(
            label=f"Add '{word}' to dictionary",
            command=lambda: self.add_specific_word(word)
        )
        
        # Show menu
        context_menu.post(event.x_root, event.y_root)
    
    def get_word_at_position(self, line_text, col):
        """Extract word at given column position"""
        if col >= len(line_text):
            return "", 0, 0
        
        # Find word start
        start = col
        while start > 0 and (line_text[start - 1].isalpha() or line_text[start - 1] == "'"):
            start -= 1
        
        # Find word end
        end = col
        while end < len(line_text) and (line_text[end].isalpha() or line_text[end] == "'"):
            end += 1
        
        word = line_text[start:end]
        return word, start, end
    
    def replace_word(self, line, start, end, suggestion, original):
        """Replace a word with suggestion"""
        start_idx = f"{line}.{start}"
        end_idx = f"{line}.{end}"
        
        # Delete old word
        self.text_widget.delete(start_idx, end_idx)
        
        # Insert suggestion
        self.text_widget.insert(start_idx, suggestion)
        
        # Record correction for learning
        self.engine.record_correction(original, suggestion)
        
        # Highlight briefly
        new_end_idx = f"{start_idx}+{len(suggestion)}c"
        self.text_widget.tag_add("corrected", start_idx, new_end_idx)
        self.root.after(2000, lambda: self.text_widget.tag_remove("corrected", start_idx, new_end_idx))
        
        # Recheck spelling
        self.check_spelling()
    
    def add_word_to_dict(self):
        """Add selected word to custom dictionary"""
        try:
            selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                self.add_specific_word(selected_text.strip())
        except tk.TclError:
            messagebox.showinfo(
                "No Selection",
                "Please select a word to add to the dictionary."
            )
    
    def add_specific_word(self, word):
        """Add a specific word to dictionary"""
        if word and word.isalpha():
            self.engine.add_to_dictionary(word)
            messagebox.showinfo(
                "Word Added",
                f"'{word}' has been added to your custom dictionary."
            )
            self.check_spelling()  # Recheck to remove highlighting
    
    def clear_text(self):
        """Clear all text"""
        if messagebox.askyesno("Clear Text", "Are you sure you want to clear all text?"):
            self.text_widget.delete("1.0", tk.END)
            self.update_word_count()
    
    def toggle_autocorrect(self):
        """Toggle autocorrect on/off"""
        self.update_status_label()
        if self.autocorrect_enabled.get():
            self.check_spelling()
    
    def refresh_highlighting(self):
        """Refresh error highlighting"""
        self.update_status_label()
        if self.highlight_errors.get():
            self.check_spelling()
        else:
            self.text_widget.tag_remove("misspelled", "1.0", tk.END)
    
    def update_status_label(self):
        """Update the status label"""
        ac_status = "ON" if self.autocorrect_enabled.get() else "OFF"
        hl_status = "ON" if self.highlight_errors.get() else "OFF"
        
        color = "green" if self.autocorrect_enabled.get() else "orange"
        
        self.status_label.config(
            text=f"✓ Autocorrect: {ac_status} | Highlight: {hl_status}",
            foreground=color
        )
    
    def update_word_count(self):
        """Update word count display"""
        text = self.text_widget.get("1.0", tk.END)
        words = text.split()
        self.word_count_label.config(text=f"Words: {len(words)}")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Autocorrect Keyboard",
            "Autocorrect Keyboard System v1.0\n\n"
            "A real-time spell checker and autocorrect tool.\n\n"
            "Features:\n"
            "• Real-time spell checking\n"
            "• Smart autocorrection\n"
            "• Custom dictionary support\n"
            "• Learning from corrections\n\n"
            "Powered by pyspellchecker library"
        )


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = AutocorrectUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
