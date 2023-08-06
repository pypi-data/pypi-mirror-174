import pandas as pd
import statsmodels.api as sm
import time
import warnings
warnings.filterwarnings('ignore')

from dateutil.relativedelta import relativedelta
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

# evaluate an ARIMA model for a given order (p,d,q)
def evaluate_arima_model(X, arima_order):
	# prepare training dataset
	train_size = int(len(X) * 0.66)
	train, test = X[0:train_size], X[train_size:]
	history = [x for x in train]
	# make predictions
	predictions = list()
	for t in range(len(test)):
		model = ARIMA(history, order = arima_order)
		model_fit = model.fit()
		yhat = model_fit.forecast()[0]
		predictions.append(yhat)
		history.append(test[t])
	# calculate out of sample error
	error = mean_squared_error(test, predictions)
	return error


# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
	dataset = dataset.astype('float32')
	best_score, best_cfg = float("inf"), None
	for p in p_values:
		for d in d_values:
			for q in q_values:
				order = (p,d,q)
				try:
					mse = evaluate_arima_model(dataset, order)
					if mse < best_score:
						best_score, best_cfg = mse, order
					print('ARIMA%s MSE=%.3f' % (order,mse))
				except:
					continue
	return best_cfg, best_score


def forecasting_bzdata(X, acc_number, transaction_type, months_to_predict):

    # Starting
    start = time.time()
    print("Processing data {} ...\n".format(acc_number))

    # Loading DataFrame
    # raw_data = pd.read_excel(Dataset)

    # backup the original data
    data = X.copy()

    # renaming columns
    data.columns = data.columns.str.replace(' ', '_')

    # deleting nan value on account variable.
    data = data.dropna(subset = 'Account')

    # it seems like the data of Account is a float type value. We've convert it to int
    data['Account'] = data['Account'].astype(int)

    # Filtering columns for Debet information / YEAREND document and #ERROR! value on Debet columns
    data_to_process = data[(data['Supporting_Document'] != 'YEAREND') &            # Drop data for YEAREND document
                  (data[transaction_type] != '#ERROR!') &                          # Drop #ERROR! record
                  (data['Account'] == acc_number)][['Date', transaction_type]]     # filtering account

    # removing nan values
    data_to_process.dropna(inplace=True)

    # convert to int
    data_to_process[transaction_type] = data_to_process[transaction_type].astype(str).astype(float).astype(int)

    # converting Date columns to datetime format
    data_to_process['Date'] = pd.to_datetime(data_to_process['Date'], infer_datetime_format = True)
    data_to_process.set_index('Date', inplace = True)
    data_to_process.sort_index(inplace = True)

    # Resampling data - monthly resample
    data_to_process_per_month = data_to_process.resample('M').sum()

    # evaluate parameters
    print("Searching for the best ARIMA order >>>")
    p_values = [0, 1, 2, 4, 6, 8, 10]
    d_values = range(0, 3)
    q_values = range(0, 3)
    warnings.filterwarnings("ignore")
    best_param, best_score = evaluate_models(data_to_process_per_month.values, p_values, d_values, q_values)

    print('\nBest ARIMA%s MSE=%.3f\n' % (best_param, best_score))

    # forcasting with ARIMA model
    model_testing = sm.tsa.statespace.SARIMAX(data_to_process_per_month, order = (best_param), seasonal_order= best_param + (12,))
    # 12 is seasonal factor, we assume that seasonal cycle is happening each year (12 months)

    print("Training the ARIMA model with {} order ...\n".format(best_param))
    model_testing_fit = model_testing.fit() # Training the model

    # 24 month forcasting
    date_list = [data_to_process_per_month.index[-1] + relativedelta(months = x) for x in range(0, months_to_predict)]
    future_prediction = pd.DataFrame(index = date_list, columns = data_to_process_per_month.columns)

    num_of_month = data_to_process_per_month.shape[0] # number of months / no. of the last month
    forcast_by_month = pd.concat([data_to_process_per_month, future_prediction])
    forcast_by_month['future_prediction'] = model_testing_fit.predict(start = num_of_month - 1, end = num_of_month + months_to_predict, dynamic = True)
    forcast_by_month = forcast_by_month[[transaction_type,'future_prediction']]

    # ending process
    end = time.time()
    print("Processing time : {} seconds".format(round(end - start)))

    return forcast_by_month.loc[data_to_process_per_month.index[-1]:]


def forecast_to_excel(Filename, Sheet_name, output_name, months_to_predict):

    #loading data
    data = pd.read_excel(Filename, sheet_name = Sheet_name)
    datac = data.copy()

    # deleting nan value on account variable.
    datac = datac.dropna(subset = 'Account')

    # it seems like the data of Account is a float type value. We've convert it to int
    datac['Account'] = datac['Account'].astype(int)

    debet_data_forcast = pd.DataFrame(columns = ['Account', 'Debet', 'Date'])
    credit_data_forcast = pd.DataFrame(columns = ['Account', 'Credit', 'Date'])
    credit_account_error = []
    debit_account_error = []
    transactions = ['Debet', 'Credit']

    start = time.time() # marking start of forecasting process
    for transaction_type in transactions:
        if transaction_type == 'Debet':
            for i in datac['Account'].unique():
                try:
                    forecast_data = forecasting_bzdata(data, i, 'Debet', months_to_predict)
                    for k, l in enumerate(forecast_data['future_prediction'][1:]):
                        new_row = {'Account' : i, 'Date' : forecast_data['future_prediction'][1:].index[k], 'Debet' : l}
                        debet_data_forcast = debet_data_forcast.append(new_row, ignore_index = True)
                except Exception:
                    print("Can't process data on {} account-type, \nbut the program will continue to forecast other data".format(i))
                    debit_account_error.append(i)
                    pass

        else :
            for i in datac['Account'].unique():
                try:
                    forecast_data = forecasting_bzdata(data, i, 'Credit', months_to_predict)
                    for k, l in enumerate(forecast_data['future_prediction'][1:]):
                        new_row = {'Account' : i, 'Date' : forecast_data['future_prediction'][1:].index[k], 'Credit' : l}
                        credit_data_forcast = credit_data_forcast.append(new_row, ignore_index = True)
                except Exception:
                    print("Can't process data on account-type {}, \nbut the program will continue to forecast other data".format(i))
                    credit_account_error.append(i)
                    pass

    # combine credit and debit forecasted data
    ddf_copy = debet_data_forcast.copy()
    for i in range(credit_data_forcast.shape[0]):
        ddf_copy = ddf_copy.append(credit_data_forcast.loc[i], ignore_index = True)

    # combine the forecasted data and original data
    data_coba = data.copy()
    for i in range(ddf_copy.shape[0]):
        data_coba = data_coba.append(ddf_copy.loc[i], ignore_index = True)

    data_coba = data_coba[data_coba['Supporting Document'] != 'YEAREND']
    data_coba['Date'] = pd.to_datetime(data_coba['Date'], infer_datetime_format = True)
    data_coba.sort_values('Date', inplace=True)

    end = time.time() # marking the end of the forecasting process
    print("Processing time : {} seconds".format(round(end - start)))

    data_coba.to_excel(output_name)
