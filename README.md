# CV and Cover Letter Builder

## Introduction

Python script and LaTeX files to generate a CV with a cover letter, designed to make it easy to apply for jobs as quickly as possible.

## Preamble
This program needs `python3`, `pdftk`, `latexmk` and `pyyaml` to run.

On MacOS:

```
brew install python3 pdftk-java mactex
```

On Debian based systems:

```
sudo apt-get install python3 pdftk latexmk
```

On Arch based systems:

```
sudo pacman -S python pdftk texlive-binextra
```

Once all these are installed, `pyyaml` can be installed by:

```
pip3 install pyyaml
```

## Basic Information

Basic information such as your name, website, email address and LinkedIn progile can be modified in the `config.yaml` file. This information will be used on both the CV and cover letter. An example config file would look like:

```
name:     Dominic Schmidt-Toms
website:  domtoms.com
email:    dominictoms9997@gmail.com
linkedin: linkedin.com/in/domtoms
```

The script will generate hyperlinks without needing to specify `https://` at the beginning of urls.

## Profile Generation

The CV features a profile section which should contain a short paragraph about yourself. You can add multiple profiles as text files in the `profiles` directory. Running `build.py` will allow you to select which profile you wish to build the CV with.

```
Select a profile to use
1. Default profile
2. Silly profile
3. Serious profile
>
```

## Cover Letter Generation

Just like profiles, cover letters are stored as text files in the `letters` directory. When the `build.py` script is run, a specific cover letter can be selected. Letters can include `<company>` in place of the companies name. For example:

```
I would love to work at <company>!
```

Would be built into:

```
I would love to work at Apple!
```

If the company is set to Apple when the `build.py` script is run.

## Careers and Education

A list of careers and education can be found in the `careers.yaml` and `education.yaml` files respectively.

```
- role:    Computer Programmer
  company: A Cool Company
  start:   Jan 1970
  end:     Present
  skills:
    - C++
    - Unix
  achievements:
    - Did some cool computer stuff.
    - And more...
```

Each entry contains a role, company, start and end date, a list of skills and a list of achievements. You can have as many entries as possible for both careers and education.

## Building

Once everything is set up, you can run the `build.py` script to generate the CV. All output files will be stored in the `output` directory. The output files include the CV and cover letter as individual PDF files, a PDF file combining both the CV and cover letter as a single PDF file, and finally a text file containing the contents of the cover letter.

