# Welcome to SCAD-THC3 Documentation!

In a nutshell **SCAD-THC3** is an open-source tool to detect anomalous source code objects (files) in a code repository. The tool uses the fundamental principles of probability and statistics to find anomalous source files in a repository.

>**Note:** This tool was developed as a submission to HACKFEST 2023 by Team Ragnarök.


# Usage

The tool has inbuilt git automation to download multiple repositories while avoiding redundancy. The repo-URLs must be inserted in the **github_table.txt** file, each link in a new line.

To run the CLI-based tool:
>python main.py

>**Note:** Leave the initial input fields empty so that the program can assume default values.



## Principles/Approach

The tool considers only the UTF-8 encoded files (usually source codes and documentations) in the repository. Statistics are calculated of each such file using the **UTF-8** or **ASCII** values of each character in the file. The statistics that we are interested in are the mean and standard deviation of those files. These form multiple samples of the repository (i.e., the population).

All the sample parameters are then used to estimate the population parameters. The population must be approximately normal according to the central limit theorem (**CLT**). This distribution is then modelled and used along with the **Empirical Rule** of statistics to detect the anomalous source/documentation files.

>**Note:** The main idea is to detect how far a source file is from the population mean by-parts to the standard deviation of the natural (Gaussian) distribution.