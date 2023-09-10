from flask import Flask, request, make_response
import numpy as np
import pandas as pd
from flask_cors import CORS
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
CORS(app)

@app.route('/process-csv', methods=['POST'])
def process_csv():
    file = request.files['file']

    file_path = 'uploaded_file.csv'
    file.save(file_path)
 
    data = pd.read_csv(file_path)
    if "Date" in data.columns:
        data.index = pd.to_datetime(data["Date"])
        data = data.drop("Date", axis=1)
    elif not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    # Create a list of years
    years = list(range(2016, 2023)) 

    # Create a DataFrame to store the predictions
    predictions = pd.DataFrame(columns=data.columns)

    # For each year, predict the values
    for year in years:
        train_data = data[data.index.year <= year - 1]
        test_data = data[data.index.year == year]

        # Check if test_data is empty
        if test_data.empty:
            continue 

        # Take the mod of the negative values
        test_data[test_data < 0] = np.mod(test_data[test_data < 0], 2)

        model = LinearRegression()
        model.fit(train_data, train_data)

        # Predict the values and create a DataFrame with matching column names
        predicted_values = pd.DataFrame(model.predict(test_data), columns=data.columns, index=test_data.index)

        predictions = pd.concat([predictions, predicted_values])

    # Create a new row with the values for the year 2022
    new_row = pd.DataFrame(
        np.zeros((1, len(data.columns))),
        columns=data.columns,
        index=pd.to_datetime(["2022"])
    )
    new_row[new_row < 0] = np.mod(new_row[new_row < 0], 2)
    data = pd.concat([data, new_row])

    # Predict the 2022 data
    train_data = data[data.index.year <= 2021]
    test_data = data[data.index.year == 2022]

    # Check if test_data is empty
    if not test_data.empty:
        model = LinearRegression()
        model.fit(train_data, train_data)

        # Predict the values and create a DataFrame with matching column names
        predicted_values = pd.DataFrame(model.predict(test_data), columns=data.columns, index=test_data.index)

        predictions = pd.concat([predictions, predicted_values])

    # Combine the previous data and predictions
    combined_data = pd.concat([data, predictions], axis=0)
 
    # Save the combined data to an Excel file
    output_path = 'processed_data.xlsx'
    combined_data.iloc[:-2]._append(combined_data.iloc[[-1]]).to_excel(output_path, index=True, index_label='Date')

    with open(output_path, 'rb') as file:
        file_data = file.read()

    # Create a response with the file data
    response = make_response(file_data)

    # Set the response headers for file download
    response.headers['Content-Disposition'] = 'attachment; filename=processed_data.xlsx'
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    return response

 
if _name_ == '__main__':
    app.run()
