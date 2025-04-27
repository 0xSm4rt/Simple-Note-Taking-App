# 📝 Simple Note Taking App

A lightweight command-line note-taking application for quickly capturing and organizing your thoughts.

## ✨ Features

- 📝 Create notes with titles and content
- 🏷️ Organize notes with tags
- 🔍 Search notes by content
- 📋 List and filter notes
- ✏️ Edit existing notes
- 🗑️ Delete notes you no longer need
- 📊 View tag statistics
- 📁 Store notes locally in JSON format

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xSm4rt/simple-notes.git
cd simple-notes
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <command> [options]
```

## ⚙️ Commands

- `new`: Create a new note
- `list`: List notes
- `view`: View a specific note
- `edit`: Edit a note
- `delete`: Delete a note
- `tags`: List all tags

## 📋 Command Options

### Create a note:
```bash
python main.py new <title> [options]
```

#### Options:

- `-c, --content`: Note content (if not provided, your default text editor will open)
- `-t, --tags`: Comma-separated list of tags

### List notes:
```bash
python main.py list [options]
```

#### Options:

- `-t, --tag`: Filter by tag
- `-s, --search`: Search term in title and content

### View a note:
```bash
python main.py view <id>
```

### Edit a note:
```bash
python main.py edit <id> [options]
```

#### Options:

- `-i, --title`: New title
- `-c, --content`: New content (if not provided, your default text editor will open)
- `-t, --tags`: New comma-separated list of tags
- `-a, --append`: Append content instead of replacing

### Delete a note:
```bash
python main.py delete <id>
```

### List tags:
```bash
python main.py tags
```

### Global options:

- `-f, --file`: Notes storage file (default: ~/.simple_notes.json)

