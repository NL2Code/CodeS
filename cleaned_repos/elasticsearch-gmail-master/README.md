Elasticsearch-gmail
=======================

#### What's this all about?

I recently looked at my Gmail inbox and noticed that I have well over 50k emails, taking up about 12GB of space but there is no good way to tell what emails take up space, who sent them to, who emails me, etc

Goal of this tutorial is to load an entire Gmail inbox into Elasticsearch using bulk indexing and then start querying the cluster to get a better picture of what's going on.

#### The Source Code

The overall program will look something like this:

```python
mbox = mailbox.mbox('emails.mbox') // or mailbox.MH('inbox/')

for msg in mbox:
    item = convert_msg_to_json(msg)
	upload_item_to_es(item)

print "Done!"
```