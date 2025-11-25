# Stock-Market-Analyzer-
A python-based stock market analysis tool with real-time data, interaction charts, and technical indicators built with Streamlit and Yfinance 
📈 Stock Market Analyzer
A comprehensive Python-based stock market analysis tool that provides real-time data, interactive visualizations, and technical indicators to help users make informed investment decisions.
🌟 Features

Real-Time Stock Data: Fetch current and historical stock prices from Yahoo Finance
Interactive Charts: Visualize stock performance with dynamic, interactive graphs
Technical Indicators:
    50-day and 200-day Moving Averages
    Relative Strength Index (RSI)
    Volume analysis


Stock Comparison: Compare multiple stocks side-by-side

Key Metrics Display: View essential information including:
    Current price and daily change
    Market capitalization
    Trading volume
    52-week high/low
    P/E ratio

Flexible Time Periods: Analyze data across various timeframes (1 week to 5 years)

Data Export: Download stock data as CSV files

User-Friendly Interface: Clean, intuitive design built with Streamlit

Error Handling: Robust validation for invalid ticker symbols.

🚀 Demo
    Live Demo 
    To see the application in action, follow the installations below and run :
        streamlit run app.py
📋 Prerequisites
    Python 3.8 or higher
    pip package manager
    Internet connection (for fetching real-time data)

🔧 Installation

Clone the repository

    bgit clone https://github.com/yourusername/stock-market-analyzer.git
    cd stock-market-analyzer

Create a virtual environment (recommended)

    python -m venv venv

    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate

Install required packages

   pip install -r requirements.txt
  Or install packages individually:
    pip install yfinance pandas plotly streamlit numpy

💻 Usage

Run the application

    streamlit run app.py

Open your browser

    The app will automatically open at http://localhost:8501
    If not, manually navigate to the URL shown in your terminal

Start analyzing stocks

    Enter a stock ticker symbol (e.g., AAPL, GOOGL, MSFT)
    Select your preferred time period
    Explore charts and technical indicators
    Compare multiple stocks
    Download data for further analysis

📊 Supported Stock Markets

    US Stocks: All major US exchanges (NYSE, NASDAQ)
    International Stocks: Major global markets
    Saudi Market: Tadawul stocks (add .SR suffix, e.g., 2222.SR for Aramco)
    Cryptocurrencies: Major cryptocurrencies (add -USD suffix, e.g., BTC-USD)
🛠️ Technologies Used

    Python: Core programming language
    yfinance: Yahoo Finance API wrapper for fetching stock data
    Streamlit: Web application framework
    Plotly: Interactive visualization library
    Pandas: Data manipulation and analysis
    NumPy: Numerical computing

📁 Project Structure
    stock-market-analyzer/
    │
    ├── app.py                  # Main application file
    ├── requirements.txt        # Python dependencies
    ├── README.md              # Project documentation
    ├── .gitignore             # Git ignore file
    │
    ├── utils/                 # Utility functions (optional)
    │   ├── indicators.py      # Technical indicator calculations
    │   └── data_fetch.py      # Data fetching functions
    │
    └── assets/                # Screenshots and images (optional)
        └── demo.png

🎯 Key Functions:

    Fetching Stock Data
    import yfinance as yf

    stock = yf.Ticker("AAPL")
    df = stock.history(period="1y")

    Calculating Technical Indicators
    # Moving Average
    df['MA50'] = df['Close'].rolling(window=50).mean()

    # RSI
    def calculate_rsi(data, periods=14):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
🔮 Future Enhancements

    Portfolio tracking and management
    Price prediction using machine learning
    News sentiment analysis
    Email/SMS price alerts
    Watchlist functionality with local storage
    Dark mode toggle
    Export reports as PDF
    Mobile responsive design
    User authentication system
    Real-time notifications

🤝 Contributing
    Contributions are welcome! Please feel free to submit a Pull Request.

    Fork the project
    Create your feature branch (git checkout -b feature/AmazingFeature)
    Commit your changes (git commit -m 'Add some AmazingFeature')
    Push to the branch (git push origin feature/AmazingFeature)
    Open a Pull Request

📝 License
    This project is licensed under the MIT License - see the LICENSE file for details.
    👨‍💻 Author
    Layan Alshaghdari

    GitHub: layanalshaghdari
    Email: lalshaghdari@mocs.flsouthern.edu

🙏 Acknowledgments

    Data provided by Yahoo Finance
    Built as part of CSC 1980/2280 Innovation Time Project
    University of Pittsburgh
    Special thanks to the open-source community

⚠️ Disclaimer
    This tool is for educational and informational purposes only. It should not be considered financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.
📞 Support
    If you encounter any issues or have questions:
        Open an issue on GitHub
        Contact: your.email@example.com

⭐ Show Your Support
    If you find this project helpful, please give it a ⭐ on GitHub!

Made with ❤️ and Python

