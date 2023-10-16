
def rephrase_text(var1):
    list2 = list(var1.split(" "))
    var1_len = len(list2)
    result = []
    for i in range(0,var1_len,1):
        list1 = list2
        
        for j in range(0,var1_len,1):
            temp = list1[i]
            list1[i] = list1[j]
            list1[j] = temp           
            str = " ".join(list1)
            new = rephrase_sentence(str)
            for k in range(0 ,len(list1),1):
                result.append(new[k])
            temp = list1[i]
            list1[i] = list1[j]
            list1[j] = temp
    return result

def rephrase_sentence(input_sentence):
    words = input_sentence.split()
    result = []

    for i in range(len(words)):
        new_sentence = ' '.join(words[i:] + words[:i])
        result.append(new_sentence)

    return result

result = rephrase_text("foundation structure district mineral")
print(len(result))
for i in range(0,len(result),1):
    print(result[i])
# print(result)

