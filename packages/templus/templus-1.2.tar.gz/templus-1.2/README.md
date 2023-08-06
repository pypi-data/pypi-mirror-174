**Code example**
---
```import templus
client = templus.Client() #insert mail as an argument if you want to interact with it through a class attribute
mails = client.generate_mails(10)
print("generated mails: %s" % ", ".join(mails))
mail = mails[0]
msgs_ids = client.get_messages(mail).id
for id in msgs_ids:
	print(client.read_message(id, mail).text)```
