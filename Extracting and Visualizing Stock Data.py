# Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this assignment, you will extract some stock data, you will then display this data in a graph.(Trích xuất dữ liệu cần thiết từ tập dữ liệu và hiển thị nó là một phần cần thiết của khoa học dữ liệu; do đó các cá nhân có thể đưa ra quyết định chính xác dựa trên dữ liệu. Trong bài tập này, bạn sẽ trích xuất một số dữ liệu chứng khoán, sau đó bạn sẽ hiển thị dữ liệu này dưới dạng biểu đồ.)

# Table of Contents
# Define a Function that Makes a Graph
# Question 1: Use yfinance to Extract Stock Data
# Question 2: Use Webscraping to Extract Tesla Revenue Data
# Question 3: Use yfinance to Extract Stock Data
# Question 4: Use Webscraping to Extract GME Revenue Data
# Question 5: Plot Tesla Stock Graph
# Question 6: Plot GameStop Stock Graph


#Nhập thư viện
import yfinance as yf
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os


# Bỏ qua cảnh báo
import warnings
warnings.filterwarnings("ignore", category = FutureWarning)


# Define Graphing Function. In this section, we define the function make_graph. You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.(Xác định hàm đồ thị. Trong phần này, chúng ta định nghĩa hàm make_graph. Bạn không cần phải biết chức năng hoạt động như thế nào, bạn chỉ nên quan tâm đến đầu vào. Nó lấy một khung dữ liệu có dữ liệu chứng khoán (khung dữ liệu phải chứa cột Ngày và Đóng), khung dữ liệu có dữ liệu doanh thu (khung dữ liệu phải chứa cột Ngày và Doanh thu) và tên của cổ phiếu.)


def make_graph(stock_data, revenue_data, stock):
	fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
	stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
	revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
	fig.add_trace(go.Scatter(x = pd.to_datetime(stock_data_specific.Date, infer_datetime_format = True), y = stock_data_specific.Close.astype("float"), name = "Share Price"), row = 1, col = 1)
	fig.add_trace(go.Scatter(x = pd.to_datetime(revenue_data_specific.Date, infer_datetime_format = True), y =revenue_data_specific.Revenue.astype("float"), name = "Revenue"), row = 2, col = 1)
	fig.update_xaxes(title_text = "Date", row = 1, col = 1)
	fig.update_xaxes(title_text = "Date", row = 2, col = 1)
	fig.update_yaxes(title_text = "Price ($US)", row = 1, col = 1)
	fig.update_yaxes(title_text = "Revenue ($US Millions)", row = 2, col = 1)
	fig.update_layout(showlegend = False,
	height = 900,
	title = stock,
	xaxis_rangeslider_visible = True)
	fig.show()


# Use the make_graph function that we’ve already defined. You’ll need to invoke it in questions 5 and 6 to display the graphs and create the dashboard.
# Note: You don’t need to redefine the function for plotting graphs anywhere else in this notebook; just use the existing function.(Sử dụng hàm make_graph mà chúng ta đã xác định. Bạn sẽ cần gọi nó trong câu hỏi 5 và 6 để hiển thị biểu đồ và tạo trang tổng quan. Lưu ý: Bạn không cần xác định lại chức năng vẽ đồ thị ở bất kỳ nơi nào khác trong sổ ghi chép này; chỉ cần sử dụng chức năng hiện có.)

# Question 1: Use yfinance to Extract Stock Data. Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is TSLA.(Câu hỏi 1: Sử dụng yfinance để trích xuất dữ liệu chứng khoán. Sử dụng hàm Ticker nhập mã cổ phiếu của cổ phiếu mà chúng ta muốn trích xuất dữ liệu để tạo đối tượng mã cổ phiếu. Cổ phiếu là Tesla và mã chứng khoán là TSLA.)
Tesla = yf.Ticker('TSLA')
print(Tesla)


	#Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data. Set the period parameter to "max" so we get information for the maximum amount of time.(Sử dụng đối tượng mã đánh dấu và lịch sử hàm để trích xuất thông tin chứng khoán và lưu nó vào khung dữ liệu có tên tesla_data. Đặt tham số khoảng thời gian thành "tối đa" để chúng tôi nhận được thông tin trong khoảng thời gian tối đa.)

tesla_data = Tesla.history(period = "max")
print(type(tesla_data))
print(tesla_data)
print("---------------------------------------------------------------------------------------------------------------------")


	# Reset the index using the reset_index(inplace=True) function on the tesla_data DataFrame and display the first five rows of the tesla_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.(Đặt lại chỉ mục bằng cách sử dụng hàm reset_index(inplace=True) trên DataFrame tesla_data và hiển thị năm hàng đầu tiên của khung dữ liệu tesla_data bằng hàm head. Chụp màn hình kết quả và code từ đầu câu 1 đến kết quả bên dưới.)
tesla_data.reset_index(inplace = True)
print(tesla_data.head())
print("---------------------------------------------------------------------------------------------------------------------")


# Question 2: Use Webscraping to Extract Tesla Revenue Data
# Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named html_data.(Câu hỏi 2: Sử dụng Webscraping để trích xuất dữ liệu doanh thu của Tesla. Sử dụng thư viện yêu cầu để tải xuống trang web https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Lưu văn bản của phản hồi dưới dạng một biến có tên html_data.)
url = " https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
path = os.path.join(os.getcwd(),'html_data.txt')
html_data = requests.get(url).text
print(html_data)
print("---------------------------------------------------------------------------------------------------------------------")


#Parse the html data using beautiful_soup using parser i.e html5lib or html.parser, Using BeautifulSoup or the read_html function extract the table with Tesla Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue.(Sử dụng hàm BeautifulSoup hoặc hàm read_html để trích xuất bảng bằng Tesla Revenue và lưu trữ bảng đó vào khung dữ liệu có tên tesla_revenue. Khung dữ liệu phải có các cột Ngày và Doanh thu.)
soup = BeautifulSoup(html_data, "html.parser")
print(soup)
print("---------------------------------------------------------------------------------------------------------------------")
print(soup.prettify())
print("---------------------------------------------------------------------------------------------------------------------")

# Using BeautifulSoup or the read_html function extract the table with Tesla Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue.
# Step-by-step instructions
# Here are the step-by-step instructions:
	# 1. Create an Empty DataFrame
	# 2. Find the Relevant Table
	# 3. Check for the Tesla Quarterly Revenue Table
	# 4. Iterate Through Rows in the Table Body
	# 5. Extract Data from Columns
	# 6. Append Data to the DataFrame

# 1. Create an Empty DataFrame	
tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"])


# 2. Find the Relevant Table
Relevant_tables = soup.find_all("tbody")[1]
print(Relevant_tables)
print("---------------------------------------------------------------------------------------------------------------------")

# 3. Check for the Tesla Quarterly Revenue Table(tự xem trên web)

#4. Iterate Through Rows in the Table Body
for row in Relevant_tables.find_all('tr'):
	col = row.find_all("td")

# 5. Extract Data from Columns
	date = col[0].text	 	
	revenue = col[1].text

# 6. Append Data to the DataFrame
	tesla_revenue = pd.concat([tesla_revenue,pd.DataFrame({"Date":[date], "Revenue": [revenue]})], ignore_index = True)

print(tesla_revenue.head())
print("---------------------------------------------------------------------------------------------------------------------")

#Execute the following lines to remove an null or empty strings in the Revenue column.
tesla_revenue.dropna(inplace = True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


#Execute the following line to remove the comma and dollar sign from the Revenue column.
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace('[$,]', '', regex = True).astype(int)
print(tesla_revenue)
print("---------------------------------------------------------------------------------------------------------------------")


#Display the last 5 row of the tesla_revenue dataframe using the tail function
print(tesla_revenue.tail(5))
print("---------------------------------------------------------------------------------------------------------------------")

# Question 3: Use yfinance to Extract Stock Data
# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is GME.(Câu hỏi 3: Sử dụng yfinance để trích xuất dữ liệu chứng khoán. Sử dụng hàm Ticker nhập mã cổ phiếu của cổ phiếu mà chúng ta muốn trích xuất dữ liệu để tạo đối tượng mã cổ phiếu. Cổ phiếu là GameStop và mã cổ phiếu của nó là GME.)
GameStop = yf.Ticker("GME")
print(GameStop)


# Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data. Set the period parameter to "max" so we get information for the maximum amount of time.
gme_data = GameStop.history(period = 'max')
print(gme_data)
print("---------------------------------------------------------------------------------------------------------------------")


#Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.(Đặt lại chỉ mục bằng cách sử dụng hàm reset_index(inplace=True) trên Khung dữ liệu gme_data và hiển thị năm hàng đầu tiên của khung dữ liệu gme_data bằng hàm head. Chụp màn hình kết quả và code từ đầu câu 3 đến kết quả bên dưới.)
gme_data.reset_index(inplace = True)
print(gme_data.head())
print("---------------------------------------------------------------------------------------------------------------------")



# Question 4: Use Webscraping to Extract GME Revenue Data
# Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named html_data_2.
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2 = requests.get(url).text
print(html_data_2)
print("---------------------------------------------------------------------------------------------------------------------")


#Using BeautifulSoup or the read_html function extract the table with GameStop Revenue and store it into a dataframe named gme_revenue. The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column.
soup = BeautifulSoup(html_data_2, "html.parser")
print(soup)
print("---------------------------------------------------------------------------------------------------------------------")

#Bước 1: tạo một dataframe rỗng
gme_revenue = pd.DataFrame(["Date", "Revenue"])

#Bước 2: Tìm bảng liên quan
Relevant_tables = soup.find_all("tbody")[1]
print(Relevant_tables)
print("---------------------------------------------------------------------------------------------------------------------")


#Bước 3: tự check bảng ở trang web

#Bước 4: Lặp qua từng hàng và cột để lấy giá trị
for row in Relevant_tables.find_all('tr'):
	col = row.find_all('td')

#Bước 5: lấy giá trị
	date = col[0].text
	revenue = col[1].text


#Bước 6: cộng các giá trị này vào dataframe rỗng đã được tạo:
	gme_revenue = pd.concat([gme_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index = True)	
gme_revenue = gme_revenue.drop(columns = [0])	
print(gme_revenue)	
print("---------------------------------------------------------------------------------------------------------------------")

#Xoá giá trị rỗng
gme_revenue.dropna(inplace = True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]


#Xoá dấu dollar và dấu phẩy
gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace('[$,]', '', regex=True).astype(int)
print(gme_revenue)
print(gme_revenue.tail(5))
print("---------------------------------------------------------------------------------------------------------------------")



# Question 5: Plot Tesla Stock Graph
# Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph. Note the graph will only show data upto June 2021.(Câu 5: Vẽ đồ thị cổ phiếu Tesla, Sử dụng hàm make_graph để vẽ biểu đồ Dữ liệu chứng khoán Tesla, đồng thời cung cấp tiêu đề cho biểu đồ. Lưu ý biểu đồ sẽ chỉ hiển thị dữ liệu cho đến tháng 6 năm 2021.)
# You just need to invoke the make_graph function with the required parameter to print the graphs.The structure to call the `make_graph` function is `make_graph(tesla_data, tesla_revenue, 'Tesla')(Bạn chỉ cần gọi hàm make_graph với tham số bắt buộc để in biểu đồ. Cấu trúc để gọi hàm `make_graph` là `make_graph(tesla_data, tesla_revenue, 'Tesla'))
 #make_subplots là một hàm từ thư viện plotly giúp tạo nhiều đồ thị con (subplots) trên cùng một biểu đồ.
# Các tham số ý nghĩa như sau:
			# rows = 2, cols = 1: Tạo hai hàng và một cột cho biểu đồ, tức là biểu đồ sẽ có 2 phần riêng biệt xếp chồng theo chiều dọc.
			# shared_xaxes = True: Cả hai đồ thị con sẽ dùng chung trục x (dòng thời gian).
			# subplot_titles: Tiêu đề riêng cho mỗi đồ thị con, ở đây lần lượt là:
			# Historical Share Price (Lịch sử giá cổ phiếu).
			# Historical Revenue (Lịch sử doanh thu).
			# vertical_spacing=0.3: Khoảng cách dọc giữa 2 đồ thị con
def make_graph2(stock_data, revenue_data, stock):
	fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
	stock_data_specific = stock_data[stock_data.Date <= '2021-06-30'] #chỉ lấy giá trị date trong và sau ngày 1/6/2021
	revenue_data_specific = revenue_data[revenue_data.Date <= '2021-06-30'] ##chỉ lấy giá trị date trong và sau ngày 1/6/2021


#Thêm dữ liệu đồ thị vào biểu đồ, go.Scatter: Dùng để tạo một biểu đồ đường (line chart).
		# x: Trục x là ngày tháng (dữ liệu trong cột Date), được chuyển thành kiểu datetime bằng pd.to_datetime.
		# y: Trục y là giá đóng cửa (Close) từ stock_data_specific. Dữ liệu được chuyển sang kiểu float để đảm bảo tính toán chính xác.
		# name: Tên của trace là “Share Price” (Giá cổ phiếu).
	fig.add_trace(go.Scatter(x = pd.to_datetime(stock_data_specific.Date, infer_datetime_format = True), y = stock_data_specific.Close.astype("float"), name = "Share Price"), row = 1, col = 1)
	fig.add_trace(go.Scatter(x = pd.to_datetime(revenue_data_specific.Date, infer_datetime_format = True), y =revenue_data_specific.Revenue.astype("float"), name = "Revenue"), row = 2, col = 1)


#Thêm và update chú giải
		# showlegend=False: Ẩn chú giải (legend). Điều này là do tên "Share Price" và "Revenue" đã rõ ràng trên trục y từng đồ thị.
		# height=900: Chiều cao toàn bộ biểu đồ là 900 pixel.
		# title=stock: Tiêu đề biểu đồ là tên của cổ phiếu (do tham số stock cung cấp, ví dụ: "Tesla").
		# xaxis_rangeslider_visible=True: Bật chế độ thanh trượt (range slider) phía dưới, cho phép zoom và chọn một khoảng thời gian cụ thể trên trục x.
	fig.update_xaxes(title_text = "Date", row = 1, col = 1)
	fig.update_xaxes(title_text = "Date", row = 2, col = 1)
	fig.update_yaxes(title_text = "Price ($US)", row = 1, col = 1)
	fig.update_yaxes(title_text = "Revenue ($US Millions)", row = 2, col = 1)
	fig.update_layout(showlegend = False,
	height = 900,
	title = stock,
	xaxis_rangeslider_visible = False)

	fig.show()
	
make_graph2(tesla_data, tesla_revenue, 'Tesla')


#Question 6: Plot GameStop Stock Graph: Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the make_graph function is make_graph(gme_data, gme_revenue, 'GameStop'). Note the graph will only show data upto June 2021.(Câu 6: Vẽ đồ thị chứng khoán GameStop: Sử dụng hàm make_graph để vẽ biểu đồ Dữ liệu chứng khoán GameStop, đồng thời cung cấp tiêu đề cho biểu đồ. Cấu trúc để gọi hàm make_graph là make_graph(gme_data, gme_revenue, 'GameStop'). Lưu ý biểu đồ sẽ chỉ hiển thị dữ liệu cho đến tháng 6 năm 2021.)
def make_graph3(stock_data, revenue_data, stock):
	fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
	stock_data_specific = stock_data[stock_data.Date <= '2021-06-30']
	revenue_data_specific = revenue_data[revenue_data.Date <= '2021-06-30']
	fig.add_trace(go.Scatter(x = pd.to_datetime(stock_data_specific.Date, infer_datetime_format = True), y = stock_data_specific.Close.astype("float"), name = "Share Price"), row = 1, col = 1)
	fig.add_trace(go.Scatter(x = pd.to_datetime(revenue_data_specific.Date, infer_datetime_format = True), y =revenue_data_specific.Revenue.astype("float"), name = "Revenue"), row = 2, col = 1)
	fig.update_xaxes(title_text = "Date", row = 1, col = 1)
	fig.update_xaxes(title_text = "Date", row = 2, col = 1)
	fig.update_yaxes(title_text = "Price ($US)", row = 1, col = 1)
	fig.update_yaxes(title_text = "Revenue ($US Millions)", row = 2, col = 1)
	fig.update_layout(showlegend = False,
	height = 900,
	title = stock,
	xaxis_rangeslider_visible = True)
	fig.show()

make_graph3(gme_data, gme_revenue, 'GameStop')