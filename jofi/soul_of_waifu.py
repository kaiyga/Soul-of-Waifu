print('''
   _____             __         ____   _       __      _ ____     
  / ___/____  __  __/ /  ____  / __/  | |     / ____ _(_/ ____  __
  \__ \/ __ \/ / / / /  / __ \/ /_    | | /| / / __ `/ / /_/ / / /
 ___/ / /_/ / /_/ / /  / /_/ / __/    | |/ |/ / /_/ / / __/ /_/ / 
/____/\____/\__,_/_/   \____/_/       |__/|__/\__,_/_/_/  \__,_/  
                                                                                          
                                                         [by jofi]
''')
import os
import asyncio
import time
import sounddevice as sd


import keyboard
from whisper_mic import WhisperMic
from gpytranslate import Translator


from characterai import PyAsyncCAI
from elevenlabs import generate, set_api_key, play
import torch


set_api_key("API-ключ от ElevenLabs") #Сюда надо ввести API с сайта ElevenLabs
cAI_client = PyAsyncCAI('API-ключ от Character AI') #Сюда надо ввести API с сайта Character AI
cAI_character = 'ID персонажа Character AI' #Сюда надо ввести ID персонажа с Character AI, с которым вы будете разговаривать

language = 'ru' #Выбираете язык модели
model_id = 'v4_ru' #Выбираете модель и вписываете её ID
local_file = 'model.pt'
pyTorch_device = torch.device('cpu')
torch.set_num_threads(12) #Число потоков вашего процессора

speaker = 'baya' #Все голоса: 'aidar', 'baya', 'kseniya', 'xenia', 'random'
sample_rate = 48000 #Все частоты дискретизации: '8000', '24000', '48000'
put_accent=True
put_yo=True

voice = "Penelope" #Тут вы выбираете голос для TTS от EleveneLabs

if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                   local_file)  

async def main():
    mode = input("Выбери технологию Text-To-Speech (1 - ElevenLabs, 2 - Silero TTS (Только персонаж), 3 - Silero TTS (Персонаж и пользователь)): ")
    if mode == '1':
        print("Нажми ПРАВЫЙ SHIFT, чтобы запустить программу...")
        while True:
            if keyboard.is_pressed('RIGHT_SHIFT'):
                while True:
                    t = Translator()
                    chat = await cAI_client.chat2.get_chat(cAI_character)
                    author = {'author_id': chat['chats'][0]['creator_id']}
                    mic = WhisperMic(model='small', english=False, energy=300, pause=1, mic_index=1)
                    print("Запись пошла, говорите...")
                    msg1 = mic.listen()
                    messageC = msg1
                    print("Ты сказал:", msg1)
                    async with cAI_client.connect() as chat2:
                        data = await chat2.send_message(
                            cAI_character, chat['chats'][0]['chat_id'],
                            messageC, author
                        )
                    textil = data['turn']['candidates'][0]['raw_content']
                    translation = await t.translate(textil, targetlang="ru") #Язык, на который будут переводиться слова
                    audio = generate(
                        text = translation.text,
                        voice = voice,
                        model = "eleven_multilingual_v2",
                    )
                    print(f"Персонаж ответил: {translation.text}")
                    play(audio)
                    
                
    elif mode == '2':
        print("Нажми ПРАВЫЙ SHIFT, чтобы записать голос")
        while True:
            if keyboard.is_pressed('RIGHT_SHIFT'):
                while True:
                    t = Translator()
                    

                    # INIT chrAI 
                    chat = await cAI_client.chat2.get_chat(cAI_character)
                    author = {'author_id': chat['chats'][0]['creator_id']}
                    
                    # Init Input Mic Interface 
                    mic = WhisperMic(model='small', english=False, energy=300, pause=1, mic_index=1)
                    print("Запись пошла, говорите...")
                    # Use Input interface
                    msg1 = mic.listen()
                    messageC = msg1
                    print("Ты сказал:", msg1)


                    # Send to AI
                    async with cAI_client.connect() as chat2:
                        data = await chat2.send_message(
                            cAI_character, chat['chats'][0]['chat_id'],
                            msg1, author
                        )
                    textil = data['turn']['candidates'][0]['raw_content']
                    translation = await t.translate(textil, targetlang="ru") #Язык, на который будут переводиться слова
                    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
                    model.to(pyTorch_device)
                    audio = model.apply_tts(text=translation.text,
                                            speaker=speaker,
                                            sample_rate=sample_rate,
                                            put_accent=put_accent,
                                            put_yo=put_yo)
                    print(f"Персонаж ответил: {translation.text}")
                    sd.play(audio, sample_rate)
                    time.sleep(len(audio) / sample_rate)
                    sd.stop()
    
    elif mode == '3':
        print("Нажми ПРАВЫЙ SHIFT, чтобы записать голос")
        while True:
            if keyboard.is_pressed('RIGHT_SHIFT'):
                while True:
                    t = Translator() # Translator Inteface 

                    # Init AI Chat

                    chat = await cAI_client.chat2.get_chat(cAI_character)
                    author = {'author_id': chat['chats'][0]['creator_id']}

                    # Init Input Interface 
                    mic = WhisperMic(model='small', english=False, energy=300, pause=1, mic_index=1)

                    # Use Input -> Str
                    print("Запись пошла, говорите...")
                    msg1 = mic.listen()

                    print("Ты сказал:", msg1)

                    # Translate Str

                    translation = await t.translate(msg1, targetlang='en') #Язык, на который будут переводиться слова
                    translation_text = translation.text

                    # Send Translated text to AI chat 

                    async with cAI_client.connect() as chat2:
                        data = await chat2.send_message(
                            cAI_character, chat['chats'][0]['chat_id'],
                            translation_text, author
                        )

                    # Response AI Chat Answer 
                    textil = data['turn']['candidates'][0]['raw_content']
                    translation = await t.translate(textil, targetlang='ru') #Язык, на который будут переводиться слова
                    translation_text = translation.text

                    # Get Audio of Answer 
                    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
                    model.to(pyTorch_device)
                    audio = model.apply_tts(text=translation_text,
                                            speaker=speaker,
                                            sample_rate=sample_rate,
                                            put_accent=put_accent,
                                            put_yo=put_yo)
                    

                    print(f"Персонаж ответил: {translation_text}")

                    # Play Audio
                    sd.play(audio, sample_rate)
                    time.sleep(len(audio) / sample_rate)
                    sd.stop()                

asyncio.run(main())
