notes = {'1': '12123', '2': '123123'}

def get_note(id):
    if id in notes:
        return notes[id]
    return notes

def save_note(id, note):
    notes[id] = note

def get_notes():
    return notes

def delete_note(id):
    notes.pop(id)
