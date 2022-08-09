#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
from datetime import datetime

import model_related as mr

logging.basicConfig(level=logging.INFO) 
# ALL < TRACE < DEBUG < INFO < WARN < ERROR < FATAL < OFF

accountDICT = json.load(open("account.info", encoding="utf-8")) 


class BotClient(discord.Client):

    def resetMSCwith(self, messageAuthorID): #清空與 messageAuthorID 之間的對話記錄
        logging.info("--Reset--")
        templateDICT = {"updatetime" : None,
                             "msgSTR": "",
                             "rejectLIST": [],
                             "replySTR": "",
                             "ingr_inseason": "",
        }
        templateDICT["updatetime"] = datetime.now()
        return templateDICT

    async def on_ready(self): #當機器人完成啟動時
        logging.info('{} ( id : {} ) 上線囉！'.format(client.user, client.user.id)) #client.user為目前登入的帳號
        
        #Multi-Session Conversation :設定多輪對話資訊#
        self.templateDICT = {"updatetime" : None,
                             "msgSTR": "",
                             "rejectLIST": [],
                             "replySTR": "",
                             "ingr_inseason": "",
        }
        self.mscDICT = { #userid:templateDICT
        }
        
    async def on_message(self, message): #當有訊息時
        logging.info("收到來自 {} 的訊息：{}".format(message.author, message.content.replace("<@{}> ".format(client.user.id), "").strip()))

        #排除自己的訊息，避免陷入無限循環
        if message.author == client.user:
            return None

        #bot點名
        elif message.content.lower().replace(" ", "") in ("bot點名"):
            await message.reply("有！")

        #當bot被呼叫到
        if client.user.mentioned_in(message):
            logging.info("bot被呼叫到了。") 
            
            msgSTR = message.content.replace("<@{}> ".format(client.user.id), "").strip()

            #測試訊息
            if msgSTR in '呼叫機器人':
                await message.reply('幹嘛')
                return None

            #初次對話，init template
            if message.author.id not in self.mscDICT.keys(): 
                self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
            #有講過話，與上次對話差超過 2 分鐘(視為沒有講過話)，刷新template
            else: 
                timeDIFF = datetime.now() - self.mscDICT[message.author.id]["updatetime"] #判斷對話時間差
                if timeDIFF.total_seconds() > 120: 
                    await message.reply('你剛說的我忘了，現在要聊啥別的')
                    self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)

            #開始處理正式對話，接上 NLU 模型
            self.mscDICT[message.author.id]["msgSTR"] = msgSTR
            self.mscDICT[message.author.id] = mr.model(self.mscDICT[message.author.id])

            #送出回覆
            await message.reply(self.mscDICT[message.author.id]["replySTR"])

            #紀錄說話者說話內容
            self.mscDICT[message.author.id]["msgSTR"] = msgSTR 

            logging.info("暫存資訊：{}".format(self.mscDICT))


if __name__ == "__main__":

    client = BotClient()
    client.run(accountDICT["discord_token"])

    