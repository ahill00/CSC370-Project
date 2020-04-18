import csv
import random

# NOTE(andy): data gathered from https://www.teoalida.com/cardatabase/samples/Year-Make-Model-Trim-Full-Specs-by-Teoalida-SAMPLE.csv  # noqa: E501


with open('data_cleaned.csv') as fh:
    # ignore header lines
    data = list(csv.reader(fh))[1:]
    random.shuffle(data)

num_records = len(data)

# 20% training data, 80% learning
twenty_percent = int(num_records * 0.2)
answer_set = data[0:twenty_percent]
data_set = data[twenty_percent:]

# NOTE(andy): our data set already has the answer, which needs to be removed
# from the learning data.
for item in data_set:
    del item[-1]

with open('AnswerSet_Extra_Data.csv', 'w') as fh:
    w = csv.writer(fh)
    w.writerows(answer_set)

with open('DataSet_Extra_data.csv', 'w') as fh:
    w = csv.writer(fh)
    w.writerows(data_set)
