import csv
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os


# 文件选择弹窗
def choose_file(file_type):
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口
    file_path = filedialog.askopenfilename(title=f"选择{file_type}文件",
                                           filetypes=[(f"{file_type} files", f"*.{file_type.lower()}")])
    return file_path


# 日期格式转换函数
def convert_date_format(date_str):
    # 将 CSV 中的日期格式（YYYY/MM/DD）转换为 TXT 格式（YYYY-MM-DD）
    try:
        return str(datetime.strptime(date_str, '%Y-%m-%d')).split(' ')[0] # 避免转换时生成时分秒
    except ValueError:
        return str(datetime.strptime(date_str.strip(), "%Y/%m/%d").strftime("%Y-%m-%d")).split(' ')[0] # 避免转换时生成时分秒


# 读取 CSV 文件并返回按日期排序的主成分数据
def read_csv(csv_file):
    principal_components = []
    with open(csv_file, mode='r', newline='') as file:
        csvreader = csv.reader(file)
        # 跳过表头
        next(csvreader)
        print("Date in csv file:")
        for row in csvreader:
            date = convert_date_format(row[0])  # 假设时间是 CSV 文件的第一列
            print(date)
            principal_components.append((date, row[1], row[2]))  # 主成分1和2分别是第2列和第3列
    # 按日期降序排序
    principal_components.sort(key=lambda x: x[0],reverse=True)
    return principal_components


# 根据当前时间戳生成新 TXT 文件名
def generate_new_txt_filename(txt_file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(txt_file)
    return f"{base}_{timestamp}{ext}"


# 更新 TXT 文件，添加 Principal Component 列
def update_txt_with_csv(txt_file, principal_components):
    updated_lines = []

    # 读取 TXT 文件内容
    with open(txt_file, mode='r') as file:
        lines = file.readlines()

        # 表头更新，添加 Principal Component 列
        header = lines[0].strip() + ",Principal Component 1,Principal Component 2"
        updated_lines.append(header.strip())  # 将表头添加到更新的行列表中

        # 存储 TXT 文件中的日期
        existing_dates = {line.strip().split(',')[0] for line in lines[1:]}

        # 设置一个指针，指向 CSV 中的当前主成分
        principal_index = 0

        # 遍历 TXT 文件中的每一行
        for line in lines[1:]:
            columns = line.strip().split(',')  # 假设列是用逗号分隔
            timestamp = columns[0].strip()  # 获取日期并去除可能的空格
            # print(timestamp)
            # print(principal_components)
            # print(type(principal_components))
            # print(principal_components[principal_index])
            # 如果当前日期小于或等于当前主成分日期，则更新
            # print(timestamp)
            # print(principal_components[-1][0])
            # print(timestamp < principal_components[-1][0])
            if timestamp < principal_components[-1][0]:
                columns.append('None')  # 如果没有主成分，保持为空
                columns.append('None')
            elif timestamp < principal_components[principal_index][0]:
                principal_index += 1
            if principal_index < len(principal_components) and timestamp >= principal_components[-1][0]:
                current_principal_components = principal_components[principal_index][1], principal_components[principal_index][2]
                columns.append(current_principal_components[0])  # Principal Component 1
                columns.append(current_principal_components[1])  # Principal Component 2
            updated_lines.append(','.join(columns))  # 将更新后的行添加到结果中

        # 遍历 CSV 中的新日期，如果该日期不在 TXT 中，添加新行
        for date, component_1, component_2 in principal_components:
            if date not in existing_dates:
                # 如果 CSV 中的日期不在 TXT 中，添加新行
                new_row = [date] + ['None'] * (len(header.split(',')) - 3)  # 填充空白列
                new_row.append(component_1)  # Principal Component 1
                new_row.append(component_2)  # Principal Component 2
                updated_lines.append(','.join(new_row))

    # 按日期倒序排序结果
    updated_lines.sort(key=lambda x: x.split(',')[0], reverse=True)

    # 生成新的 TXT 文件名
    new_txt_file = generate_new_txt_filename(txt_file)

    # 将更新后的内容写入新的 TXT 文件
    with open(new_txt_file, mode='w') as file:
        for line in updated_lines:
            file.write(line + '\n')

    print(f"文件已成功更新并保存为 {new_txt_file}")


# 主程序
def main():
    # 选择文件
    txt_file = choose_file("TXT")
    csv_file = choose_file("CSV")

    # 读取 CSV 文件并获取 Principal Component 数据
    principal_components = read_csv(csv_file)

    # 更新 TXT 文件并生成新文件
    update_txt_with_csv(txt_file, principal_components)


if __name__ == "__main__":
    main()
