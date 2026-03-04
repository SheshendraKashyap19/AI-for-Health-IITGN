AI-for-Health-IITGN

Note: Due to dataset size constraints, raw data is not included.
Please place participant folders inside the Data/ directory before running the code.

**i run all these codes in colab i copied every cell code i will check again if i missed any** 3/4/2026 at 10:21pm

1. Understanding Data & Visualization

The dataset contains physiological signals such as nasal airflow, thoracic movement, and SpO₂.

Each data file contains values in a single line separated by ;.

To process the data:

Split the line using ; to extract individual values.

Convert timestamps into datetime format: %d%m%y %H%M%S.

Preprocessing is done for all signals (nasal, thoracic, SpO₂) using a common base path, so you don’t need to repeat the code for each signal.

Data Visualization

Graphs are plotted for 8 hours of data per participant, overlaying nasal airflow, thoracic movement, and SpO₂.

Events are marked on the graph using red overlays.

Libraries used: pandas, matplotlib.pyplot.

All visualizations are saved as visualization.pdf in the output folder.

2. Signal Preprocessing & Dataset Creation

Frequency filtering: 0.17–0.4 Hz

Removes baseline drift and high-frequency noise.

Event labeling logic:

If Overlap duration / Window duration > 0.5 → assign event label

Else → assign normal label

This generates a preprocessed dataset ready for further analysis or model training.

3. Creating CNN Model

Although this was my first hands-on experience with Convolutional Neural Networks (CNNs), I learned a lot by exploring multiple sources such as Wikipedia, YouTube tutorials, and open-source code examples.

Typing out and testing every line of code helped me understand key concepts like accuracy, recall, precision, and confusion matrix.

Steps followed for building the CNN model:

Load and preprocess data – prepared the preprocessed dataset for model input.

Train the model – implemented a CNN using libraries such as PyTorch.

Evaluate the model – assessed performance using metrics like accuracy, recall, precision, and confusion matrix.

This process not only increased my practical knowledge but also sparked curiosity to explore deep learning further.


**for outputs of these codes i uploaded them in visualisation**
