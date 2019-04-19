import sys
serverFile = "todo.txt"
f0 = open(serverFile, "r")
fileContent = f0.readlines()
f0.close()
taskNumber = 0
for line in fileContent:
    taskNumber += 1
    print(taskNumber)
    print(line)

##    split = fileContent.split(")")
##    print(split[0])
##    if split[0] != clientParameter:
##        f1.write(line)
