# HP Warranty Checker 🖥️🔍  

A Python-based **HP warranty checker** that automatically retrieves warranty information from HP's website using **Selenium**.  

## 🚀 Features  
✅ **Automated Warranty Lookup** – Fetch warranty details using serial numbers  
✅ **Headless Mode** – Runs in the background without opening a browser  
✅ **CSV Support** – Bulk check multiple serial numbers from a file  
✅ **Fast & Efficient** – No manual input needed  

## 🛠 Tech Stack  
- **Python** 🐍  
- **Selenium** (for web automation)  
- **ChromeDriver / EdgeDriver** (for browser automation)  
- **Pandas** (for handling CSV files, if applicable)  

## 📌 Installation  
1️⃣ **Clone the repository**  
```bash
git clone https://github.com/kevinxlim/hp-warranty-checker.git
cd hp-warranty-checker
```
<br>
2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
<br>
3️⃣ Download WebDriver (e.g., ChromeDriver)

Place it in the project folder or set it in the system PATH

<br>
4️⃣ Run the script

```bash
python warranty_checker.py
```
<br>
🎯 Usage
<br><br>
Populate the serial numbers in the serial_numbers.csv file

The script will fetch the warranty details automatically

<br>
🔒 License
This project is licensed under the MIT License.

<br><br>
📌 Contributions & Issues? Feel free to fork, star, or submit a pull request! 🚀
