import requests
from bs4 import BeautifulSoup
import telebot

bot = telebot.TeleBot("")


# mask = /np <url> <№>

startMsg =  "Ви можете виконати такі команди:\n*/np <Посилання на список> <№ У рейтинговому списку>*\n"
startMsg += 'ПРИКЛАД:\n"*/np https://abit-poisk.org.ua/rate2019/direction/611171 9*"\n'
startMsg += 'Бот покаже кількість абітурієнтів у спику abit-poisk.org.ua та їх пріорітети.\n'
startMsg += 'Використовуйте посилання на *ПЕРШУ* сторінку рейтингового списку вашої професії!'
	

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	bot.send_message(message.chat.id, startMsg, parse_mode = "Markdown")

def sort(val):
	return val[3]

@bot.message_handler(commands=['np'])
def find_me(message):
	
	try:
		quota = 0
		url = str(message.text).split(' ')[1]
		myRank = int(str(message.text).split(' ')[2])
		arr =[]
		priors = [0, 0, 0, 0,  0,  0,  0, 0]
		r = requests.get(url).text
		html = BeautifulSoup(r, 'lxml')
		blocks = html.findAll('tr', class_ = 'application-status')
		pages = len(html.findAll('div', class_ = 'card-header')[1].findAll('a')) - 1
		for i in range(2, pages + 1):
			URL = 'https://abit-poisk.org.ua/rate2019/direction/611171/?page=' + str(i)
			r = requests.get(URL).text
			html = BeautifulSoup(r, 'lxml')
			blocks += html.findAll('tr', class_ = 'application-status')

		for block in blocks:
			info = block.findAll('td')
			num = int(str(info[0].text).replace(' ', '').replace('\n', ''))
			name = str(info[1].find('a').text).replace(' ', '').replace('\n', '')
			prior = str(info[2].text).replace(' ', '').replace('\n', '')
			
			if prior == 'К': prior = 0
			else: prior = int(prior)
			score = float(str(info[3].text).replace(' ', '').replace('\n', ''))
			
			inf = (num, name, prior, score)
			
			if str(info[6].text.replace(' ', '').replace('\n', '')) == '—': arr.append(inf)
			else: quota += 1 
		
		# print(myRank)
		# print(arr[219])
		# k = 0
		# for i in arr: 
		# 	print(str(k) + str(i))
		# 	k += 1

		myPrior = arr[myRank - 1][2]
		me = arr[myRank - quota - 1]
		
		arr.sort(key = sort, reverse = True)


		myPos = arr.index(me)

		
		
		k = 0
		for i in range(0, int(myPos)):
			priors[arr[i][2]] += 1
			k += 1
			# print(str(arr[i][0]))

		outputMessage = f"У рейтинговому списку перед вами є така кількість абітурієнтів: *{myPos} (БЕЗ АБІТУРІЄНТІВ З КВОТОЮ)*\nАбітурієнтів із пріорітетом K: {priors[0]}\n"
		outputMessage += f"Абітурієнтів із пріорітетом 1: {priors[1]}\nАбітурієнтів із пріорітетом 2: {priors[2]}\nАбітурієнтів із пріорітетом 3: {priors[3]}\n"
		outputMessage += f"Абітурієнтів із пріорітетом 4: {priors[4]}\nАбітурієнтів із пріорітетом 5: {priors[5]}\n"
		outputMessage += f"Абітурієнтів із пріорітетом 6: {priors[6]}\nАбітурієнтів із пріорітетом 7: {priors[7]}\n"
		outputMessage += f"Всього абітурієнтів із пріорітетом *більше ніж 1*: {priors[2] + priors[3] + priors[4] + priors[5] + priors[6] + priors[7]}\n"
		outputMessage += "\n*THX 4 USING!!!*"
		bot.send_message(message.chat.id, 'Це ви? ' + str(arr[myPos]) + "\nБот *ІГНОРУЄ* *ВСІ* місця з квотою!", parse_mode = "Markdown")
		bot.send_message(message.chat.id, outputMessage, parse_mode = "Markdown")


		# print(arr)
		# print(quota)


	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, "*Помилка!!!*\n*Перевірте правильність введення даних:*\n*/np <Посилання на список> <№ У рейтинговому списку>*", parse_mode = "Markdown")
		

	# bot.reply_to(message, "qq" + message.text)






bot.polling()