import json

class json_loader:

	def __init__(self, path, listOfOptions, name):

		self.name = name

		self.configData = ""

		file = open(path,"r")

		self.configData = json.load(file)

		file.close()

		print("Inputed path" + str(path))
		print("Inputed options" + str(listOfOptions))
		print("Retrevied Data" + str(self.configData))

		# for option in listOfOptions:

		# 	self.configs[option].append(self.configData[option])

		# 	print("Added option " + str(option) + " with value " + str(self.configs[option]) + " to " + self.name)

		# print("New Data: " + str(self.configs))

	def getOption(self, option):

		return self.configData[option]


	def setOption(self, option, value):

		#print("Setting option " + self.configData[option] + " to value " + value)
		self.configData[option] = value
		#print("New Data: " + self.configData)

	def saveConfig(self,path):

		file = open(path,"w")

		#print("Saving Data: " + str(self.configData))

		json.dump(self.configData,file,ensure_ascii = False, indent=4)

		file.close()