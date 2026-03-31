import face_recognition
known_image = face_recognition.load_image_file("assets/known.jpg")
unknown_image = face_recognition.load_image_file("assets/unknow4.jpg")

known_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)

# results = face_recognition.compare_faces([known_encoding], unknown_encoding)
# print(*results)

s=[]
for i in range(0, len(unknown_encoding)):
    if face_recognition.compare_faces([known_encoding], unknown_encoding[i])[0] == True:
        s.append(i)
    else:
        continue
if len(s)!=0:
    print(f"Лицо под номером {s[0]+1} - известно")
else:
    print('Известных лиц не найдено')