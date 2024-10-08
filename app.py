import csv
import sys
import argparse
import time
from OstrovokModel import OstrovokModel
from AccuracyScore import compare_csv_files


parser=argparse.ArgumentParser()

parser.add_argument("--content", help="A path to rates CSV file")
parser.add_argument("--pred_type", help="0 - Predicts 3 main parameters;\n1 - Predicts 7 parameters;\n2 - Predicts 10 parameters;", default=1, type=int)
parser.add_argument("--need_create", help="0 - Load pre-trained models from files;\n1 - Train new neural network models;", default=0, type=int)

args=parser.parse_args()



def main():
    model = OstrovokModel(
        pred_type=args.pred_type,
        need_create=args.need_create
    )

    result = csv.writer(sys.stdout, lineterminator='\n')
    result.writerow(
        ['rate_name'] + model.col_names
    )

    with open(args.content) as f:
        reader = csv.reader(f)
        next(reader)
        predict_data = [row[0] for row in reader]
            
        start_time = time.time()
        model_ans = model.predict(predict_data)
        end_time = time.time()
        
        for row in model_ans:
            result.writerow(row.values())

    time_per_1_row = f'{((end_time - start_time)*1000*1000 / len(model_ans)):.2f} microseconds'
    accuracy = f'{compare_csv_files(args.content, "/opt/data/result.csv"):.2f}%'
    print(f'Time per 1 row: {time_per_1_row}, Accuracy: {accuracy}', file=sys.stderr)
      
    
if __name__ == '__main__':
    main()