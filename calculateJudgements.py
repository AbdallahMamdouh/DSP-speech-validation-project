from loadMFCC import loadUser, loadReferences
import matplotlib.pyplot as plt
import pandas as pd,numpy as np

print("reading files...")
references = loadReferences('reference')
users = loadUser('users')


for reference in references:
    reference.setTestUtterence()

for user in users:
    user.setTestUtterence()
    user.calculateReference(references)


usersSize = len(users)
print('usersSize: ', usersSize)
# id = int(input('enter user id to analyze: '))
# assert id < usersSize and id>=0, 'user id is out of range'

judgements = np.zeros((3,122,5))
for i,user in enumerate(users):
    print('user: {}, group: {}, student: {}, type: {}, age: {} '.format(i+1,user.group, user.student, user.Type, user.age))
    user.calculateJudgements(judgements,references)
total = [[0,0],[0,0],[0,0]]
totalCorrect = 0
totalWrong = 0
for i,Type in enumerate(judgements):
    for word in Type:
        total[i][0] += word[3]
        total[i][1] += word[4]
    totalCorrect += total[i][0]
    totalWrong += total[i][1]
totalUtterences = totalCorrect+totalWrong
totalMale = total[0][0]+total[0][1]
totalFemale = total[1][0]+total[1][1]
totalChild = total[2][0]+total[2][1]
print("male: correct = {}, wrong = {}, total = {}, correct percentage = {:.2f}%, wrong percentage = {:.2f}%".format(total[0][0],total[0][1],total[0][0]+total[0][1],total[0][0]*100/totalMale,total[0][1]*100/totalMale))
print("female: correct = {}, wrong = {}, total = {}, correct percentage = {:.2f}%, wrong percentage = {:.2f}%".format(total[1][0],total[1][1],total[1][0]+total[1][1],total[1][0]*100/totalFemale,total[1][1]*100/totalFemale))
print("child: correct = {}, wrong = {}, total = {}, correct percentage = {:.2f}%, wrong percentage = {:.2f}%".format(total[2][0],total[2][1],total[2][0]+total[2][1],total[2][0]*100/totalChild,total[2][1]*100/totalChild))


print(judgements)
print('correct',totalCorrect, totalCorrect*100/totalUtterences,"%")
print('wrong',totalWrong, totalWrong*100/totalUtterences,"%")

csvfile = "judgements"
pd.DataFrame(judgements[0,:,:]).to_csv(csvfile+"_male.csv", index=False, header=["other","word2","word1","correct","wrong"])
pd.DataFrame(judgements[1,:,:]).to_csv(csvfile+"_female.csv", index=False, header=["other","word2","word1","correct","wrong"])
pd.DataFrame(judgements[2,:,:]).to_csv(csvfile+"_child.csv", index=False, header=["other","word2","word1","correct","wrong"])



# userId = int(input('enter user id to analyze: '))
# assert userId >=0 and userId < usersSize, 'user id is out of range'

# user = users[userId]
# numberOfUtterences = int(input('enter number of utterences to analyze: '))
# columns = int(np.sqrt(numberOfUtterences))
# rows = int(np.round(numberOfUtterences/columns+0.5))
# i = 0
# j = 0
# while i < numberOfUtterences and j <len(user.utterences):
#     plt.subplot(rows,columns,i+1)
#     dist, reconstructed, distances = user.utterences[j].reconstruct(references[user.reference].utterences[j])
#     j += 1 
#     if distances is not None:
#         plt.plot(distances)
#         i += 1
# plt.show()

types = [
    'M',
    'F',
    'C'
]
sources = [
    'C',
    'M',
    'W'
]


for user in users:
    name = "G{}S{}{}{}{}".format(user.group,user.student,types[user.Type],user.age,sources[user.source])
    plt.figure(name)
    rows = int(np.sqrt(len(user.utterences)))
    columns = int(np.round(len(user.utterences)/rows+0.5))
    for i,utterence in enumerate(user.utterences):
        plt.subplot(rows,columns,i+1)
        dist, reconstructed, distances = utterence.reconstruct(references[user.reference].utterences[i])
        if distances is not None:
            plt.plot(distances)
    print("saving figure: ", name)
    plt.savefig("plots/"+name+".png")