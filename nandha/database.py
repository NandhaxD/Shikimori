

from nandha import db

db = db['chats']

def set_chat_mode(chat_id: int, chatname, mode):
     chat = {'chat_id': chat_id}
     db.update_one(chat,
            {'$set': {'chat': mode, 'name': chatname}}, upsert=True
                  )
     return True

def get_chats():
     data = []
     for chat in db.find():
           data.append(
                {'name': chat['name'], 'chat_id': chat['chat_id'], 'chat': chat['chat']}
           )
     if len(data) == 0:
          chat_ids = data
     else:
          chat_ids = [list(item.values())[0] for item in data]
     return chat_ids, data
     
              
def get_chat_mode(chat_id: int, chatname):
      chat = {'chat_id': chat_id}
      if not db.find_one(chat):
          set_chat_mode(chat_id, chatname, False)
      chat = db.find_one(chat)
      return chat['chat']


def scan_sticker(file_id: str):
    return {         
         chat["chat_id"]: file_id 
         for chat in db.find() if 'stickers' in chat 
         for sticker_ids in chat['stickers'] if file_id in sticker_ids
    }
     

def remove_sticker(chat_id: int, file_id: str):
    chat = {'chat_id': chat_id}
    if db.find_one(chat) is not None:
        db.update_one(
            chat,
            {"$pull": {"stickers": file_id}}
        )
         
def get_all_stickers():
     all_stickers = [sticker for chat in db.find() if chat.get('stickers') for sticker in chat['stickers']]
     return all_stickers
     
           
def get_chat_stickers(chat_id: int):
    chat_js = {'chat_id': chat_id}
    chat = db.find_one(chat_js)
    stickers = []
    if chat:
         if 'stickers' in list(chat.keys()):
             return stickers + chat['stickers']
         else:
              return stickers
    else:
         return stickers
     
def add_chat_sticker(chat_id: int, sticker_id):
    chat_js = {'chat_id': chat_id}
    chat = db.find_one(chat_js)
    if 'stickers' in list(chat.keys()):
           stickers = get_chat_stickers(chat_id)
           if sticker_id in stickers:
                 return
         
           else:
                db.update_one(
                     chat_js, {'$push': {'stickers': sticker_id}})
                return True
    else:
         db.update_one(
              chat_js, {'$set': {'stickers': [sticker_id]}})
         return True
         
          

    
