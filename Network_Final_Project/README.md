#  Encrypted Network Traffic Analysis & Classification

This project analyzes and classifies encrypted internet traffic using Python, data visualization, and machine learning techniques. 
It includes traffic capture from various applications, statistical analysis, and traffic classification using a Random Forest classifier.

##  Tools & Technologies

- Python 3.11.9
- Pandas, NumPy
- Matplotlib
- Scikit-learn (RandomForestClassifier)
- Regular Expressions (re)
- Wireshark (for packet inspection)

---

##  Part A: Traffic Feature Analysis

### A. Protocol Distribution by App  
Side-by-side bar chart showing protocol usage per app.

### B. Top 5 Destination IPs  
Bar charts displaying most frequent destination addresses per app.

### C. TLS Handshake Types  
"Client Hello" vs. "Server Hello" counts extracted via regex.

### D. Packet Size Distribution  
Histogram showing packet sizes (log scale).

### E. Inter-Arrival Times  
Time difference between packets to understand flow behavior.

### F. Flow Size  
Number of packets per application.

### G. Flow Volume  
Total bytes transmitted per app.

---

##  Part B: Machine Learning Classifier

###  Preprocessing
- CSV merging with `merge_csv_files()`
- Feature engineering: Flow_ID, Time_Diff, Ports
- Dataset split (train/test)

###  Models Trained
- **Scenario 1:** Using `Flow_ID`, `Length`, `Time`
- **Scenario 2:** Using only `Length`, `Time`

###  Performance
- Accuracy scores
- Classification reports
- Actual vs Predicted tables
- Bar plots for both scenarios

---

##  Part C: Advanced Traffic Detection (Mixed Data)

- Uses mixed traffic files like `Firefox_with_Spotify.csv`
- Classifier tested on harder scenarios where flows are mixed
- Evaluates classifier generalization to unseen patterns

---

##  Key Findings

- Packet size & time features alone provide >85% accuracy
- Flow ID improves accuracy significantly (to ~95–99%)
- QUIC protocol is dominant in modern apps (like Firefox)
- TCP shows higher sensitivity to network conditions than UDP

---

## 🏁 How to Run

```bash
pip install pandas, numpy, matplotlib, scikit-learn
python main.py          


