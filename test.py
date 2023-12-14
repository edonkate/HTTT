import numpy as np
import pandas as pd
import csv
file_path = 'Case.xlsx'
retreat_file = 'unAdvisableCase.csv'
from openpyxl import load_workbook
dataset = pd.read_excel(file_path)

def validate_input(prompt, valid_options):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_options:
                break
            else:
                print("Giá trị không hợp lệ. Hãy chọn lại!")
        except ValueError:
            print("Hãy nhập một số nguyên!")
    return value

weight_range = []
for i in range(40, 201):
    weight_range.append(i)

height_range = []
for i in range(100, 251):
    height_range.append(i)

age_range = []
for i in range(0, 150):
    age_range.append(i)

class User:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

def get_bmi(weight, height):
    return weight / (height * height)

def get_bmi_level(bmi):
    if bmi < 18.5:
        return 1
    elif bmi < 24.9:
        return 2
    elif bmi < 29.9:
        return 3
    elif bmi < 34.9:
        return 4
    return 5

bmi_similarity_matrix = np.array([
    [1.0, 0.75, 0.6, 0.3, 0.0],
    [0.75, 1.0, 0.8, 0.6, 0.0],
    [0.6, 0.8, 1.0, 0.75, 0.3],
    [0.3, 0.6, 0.75, 1.0, 0.8],
    [0.0, 0.0, 0.3, 0.8, 1.0]
])

phase_similarity_matrix = np.array([
    [1.0, 0.25, 0.5, 0.75],
    [0.25, 1.0, 0.3, 0.55],
    [0.5, 0.3, 1.0, 0.2],
    [0.75, 0.55, 0.2, 1.0]
])

level_similarity_matrix = np.array([
    [1.0, 0.7, 0.3],
    [0.7, 1.0, 0.75],
    [0.3, 0.75, 1.0]
])

sport_similarity_matrix = np.array([
    [1.0, 0.8, 0.2],
    [0.8, 1.0, 0.3],
    [0.2, 0.3, 1.0]
])

freq_similarity_matrix = np.array([
    [1.0, 0.7, 0.3],
    [0.7, 1.0, 0.65],
    [0.3, 0.65, 1.0]
])


def cbr_recommendation(weight, height, phase, level, sport, frequently, injury):
    x=0
    bmi = get_bmi_level(get_bmi(weight, height))
    for i in range (1,120):
        if dataset.loc[i]['Chấn thương']==injury:
            a = (5 * phase_similarity_matrix[phase-1][int(dataset.loc[i]['Giai đoạn']-1)] + 4 * bmi_similarity_matrix[bmi-1][int(dataset.loc[i]['BMI']-1)] + 3 * level_similarity_matrix[level-1][int(dataset.loc[i]['Cấp độ']-1)] +2 * freq_similarity_matrix[frequently-1][int(dataset.loc[i]['Tần suất tập luyện']-1)] + sport_similarity_matrix[sport-1][int(dataset.loc[i]['Thể thao khác']-1)]) / 15

            if a>x: 
                diet_recommendation = dataset.loc[i]['Dinh dưỡng']
                exercise_recommendation = dataset.loc[i]['Bài tập']
                x=a
    if(x>0.75):
        print('Lời khuyên:')
        print('Thực đơn ăn uống:\n', diet_recommendation)
        print('Chế độ tập luyện:\n', exercise_recommendation)
        print("Lưu ý các bài tập với tạ/thanh đòn có tạ sẽ tập theo mức tạ khi bạn tập hết sức và làm được 10 lần với mức tạ đó")
    else:
        print("Với các thông số bạn đưa ra hệ thống chưa thể đưa ra lời khuyên chính xác, chúng tôi sẽ chuyển tới cho chuyên gia và sẽ đưa cho bạn lời khuyên sớm nhất!")
        data = [bmi, phase, level, sport, frequently, injury]
        # Mở file CSV ở chế độ ghi tiếp
        with open(retreat_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        


def hello_process():
    print('Xin chào, tôi là hệ thống chatbot tư vấn dinh dưỡng và chế độ luyện tập cho vận động viên thể hình với nhiều cấp độ và giai đoạn khác nhau')
    User.name = input('Vui lòng nhập tên của bạn: ')
    print('Xin chào ', User.name)
    User.age = validate_input('Vui lòng nhập tuổi của bạn: ',valid_options=age_range)
    User.gender = input('Vui lòng nhập giới tính của bạn: ')
    print('Xin chào',User.name,User.age,'Tuổi. Giới tính:',User.gender,'. Hãy chọn sẵn sàng nếu bạn muốn bắt đầu nhận tư vấn!')

def question_process():
    while 1:
        x=validate_input('1. Sẵn sàng\n'+
                        '2. Chưa sẵn sàng\n',valid_options=[1, 2])
        if(x==2): 
            print('Xin chào và hẹn gặp lại!')
            break
        w = validate_input('Hãy nhập vào cân nặng(kg): ', valid_options=weight_range)
        h = validate_input('Hãy nhập vào chiều cao(cm): ', valid_options=height_range)
        phase = validate_input('Hãy nhập vào giai đoạn tập luyện: '+'\n'
                            '1. Tăng cơ ' + '\n'
                            '2. Giảm mỡ ' + '\n'
                            '3. Thi đấu ' + '\n'
                            '4. Phục hồi ' + '\n', valid_options=[1, 2, 3, 4])
        level = validate_input('Hãy nhập vào cường độ tập luyện mong muốn: '+'\n'
                            '1. Ít ' + '\n'
                            '2. Trung bình ' + '\n'
                            '3. Nhiều ' + '\n', valid_options=[1, 2, 3])
        sport = validate_input('Hãy chọn các môn thể thao khác hay chơi: '+'\n'
                            '1. Không ' + '\n'
                            '2. Các môn thể thao ít vận động (cờ vua, esport, ...)' + '\n'
                            '3. Các môn thể thao vận động nhiều (đá bóng, bơi lội, ...) ' + '\n', valid_options=[1, 2, 3])
        freq = validate_input('Hãy nhập thời gian tập luyện mong muốn: '+'\n'
                            '1. Ít (1 - 3 buổi/ tuần)' + '\n'
                            '2. Trung bình (2 - 4 buổi/ tuần)' + '\n'
                            '3. Nhiều (3 - 5 buổi/ tuần)' + '\n', valid_options=[1, 2, 3])
        injury = validate_input('Bạn có đang gặp chấn thương nào không: '+'\n'
                            '1. Không ' + '\n'
                            '2. Chấn thương tay ' + '\n'
                            '3. Chấn thương chân ' + '\n'
                            '4. Chấn thương ngực ' + '\n', valid_options=[1, 2, 3, 4])
        cbr_recommendation(w, h/100, phase, level, sport, freq, injury)

        if validate_input('Bạn có muốn được tư vấn tiếp không: '+'\n'
                    '1. Có ' + '\n'
                    '2. Không' + '\n', valid_options=[1, 2])==2: 
            print('Xin chào và hẹn gặp lại!')
            break


if __name__ == "__main__":
    hello_process()
    question_process()