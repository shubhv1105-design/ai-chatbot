from ollama import chat
import database

database.init_db()

print("=== Chatbot ===")
print("1. New conversation")
print("2. Load past conversation")
choice = input("Choose (1 or 2): ")

if choice == "2":
    conversations = database.list_conversations()
    if not conversations:
        print("No past conversations found. Starting a new one.\n")
        conversation_id = database.create_conversation()
        conversation = []
    else:
        for conv_id, created_at in conversations:
            print(f"[{conv_id}] started at {created_at}")
        conversation_id = int(input("Enter conversation ID to load: "))
        conversation = database.load_conversation(conversation_id)
        print("\n--- Conversation history ---")
        for msg in conversation:
            print(f"{msg['role']}: {msg['content']}")
        print("--- End of history ---\n")
else:
    conversation_id = database.create_conversation()
    conversation = []

print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    conversation.append({'role': 'user', 'content': user_input})
    database.save_message(conversation_id, 'user', user_input)

    response = chat(model='gemma3', messages=conversation)
    reply = response['message']['content']
    print(f"Bot: {reply}\n")

    conversation.append({'role': 'assistant', 'content': reply})
    database.save_message(conversation_id, 'assistant', reply)