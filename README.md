<p align="center">
<h1 style='font-size:38px;' align="center">mangadex-dl</h1>
</p>
<h2><font color="red">DISCLAIMER</font></h2>
I am not updating this repository any longer. The code here is mostly for reference if anyone is intrested. </br></br>
mangadex-dl is a command line interface written in python that downloads manga from [mangadex.org](https://mangadex.org/) as PDF or images

<h2>What does mangadex-dl do? </h2>

mangadex-dl enables you to : </br>

- Download manga from [mangadex.org](https://mangadex.org/) using manga-urls or chapter-urls
- Multiple chapters can be downloaded using manga urls
- Single chapters can be downloaded using chapter-urls
- Downloaded manga can be saved as PDFs or as images
- Multiple chapter PDFs can be merged into one
- Download manga in any language that is availiable in mangadex
- Multiple chapter images can be brought into a single folder for a smoother reading experience
- Downloaded Images are saved with a naming convention that ensures proper order of images in mobiles
- Have a local library of your manga inside your computer that can be managed from within the program
<h2>How does mangadex-dl download manga? </h2>

mangadex-dl utilises the [mangadex api](https://api.mangadex.org/) to search and download manga

<h2>Installation</h2>

mangadex-dl can be downloaded by running the command :

```
pip install mangadex-dl
```

to ensure package is installed correctly, run this script form shell:

```
mangadex-dl --version
```
and it should return the version of managdex-dl you downloaded.

if you see an error like this :

```
'mangadex-dl' is not recognized as an internal or external command,
operable program or batch file.
```

ensure that you are using the proper python environment using which you downloaded the CLI, if it doesn't work even after reinstalling the program, please open an issue on [github.](https://github.com/john-erinjery/mangadex-dl/)

<h2>Usage</h2>

CLI Arguments are given below :

```
usage: mangadex-dl [options]

Python CLI that downloads manga from mangadex.org as PDF or images

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -lib, --library       start a library session where you can view and modify your local library
  -t , --manga-url      the manga homepage url
  -tcode , --manga-code
                        The library code of the manga, as stored in local lib
  -c , --chapter-url    the chapter url
  -pdf                  organise manga into chapterwise PDFs
  -m, --merge           merge chapter PDFs into single PDF (-pdf must be provided)
  -img                  organise manga into chapterwise image folders
  -s, --single-folder   organise manga into chapterwise image folders (-img must be provided)
  --data                enable data saver (default)
  -r  , --range         range of chapters to download, eg: -r 1 5 (download chapters 1 - 4)
  -tl , --translated-language
                            language code of translation (default : en, others availiable on github homepage)
```

<h2>Example Usage </h2>

1. Downloads chapters 1 to 9 of manga as merged PDF
   
    ```
    mangadex-dl -t https://mangadex.org/title/2e0fdb3b-632c-4f8f-a311-5b56952db647/bocchi-the-rock -pdf -m -r 1 10
    ```
</br>
 
2. Downloads chapters 1 to 9 of manga as single-folder images
   ```
   mangadex-dl -t https://mangadex.org/title/2e0fdb3b-632c-4f8f-a311-5b56952db647/bocchi-the-rock -img -s -r 1 10
   ```
</br>
 
3. Downloads chapter as PDF
   ```
   mangadex-dl --chapter-url https://mangadex.org/chapter/63b17ee1-857f-441a-85a7-2e3767204497 -pdf
   ```
</br>
 
4. Downloads chapter as Images
   ```
   mangadex-dl --chapter-url https://mangadex.org/chapter/63b17ee1-857f-441a-85a7-2e3767204497 -img
   ```
</br>
 
5. Downloads chapters 1 to 9 as chapterwise PDFs
    ```
    mangadex-dl -t https://mangadex.org/title/2e0fdb3b-632c-4f8f-a311-5b56952db647/bocchi-the-rock -pdf -r 1 10
    ```
</br>

6. Downloads chapters 1 to 9 as chapterwise images
   ```
   mangadex-dl -t https://mangadex.org/title/2e0fdb3b-632c-4f8f-a311-5b56952db647/bocchi-the-rock -img -r 1 10
   ```
</br>

7. To access your library
    ```
    mangadex-dl --library
    ```
</br>

8. To download a manga using library code (S.No in local library):
   ```
   mangadex-dl -tcode 1 -pdf -m -r 1 3
   ```
   > here the manga with S.No 1 in the library will be downloaded. note that if the S.No does not exist in the library an error will be raised

</br>

9.  Downloads chapters 1 to 9 as merged PDF in French
    ```
    mangadex-dl -t https://mangadex.org/title/2e0fdb3b-632c-4f8f-a311-5b56952db647/bocchi-the-rock -pdf -m -tl fr
    ```
</br>
<h2 id='codes'>Language Codes </h2>

|  Code     |          Language              |
|-------|------------------------|
| sa    | Arabic                 |
| bd    | Bengali                |
| bg    | Bulgarian              |
| mm    | Burmese                |
| ct    | Catalan                |
| cz    | Czech                  |
| dk    | Danish                 |
| nl    | Dutch                  |
| en    | English                |
| ph    | Filipino               |
| fi    | Finnish                |
| fr    | French                 |
| de    | German                 |
| gr    | Greek                  |
| il    | Hebrew                 |
| in    | Hindi                  |
| hu    | Hungarian              |
| id    | Indonesian             |
| it    | Italian                |
| ja    | Japanese               |
| kr    | Korean                 |
| lt    | Lithuanian             |
| my    | Malay                  |
| mn    | Mongolian              |
| ir    | Persian                |
| pl    | Polish                 |
| br    | Portuguese (Br)        |
| pt    | Portuguese (Pt)        |
| ro    | Romanian               |
| ru    | Russian                |
| rs    | Serbo-Croatian         |
| es    | Spanish (Es)           |
| mx    | Spanish (LATAM)        |
| se    | Swedish                |
| th    | Thai                   |
| tr    | Turkish                |
| ua    | Ukrainian              |
| vn    | Vietnames              |
| zh    | Simplified Chinese     |
| zh-hk | Traditional Chinese    |
| pt-br | Brazilian Portugese    |
| es-la | Latin American Spanish |
| ja-ro | Romanized Japanese     |
| ko-ro | Romanized Korean       |
| zh-ro | Romanized Chinese      |


<h2> Credits </h2>

- This program is build using a [mangadex api wrapper](https://pypi.org/project/mangadex/) build by Eduardo Ceja and maintained by [EMACC99.](https://pypi.org/user/EMACC99/)

- In certain parts of the program, it uses the official [mangadex api](https://api.managdex.org/) directly.
- The program is build using these tools, whose credits goes to their devolopers and maintainers
  
<br/>
<h2>In coming releases..</h2>

- Support for MangaDex user account, access to library and reading lists
- Functionality to search new manga from within the shell

