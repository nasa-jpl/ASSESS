import os
import subprocess


def parse_text(pdf):
    filepath = "./data/" + pdf.filename
    if os.path.exists(filepath + "_parsed.txt"):
        # todo: remove this. Caches the parsed text.
        return str(open(filepath + "_parsed.txt", "r").read())
    pdf.write(filepath)
    bashCommand = "java -jar standards_extraction/lib/tika-app-1.16.jar -t " + filepath
    output = ""
    try:
        output = subprocess.check_output(["bash", "-c", bashCommand])
        # file = open(filepath + "_parsed.txt", "wb")
        # file.write(output)
        # file.close()
        # Returns bytestring with lots of tabs and spaces.
        if type(output) == bytes:
            output = output.decode("utf-8").replace("\t",
                                                    " ").replace("\n", " ")
    except subprocess.CalledProcessError as e:
        print(e.output)
    return str(output)
