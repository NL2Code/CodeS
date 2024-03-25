# Shreddit

Shreddit is a Python command line program which will take a user's post history on the website
[Reddit](http://reddit.com), and will systematically go through the user's history deleting one post/submission at a
time until only those whitelisted remain. It allows you to maintain your normal reddit account while having your history
scrubbed after a certain amount of time.

When it became known that post edits were *not* saved but post deletions *were* saved, code was added to edit your post
prior to deletion. In fact you can actually turn off deletion all together and just have lorem ipsum (or a message
about Shreddit) but this will increase how long it takes the script to run as it will be going over all of your messages
every run.

## Usage

After installing the `shreddit` command line utility, the first step is setting up the tool's configuration files.
Simply typing `shreddit -g` will generate configs. After configuring credentials, running the tool with the `shreddit`
command will begin the tool's operation.