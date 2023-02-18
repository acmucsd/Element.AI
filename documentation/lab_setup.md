# Element.AI CSE Basement Lab Setup

## Required

- **When you log in**
  - Run `conda init`
  - Go to [http://128.54.69.222:3000](http://128.54.69.222:3000) into your browser of choice and log in with your ACM AI account. This is where you'll upload submissions.
- **When the repo is made available**
  - ctrl+shift+p
  - in the bar, type Python: Select Interpreter
  - when it prompts you to enter a path, paste in `/home/linux/ieng6/icpc23/public/ai-env`
- **When you begin coding**
  - `conda activate /home/linux/ieng6/icpc23/public/ai-env`


## Sanity Checks

Run the following in a terminal:

### VSCode
#### Check
```
code --list-extensions
```
#### Expected Output
Includes *at least*:
```
ms-python.python
ms-python.vscode-pylance
redhat.java
vscjava.vscode-maven
```

### Java
#### Check
```
java -version
```
#### Expected Output
```
openjdk version "19.0.1" 2022-10-18
OpenJDK Runtime Environment (build 19.0.1+10-21)
OpenJDK 64-Bit Server VM (build 19.0.1+10-21, mixed mode, sharing)
```

### Maven
#### Check
```
mvn -version
```
#### Expected Output
```
Apache Maven 3.9.0 (9b58d2bad23a66be161c4664ef21ce219c2c8584)
Maven home: /home/linux/ieng6/icpc23/public/apache-maven-3.9.0
Java version: 19.0.1, vendor: Oracle Corporation, runtime: /software/CSE/openjdk-19.0.1
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "3.10.0-1160.80.1.el7.x86_64", arch: "amd64", family: "unix"
```