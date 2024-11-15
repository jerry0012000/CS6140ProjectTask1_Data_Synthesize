# Jingming Cheng November 14th 2024.
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
    return datetime.strptime(date_str.strip(), "%Y/%m/%d").strftime("%Y-%m-%d")


# 读取 CSV 文件并返回日期与主成分列的数据
def read_csv(csv_file):
    principal_components = {}
    with open(csv_file, mode='r', newline='') as file:
        csvreader = csv.reader(file)
        # 跳过表头
        header = file.readline().strip()
        print(header)
        for row in csvreader:
            date = row[0]  # 假设时间是 CSV 文件的第一列
            principal_components[date] = (row[1], row[2])  # 假设主成分在第2列和第3列
    return header, principal_components


# 根据当前时间戳生成新 TXT 文件名
def generate_new_txt_filename(txt_file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(txt_file)
    return f"{base}_{timestamp}{ext}"


# 更新 TXT 文件，添加 Principal Component 列
def update_txt_with_csv(txt_file, csv_headers, principal_components):
    print(principal_components)
    updated_lines = []

    # 读取 TXT 文件内容
    with open(txt_file, mode='r') as file:
        lines = file.readlines()

        # 跳过表头
        header = lines[0].strip() + csv_headers # 表头拼接
        updated_lines.append(header.strip())  # 将表头添加到更新的行列表中

        # 存储 TXT 文件中的日期
        existing_dates = {line.strip().split(',')[0] for line in lines[1:]}
        for line in lines[1:]:
            columns = line.strip().split(',')  # 假设列是用逗号分隔
            timestamp = columns[0].strip()  # 去除可能的空格

            if timestamp in principal_components:
                # 如果找到匹配的日期，加入 Principal Component 1 和 2
                columns.append(principal_components[timestamp][0])  # Principal Component 1
                columns.append(principal_components[timestamp][1])  # Principal Component 2
            updated_lines.append(','.join(columns))

        # 遍历 CSV 中的新日期，如果该日期不在 TXT 中，添加新行
        for date, components in principal_components.items():
            if date not in existing_dates:
                # 如果 CSV 中的日期不在 TXT 中，添加一行
                new_row = [date] + [''] * (len(header.strip().split(',')) - 3)  # 填充空白列
                new_row.append(components[0])  # Principal Component 1
                new_row.append(components[1])  # Principal Component 2
                updated_lines.append(','.join(new_row))
        updated_lines.sort(reverse=True)

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
    header, principal_components = read_csv(csv_file)

    # 更新 TXT 文件并生成新文件
    update_txt_with_csv(txt_file, header, principal_components)


if __name__ == "__main__":
    main()
