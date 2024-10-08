"""
xl: lower limit for x
xu: upper limit for x 
and so on for y and z
result for the values is simply result
For each point in the hyperspace, we need a splitting criteria such that 
clustering is done correctly.
Advantages:
----------
Flexibility: Can handle data distributions that change over time.
Efficiency: Potentially faster than methods that require complete retraining for every new data point.
Interpretability: The range-based approach can often be easier to understand than complex models.
Potential Applications
Given the adaptive nature, your approach could be particularly well-suited for:

Real-time systems: Where data streams in continuously and models need to adapt quickly.
Concept drift: Scenarios where the underlying data distribution changes over time.
Anomaly detection: Identifying data points that fall outside established ranges.
"""
# Opening the dataset for reading. (x, y, z, result)
file = open("dataset.csv", "r")
ls = []
for i in range(1000): # reading first 50000 for training 
    line = file.readline()
    ls.append(list(map(float, line.split(','))))
    
file.close()
#ls: this stores the train dataset 
"""
[[38.0, 40.0, 84.0, 883.0], 
[12.0, 49.0, 185.0, 210.1], 
[35.0, 49.0, 127.0, 797.1], 
[60.0, 42.0, 187.0, 1291.8]]
in this format.
"""
# Data Loaded.
# Performing training.
outputs = []
# to get result use temp[0][3]
# to get x ranges use temp[0][0]  
model = []
import math
# for initial training and setting up some values in the model.
def distance(model, i, x, y, z):
    # distance = √((x₂ - x₁)² + (y₂ - y₁)² + (z₂ - z₁)²))
    return math.sqrt(pow(abs(x - model[i][0][1]), 2) + pow(abs(y - model[i][1][1]), 2) + pow(abs(z - model[i][2][1]), 2))
def extend(model, i, x, y, z):
    if x > model[i][0][1]:
        model[i][0][1] = x
    elif x < model[i][0][0]:
        model[i][0][0] = x 
    if y > model[i][1][1]:
        model[i][1][1] = y
    elif y < model[i][1][0]:
        model[i][1][0] = y
    if z > model[i][2][1]:
        model[i][2][1] = z
    elif z < model[i][2][0]:
        model[i][2][0] = z
for pair in ls:
    x = pair[0]
    y = pair[1]
    z = pair[2]
    result = pair[3]
    for i in range(len(model) + 1):
        i -= 1
        if len(model) == 0 or result not in outputs: 
            model.append([[x, None],[y, None],[z, None], result])
            outputs.append(result)
            break
        # I's value, len(model) 2 2
        
        if model[i][0][1] != None and model[i][1][1] != None and model[i][2][1] != None:
            if x <= model[i][0][1] and x >= model[i][0][0]and y <= model[i][1][1] and y >= model[i][1][0] and z <= model[i][2][1] and z >= model[i][2][0]:
                res = model[i][3]
                if res != result:
                    # need to resolve the conflict
                    # split into two ranges
                    range_for_xlu = abs((x + model[i][0][0]) / 2)
                    range_for_xul = abs((x + model[i][0][1]) / 2)
                    range_for_ylu = abs((y + model[i][1][0]) / 2)
                    range_for_yul = abs((y + model[i][1][1]) / 2)
                    range_for_zlu = abs((z + model[i][2][0]) / 2)
                    range_for_zul = abs((z + model[i][2][1]) / 2)
         
                    split1 = [[model[i][0][0], range_for_xlu], [model[i][1][1], range_for_ylu], [model[i][2][1], range_for_zlu], res]
                    split2 = [[range_for_xul, model[i][0][0]], [range_for_yul, model[i][1][0]], [range_for_zul, model[i][2][0]], res]
                    split3 = [[range_for_xlu, x], [range_for_ylu, y], [range_for_zlu, z], result]
                    split4 = [[x, range_for_xul], [y, range_for_yul], [z, range_for_zul], result]
    
                    model.append(split1)
                    model.append(split2)
                    model.append(split3)
                    model.append(split4)
                    model.remove(model[i])
                    print(" SPLITTED ")
                        
            else: # we know it is exceeding the ranges.
                # distance = √((x₂ - x₁)² + (y₂ - y₁)² + (z₂ - z₁)²))
                # set the values to the nearest pair matching result and increment their ranges.                    
                min_distance = float('inf')
                min_index = None
                index = 0
                for point in model:
                    if result == point[3] and not (point[0][1] == None or point[1][1] == None or point[2][1] == None):
                        temp_distance = distance(model, index, x, y, z)
                        
                        if temp_distance < min_distance:
                            min_distance = temp_distance
                            min_index = index
                    index += 1                            
                
                if min_index == None:
                    min_index = i
                extend(model, min_index, x, y, z)
                print(" EXTENDED ")
        else:
            # we know result so we need to set the upper limit 
            # of the respective vars.
            for j in model:
                if j[3] == result: # j = [[1, ], [3, ], [5, ], 7]
                    if x >= j[0][0]:
                        j[0][1] = x
                    else:
                        j[0][1] = j[0][0]
                        j[0][0] = x
                    if y >= j[1][0]:
                        j[1][1] = y
                    else:
                        j[1][1] = j[1][0]
                        j[1][0] = y
                    if z >= j[2][0]:
                        j[2][1] = z
                    else:
                        j[2][1] = j[2][0]
                        j[2][0] = z
                    break
            break
print("Data Loaded")
# training algorithm completed not optimized               
# print(model)
file = open("dataset.csv", "r")
ls = []
for i in range(300):
    line = file.readline()
    ls.append(list(map(float, line.split(','))))
file.close()


# here comes testing.
def accuracy(model, ls):
    acc = 0
    total = len(ls)
    for i in ls:
        result = i[3]
        for j in model:
            if not j[0][1] == None: 
                if j[0][1] >= i[0] >= j[0][0] and j[1][1] >= i[1] >= j[1][0] and j[2][1] >= i[2] >= j[2][0]: 
                    res = j[3]
                    if res == result:
                        acc += 1
                        break
    return (acc / total) * 100 
print("Trained Model", model)
print("Model Accuracy = ", accuracy(model, ls))

# determine accuracy after test.
# Around 95+ % accuracy.
