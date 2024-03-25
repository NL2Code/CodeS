# RSS to Telegram Bot

**A Telegram RSS bot that cares about your reading experience**

## Highlights

- Multi-user
- I18n
    - English, Chinese, Cantonese, Italian, and [more](docs/translation-guide.md)!
- The content of the posts of an RSS feed will be sent to Telegram
    - Keep rich-text format
    - Keep media (customizable)
        - Images, Videos, and Audio both in the post content and enclosure; Documents in the post enclosure
        - Long images will be sent as files to prevent Telegram from compressing the image and making it unreadable
        - Drop annoying icons, they break the reading experience
    - Automatically replace emoji shortcodes with emoji
    - Automatically replace emoji images with emoji or its description text
    - Automatically determine whether the title of the RSS feed is auto-filled, if so, omit the title (customizable)
    - Automatically show the author-name (customizable)
    - Automatically split too-long messages
        - If configured Telegraph, the message will be sent via Telegraph (customizable)
- Various customizable formatting settings
    - Hashtags, custom title, etc.
- Individual proxy settings for Telegram and RSS feeds
- OPML importing and exporting (keep custom title)
- Optimized performance
- User-friendly
- HTTP Caching