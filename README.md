# Final Assignment


## 1. Giới thiệu

### Team members

| Student Name    | Student ID |
| -------- | ------- |
|Trương Minh Hoàng|22280034|
|Nguyễn Duy Huân|22280035|

### Question 1: Tích hợp LLM
#### Single Text Translation
- **Mô tả nhiệm vụ**: 
  Viết mã Python sử dụng Gemini API để dịch một đoạn văn bản đầu vào sang tiếng Việt. Giữ nguyên nếu văn bản đã ở ngôn ngữ đích.
- **Ví dụ**: 
  - Đầu vào: `"Hello"` → Đầu ra: `"Xin chào"`.
  - Đầu vào: `"Xin chào"` → Đầu ra: `"Xin chào"`.
#### Multiple Texts Translation 
- **Mô tả nhiệm vụ**: 
  Viết mã Python để dịch danh sách các đoạn văn bản đầu vào sang tiếng Việt. 
- **Ví dụ**:
  - Đầu vào: `["Hello", "I am John", "Tôi là sinh viên"]`  
    → Đầu ra: `["Xin chào", "Tôi tên là John", "Tôi là sinh viên"]`.


### Question 2: Phát triển Chatbot 
#### Data Access and Indexing 
- **Mô tả nhiệm vụ**:
  - Thu thập dữ liệu từ trang web [https://www.presight.io/privacy-policy.html](https://www.presight.io/privacy-policy.html).
  - Xử lý và tổ chức dữ liệu thành một chỉ mục có thể tìm kiếm để hỗ trợ truy vấn thông tin.
#### Chatbot Development 
- **Mô tả nhiệm vụ**:
  - Phát triển chatbot sử dụng xử lý ngôn ngữ tự nhiên (NLP) để trả lời các câu hỏi của người dùng dựa trên dữ liệu đã được thu thập.

## 2.   Chú thích các thư mục
| Thư mục                | Mô tả                               |
|-----------------------|-------------------------------------|
| .env                  | File cấu hình chứa API key           |
| Final Assignment.pdf  | Đề bài tập                          |
| app.py                | Mã nguồn để deploy question 2 trên streamlit |
| data.json             | Dữ liệu thu thập được scrawling và indexing từ trang web |
| requirements.txt      | Danh sách thư viện cần thiết         |
| source.ipynb          | Notebook và mã nguồn cho question 1 và 2 |


## 3. Hướng dẫn sử dụng
### 3.1 Cài đặt môi trường
- Cài đặt Python: Yêu cầu phiên bản Python >= 3.8.
- Cài đặt các thư viện cần thiết: pip install -r requirements.txt
- Cấu hình API thành biến môi trường
### 3.2 Chạy chương trình
#### Question 1 và Question 2
- Mã nguồn của question 1 và 2 được lưu trên file source.ipynb
- Chạy các bài tập riêng lẻ
- Có thể xem chi tiết quá trình scrawling và indexing 
#### Deploy chatbot ở question 2
- Chạy mã nguồn được lưu trong app.py bằng lệnh: streamlit run app.py
- Hoặc truy cập vào link trực tuyến đã tạo và được tag trong source.ipynb
