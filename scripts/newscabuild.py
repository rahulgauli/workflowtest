import os
import subprocess


java_8 = {
    "build_tools": ["mavan", "gradle"]
}


subprocess.run(["sudo", "apt", "update"])
subprocess.run(["apt", "install", "-y", "openjdk-8-jdk"])
subprocess.run(["apt", "install", "-y", "maven"])
