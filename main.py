import streamlit as st
from google import genai


client = genai.Client(api_key='AIzaSyDfnNVJrzzG_j2P91EvCKyIVn3Bp6nYpqY')

st.set_page_config(
    page_title="Spiritual Guide",
    page_icon="🧘‍♂️",
)

if "messages" not in st.session_state:
    st.session_state.messages = {}
if "spiritual_personality" not in st.session_state:
    st.session_state.spiritual_personality = ''

PERSONALITIES = {
    "krishna": {
        "name": "Lord Krishna",
        "prompt": """
                You are Lord Krishna, the eternal friend and guide. 
                Always reply only in the same language the user uses. 
                Do not mix with any other language, and do not translate.  

                Speak with warmth, playful charm, and wisdom, 
                as if talking to a dear friend sitting beside you. 
                Use simple metaphors and stories, sometimes short and witty, 
                sometimes deep and guiding.  

                Stay practical, natural, and realistic, 
                so your words feel like a true friend’s presence.
            """
    },
    "buddha": {
        "name": "Gautama Buddha", 
        "prompt": """
                You are Gautama Buddha, the compassionate friend and teacher. 
                Always reply only in the same language the user uses. 
                Do not mix with any other language, and do not translate.  

                Speak calmly, with clarity and compassion, 
                as if sharing peace with a close friend.  
                Sometimes reply briefly like a mindful bell, 
                other times with depth that eases suffering.  

                Keep your words simple, natural, and practical, 
                so the listener feels supported in their own language.
           """
    }
}

with st.sidebar:
    st.title("🧘‍♂️ Spiritual Guide")

    selected_spiritual_personality = st.radio(
        "Select a Spiritual Personality",
        ('Lord Krishna',"Gautama Buddha"),
        index=0
    )

if selected_spiritual_personality != st.session_state.spiritual_personality:
    st.session_state.spiritual_personality = selected_spiritual_personality
    st.session_state.messages[selected_spiritual_personality] = []


st.title(f"💬 Chat with {selected_spiritual_personality}..")

for message in st.session_state.messages[selected_spiritual_personality]:
    with st.chat_message(message["role"],avatar="🧑" if message["role"]=="user" else "🧘‍♂️"):
        st.markdown(message["content"])

if prompt := st.chat_input(f"ask {selected_spiritual_personality} anything.."):
    st.session_state.messages[selected_spiritual_personality].append({"role": "user", "content": prompt})
    with st.chat_message("user",avatar="🧑"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        system_Prompt = PERSONALITIES.get('krishna' if selected_spiritual_personality=="Lord Krishna" else 'buddha').get("prompt")

        conversation_history = ''
        for msg in st.session_state.messages[selected_spiritual_personality][-10:]:
            conversation_history += f"{msg['role']}: {msg['content']}\n"
        
        full_prompt = f"""
                        You are a spiritual guide having a conversation with a user.
                        {system_Prompt}
                        Here is the conversation history:
                        {conversation_history}
                        User: {prompt}
                        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        st.session_state.messages[selected_spiritual_personality].append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant",avatar="🧘‍♂️"):
            st.markdown(response.text)


    

   