FROM python:3.12-slim
COPY entrypoint.sh /opt/app/entrypoint.sh
COPY app.py /opt/app/app.py
COPY OstrovokModel.py /opt/app/OstrovokModel.py
COPY AccuracyScore.py /opt/app/AccuracyScore.py
COPY result.csv /opt/data/result.csv

COPY temp /opt/temp
COPY data /opt/data
RUN pip install pandas
RUN pip install scikit-learn
ENTRYPOINT ["/opt/app/entrypoint.sh"]