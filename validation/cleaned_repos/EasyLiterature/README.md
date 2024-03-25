# EasyLiterature
**EasyLiterature** is a Python-based command line tool for automatic literature management. Welcome star or contribute!

Simply list the paper titles (or ids) you want to read in a markdown file and it will automatically `collect and refine its information in the markdown file`, `download the pdf to your local machine`, and `link the pdf to your paper in the markdown file`. You can forever keep your notes within the pdfs and mds on your local machine or cloud driver.

Inspired by [Mu Li](https://www.bilibili.com/video/BV1nA41157y4), adapted from [autoLiterature](https://github.com/wilmerwang/autoLiterature). 
Compared to autoLiterature, **EasyLiterature** is much easier to use and supports a wider range of features, such as `title-based paper match`, `paper search and download on Google Scholar and DBLP` (the two main sites for scholars), `citation statistics`, `mannual information update assitant`, etc. **EasyLiterature covers almost all papers thanks to the support of Google Scholar and DBLP!**

## A simple example
1. Have the python installed on your local machine (preferably >= 3.7).
2. Run `pip install easyliter` in your command line to install.
3. Prepare your markdown note file (e.g., `Note.md`). <br>**Attention:** You may need to download a markdown editor to create/edit this file. I am using [Typora](https://typora.io/), which is not totally free. You can also choose other alternatives.
4. List the formated papers titles in your markdown note file according to the Section 4 below (Recognition Rules). e.g.,<br>
  \- {{BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.}}<br>
  \- {{Xlnet: Generalized autoregressive pretraining for language understanding.}}<br>
  **(pay attention to the space after ‘\-’)** 
5. Create a folder to store the downloaded pdfs (e.g., `PDFs/`).
6. Run `easyliter -i <path to your md file> -o <path to your pdf folder>`. 
<br> (Replace `<path to your md file>` with the actual path to your markdown note file, `<path to your pdf folder>` with the actual path to your pdf folder)
<br>e.g., `easyliter -i "/home/Note.md" -o "/home/PDFs"`
7. Your should able to see that the updated information and downloaded pdf files if no error is reported.
8. This is a simple and common use case. For other features, please read the below sections carefully and follow the instructions.

## Arguments
```bash
easyliter

optional arguments:

  -h, --help            show this help message and exit
  
  -i INPUT, --input INPUT
  The path to the note file or note file folder.

  -o OUTPUT, --output OUTPUT
  Folder path to save paper pdfs and images. NOTE: MUST BE FOLDER.

  -p PROXY, --proxy PROXY
  The proxy. e.g. 127.0.0.1:1080. If this argument is specified, the google scholar will automatically use a free proxy (not necessarily using the specified proxy address). To use other proxies for google scholar, specify the -gp option. If you want to set up the proxies mannually, change the behaviour in GoogleScholar.set_proxy(). See more at https://scholarly.readthedocs.io/en/stable/ProxyGenerator.html.

  -gp GPROXY_MODE, --gproxy_mode GPROXY_MODE
  The proxy type used for scholarly. e.g., free, single, Scraper. (Note: 1. <free> will automatically choose a free proxy address to use, which is free, but may not be fast. 2. <single> will use the proxy address you specify. 3. <Scraper> is not free to use and need to buy the api key.).

  -d, --delete
  Delete unreferenced attachments in notes. Use with caution, when used, -i must be a folder path including all notes.

  -m MIGRATION, --migration MIGRATION
  The pdf folder path you want to reconnect to.
```

## Recognition Rules
- If the notes file contains `- {paper_id}`, it will download the information of that literature, but not the PDF.
- If the notes file contains `- {{paper_id}}`, it will download both the information of that literature and the PDF.

- Note: `paper_id` supports `article title`, published articles' `doi`, and pre-published articles' `arvix_id`, `biorvix_id`, and `medrvix_id`. It will try all the possible sources online.

## Usage
### Basic Usage
Assuming `input` is the folder path of the literature notes (.md files) and `output` is the folder path where you want to save the PDFs.

```bash
# Update all md files in the input folder
easyliter -i input -o output 

# Only update the input/example.md file
easyliter -i input/example.md -o output  

# -d is an optional flag, when -i is a folder path, using -d will delete unrelated pdf files in the PDF folder from the literature notes content
easyliter -i input -o output -d
```

### Migrating Notes and PDF Files
When you need to move the literature notes or the PDF folder, the links to the PDFs in the literature notes might become unusable. You can use `-m` to re-link the PDF files with the literature notes.

```bash
# Update all md files in the input folder
easyliter -i input -m movedPDFs/

# Only update the input/example.md file
easyliter -i input/example.md -m movedPDFs/  
```