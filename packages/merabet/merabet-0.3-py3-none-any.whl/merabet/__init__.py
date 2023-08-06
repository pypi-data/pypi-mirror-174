import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math           
           

def r_squared_and_RMSD(data):
    '''
    R-SQUARED:
    Coefficient of Determination also popularly known as R square value is a regression error metric 
    to evaluate the accuracy and efficiency of a model on the data values that it would be applied to.
    R square values describe the performance of the model. It describes the variation in the response or 
    target variable which is predicted by the independent variables of the data model.
    
    RMSE:
    The root-mean-square deviation (RMSD) or root-mean-square error (RMSE) is a frequently used measure 
    of the differences between values (sample or population values) predicted by a model or an estimator 
    and the values observed. The RMSD represents the square root of the second sample moment of the differences 
    between predicted values and observed values or the quadratic mean of these differences. 
    These deviations are called residuals when the calculations are performed over the data sample that was used 
    for estimation and are called errors (or prediction errors) when computed out-of-sample.
    
    '''
    
    #CALCULATE R_SQUARED WITH NUMPY AND ADD IT TO DATAFRAME
    actual = data['y']
    predict = data['prediction']
 
    corr_matrix = np.corrcoef(actual, predict)
    corr = corr_matrix[0,1]
    R_sq = corr**2
    
    data['R_squared'] = '--'
    data.at[0,'R_squared'] = R_sq
    
    
    
    #CALCULATE 
    N = data.shape[0]
    RMSD = math.sqrt( ((data['y'] - data['prediction'])**2).sum() / N)
    
    data['RMSD'] = '--'
    data.at[0,'RMSD'] = RMSD
    
    return data

def data_to_df(data):
    '''
    Transforms input data into a pandas dataframe.
    Data can be a :
        - string describing a function, such as 'y = x + 2'.
        - a list of tuples (x,y) representing the data points.
        - a list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).

    '''
        
    if type(data) == str:
        
        equal_sign_pos = data.find('=')
        new_str = data[equal_sign_pos + 1:].lstrip()
        
        x = np.arange(10)
        y_values = eval(new_str)
        
        #Create DF:
        
        df = pd.DataFrame({'x': x, 'y': y_values})
        
    
    elif type(data) == list:
        
        if type(data[0]) == tuple:
            x_values = [pair[0] for pair in data]
            y_values = [pair[1] for pair in data]

            df = pd.DataFrame({'x': x_values, 'y': y_values})
        
        elif type(data[0] == list):
            
            name_columns = ['y']
            
            if len(data) == 2:
                name_columns.append('x')
            
            else:
                for i in range(1, len(data)):
                    name_columns.append(f'x{i}')

            data = np.array(data).T

            df = pd.DataFrame(data, columns = name_columns)
            
    return df

def simple_linear_regression(data):
    
    '''
    Models the relationship between two variables by fitting a 
    linear equation to observed data, where one variable is considered 
    to be an explanatory variable and the other as a dependent variable. 
    
    Follows the least squares method, obtaining m and b as described in the code, having 
    y = m * x + b as final result.
    
    Data can be a :
        - string describing a function, such as 'y = x + 2'.
        - a list of tuples (x,y) representing the data points.
        - a list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).

    
    '''
    
    df = data_to_df(data)
    
    df['x * y'] = df['x'] * df['y']
    
    df['x**2'] = (df['x']) ** 2
    
    
    
    sum_x = df['x'].sum()
    sum_y = df['y'].sum()
    sum_xy = df['x * y'].sum()
    sum_x2 = df['x**2'].sum()

    
    # y = mx + b

    n = df.shape[0]

    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - (sum_x) ** 2)
    b = (sum_y - m * sum_x) / n
    
    if b >= 0 :
        equation = f'LINEAL: y = {round(m,3)} * x + {round(b,3)}'
    else:
        equation = f'LINEAL: y = {round(m,3)} * x - {abs(round(b,3))}'
    
    df['prediction'] = df['x'] * m + b
    
    x = df['x']
    y = df['y']
    prediction = df['prediction']
    
    r_squared_and_RMSD(df)
    
    #%matplotlib inline
    plt.rcParams['text.color'] = 'blue'
    plt.scatter(x, y)
    plt.plot(x, prediction, color = 'red')
    plt.title(equation)
    
    #plt.show()
    
    return df

#Set up up figure size and DPI for screen demo
plt.rcParams['figure.figsize'] = (6,4)
plt.rcParams['figure.dpi'] = 70

def multiple_linear_regression(data):
    
    '''
    IMPORTANT: If using Jupyter Notebook, please introduce %matplotlib notebook in the cell.
    Model that estimates the relationship between a quantitative dependent 
    variable and two or more independent variables using a straight line.
    
    Follows the matrix approach, using the formula defined in the beta variable.
    
    Data is a list of list of the following structure:
    
    Data = [ [9, 10, 13, 14, 16], [1, 3, 4, 6, 7],[10, 14, 15, 18, 20]...]
    
    where the first list contains all values of the dependant variable (Y), and
    the remaining lists contain values of the independent variables (x1, x2 ...).
    
    PD: Make sure every list has the same length.
    '''
    
    name_columns = ['y']
    for i in range(1, len(data)):
        name_columns.append(f'x{i}')
    
    data = np.array(data).T
    
    df = pd.DataFrame(data, columns = name_columns)
    ones_array = np.ones_like(df['y'])
    df.insert(loc = 1, column = 'ones', value = ones_array)
    matrix = np.array(df.iloc[:, 1:])
    
    
    
    # Beta = (Xt * X)**-1 * Xt*Y     where Xt is the transposed matrix
    Xt = matrix.T
    beta = np.matmul(np.linalg.inv(np.matmul(Xt, matrix)), np.matmul(Xt, df['y'])) #coefficients
    
    df['prediction'] = (beta * df.iloc[:, 1:]).sum(axis = 1)
    
    plane_variables = ['x', 'y', 'z', 't', 's']
    beta_0, beta_1, beta_2 = beta
    
    plane = 'MULTIPLE: '
    
    plane += str(round(beta_0, 3)) + plane_variables[0]
    
    for i in range(1, len(beta)):
        aprox_beta = round(beta[i], 3)
        if aprox_beta >= 0:
            plane += ' + ' +str(aprox_beta) + plane_variables[i] 
        else:
            plane += ' - ' +str(abs(aprox_beta)) + plane_variables[i]
    
    r_squared_and_RMSD(df)
    
    #3D Axes
    if len(data.T) == 3:  #only plot if there are 3 variables (3D)
        
        x1 = df['x1']
        x2 = df['x2']
        y = df['y']
        
        #GENERATE PLANE
        
        #%matplotlib notebook
        max_value_prediction = int(df['prediction'].max()) * 2
        
        x1_s = np.tile(np.arange(max_value_prediction), (max_value_prediction,1))
        x2_s = np.tile(np.arange(max_value_prediction), (max_value_prediction,1)).T
        beta_0, beta_1, beta_2 = beta
        z = beta_0 + beta_1 * x1_s + beta_2 * x2_s
        
        
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(x1, x2, y, color = 'red')
        ax.plot_surface(x1_s, x2_s, z , alpha=0.2)
        ax.set_title(plane)
        plt.show()

    return df

def non_linear_exponential_regression(data):
    '''
    This function finds the equation of the exponential function that fits best for a set of data. 
    As a result, we get an equation of the form y = a * e^(bx) where a≠0 
    
    Data can be a :
    - string describing a function, such as 'y = x + 2'.
    - a list of tuples (x,y) representing the data points.
    - a list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).

    '''
    
    
    df = data_to_df(data)
    df['z = ln(y)'] = np.log(df['y'])
    df['xz'] = df['x'] * df['z = ln(y)']
    df['x^2'] = df['x'] ** 2
    
    n = df.shape[0]
    a1 = (n * df['xz'].sum() - df['x'].sum() * df['z = ln(y)'].sum()) / \
    (n * df['x^2'].sum() - (df['x'].sum())**2 )
    
    
    a0 = (df['z = ln(y)'].sum() / n) - a1 * (df['x'].sum() / n)

    A = math.e ** a0
    b = a1
    

    df['prediction'] = A * math.e ** (b * df['x'])
    r_squared_and_RMSD(df)
    
    equation = f'EXPONENTIAL: y = {round(A,5)} * {round(math.e, 3)} ^ ({round(b,3)}x)'
    
    #%matplotlib inline
    plt.scatter(df['x'],df['y'])
    plt.plot(df['x'], df['prediction'], color = 'red')
    plt.title(equation)
    plt.show()
    
    return df        

def non_linear_logarithmic_regression(data):

    '''
    Returns logarithmic regression of the data, getting as a result the curve y = a*ln(x) + b.
    
    Data can be a :
    - string describing a function, such as 'y = x + 2'.
    - a list of tuples (x,y) representing the data points.
    - a list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).

    '''
    
    df = data_to_df(data)
    
    df["x' = lnX"] = np.log(df['x'])
    df["x'y"] = df["x' = lnX"] * df['y']
    df["x'^2"] = df["x' = lnX"] ** 2
    
    n = df.shape[0]
    
    b = ( n * df["x'y"].sum() - df["x' = lnX"].sum() * df['y'].sum() ) /\
    (n * df["x'^2"].sum() - (df["x' = lnX"].sum())**2 )
    
    a = (df['y'].sum() / n) - b * (df["x' = lnX"].sum() / n)
    
    df['prediction'] = a + b * df["x' = lnX"]
    
    
    if b >= 0 :
        equation = f'LOGARITHMIC: y = {round(a,3)} * ln(x) + {round(b,3)}'
    else:
        equation = f'LOGARITHMIC: y = {round(a,3)} * ln(x) - {abs(round(b,3))}'
    
    
    r_squared_and_RMSD(df)
    
    #%matplotlib inline
    plt.scatter(df['x'], df['y'], color = 'blue')
    plt.plot(df['x'], df['prediction'], color = 'red')
    plt.title(equation)
    plt.show()
    
    return df

def non_linear_polynomial_regression(data, polynomial_degree):
    '''
    Returns the polynomial regression of the input data and the given degree.
    
    Data can be a :
    - string describing a function, such as 'y = x + 2'.
    - a list of tuples (x,y) representing the data points.
    - a list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).
      
    
    '''
    if polynomial_degree == 1:
        return simple_linear_regression(data)
    
    else:
        df = data_to_df(data)

        for i in range(polynomial_degree * 2 + 1):
            df['x^' + str(i)] = df['x']**i

        values_a = []
        for i in range(2 * polynomial_degree + 1):
            values_a.append(round(df['x^' + str(i)].sum(), 3))

        matrix = []
        for i in range(polynomial_degree + 1):
            matrix.append(values_a[i: i + polynomial_degree + 1 :])

        matrix_a = np.array(matrix)

        for e in range(1, polynomial_degree + 1):
            df['x^'+str(e)+' * y'] = df['x^'+str(e)] * df['y']



        values_b = [df['y'].sum()]
        for j in range(1, polynomial_degree + 1):
            values_b.append(round(df['x^'+str(j)+' * y'].sum(), 3))
        matrix_b = np.array(values_b)


        solution = np.linalg.solve(matrix_a, matrix_b)


        df['prediction'] =  (solution * df.iloc[:, 2: 3 + polynomial_degree]).sum(axis = 1)
        r_squared_and_RMSD(df)
        
        eq_variables = []    
        for col in (df.iloc[:, 2: 3 + polynomial_degree]).columns:
            eq_variables.append(col)
        
        equation = 'POLYNOMIAL: '
        
        equation += str(round(solution[0], 3))
        
        for i in range(1, len(solution)):
            
            coeff = round(solution[i], 3)
            var = eq_variables[i]
            
            if coeff >= 0:
                equation += ' + ' + str(coeff) + var
            
            elif var == 'x^1':
                equation += ' + ' + str(coeff) + 'x'
            
            else:
                equation += ' - ' + str(abs(coeff)) + var
        
        
        
        #%matplotlib inline
        plt.scatter(df['x'], df['y'], color = 'blue')
        plt.plot(df['x'], df['prediction'], color = 'red')
        plt.title(equation)
        
        
        return df

def best_regression_model(data):
    '''
    Returns best regression model by R-squared measurement.
    
    Data can be a :
    - string describing a function, such as 'y = x + 2'.
    - a list of tuples (x,y) representing the data points.
    - a list of lists, where each list contains all values of a variable.(IMPORTANT: first list must be variable Y values).

    '''

    models = ['simple_linear_regression', 'multiple_linear_regression', 'non_linear_exponential_regression', 'non_linear_logarithmic_regression', 'non_linear_polynomial_regression']
    r_sq = []
   
    if len(data) < 3:    
        
        for model in models:

            if model not in ['multiple_linear_regression', 'non_linear_polynomial_regression']:
                r_sq.append(eval(model+'(data)').at[0,'R_squared'])
                plt.show()


            elif model == 'multiple_linear_regression' and len(data) < 3:
                r_sq.append(0)   


            #DUDA: Si el r^2 del grado 1 es mejor que el grado 2, se asegura que el grado 1 será mejor que TODOS los grados restantes?     

            elif model == 'non_linear_polynomial_regression':  

                #obtain best degree
                flag = 0
                rsq_polynomial = 0
                max_rsq = 0
                degree = 1


                while flag == 0:

                    rsq_polynomial = (eval(model+'(data, degree)').at[0,'R_squared'])

                    if rsq_polynomial > max_rsq:
                        max_rsq = rsq_polynomial
                        degree += 1
                        plt.cla()  #clear plot of non-optimal degrees
                    else:
                        flag = -1

                optimal_degree = degree - 1            
                r_sq.append(max_rsq)

        
        
        #FIND BEST MODEL:

        sorted_rsq = sorted(r_sq, reverse=True)

        greatest_rsq = sorted_rsq[0]
        second_greatest = sorted_rsq[1]

        greatest_rsq_position = r_sq.index(greatest_rsq)
        sec_greatest_rsq_position =  r_sq.index(second_greatest)

        best_model = models[greatest_rsq_position]
        sec_best_model = models[sec_greatest_rsq_position]                             

        #Since polynomial 
        results = pd.DataFrame([r_sq], columns = ['simple', 'multiple', 'exponential', 'logarithmic', 'polynomial (degree = ' + str(optimal_degree) + ')'],
                              index = ['R_Squared'])

        
        if best_model == 'non_linear_polynomial_regression':
            response = f'Best model is {best_model}, with an optimal degree of {optimal_degree}.\nThe second best model is {sec_best_model}'
        
        plt.show()
        print(response)
        return(results)
        
        
        
    else:
        print('Only Multiple Linear Regression can be applied')
        return (multiple_linear_regression(data))        