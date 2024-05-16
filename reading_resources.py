import streamlit as st

def render_reading_resources():
    st.title("Reading Resources")

    st.write("""
    Welcome to the Reading Resources section! Here, you can find various educational materials to enhance your understanding of investment fundamentals and make informed decisions.
    """)

    st.header("Select Resource Category")

    selected_category = st.radio("", ["Educational Articles", "Video Tutorials", "Podcasts", "Recommended Books", "Online Courses"])

    if selected_category == "Educational Articles":
        st.subheader(selected_category)
        st.markdown("""
        - [Introduction to Investing](https://www.investopedia.com/articles/investing/082614/how-stock-market-works.asp): Learn the basics of the stock market and how it operates.
        - [Understanding Stocks](https://www.nerdwallet.com): Discover what stocks are and how they work as investment vehicles.
        - [Guide to Mutual Funds](https://www.sec.gov): Get insights into mutual funds and how to invest in them.
        - [Basics of Bonds](https://www.investor.gov): Understand the fundamentals of bonds and fixed-income products.
        """)

    elif selected_category == "Video Tutorials":
        st.subheader(selected_category)
        st.markdown("""
        - [Investing for Beginners](https://www.youtube.com/watch?v=F3QpgXBtDeo): Beginner-friendly tutorial on investing principles.
        - [Understanding Mutual Funds](https://www.youtube.com/watch?v=JUtes-k-VX4): Video explaining mutual funds and their benefits.
        - [Introduction to Bonds](https://www.youtube.com/watch?v=vAdn7aLHpO0): Introduction to bonds and bond investing.
        - [Value Investing Principles](https://www.youtube.com/watch?v=dWDPMD_rCY0): Learn about value investing strategies.
        - [Risk Management Strategies](https://www.youtube.com/watch?v=K6fCnXJ2F24): Explore different risk management techniques for investments.
        """)

    elif selected_category == "Podcasts":
        st.subheader(selected_category)
        st.markdown("""
        - [InvestED Podcast](https://www.ruleoneinvesting.com/podcast/): Dive deep into investing with insights from experienced investors.
        - [The Investor's Podcast Network](https://www.theinvestorspodcast.com/): Network of podcasts covering various investment topics.
        - [The Motley Fool Podcasts](https://www.fool.com/podcasts/): Listen to discussions on finance and investing by Motley Fool experts.
        - [We Study Billionaires](https://www.theinvestorspodcast.com/): Podcast focused on billionaire investors and their strategies.
        - [Market Foolery](https://www.fool.com/podcasts/marketfoolery/): Stay updated on market news and analysis with this podcast.
        """)

    elif selected_category == "Recommended Books":
        st.subheader(selected_category)
        st.markdown("""
        - "The Intelligent Investor" by Benjamin Graham: Classic book on value investing principles.
        - "A Random Walk Down Wall Street" by Burton G. Malkiel: Insights into efficient market theory and investment strategies.
        - "The Little Book of Common Sense Investing" by John C. Bogle: Guide to passive investing and index funds.
        - "The Essays of Warren Buffett: Lessons for Corporate America" by Warren Buffett: Learn from the legendary investor's wisdom.
        - "Common Stocks and Uncommon Profits" by Philip Fisher: Detailed analysis of stock selection and investment strategies.
        - "One Up On Wall Street" by Peter Lynch: Insights from one of the most successful investors of all time.
        """)

    elif selected_category == "Online Courses":
        st.subheader(selected_category)
        st.markdown("""
        - [Coursera - Financial Markets](https://www.coursera.org/learn/financial-markets-global): Learn about global financial markets and investment strategies.
        - [Udemy - Investment Management](https://www.udemy.com/course/investment-management/): Comprehensive course covering various aspects of investment management.
        - [edX - Finance Essentials](https://business.edx.org/): Essential finance concepts and principles taught by industry experts.
        - [Khan Academy - Investment and Retirement](https://www.khanacademy.org/): Free courses on investment and retirement planning.
        - [LinkedIn Learning - Investment Strategies](https://www.linkedin.com/learning/): Develop investment strategies and portfolio management skills.
        """)

