import telebot,os,datetime,csv,os.path,requests
from telebot import types
bot = telebot.TeleBot("token")

def extract_data(country):
    dia_actual = datetime.datetime.now();
    day = str(int(dia_actual.strftime("%d")) - 1)
    month = dia_actual.strftime("%m")
    year = "20" + dia_actual.strftime("%y")
    web_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
    csv_archive = month + '-' + day + '-' + year +".csv"
    request = requests.get(web_link + csv_archive)
    if request.status_code == 200:
        if  not os.path.exists(csv_archive):
            os.system("wget " + web_link + month + '-' + day + '-' + year +".csv")
    else:
         csv_archive = month + '-' + str(int(day)-1) + '-' + year +".csv"
    with open(csv_archive,'r') as file:
        reader = csv.reader(file)
        dades = [0,0,0]
        for row in reader:
            if row[1] == country:
                dades[0] += int(row[3])
                dades[1] += int(row[4])
                dades[2] += int(row[5])
    return dades

def imprimir_info(dades,id):
    bot.send_message(id,"Número de infectados: " + str(dades[0]) + "\nNúmero de muertos: " + str(dades[1]) + "\nNúmero de recuperados: "+ str(dades[2]) )


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bienvenido al bot de telegram que comparte información en tiempo real sobre el Covid-19. \n Para recibir información sobre los distintos países solo tienes que escribir el nombre (en inglés) o pulsar su bandera si aparece. \n Si quieres más información escribe /help")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,"/help Para más información. \n/start Para reiniciar. \n los nombres de los países tienen que estar en inglés \n Si el país de tu interés no es alguno de los predeterminados en los botones, puedes buscarlo por teclado normal")


def handle_messages(messages):
    x = True
    for message in messages:
        if (x or (message.text != "/start" and message.text != "/help")):
            markup = types.ReplyKeyboardMarkup()
            itemes = types.KeyboardButton('🇪🇸')
            itemit = types.KeyboardButton('🇮🇹')
            itemgb = types.KeyboardButton('🇬🇧')
            itemfr = types.KeyboardButton('🇫🇷')
            itemde = types.KeyboardButton('🇩🇪')
            markup.row(itemes, itemit, itemgb)
            markup.row(itemde, itemfr)
            print(str(message.chat.id) + ' ' + str(message.chat.username))
            if message.text == '🇪🇸':
                d = extract_data('Spain')
                imprimir_info(d,message.chat.id)
            elif message.text == '🇮🇹':
                d = extract_data('Italy')
                imprimir_info(d,message.chat.id)
            elif message.text == '🇬🇧':
                d = extract_data('United Kingdom')
                imprimir_info(d,message.chat.id)
            elif message.text == '🇫🇷':
                d = extract_data('France')
                imprimir_info(d,message.chat.id)
            elif message.text == '🇩🇪':
                d = extract_data('Germany')
                imprimir_info(d,message.chat.id)
            elif message.text != "/start" and message.text != "/help":
                d = extract_data(message.text)
                imprimir_info(d,message.chat.id)
            x = False
            bot.send_message(message.chat.id, "Sobre que país desea obtener información: ", reply_markup=markup)

bot.set_update_listener(handle_messages)
bot.polling()
