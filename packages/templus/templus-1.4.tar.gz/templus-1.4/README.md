---

__install using pip__

```python
pip install templus

```

---

__code example__

```python
import templus

client = templus.Client() #insert mail as an argument if you want to interact with it through a class attribute
mails = client.generate_mails(10)
print("generated mails: %s" % ", ".join(mails))
mail = mails[0]
msgs_ids = client.get_messages(mail).id
for id in msgs_ids:
	print(client.read_message(id, mail).text)

```

---

* __objects__

>`get_messages() -> Messages`

>>__attributes__:

>>json

>>id

>>is_new

>>from_mail

>>from_name

>>title

>>date

> `read_message() -> Message`

>>__attributes__:

>>json

>>id

>>from_mail

>>from_name

>>title

>>text

>>attachments

>>date

---

* __project links__

>[github](https://github.com/BitterTruth1/templus/tree/main)

>[telegram](https://t.me/xarlchat)

---
