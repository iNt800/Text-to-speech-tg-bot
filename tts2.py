import torch
import sounddevice as sd
import time
import telebot

sp = None
text = None

def speak(speech, tof, sp):
    
    language = 'ru'
    model_id = 'ru_v3'
    sample_rate = 48000
    speaker = sp
    put_accent = True 
    put_yo = True
    device = torch.device('cpu')
    text = speech

    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                            model='silero_tts',
                            language=language,
                            speaker=model_id)
    model.to(device)

    audio = model.apply_tts(text=text,
                                speaker=speaker,
                                sample_rate=sample_rate,
                                put_accent=put_accent,
                                put_yo=put_yo)
    
    if tof == True:
        model.save_wav(text=text,
                                speaker=speaker,
                                sample_rate=sample_rate)
        pass
    elif tof == False:
        pass
    
    else:
        print('the second parameter takes the values true or false')
        pass
    
bot = telebot.TeleBot('?')
    
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Это бот для преобразования текста в речь! Введите команду /help чтобы узнать существующие команды.')

@bot.message_handler(commands=['speak_text'])
def edit_text(message):
    bot.send_message(message.chat.id, 'Введите текст который хотите преобразовать в аудио')
    bot.register_next_step_handler(message, speak_text)

def speak_text(message):
    global text
    text = message.text
    speak(text, True, sp)
    file = open('test.wav', 'rb')
    bot.send_audio(message.chat.id, file)
    
@bot.message_handler(commands=['speaker'])  
def edit_speaker(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    item = telebot.types.InlineKeyboardButton('Мужской', callback_data='Мужской')
    item1 = telebot.types.InlineKeyboardButton('Женский', callback_data='Женский')
    
    markup.add(item, item1)
    bot.send_message(message.chat.id, 'Вы можете изменить пол спикера:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global sp
    if call.data == 'Мужской':
            bot.send_message(call.message.chat.id, 'Спикер успешно сменён на мужчину')
            sp = 'aidar'
    elif call.data == 'Женский':
            sp = 'baya'
            bot.send_message(call.message.chat.id, 'Спикер успешно сменён на девушку')

@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, 'Команды:')
    bot.send_message(message.chat.id, '/speaker: выбрать спикера.')
    bot.send_message(message.chat.id, '/speak_text: конвертация текста в речь.')
    
def main():
    bot.polling(none_stop=True)
    
if __name__ == '__main__':
    main()