# RedditStorage
Cloud storage that uses Reddit as a backend. 

RedditStorage is an application that allows you to store on reddit subreddits via raw bytes. The file is encoded into characters and encrypted using AES encryption, after which it can be stored on a subreddit of choice (ideally your own private subreddit). To retrieve the file, the process is simply reversed. Unfortunately, reddit comments have a character limit of 10000. If your file exceeds that amount, it will be split up among comments in the same thread which form links by replying to each other. 

How to Use:

1. RedditStorage uses an AES encryption algorithm which requires you to choose a password(e.g. "bunny").
2. Run: `python RedditStorage.py`
3. Enter your username, password, subreddit and desired encryption key
4. Choose the file you want to upload
5. When getting the file, choose the file you want to get and how/where you want to save it
