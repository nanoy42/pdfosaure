# Pdfosaure

![pdfosaure](https://images.nanoy.fr/dino.jpg)

 * [Introduction](#introduction)
 * [Installation](#installation)
 * [Command lime usage](#command-line-usage)

## Introduction

Pdfosaure is small python utility to do a bunch of actions on pdf files :

 * encrypt and decrypt pdf files
 * rotate one, several or all pages of a pdf file
 * scale one, several or all pages of a pdf file
 * compress a pdf file
 * delete one or several pages of a pdf file
 * merge several pdf files together
 * explode (or split) a pdf files into several pdf files
 * convert pages of a pdf file to jpeg images
 * merge jpeg images to create a pdf file

Pdfosaure is a hungry dino tooling up pdfs.

Special thanks to zaiken for the logo.
## Installation

### Script

A one file script is available in the releases section of the github project : https://github.com/nanoy42/pdfosaure/releases.

### Developpement

For now the script can only be installed from the sources. Clone the git repository :

```
git clone https://github.com/nanoy42/pdfosaure
```

and install the requirements :

```
pip3 install -r requirements.txt
```

The script needs 4 dependencies :
 * [PyPDF2](https://pypi.org/project/PyPDF2/)
 * [img2pdf](https://pypi.org/project/img2pdf/)
 * [pdf2image](https://pypi.org/project/pdf2image/)
 * [docopt](https://pypi.org/project/docopt/)

## Command line usage

The commandes can be summarized as 
```
Pdfosaure.

To see examples and extended documentation, please visit https://github.com/nanoy42/pdfosaure

Usage:
  pdfosaure.py infos <filename>
  pdfosaure.py encrypt <filename> [<output>]
  pdfosaure.py decrypt <filename> [<output>]
  pdfosaure.py rotate <filename> <angle> [<output>] [--include=<pages_in> | --exclude=<pages_out>]
  pdfosaure.py scale <filename> <factor> [<output>] [--include=<pages_in> | --exclude=<pages_out>]
  pdfosaure.py compress <filename> [<output>] [--stats]
  pdfosaure.py deletepages <filename> <pages> [<output>]
  pdfosaure.py merge <filenames> <filenames>... [--output_filename=<output>]
  pdfosaure.py explode <filename> [--output=<output_scheme>]
  pdfosaure.py split <filename> <pages> [--output=<output_scheme>]
  pdfosaure.py pdftojpeg <filename> [<pages>] [--output=<output_scheme>]
  pdfosaure.py jpegtopdf <filenames>... [--output_filename=<output>]
  pdfosaure.py (-h | --help)
  pdfosaure.py --version

Options:
  <filename>                  Refers to the filename of the input pdf file
  <output>                    Refers to the filename of the output pdf file. By default, the script overwrites the input pdf.
  <angle>                     Rotation angle. Should be a multiple of 90. The rotation is clockwise.
  --include=<pages_in>        List of pages on which the effect should apply. The pages should be seperated by commas (,) without spaces. Cannot be use with --exclude.
  --exclude=<pages_out>       List of pages on which the effect should not apply. The pages should be seperated by commas (,) without spaces. Cannot be use with --include.
  --stats                     Print before and after sizes when compressing.
  <pages>                     List of pages on which the effect should apply. The pages should be separated by commas (,) without spaces.
  <filenames>                 Refers to one or more input filename (when merging pdfs of jpegs by instance).
  --output_filename=<output>  Refers to the filename of the output pdf file. By default, the script overwrites the input pdf.
  --output=<output_scheme>    When multiple files are generated, the names of output files look like {output_scheme}-{number}.{extension}
  -h --help                   Show this screen.
  --version                   Show version.

```

### `infos` command

```
pdfosaure.py infos <filename>
```

Return information on a pdf file (`<filename>`).

Example:

```
python3 pdfosaure.py infos test.pdf
```
will print information of test.pdf

### `encrypt` command

```
pdfosaure.py encrypt <filename> [<output>]
```

Encrypt a pdf file (`<filename>`). The script will prompt for password (using getpass). The result is stored as `<output>`. If not precised, the scrit overwrites `<filename>`. The script will fail if you try to encrypt an encrypted pdf file.

Examples: 

```
python3 pdfosaure.py encrypt test.pdf
```

will replace the test.pdf file by its encrypted version. 

```
python3 pdfosaure.py encrypt test.pdf test2.pdf
```
will create a test2.pdf encrypted file. The test.pdf file will remain not encrypted.

### `decrypt` command

```
pdfosaure.py decrypt <filename> [<output>]
```

Decrypt a pdf file (`<filename>`). The script will prompt for password (using getpass). The result is stored as `<output>`. If not precised, the scrit overwrites `<filename>`. The script will fail if you try to decrypt an unencrypted pdf file.

Examples: 

```
python3 pdfosaure.py decrypt test.pdf
```

will replace the test.pdf file by its unencrypted version. 

```
python3 pdfosaure.py decrypt test.pdf test2.pdf
```
will create a test2.pdf unencrypted file. The test.pdf file will remain encrypted.

### `rotate` command

```
pdfosaure.py rotate <filename> <angle> [<output>] [--include=<pages_in> | --exclude=<pages_out>]
```

Rotate the selected pages of `<filename>` by `<angle>` and write the result to `<output>`. If not precised, the script overwrites `<filename>`. The pages can select either by giving the list of pages (separated by commas without spaces) you want to rotate in the --include option or the pages you don't want to rotate in --exclude option. If both options are unused, all pages are rotated. You can't use both options at the same time. The rotation is made clockwise. The `<angle>` should be a multiple of 90.

Examples:

```
python3 pdfosaure.py rotate test.pdf 90
```
will rotate all pages of test.pdf by 90 degrees clockwise, and overwrite test.pdf with the rotated version.

```
python3 pdfosaure.py rotate test.pdf 180 output.pdf --inlcude 1,2
```
will rotate the first two pages by 180 degrees and write the result to output.pdf.

```
python3 pdfosaure.py rotate test.pdf 270 --exclude 1,2
```
will rotate all pages but the first and second ones by 270 degrees and overwrite test.pdf.

### `scale` command

```
pdfosaure.py scale <filename> <factor> [<output>] [--include=<pages_in> | --exclude=<pages_out>]
```

Scale the selected pages of `<filename>` by `<factor>` and write the result to `<output>`. If not precised, the script overwrites `<filename>`. The pages can select either by giving the list of pages (separated by commas without spaces) you want to rotate in the --include option or the pages you don't want to rotate in --exclude option. If both options are unused, all pages are rotated. You can't use both options at the same time. The factor should be a float.

Examples:

```
python3 pdfosaure.py scale test.pdf 2
```
will scale all pages of test.pdf by 2, and overwrite test.pdf with the scaled version.

```
python3 pdfosaure.py scale test.pdf 0.2 output.pdf --inlcude 1,2
```
will scale the first two pages by 0.2 and write the result to output.pdf.

```
python3 pdfosaure.py scale test.pdf 0.8 --exclude 1,2
```
will scale all pages but the first and second ones by 0.8 and overwrite test.pdf.

### `compress` command
```
pdfosaure.py compress <filename> [<output>] [--stats]
```

Compress `<filename>` and write result to `<output>`. If not precised, the script overwrites `<filename>`. If `--stats` is enabled, the script prints before and after sizes of pdf files.

```
python3 pdfosaure.py compress test.pdf
```
will compress the test.pdf file.

```
python3 pdfosaure compress test.pdf test2.pdf --stats
```
will save the compressed version of test.pdf as test2.pdf amd print size information.

### `deletepages` command
```
pdfosaure.py deletepages <filename> <pages> [<output>]
```

Delete pages from `<filename>` and write result to `<output>`. If not precised, the script overwrites `<filename>`. `<pages>` should be a list of pages separated by commas wihtout spaces.

Examples:

```
python3 pdfosaure.py deletepages test.pdf 1,6,7
```
will delete the first, sixth and seventh pages and overwrite test.pdf file.

```
python3 pdfosaure.py deletepages test.pdf 1,6,7 test2.pdf
```
will do the same thing without overwriting.

### `merge` command
```
pdfosaure.py merge <filenames> <filenames>... [--output_filename=<output>]
```

Merge several pdf files. The ouput_filename option is used to change the filename of the merge pdfs. If not precised, the pdf is named output.pdf.

Examples:

```
python3 pdfosaure.py pdf1.pdf pdf2.pdf
```
will merge the two pdfs into output.pdf.

```
python3 pdfosaure.py pdf1.pdf pdf2.pdf pdf3.pdf pdf4.pdf --output_filename=final.pdf
```
will merge the 4 pdfs into final.pdf

### `explode` command
```
pdfosaure.py explode <filename> [--output=<output_scheme>]
```

Explod command will save each page of `<filename>` into a separate pdf file. By default the output files are named like output-{number}.pdf, but output can be change with the `--output` parameter.

Examples:

```
python3 pdfosaure.py test.pdf --output=final
```
will create final-1.pdf, final-2.pdf, ... final-{number of pages in test.pdf}.pdf

### `split` command
```
pdfosaure.py split <filename> <pages> [--output=<output_scheme>]
```

Split will split the pdf `<filename>` at the given `<pages>` into several pdf files. The pages should be given separated by commas without spaces. By default the output files are named like output-{number}.pdf, but output can be change with the `--output` parameter.

Examples:

```
python3 pdfosaure.py test.pdf 4,8,19 --output=final
```
will create the following pdf :
 * final-1.pdf, pages 1 to 3
 * final-2.pdf, pages 4 to 7
 * final-3.pdf, pages 8 to 18
 * final-4.pdf, pages 19 to last page

### `pdftojpeg` command
```
pdfosaure.py pdftojpeg <filename> [<pages>] [--output=<output_scheme>]
```

Export all or some pages to jpeg from pdf `<filename>`. If not pages are precised, all pages are exported. Pages should be precised separated by commas, without spaces. By default the output files are named like output-{number}.jpg, but output can be change with the `--output` parameter.

Examples:

```
python3 pdfosaure.py test.pdf
```
will export all pages of test.pdf in output-1.jpg, output-2.jpg...

```
python3 pdfosaure.py test.pdf 1,5 --output=final
```
will export pages 1 and 5 into final-1.jpg and final-2.jpg.

### `jpegtopdf` command
```
pdfosaure.py jpegtopdf <filenames>... [--output_filename=<output>]
```

Merge jpg into one pdf. `<filenames>` are the filenames of the jpeg files. The ouput_filename option is used to change the filename of the merge jpegs. If not precised, the pdf is named output.pdf.

Examples:

```
python3 pdfosaure.py jpegtopdf jpeg1.jpg
```
will transform jpeg1.jpg file into a pdf named output.pdf

```
python3 pdfosaure.py jpegtopdf jpeg1.jpg jpeg2.jpg --output_filename=final.pdf
```
will merge jpeg1.jpg and jpeg2.jpg into final.pdf
