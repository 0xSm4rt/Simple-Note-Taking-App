#!/usr/bin/env python3

import argparse
import json
import os
import sys
import tempfile
import subprocess
from datetime import datetime

# Constants
DEFAULT_NOTES_FILE = os.path.expanduser("~/.simple_notes.json")

def load_notes(notes_file=DEFAULT_NOTES_FILE):
    """Load notes from file"""
    if os.path.exists(notes_file):
        try:
            with open(notes_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {notes_file} is corrupted")
            return []
    return []

def save_notes(notes, notes_file=DEFAULT_NOTES_FILE):
    """Save notes to file"""
    try:
        directory = os.path.dirname(notes_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(notes_file, 'w') as f:
            json.dump(notes, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving notes: {e}")
        return False

def create_note(title, content=None, tags=None, notes_file=DEFAULT_NOTES_FILE):
    """Create a new note"""
    notes = load_notes(notes_file)
    
    # Generate a unique ID
    note_id = 1
    if notes:
        note_id = max(note["id"] for note in notes) + 1
    
    # Get content from editor if not provided
    if content is None:
        content = open_editor()
    
    # Parse tags
    if tags is None:
        tags = []
    elif isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    # Create note
    note = {
        "id": note_id,
        "title": title,
        "content": content,
        "tags": tags,
        "created": datetime.now().isoformat(),
        "modified": datetime.now().isoformat()
    }
    
    notes.append(note)
    
    if save_notes(notes, notes_file):
        print(f"Note created: #{note_id} - {title}")
        return note_id
    return None

def open_editor(initial_text=""):
    """Open the default text editor and return the edited text"""
    # Determine which editor to use
    editor = os.environ.get('EDITOR', 'vim')
    if sys.platform.startswith('win'):
        editor = os.environ.get('EDITOR', 'notepad')
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp:
        temp_filename = temp.name
        temp.write(initial_text.encode())
    
    try:
        # Open the editor
        subprocess.run([editor, temp_filename], check=True)
        
        # Read the edited content
        with open(temp_filename, 'r') as f:
            return f.read()
    finally:
        # Clean up the temporary file
        os.unlink(temp_filename)

def list_notes(tag=None, search=None, notes_file=DEFAULT_NOTES_FILE):
    """List all notes, optionally filtered by tag or search term"""
    notes = load_notes(notes_file)
    
    if not notes:
        print("No notes found")
        return
    
    # Filter notes
    filtered_notes = notes
    if tag:
        filtered_notes = [note for note in filtered_notes if tag in note["tags"]]
    
    if search:
        search = search.lower()
        filtered_notes = [note for note in filtered_notes if 
                         search in note["title"].lower() or 
                         search in note["content"].lower()]
    
    if not filtered_notes:
        if tag and search:
            print(f"No notes found with tag '{tag}' and search term '{search}'")
        elif tag:
            print(f"No notes found with tag '{tag}'")
        elif search:
            print(f"No notes found containing '{search}'")
        return
    
    # Sort notes by creation date (newest first)
    filtered_notes.sort(key=lambda x: x["created"], reverse=True)
    
    print("\nNotes:")
    print("=" * 50)
    for note in filtered_notes:
        tags_str = ", ".join(note["tags"]) if note["tags"] else "No tags"
        created = datetime.fromisoformat(note["created"]).strftime("%Y-%m-%d %H:%M")
        
        # Truncate content for display
        content_preview = note["content"].replace("\n", " ")
        if len(content_preview) > 50:
            content_preview = content_preview[:47] + "..."
        
        print(f"#{note['id']} - {note['title']}")
        print(f"  Tags: {tags_str}")
        print(f"  Created: {created}")
        print(f"  Preview: {content_preview}")
        print("-" * 50)
    
    print(f"Total: {len(filtered_notes)} notes")

def view_note(note_id, notes_file=DEFAULT_NOTES_FILE):
    """View a specific note"""
    notes = load_notes(notes_file)
    
    # Find the note
    for note in notes:
        if note["id"] == note_id:
            tags_str = ", ".join(note["tags"]) if note["tags"] else "No tags"
            created = datetime.fromisoformat(note["created"]).strftime("%Y-%m-%d %H:%M")
            modified = datetime.fromisoformat(note["modified"]).strftime("%Y-%m-%d %H:%M")
            
            print("\n" + "=" * 50)
            print(f"#{note['id']} - {note['title']}")
            print("=" * 50)
            print(f"Tags: {tags_str}")
            print(f"Created: {created}")
            print(f"Modified: {modified}")
            print("-" * 50)
            print(note["content"])
            print("=" * 50)
            return True
    
    print(f"Note #{note_id} not found")
    return False

def edit_note(note_id, title=None, content=None, tags=None, append=False, notes_file=DEFAULT_NOTES_FILE):
    """Edit an existing note"""
    notes = load_notes(notes_file)
    
    # Find the note
    for note in notes:
        if note["id"] == note_id:
            # Update title if provided
            if title is not None:
                note["title"] = title
            
            # Update content
            if content is not None:
                if append:
                    note["content"] += "\n\n" + content
                else:
                    note["content"] = content
            elif content is None and not append:
                # Open editor with existing content
                note["content"] = open_editor(note["content"])
            
            # Update tags if provided
            if tags is not None:
                if isinstance(tags, str):
                    tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
                note["tags"] = tags
            
            # Update modification time
            note["modified"] = datetime.now().isoformat()
            
            if save_notes(notes, notes_file):
                print(f"Note #{note_id} updated")
                return True
            return False
    
    print(f"Note #{note_id} not found")
    return False

def delete_note(note_id, notes_file=DEFAULT_NOTES_FILE):
    """Delete a note"""
    notes = load_notes(notes_file)
    
    # Find the note
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            del notes[i]
            if save_notes(notes, notes_file):
                print(f"Note #{note_id} deleted")
                return True
            return False
    
    print(f"Note #{note_id} not found")
    return False

def list_tags(notes_file=DEFAULT_NOTES_FILE):
    """List all unique tags"""
    notes = load_notes(notes_file)
    
    if not notes:
        print("No notes found")
        return
    
    # Collect all tags
    all_tags = {}
    for note in notes:
        for tag in note["tags"]:
            if tag in all_tags:
                all_tags[tag] += 1
            else:
                all_tags[tag] = 1
    
    if not all_tags:
        print("No tags found")
        return
    
    # Sort tags by frequency
    sorted_tags = sorted(all_tags.items(), key=lambda x: (-x[1], x[0]))
    
    print("\nTags:")
    print("=" * 30)
    for tag, count in sorted_tags:
        print(f"{tag} ({count} notes)")
    print("=" * 30)
    print(f"Total: {len(sorted_tags)} unique tags")

def main():
    parser = argparse.ArgumentParser(description="Simple Note Taking App")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create note command
    create_parser = subparsers.add_parser("new", help="Create a new note")
    create_parser.add_argument("title", help="Note title")
    create_parser.add_argument("-c", "--content", help="Note content (if not provided, editor will open)")
    create_parser.add_argument("-t", "--tags", help="Comma-separated list of tags")
    
    # List notes command
    list_parser = subparsers.add_parser("list", help="List notes")
    list_parser.add_argument("-t", "--tag", help="Filter by tag")
    list_parser.add_argument("-s", "--search", help="Search term in title and content")
    
    # View note command
    view_parser = subparsers.add_parser("view", help="View a note")
    view_parser.add_argument("id", type=int, help="Note ID")
    
    # Edit note command
    edit_parser = subparsers.add_parser("edit", help="Edit a note")
    edit_parser.add_argument("id", type=int, help="Note ID")
    edit_parser.add_argument("-i", "--title", help="New title")
    edit_parser.add_argument("-c", "--content", help="New content (if not provided, editor will open)")
    edit_parser.add_argument("-t", "--tags", help="New comma-separated list of tags")
    edit_parser.add_argument("-a", "--append", action="store_true", help="Append content instead of replacing")
    
    # Delete note command
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("id", type=int, help="Note ID")
    
    # List tags command
    tags_parser = subparsers.add_parser("tags", help="List all tags")
    
    # Global options
    parser.add_argument("-f", "--file", default=DEFAULT_NOTES_FILE, 
                       help=f"Notes storage file (default: {DEFAULT_NOTES_FILE})")
    
    args = parser.parse_args()
    
    if args.command == "new":
        create_note(args.title, args.content, args.tags, args.file)
    
    elif args.command == "list":
        list_notes(args.tag, args.search, args.file)
    
    elif args.command == "view":
        view_note(args.id, args.file)
    
    elif args.command == "edit":
        edit_note(args.id, args.title, args.content, args.tags, args.append, args.file)
    
    elif args.command == "delete":
        delete_note(args.id, args.file)
    
    elif args.command == "tags":
        list_tags(args.file)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
