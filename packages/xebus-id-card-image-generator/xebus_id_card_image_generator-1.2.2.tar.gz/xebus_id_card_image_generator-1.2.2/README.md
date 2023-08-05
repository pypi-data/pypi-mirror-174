# Xebus ID Card Generator

`Xebus ID Card Generator` is a Command-Line Interface (CLI) written in Python used to generate JPEG images of Xebus ID cards.

This script generates images which size has the same portrait ratio as [ISO/IEC 7810 Identification cards ID-1](https://en.wikipedia.org/wiki/ISO/IEC_7810#ID-1) (3 3⁄8 in × 2 1⁄8 in, 54mm x 85.6mm).

## Installation

`Xebus ID Card Generator` can be easily installed with [`pipenv`]cod(https://github.com/pypa/pipenv):

```bash
$ pipenv --python 3.8 shell
$ pipenv install xebus-id-card-image-generator
```

_Note: As of October 2020, the Python Image Library (PIL) is not yet compatible with Python 3.9._

## Execution

```bash
$ ./bin/xidgen --help
usage: xidgen [-h] [-c TYPE] -f FILE [-d CHAR] [-q CHAR] [-e CHAR]
              [-s GEOMETRY] [-p SIZE] --header-file FILE [--font-name NAME]

Xebus ID Card Images Generator

optional arguments:
  -h, --help            show this help message and exit
  -c TYPE, --card-type TYPE
                        specify the type of ID cards to generate (driver,
                        guardian, securityguard, student)
  -f FILE, --csv-file FILE
                        specify the absolute path and name of the CSV file
                        containing the information of ID cards to generate
  -d CHAR, --delimiter CHAR
                        specify the character used to separate each field
                        (default to character [,])
  -q CHAR, --quotechar CHAR
                        specify the character used to surround fields that
                        contain the delimiter character (default to character
                        ["]).
  -e CHAR, --escapechar CHAR
                        specify the character used to escape the delimiter
                        character, in case quotes aren't used (default to
                        character [None]).
  -s GEOMETRY, --size GEOMETRY
                        specify the width and/or height in pixels of the image
                        to build, with the ratio of a CR80 standard credit
                        card size ID-1 in portrait mode (54mm x 85.6mm)
  -p SIZE, --padding SIZE
                        specify the space in pixels or percentage to generate
                        around the ID card
  --header-file FILE    specify the absolute path name of the header image
                        file
  --font-name NAME      specify the name of the font to display the full name
                        of each ID card
  --name-format FORMAT  specify the format of ID card file name
  --debug LEVEL         specify the logging level (value between 0 and 4, from
                        critical to debug)
```

For example:

```bash
$ xidgen --card-type student --header-file lfiduras_logo.jpg --csv-file lfiduras-students.csv
```

The user can specify the file name of the ID card images by passing the argument `name-format`.  A ID card file name format MUST be composed of field names to build this file name with.  These field names MUST be defined in braces, each field names separated with a character underscore.  For example:

```text
{id}_{first name}_{grade level}
```

_Note: The accepted field names correspond to the CSV field names._

### CSV File

The CSV file passed to the script MUST contain a first row corresponding to the header fields in whatever order:

- `#` (optional): The identification of the registration file of the card owner (as provided by the organization that manages this list)
- `ID` (required): The identification of the card owner
- `Card Type` (optional): Specify the type of the ID card (`driver`, `guardian`, `securityguard`, or `student`)
- `Class Name` (optional)
- `First Name` (optional)
- `Full Name` (required)
- `Grade Level` (optional): The number of the year a pupil has reached in this given educational
- `Grade Name` (optional): THe name given to this grade
- `Last Name` (optional)

For example:

| #             | ID                                   | First Name | Last Name | Full Name                   | Grade Level | Grade Name |
|---------------|--------------------------------------|------------| --------- | --------------------------- | ----------- | ---------- |
| `862-295-729` | 3a72a73e-c57b-11ea-8e0d-0008a20c190f | Céline     | CAUNE     | Céline Kim Anh CAUNE LÝ     | 16          | Terminale  |
| `873-774-763` | d8be1eef-2493-11eb-9dcf-0007cb040bcc | Aline      | CAUNE     | Aline Minh Anh CAUNE LÝ     | 15          | Première   |
| `457-128-612` | f6315b69-11af-11eb-bb6b-0007cb040bcc | Éline      | CAUNE     | Éline Xuân Anh CAUNE NGUYỄN | 2           | PS         |

## Available Fonts

|                                          |                                      |                                   |
| ---------------------------------------- | ------------------------------------ | --------------------------------- |
| `Amorino_beta`                           | `Calibri Light`                      | `Opificio_light_rounded`          |
| `Barlow-Black`                           | `Calibri Regular`                    | `Opificio_regular`                |
| `Barlow-BlackItalic`                     | `CaviarDreams`                       | `Opificio_rounded`                |
| `Barlow-Bold`                            | `CaviarDreams_Bold`                  | `PirataOne-Regular`               |
| `Barlow-BoldItalic`                      | `CaviarDreams_BoldItalic`            | `PlayfairDisplay-Black`           |
| `Barlow-ExtraBold`                       | `CaviarDreams_Italic`                | `PlayfairDisplay-BlackItalic`     |
| `Barlow-ExtraBoldItalic`                 | `Champagne & Limousines Bold Italic` | `PlayfairDisplay-Bold`            |
| `Barlow-ExtraLight`                      | `Champagne & Limousines Bold`        | `PlayfairDisplay-BoldItalic`      |
| `Barlow-ExtraLightItalic`                | `Champagne & Limousines Italic`      | `PlayfairDisplay-ExtraBold`       |
| `Barlow-Italic`                          | `Champagne & Limousines`             | `PlayfairDisplay-ExtraBoldItalic` |
| `Barlow-Light`                           | `Forgotbi`                           | `PlayfairDisplay-Italic`          |
| `Barlow-LightItalic`                     | `Forgottb`                           | `PlayfairDisplay-Medium`          |
| `Barlow-Medium`                          | `Forgotte`                           | `PlayfairDisplay-MediumItalic`    |
| `Barlow-MediumItalic`                    | `Forgotti`                           | `PlayfairDisplay-Regular`         |
| `Barlow-Regular`                         | `Forgotts`                           | `PlayfairDisplay-SemiBold`        |
| `Barlow-SemiBold`                        | `Giorgino`                           | `PlayfairDisplay-SemiBoldItalic`  |
| `Barlow-SemiBoldItalic`                  | `Jura-Bold`                          | `Quicksand-Bold`                  |
| `Barlow-Thin`                            | `Jura-Light`                         | `Quicksand-Light`                 |
| `Barlow-ThinItalic`                      | `Jura-Medium`                        | `Quicksand-Medium`                |
| `BebasNeue-Bold`                         | `Jura-Regular`                       | `Quicksand-Regular`               |
| `BebasNeue-Book`                         | `Jura-SemiBold`                      | `Quicksand-SemiBold`              |
| `BebasNeue-Light`                        | `LibreBaskerville-Bold`              | `Rothwell`                        |
| `BebasNeue-Regular`                      | `LibreBaskerville-Italic`            | `Skarpa regular`                  |
| `BebasNeue-Thin`                         | `LibreBaskerville-Regular`           | `SkarpaLt`                        |
| `Bedizen`                                | `Merriweather-Black`                 | `Steinerlight`                    |
| `Blacker-Display-Bold-italic-trial`      | `Merriweather-BlackItalic`           | `Teko-Bold`                       |
| `Blacker-Display-Bold-trial`             | `Merriweather-Bold`                  | `Teko-Light`                      |
| `Blacker-Display-ExtraBold-Italic-trial` | `Merriweather-BoldItalic`            | `Teko-Medium`                     |
| `Blacker-Display-ExtraBold-trial`        | `Merriweather-Italic`                | `Teko-Regular`                    |
| `Blacker-Display-Heavy-Italic-trial`     | `Merriweather-Light`                 | `Teko-SemiBold`                   |
| `Blacker-Display-Heavy-trial`            | `Merriweather-LightItalic`           | `Verdana`                         |
| `Blacker-Display-Light-Italic-trial`     | `Merriweather-Regular`               | `quarthck`                        |
| `Blacker-Display-Light-trial`            | `Montserrat-Black`                   | `quarthin`                        |
| `Blacker-Display-Medium-Italic-trial`    | `Montserrat-BlackItalic`             | `rokikier`                        |
| `Blacker-Display-Medium-trial`           | `Montserrat-Bold`                    | `rokikierc`                       |
| `Blacker-Display-Regular-Italic-trial`   | `Montserrat-BoldItalic`              | `rokikierci`                      |
| `Blacker-Display-Regular-trial`          | `Montserrat-ExtraBold`               | `rokikiere`                       |
| `Blacker-Text-Bold-Italic-trial`         | `Montserrat-ExtraBoldItalic`         | `rokikierei`                      |
| `Blacker-Text-Bold-trial`                | `Montserrat-ExtraLight`              | `rokikieri`                       |
| `Blacker-Text-Book-Italic-trial`         | `Montserrat-ExtraLightItalic`        | `rokikierl`                       |
| `Blacker-Text-Book-trial`                | `Montserrat-Italic`                  | `rokikierla`                      |
| `Blacker-Text-Heavy-Italic-trial`        | `Montserrat-Light`                   | `rokikierlai`                     |
| `Blacker-Text-Heavy-trial`               | `Montserrat-LightItalic`             | `rokikierp`                       |
| `Blacker-Text-Light-Italic-trial`        | `Montserrat-Medium`                  | `rokikierpi`                      |
| `Blacker-Text-Light-trial`               | `Montserrat-MediumItalic`            | `rokikiers`                       |
| `Blacker-Text-Medium-Italic-trial`       | `Montserrat-Regular`                 | `rokikierse`                      |
| `Blacker-Text-Medium-trial`              | `Montserrat-SemiBold`                | `rokikiersi`                      |
| `Blacker-Text-Regular-Italic-trial`      | `Montserrat-SemiBoldItalic`          | `saunder`                         |
| `Blacker-Text-Regular-trial`             | `Montserrat-Thin`                    | `vibroceb`                        |
| `Calibri Bold Italic`                    | `Montserrat-ThinItalic`              | `vibrocei`                        |
| `Calibri Bold`                           | `Opificio_Bold`                      | `vibrocen`                        |
| `Calibri Italic`                         | `Opificio_Bold_rounded`              | `vibrocex`                        |
| `Calibri Light Italic`                   | `Opificio_light`                     |                                   |
