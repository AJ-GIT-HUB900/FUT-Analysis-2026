EA FC 26 Analytics and Tactical Suite
Overview of Analysis  
This repository contains a comprehensive data analytics and tactical management suite developed for EA FC 26. The project leverages Python-based data science libraries to provide deep insights into player statistics, market trends, and team optimization through a series of interactive web applications.

Key Features
Global Player Scouting
An interactive database that allows users to filter over 17,000 players based on specific attributes, playstyles, and ratings. It utilizes data visualization via radar charts to compare player performance profiles across six core dimensions.

AI Similarity Engine
A machine learning module utilizing the K-Nearest Neighbors (KNN) algorithm. The system treats player statistics as coordinates in a six-dimensional space to identify and recommend the most statistically similar players in the database.

Tactical Squad Builder
A custom-built pitch interface designed for team visualization. It integrates real-time metadata tracking to calculate squad-wide averages for attributes such as pace, shooting, and physicality.

Automated Chemistry Auditor
A logical engine that calculates squad chemistry using official EA Sports thresholds for nations, leagues, and clubs. It includes an optimization feature that identifies "near-miss" links and suggests specific players to achieve maximum team synergy.

Pro Card Generator
An image processing tool utilizing the Pillow library to allow users to upload personal photographs and generate custom player cards with assigned attributes, positions, and playstyles.

Technical Stack
Language: Python

Web Framework: Streamlit

Data Manipulation: Pandas, NumPy

Machine Learning: Scikit-learn (Nearest Neighbors, Linear Regression)

Visualization: Plotly Express

Image Processing: Pillow (PIL)
