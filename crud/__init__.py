# Hier wirlich nur CRUD von der Datenbank! keine Logik!
from .user import create_user, get_user, get_user_by_email, update_user, delete_user
from .user_settings import update_user_settings, create_user_settings, get_user_settings
from .deck import create_deck, update_deck, delete_deck, get_deck
from .flashcard_media import create_flashcard_media, update_flashcard_media, get_flashcard_media, delete_flashcard_media
from .flashcard_state import create_flashcard_state, get_flashcard_state, update_flashcard_state, delete_flashcard_state
from .flashcard import create_flashcard, get_flashcard, update_flashcard, delete_flashcard
from .review import create_review, get_review, update_review, delete_review
from .tag import create_tag, get_tag, update_tag, delete_tag