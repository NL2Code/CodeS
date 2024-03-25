Requestium
========
Requestium is a Python library that merges the power of Requests, Selenium, and Parsel into a single integrated tool for automatizing web actions.

The library was created for writing web automation scripts that are written using mostly Requests but that are able to seamlessly switch to Selenium for the JavaScript heavy parts of the website, while maintaining the session.

Requestium adds independent improvements to both Requests and Selenium, and every new feature is lazily evaluated, so its useful even if writing scripts that use only Requests or Selenium.

## Features
- Enables switching between a Requests' Session and a Selenium webdriver while maintaining the current web session.
- Integrates Parsel's parser into the library, making xpath, css, and regex much cleaner to write.
- Improves Selenium's handling of dynamically loading elements.
- Makes cookie handling more flexible in Selenium.
- Makes clicking elements in Selenium more reliable.
- Supports Chromedriver natively plus adding a custom webdriver.
