# Setup and install Apache Kafka on Windows:

<h3> 1. Install Java 8 SDK:</h3>

Make sure you installed JAVA 8 SDK on your system.  You can use chocolatey ( https://chocolatey.org/ ) windows package manager for the same.

Click Start and type “powershell“. Right-click Windows Powershell and choose “Run as Administrator“. Paste the following command into Powershell and press enter.

Set-ExecutionPolicy Bypass -Scope Process -Force; `
  iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
