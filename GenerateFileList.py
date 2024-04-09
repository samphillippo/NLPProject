import sys
import os

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python GenerateFileList.py <folder_path> <output_file_name>")
        sys.exit(1)

    folderPath = sys.argv[1]
    outputFileName = sys.argv[2]

    files = map((lambda file: folderPath + '/' + file), filter(lambda x: x.endswith('.xz'), os.listdir(folderPath)))

    with open(outputFileName, 'w') as file:
        for fileName in files:
            file.write(fileName + '\n')
