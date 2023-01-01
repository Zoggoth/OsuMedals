import re
beatmapIDToName = {}
postdate = "2020-01-01 00:00:00"
standardPostdate = postdate


class play:
    ID = 0
    beatmap = 0
    user = 0
    FC = False
    modCode = 0
    date = ""

    def __repr__(self):
        return "ID: "+str(self.ID)+" BeatmapID: "+str(self.beatmap)+" userID: "+str(self.user)+" FC: "+str(self.FC)+" modCode: "+str(self.modCode)+" Date: "+self.date


class beatmap:
    ID = 0
    difficulty = {}

    def __repr__(self):
        return "ID: "+str(self.ID)+" SR: "+str(self.difficulty)


def modCodeToText(modCode):
    output = ""
    if modCode & 1:
        output += "NF"
    if modCode & 2:
        output += "EZ"
    if modCode & 4:
        output += "TD"
    if modCode & 8:
        output += "HD"
    if modCode & 16:
        output += "HR"
    if modCode & 32:
        if modCode & 16384:
            output += "PF"
        else:
            output += "SD"
    if modCode & 64:
        if modCode & 512:
            output += "NC"
        else:
            output += "DT"
    if modCode & 256:
        output += "HT"
    if modCode & 1024:
        output += "FL"
    if modCode & 4096:
        output += "SO"
    if modCode & 32768:
        output += "4K"
    if modCode & 65536:
        output += "5K"
    if modCode & 131072:
        output += "6K"
    if modCode & 262144:
        output += "7K"
    if modCode & 524288:
        output += "8K"
    if modCode & 1048576:
        output += "FI"
    if modCode & 16777216:
        output += "9K"
    if modCode & 1073741824:
        output += "MR"
    return output


def modCodeToDifficultyCode(modCode):
    return modCode & 17793366


def output(IDToBeatmap, userToPlays, name):
    mapAndModCodeToCountPass = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    mapAndModCodeToCountFC = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    for x in userToPlays:
        firstPass = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        firstPassDate = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        firstFC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        firstFCDate = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for y in userToPlays[x]:
            if y.modCode & 259 == 0:
                stars = int(IDToBeatmap[y.beatmap].difficulty[modCodeToDifficultyCode(y.modCode)])
                if 1 <= stars <= 10:
                    if firstPassDate[stars - 1] == 0:
                        firstPass[stars - 1] = (str(y.beatmap), osumodCodeToDifficultyCode(y.modCode))
                        firstPassDate[stars - 1] = y.date
                    else:
                        if y.date < firstPassDate[stars - 1]:
                            firstPass[stars - 1] = (str(y.beatmap), osumodCodeToDifficultyCode(y.modCode))
                            firstPassDate[stars - 1] = y.date
                    if y.FC:
                        if firstFCDate[stars - 1] == 0:
                            firstFC[stars - 1] = (str(y.beatmap), osumodCodeToDifficultyCode(y.modCode))
                            firstFCDate[stars - 1] = y.date
                        else:
                            if y.date < firstFCDate[stars - 1]:
                                firstFC[stars - 1] = (str(y.beatmap), osumodCodeToDifficultyCode(y.modCode))
                                firstFCDate[stars - 1] = y.date
        for i in range(0, 10):
            if firstPass[i] != 0:
                if firstPassDate[i] >= postdate:
                    mapAndModCodeToCountPass[i][firstPass[i]] = mapAndModCodeToCountPass[i].get(firstPass[i], 0) + 1
            if firstFC[i] != 0:
                if firstFCDate[i] >= postdate:
                    mapAndModCodeToCountFC[i][firstFC[i]] = mapAndModCodeToCountFC[i].get(firstFC[i], 0) + 1
    file = open(name+"/output.txt", "w")
    file.write("All Pass/FC medals since "+postdate+"\nOn common medals, only maps played by several people will appear\n\n")
    for i in range(0, 10):
        best = sorted(mapAndModCodeToCountFC[i].items(), key=lambda item: item[1], reverse=True)
        count = 0
        for x in best:
            count += x[1]
        file.write(str(i + 1) + " Star FC (")
        file.write(str(count) + ")\n")
        for x in best:
            if x[1] >= count / 200:
                if modCodeToText(x[0][1]) == "":
                    file.write(str(x[1]) + ": " + beatmapIDToName[x[0][0]] + " https://osu.ppy.sh/b/" + x[0][0] + "\n")
                else:
                    file.write(str(x[1]) + ": " + beatmapIDToName[x[0][0]] + " +" + modCodeToText(x[0][1]) + " https://osu.ppy.sh/b/" + x[0][0] + "\n")
        file.write("\n")
    file.write("\n")
    for i in range(0, 10):
        best = sorted(mapAndModCodeToCountPass[i].items(), key=lambda item: item[1], reverse=True)
        count = 0
        for x in best:
            count += x[1]
        file.write(str(i + 1) + " Star Pass (")
        file.write(str(count) + ")\n")
        for x in best:
            if x[1] >= count / 200:
                if modCodeToText(x[0][1]) == "":
                    file.write(str(x[1]) + ": " + beatmapIDToName[x[0][0]] + " https://osu.ppy.sh/b/" + x[0][0] + "\n")
                else:
                    file.write(str(x[1]) + ": " + beatmapIDToName[x[0][0]] + " +" + modCodeToText(x[0][1]) + " https://osu.ppy.sh/b/" + x[0][0] + "\n")
        file.write("\n")
    file.close()


def catch():
    file = open("fruits/osu_scores_fruits_high.sql", "r", encoding="utf-8")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),(?P<Beatmap>\d+),(?P<User>\d+),\d+,\d+,'\wH?',\d+,\d+,\d+,\d+,\d+,\d+,(?P<FC>0|1),(?P<ModCode>\d+),'(?P<Date>[^']*)',\d", text)
    userToPlays = {}
    textToModCode = {}
    for x in capture:
        newPlay = play()
        newPlay.ID = int(x["ID"])
        newPlay.beatmap = int(x["Beatmap"])
        newPlay.user = int(x["User"])
        newPlay.FC = (x["FC"] == "1")
        newPlay.modCode = int(x["ModCode"])
        if newPlay.modCode & 4:  # TD doesn't exist in catch, this was the easiest way to fix 2 plays that have it
            newPlay.modCode = newPlay.modCode - 4
        newPlay.date = x["Date"]
        if newPlay.user not in userToPlays:
            userToPlays[newPlay.user] = []
        userToPlays[newPlay.user].append(newPlay)
        text = modCodeToText(newPlay.modCode)
        if text not in textToModCode:
            textToModCode[text] = {}
        textToModCode[text][newPlay.modCode] = newPlay.ID
    # for x in userToPlays:
    #     for y in userToPlays[x]:
    #         print(y)
    # for x in textToModCode:
    #     print(x)
    #     print(textToModCode[x])
    file = open("fruits/osu_beatmap_difficulty.sql", "r")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),2,(?P<ModCode>\d+),(?P<SR>\d+(?:\.\d+)?)", text)
    IDToBeatmap = {}
    for x in capture:
        if int(x["ID"]) not in IDToBeatmap:
            newbeatmap = beatmap()
            newbeatmap.ID = int(x["ID"])
            newbeatmap.difficulty = {}
            IDToBeatmap[newbeatmap.ID] = newbeatmap
        IDToBeatmap[int(x["ID"])].difficulty[int(x["ModCode"])] = float(x["SR"])
    output(IDToBeatmap, userToPlays, "fruits")


def taiko():
    file = open("taiko/osu_scores_taiko_high.sql", "r", encoding="utf-8")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),(?P<Beatmap>\d+),(?P<User>\d+),\d+,\d+,'\wH?',\d+,\d+,\d+,\d+,\d+,\d+,(?P<FC>0|1),(?P<ModCode>\d+),'(?P<Date>[^']*)',\d", text)
    userToPlays = {}
    textToModCode = {}
    for x in capture:
        newPlay = play()
        newPlay.ID = int(x["ID"])
        newPlay.beatmap = int(x["Beatmap"])
        newPlay.user = int(x["User"])
        newPlay.FC = (x["FC"] == "1")
        newPlay.modCode = int(x["ModCode"])
        if newPlay.modCode & 4:  # TD doesn't exist in catch, this was the easiest way to fix 2 plays that have it
            newPlay.modCode = newPlay.modCode - 4
        newPlay.date = x["Date"]
        if newPlay.user not in userToPlays:
            userToPlays[newPlay.user] = []
        userToPlays[newPlay.user].append(newPlay)
        text = modCodeToText(newPlay.modCode)
        if text not in textToModCode:
            textToModCode[text] = {}
        textToModCode[text][newPlay.modCode] = newPlay.ID
        if newPlay.modCode & 4:
            print(newPlay.ID)
    # for x in userToPlays:
    #     for y in userToPlays[x]:
    #         print(y)
    # for x in textToModCode:
    #     print(x)
    #     print(textToModCode[x])
    file = open("taiko/osu_beatmap_difficulty.sql", "r")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),1,(?P<ModCode>\d+),(?P<SR>\d+(?:\.\d+)?)", text)
    IDToBeatmap = {}
    for x in capture:
        if int(x["ID"]) not in IDToBeatmap:
            newbeatmap = beatmap()
            newbeatmap.ID = int(x["ID"])
            newbeatmap.difficulty = {}
            IDToBeatmap[newbeatmap.ID] = newbeatmap
        IDToBeatmap[int(x["ID"])].difficulty[int(x["ModCode"])] = float(x["SR"])
    output(IDToBeatmap, userToPlays, "taiko")


def mania():
    file = open("mania/osu_scores_mania_high.sql", "r", encoding="utf-8")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),(?P<Beatmap>\d+),(?P<User>\d+),\d+,\d+,'\wH?',\d+,\d+,\d+,\d+,\d+,\d+,(?P<FC>0|1),(?P<ModCode>\d+),'(?P<Date>[^']*)',\d", text)
    userToPlays = {}
    textToModCode = {}
    for x in capture:
        newPlay = play()
        newPlay.ID = int(x["ID"])
        newPlay.beatmap = int(x["Beatmap"])
        newPlay.user = int(x["User"])
        newPlay.FC = (x["FC"] == "1")
        newPlay.modCode = int(x["ModCode"])
        if newPlay.modCode & 4:  # TD doesn't exist in catch, this was the easiest way to fix 2 plays that have it
            newPlay.modCode = newPlay.modCode - 4
        newPlay.date = x["Date"]
        if newPlay.user not in userToPlays:
            userToPlays[newPlay.user] = []
        userToPlays[newPlay.user].append(newPlay)
        text = modCodeToText(newPlay.modCode)
        if text not in textToModCode:
            textToModCode[text] = {}
        textToModCode[text][newPlay.modCode] = newPlay.ID
    # for x in userToPlays:
    #     for y in userToPlays[x]:
    #         print(y)
    # for x in textToModCode:
    #     print(x)
    #     print(textToModCode[x])
    file = open("mania/osu_beatmap_difficulty.sql", "r")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),3,(?P<ModCode>\d+),(?P<SR>\d+(?:\.\d+)?)", text)
    IDToBeatmap = {}
    for x in capture:
        if int(x["ID"]) not in IDToBeatmap:
            newbeatmap = beatmap()
            newbeatmap.ID = int(x["ID"])
            newbeatmap.difficulty = {}
            IDToBeatmap[newbeatmap.ID] = newbeatmap
        IDToBeatmap[int(x["ID"])].difficulty[int(x["ModCode"])] = float(x["SR"])
    output(IDToBeatmap, userToPlays, "mania")


def osumodCodeToDifficultyCode(modCode):
    modCode = modCode & 1374
    if modCode & 1032 == 8:
        modCode -= 8
    return modCode


def osu():
    file = open("osu/osu_scores_high.sql", "r", encoding="utf-8")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),(?P<Beatmap>\d+),(?P<User>\d+),\d+,\d+,'\wH?',\d+,\d+,\d+,\d+,\d+,\d+,(?P<FC>0|1),(?P<ModCode>\d+),'(?P<Date>[^']*)',\d", text)
    userToPlays = {}
    textToModCode = {}
    for x in capture:
        newPlay = play()
        newPlay.ID = int(x["ID"])
        newPlay.beatmap = int(x["Beatmap"])
        newPlay.user = int(x["User"])
        newPlay.FC = (x["FC"] == "1")
        newPlay.modCode = int(x["ModCode"])
        newPlay.date = x["Date"]
        if newPlay.user not in userToPlays:
            userToPlays[newPlay.user] = []
        userToPlays[newPlay.user].append(newPlay)
        text = modCodeToText(newPlay.modCode)
        if text not in textToModCode:
            textToModCode[text] = {}
        textToModCode[text][newPlay.modCode] = newPlay.ID
    file = open("osu/osu_scores_random.sql", "r", encoding="utf-8")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),(?P<Beatmap>\d+),(?P<User>\d+),\d+,\d+,'\wH?',\d+,\d+,\d+,\d+,\d+,\d+,(?P<FC>0|1),(?P<ModCode>\d+),'(?P<Date>[^']*)',\d", text)
    for x in capture:
        newPlay = play()
        newPlay.ID = int(x["ID"])
        newPlay.beatmap = int(x["Beatmap"])
        newPlay.user = int(x["User"])
        newPlay.FC = (x["FC"] == "1")
        newPlay.modCode = int(x["ModCode"])
        newPlay.date = x["Date"]
        if newPlay.user not in userToPlays:
            userToPlays[newPlay.user] = []
        userToPlays[newPlay.user].append(newPlay)
        text = modCodeToText(newPlay.modCode)
        if text not in textToModCode:
            textToModCode[text] = {}
        textToModCode[text][newPlay.modCode] = newPlay.ID
    file = open("osu/osu_beatmap_difficulty.sql", "r")
    text = file.read()
    file.close()
    capture = re.finditer(r"\((?P<ID>\d+),0,(?P<ModCode>\d+),(?P<SR>\d+(?:\.\d+)?)", text)
    IDToBeatmap = {}
    for x in capture:
        if int(x["ID"]) not in IDToBeatmap:
            newbeatmap = beatmap()
            newbeatmap.ID = int(x["ID"])
            newbeatmap.difficulty = {}
            IDToBeatmap[newbeatmap.ID] = newbeatmap
        IDToBeatmap[int(x["ID"])].difficulty[int(x["ModCode"])] = float(x["SR"])
    mapAndModCodeToCountPass = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    mapAndModCodeToCountFC = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    for x in userToPlays:
        firstPass = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        firstPassDate = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        firstFC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        firstFCDate = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for y in userToPlays[x]:
            if y.modCode & 259 == 0:
                stars = int(IDToBeatmap[y.beatmap].difficulty[osumodCodeToDifficultyCode(y.modCode)])
                if 1 <= stars <= 10:
                    if firstPassDate[stars - 1] == 0:
                        firstPass[stars - 1] = (str(y.beatmap), osumodCodeToDifficultyCode(y.modCode))
                        firstPassDate[stars - 1] = y.date
                    else:
                        if y.date < firstPassDate[stars - 1]:
                            firstPass[stars - 1] = (str(y.beatmap), osumodCodeToDifficultyCode(y.modCode))
                            firstPassDate[stars - 1] = y.date
                    if y.FC:
                        if firstFCDate[stars - 1] == 0:
                            firstFC[stars - 1] = (str(y.beatmap), osumodCodeToDifficultyCode(y.modCode))
                            firstFCDate[stars - 1] = y.date
                        else:
                            if y.date < firstFCDate[stars - 1]:
                                firstFC[stars - 1] = (str(y.beatmap), osumodCodeToDifficultyCode(y.modCode))
                                firstFCDate[stars - 1] = y.date
        for i in range(0, 10):
            if firstPass[i] != 0:
                if firstPassDate[i] >= standardPostdate:
                    mapAndModCodeToCountPass[i][firstPass[i]] = mapAndModCodeToCountPass[i].get(firstPass[i], 0) + 1
            if firstFC[i] != 0:
                if firstFCDate[i] >= standardPostdate:
                    mapAndModCodeToCountFC[i][firstFC[i]] = mapAndModCodeToCountFC[i].get(firstFC[i], 0) + 1
    file = open("osu/output.txt", "w")
    file.write("All Pass/FC medals since "+standardPostdate+"\nOn common medals, only maps played by several people will appear\n\n")
    for i in range(0, 10):
        best = sorted(mapAndModCodeToCountFC[i].items(), key=lambda item: item[1], reverse=True)
        count = 0
        for x in best:
            count += x[1]
        file.write(str(i + 1) + " Star FC (")
        file.write(str(count) + ")\n")
        for x in best:
            if x[1] >= count / 200:
                if modCodeToText(x[0][1]) == "":
                    file.write(str(x[1]) + ": " + beatmapIDToName[x[0][0]] + " https://osu.ppy.sh/b/" + x[0][0] + "\n")
                else:
                    file.write(str(x[1]) + ": " + beatmapIDToName[x[0][0]] + " +" + modCodeToText(x[0][1]) + " https://osu.ppy.sh/b/" + x[0][0] + "\n")
        file.write("\n")
    file.write("\n")
    for i in range(0, 10):
        best = sorted(mapAndModCodeToCountPass[i].items(), key=lambda item: item[1], reverse=True)
        count = 0
        for x in best:
            count += x[1]
        file.write(str(i + 1) + " Star Pass (")
        file.write(str(count) + ")\n")
        for x in best:
            if x[1] >= count / 200:
                if modCodeToText(x[0][1]) == "":
                    file.write(str(x[1]) + ": " + beatmapIDToName[x[0][0]] + " https://osu.ppy.sh/b/" + x[0][0] + "\n")
                else:
                    file.write(str(x[1]) + ": " + beatmapIDToName[x[0][0]] + " +" + modCodeToText(x[0][1]) + " https://osu.ppy.sh/b/" + x[0][0] + "\n")
        file.write("\n")
    file.close()


file = open("osu_beatmaps.sql", "r", encoding="utf-8")
text = file.read()
file.close()
capture = re.finditer(r"\((?P<ID>\d+),\d+,\d+,'(?P<Name>[^']*?(?:\\'[^']*?)*).osu'", text)
for x in capture:
    beatmapIDToName[x["ID"]] = x["Name"].replace(r"\'", "'")
osu()
taiko()
catch()
mania()
